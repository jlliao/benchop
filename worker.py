import os
import json
import requests
from oct2py import octave
from celery import Celery, Task
from config import NOTIFIER_HOST, NOTIFIER_PORT, RABBITMQ_HOST, RABBITMQ_PORT

class NotifierTask(Task):
    """Task that sends notification on completion."""
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        url = 'http://{}:{}/notify'.format(NOTIFIER_HOST, NOTIFIER_PORT)
        data = {'clientid': kwargs['clientid'], 'result': retval}
        requests.post(url, data=data)

broker = 'amqp://{}:{}'.format(RABBITMQ_HOST, RABBITMQ_PORT)
app = Celery(__name__, broker=broker)

@app.task(base=NotifierTask, name='worker.run_benchmark')
def run_benchmark(problem, clientid=None):
    """Run benchmark and return the result as a dictionary."""
    # import function run_methods from mytable.m
    filepaths, runtime, relerr = octave.run_methods(problem)
    # because results are matrix in matlab, they need to be flattened, url below
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    runtime_list = [item for sublist in runtime.tolist() for item in sublist]
    relerr_list = [item for sublist in relerr.tolist() for item in sublist]
    # merge those three lists into a dictionary { filepaths: (time, relerr) }
    return json.dumps(dict(zip(filepaths, zip(runtime_list, relerr_list))))