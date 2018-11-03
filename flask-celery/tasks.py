import os
import json
# third-party library for importing matlab funcitons to python
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
def run_benchmark(problem, K, T, r, sig):
    """Run benchmark and return the result as a dictionary."""
    # import function run_methods from mytable.m
    filepaths, runtime, relerr = octave.newtable(problem, K, T, r, sig, nout=3)
    # because results are matrix in matlab, they need to be flattened, url below
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    runtime_list = [item for sublist in runtime.tolist() for item in sublist]
    relerr_list = [item for sublist in relerr.tolist() for item in sublist]
    # merge those three lists into a dictionary { filepaths: (time, relerr) }
    d = {i[0]: list(i[1:]) for i in zip(filepaths, runtime_list, relerr_list)}
    d['problem'] = problem  # add a problem key to the dictionary
    return d
