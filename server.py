from urllib.parse import urlparse
from flask import Flask, render_template, request
from config import NOTIFIER_PORT
from worker import run_benchmark


app = Flask(__name__, template_folder='.')


@app.route('/')
def index():
    hostname = urlparse(request.url).hostname
    notifier_url = 'http://{}:{}'.format(hostname, NOTIFIER_PORT)
    return render_template('index.html', notifier_url=notifier_url)


@app.route('/runtask/<problem>', methods=['POST'])
def runtask(problem):
    clientid = request.form.get('clientid')
    run_benchmark.delay(problem=problem, clientid=clientid)
    return 'running task...', 202

if(__name__ == '__main__'):
	app.run(host = '0.0.0.0', debug = True)