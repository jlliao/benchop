import os
import json
# third-party library for importing matlab funcitons to python
from oct2py import octave
from celery import Celery, group

env = os.environ
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = env.get(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379')

octave.addpath('../benchop_files')  # set octave directory

app = Celery('tasks',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND)


@app.task()
def run_benchmark(problem, K, T, r, sig):
    """Run benchmark and return the result as a dictionary."""
    # import function run_methods from mytable.m
    filepaths, runtime, relerr = octave.newtable(problem, K, T, r, sig)
    # because results are matrix in matlab, they need to be flattened, url below
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    runtime_list = [item for sublist in runtime.tolist() for item in sublist]
    relerr_list = [item for sublist in relerr.tolist() for item in sublist]
    # merge those three lists into a dictionary { filepaths: (time, relerr) }
    d = {i[0]: list(i[1:]) for i in zip(filepaths, runtime_list, relerr_list)}
    d['problem'] = problem  # add a problem key to the dictionary
    return json.dumps(d)


@app.task(name='mytasks.group_benchmark')
def group_benchmark(problems, parameters_1, parameters_2):
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
    # group the task for parallel computation
    task = group(run_benchmark.s(problem, K, T, r, sig)
                 for problem, K, T, r, sig in zip(problems, Ks, Ts, rs, sigs))
    task.apply_async()  # run the task
    return task.id  # return the task id
