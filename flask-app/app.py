import os
from flask import Flask, render_template, request
from worker import celery
from celery.result import AsyncResult
import celery.states as states

env = os.environ
app = Flask(__name__, template_folder='.')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/runtask', methods=['POST'])
def runtask():
    # get 'problems' - a list of problems to solve - from request json
    req_data = request.get_json()
    problems = req_data['problems']
    # apply parallel processing to multiple workers
    task = celery.send_task('mytask.group_benchmark', args=problems, kwargs={})
    return 'Running task: {id}'.format(id=task.get(timeout=1)), 202


@app.route('/checktask/<string:id>')
def checktask(id):
    res = celery.AsyncResult(id)
    # check the state of result
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)


if __name__ == '__main__':
    app.run(debug=env.get('DEBUG', True),
            port=int(env.get('PORT', 8000)),
            host=env.get('HOST', '0.0.0.0')
            )
