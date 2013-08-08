import sys, os
import cPickle

import numpy as np
import treedict
import time


import env
from runs import datafile, names
import exp

def perf(cfgs):

    avg_perfs = []

    for k, testruns in enumerate(cfgs):
        avg_perfs.append([None, None, None])
        if len(testruns) > 0:
            ticks, testset = None, None
            results = []
            for filename in testruns:
                data = datafile.load_test(filename)
                assert ticks is None or ticks == data['ticks']
                assert testset is None or testset == data['testset']
                ticks = data['ticks']
                testset = data['testset']
                results.append(data['averages'])

            avg = np.average(results, axis = 0)
            std = np.std(results, axis = 0)
            avg_perfs[k] = [ticks, avg, std]

    return testset, avg_perfs

def compile_primary(expname):
    datafile.update()
    prim_names = datafile.prim_test_available()
    prim_cfgs = [[] for _ in range(10)]
    for filename in prim_names:
        cat, file_expname, primid, rep = names.name2key(filename)
        if file_expname == expname:
            prim_cfgs[primid].append(filename)
    prim_cfgs = [sorted(filenames) for filenames in prim_cfgs]
    testset, results = perf(prim_cfgs)

    cfg = treedict.TreeDict()
    cfg.hardware.resultsfile = names.r_pname(names.kPrimaryResults, expname)
    exp.save_results(cfg, time.time(), testset, results)

def compile_secondary(primname, source, expname):
    datafile.update()
    sec_names = datafile.sec_test_available()
    sec_cfgs = [[] for _ in range(10)]
    for filename in sec_names:
        cat, file_primname, primid, file_secname, secid, rep = names.name2key(filename)
        if file_primname == primname and file_secname == expname and primid == source:
            sec_cfgs[secid].append(filename)
    sec_cfgs = [sorted(filenames) for filenames in sec_cfgs]
    testset, sec_results = perf(sec_cfgs)

    cfg = treedict.TreeDict()
    cfg.hardware.resultsfile = names.r_sname(names.kSecondaryResults, primname, source, expname)

    exp.save_results(cfg, time.time(), testset, sec_results)
