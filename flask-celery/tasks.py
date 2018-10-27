import os
import json
from oct2py import octave
from celery import Celery, group

env = os.environ
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = env.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

app = Celery('tasks',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND)

@app.task()
def run_benchmark(problem):
    """Run benchmark and return the result as a dictionary."""
    # import function run_methods from mytable.m
    filepaths, runtime, relerr = octave.run_methods(problem)
    # because results are matrix in matlab, they need to be flattened, url below
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    runtime_list = [item for sublist in runtime.tolist() for item in sublist]
    relerr_list = [item for sublist in relerr.tolist() for item in sublist]
    # merge those three lists into a dictionary { filepaths: (time, relerr) }
    return json.dumps(dict(zip(filepaths, zip(runtime_list, relerr_list))))

@app.task(name = 'mytasks.group_benchmark')
def group_benchmark(problems):
    task = group(run_benchmark.s(problem) for problem in problems)
    task.apply_async()
    return task.id
