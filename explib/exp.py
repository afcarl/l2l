import cPickle
import time

import numpy as np

import toolbox
from toolbox import gfx

from runs import datafile

    ## learn ##

def noisy_order(boxee, order, ratio = 0.0001):
    noisy = []
    for oi, (oi_min, oi_max) in zip(order, boxee.m_bounds):
        a = (oi_max-oi_min)*ratio
        noisy.append(min(oi_max, max(oi_min, oi + random.uniform(-a, a))))
    return tuple(noisy)

def learn(boxee, guide, learner):
    action = guide.next_action()

    if action.type == 'goal':
        goal = action.payload
        order  = learner.infer_order(goal)
    elif action.type == 'order':
        order = action.payload

    prediction = learner.predict_effect(order)
    effect = boxee.execute_order(order)
    assert len(effect) == len(boxee.s_bounds)
    learner.add_xy(order, effect)
    guide.feedback(action, (order, prediction, effect))


    ## testing ##

def _duplicate(prefixes, combinations):
    suffixes = []
    for p in prefixes:
        for c in combinations:
            suffixes.append(p+[c])
    return suffixes

# testset
def create_tests(s_bounds, res, fixed_dim = None):
    assert res > 1
    testset = [[None]]
    for i, (si_min, si_max) in enumerate(s_bounds):
        combinations = []
        if fixed_dim is not None and fixed_dim[i] is not None:
            combinations = [fixed_dim[i]]
        else:
            combinations = [(si_max - si_min)*k/(res-1) + si_min for k in range(res)]
        testset = _duplicate(testset, combinations)
    testset = tuple(tuple(test[1:]) for test in testset)
    return testset

# learning performance
def test_results(box, learner, testset):
    p = 0
    results = []
    for i, goal in enumerate(testset):
        toolbox.gfx.print_progress(i, len(testset), prefix = '{}testing... {}'.format(gfx.purple, gfx.cyan), suffix = gfx.end)
        order  = learner.infer_order(goal)
        effect = box.execute_order(order)
        results.append((order, effect))

    print 100*" " + "\r",
    return results

def test_perfs(testset, results):
    perfs = [toolbox.norm(effect[:2], goal[:2]) for goal, (order, effect) in zip(testset, results)]
    return np.average(perfs), np.std(perfs)


    ## load & save ##

def save_data(cfg, guide):
    history = guide.datalog.package_history()
    data = {'date'    : time.time(),
            'cfg'     : cfg,
            'history' : history}
    datafile.save_data(data, cfg.hardware.datafile)

def save_test(cfg, date, testset, ticks, results, averages, stddevs):
    data = {'date'    : date,
            'cfg'     : cfg,
            'testset' : testset,
            'ticks'   : ticks,
            'results' : results,
            'averages': averages,
            'stddevs' : stddevs}
    datafile.save_test(data, cfg.hardware.testfile)

def save_results(cfg, date, testset, results):
    data = {'date'    : date,
            'cfg'     : cfg,
            'testset' : testset,
            'results' : results}
    datafile.save_results(data, cfg.hardware.resultsfile)