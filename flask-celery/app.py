import os
from flask import Flask, render_template, request, jsonify
from celery import Celery, group
from celery.result import AsyncResult
import celery.states as states
from tasks import run_benchmark

env = os.environ
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = env.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/runtask', methods=['POST'])
def runtask():
    # get 'problems' - a list of problems to solve - from request json
    req_data = request.get_json(force=True)
    problems = req_data['problems']
    parameters_1 = req_data['parameters1']
    parameters_2 = req_data['parameters2']
    Ks = []  # list of parameter K
    Ts = []  # list of parameter T
    rs = []  # list of parameter r
    sigs = []  # list of parameter sig
    if problems:
        for problem in problems:
            if problem in [1, 2, 3]:  # if standard case, apply parameters_1
                Ks.append(parameters_1[0])
                Ts.append(parameters_1[1])
                rs.append(parameters_1[2])
                sigs.append(parameters_1[3])
            elif problem in [4, 5, 6]:  # if challenging case, apply parameters_2
                Ks.append(parameters_2[0])
                Ts.append(parameters_2[1])
                rs.append(parameters_2[2])
                sigs.append(parameters_2[3])
    # apply parallel processing to multiple workers
    result = group(run_benchmark.s(problem, K, T, r, sig) for problem, K, T, r, sig in zip(problems, Ks, Ts, rs, sigs)).apply_async()
    return jsonify(id=result.id), 202


@app.route('/checktask/<string:id>', methods=['GET'])
def checktask(id):
    res = celery.AsyncResult(id)
    # check the state of result
    if res.state == states.PENDING:
        return jsonify(result='result not yet available', state=res.state), 201
    else:
        return jsonify(result=str(res.result), state='successful'), 200


if __name__ == '__main__':
    app.run(debug=env.get('DEBUG', True),
            port=int(env.get('PORT', 5000)),
            host=env.get('HOST', '0.0.0.0')
            )
