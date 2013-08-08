import env
import random, sys, os

import treedict

import config
import explib
from explib.runs import names, datafile, missing

jobgraph = missing.DependencyForest()

write_configs = False

def config_test(key):
    cfg = treedict.TreeDict()

    cfg.exp.expname = key[1]
    cfg.exp.key     = key
    cfg.exp.stage = 'primary' if key[0] == names.kPrimaryTest else 'secondary'

    cfg.test.res  = 20
    cfg.test.freq = 100
    cfg.test.max  = 10001

    seed = random.randint(0, sys.maxint)
    cfg.hardware.seed.test = seed

    datakey = (names.kPrimaryData if key[0] == names.kPrimaryTest else names.kSecondaryData,) + key[1:]
    cfg.hardware.datafile   = names.key2jobname(datakey)
    datacfg = datafile.load_config(cfg.hardware.datafile)
    cfg.test.fixed_dim = None
    if datacfg.sim.sensors == 'toy':
        cfg.test.fixed_dim = [None, None, 1.0]

    cfg.hardware.testfile   = names.key2jobname(key)
    cfg.hardware.configfile = names.key2jobname(key) + '.cfg'
    jobgraph.add_job(cfg.hardware.testfile, cfg, [cfg.hardware.datafile])

    return cfg

def config_data(key):
    cfg_id = key[-2]
    cfg = config.exps[cfg_id]
    cfg.exp.expname = key[1]
    cfg.exp.key     = key
    cfg.exp.stage = 'primary' if key[0] == names.kPrimaryData else 'secondary'

    cfg.hardware.datafile   = names.key2jobname(key)
    cfg.hardware.configfile = names.key2jobname(key) + '.cfg'
    if cfg.exp.stage == 'primary':
        jobgraph.add_job(cfg.hardware.datafile, cfg)
    else:
        assert cfg.exp.stage == 'secondary'
        cat, primname, prim_id, secname, sec_id, rep = key
        cfg.hardware.primaryfile = names.key2jobname((names.kPrimaryData, primname, prim_id, rep))
        jobgraph.add_job(cfg.hardware.datafile, cfg, [cfg.hardware.primaryfile])

    return cfg

def config_results(key, jobdep):
    cfg = treedict.TreeDict()
    cfg.exp.key = key
    cfg.hardware.configfile = names.key2jobname(key) + '.cfg'
    jobgraph.add_job(names.key2jobname(key), cfg, dependencies = jobdep)
    return cfg


def bias_exp( repeat = 3, primname = 'mbab01K'):

    expname = 'imbias'

    for rep in range(repeat):

        # secondary data for every possibilities
        for prim in range(10):
            for sec in range(10):
                cfg = config_data((names.kSecondaryData, primname, prim, expname, sec, rep))
                cfg.exp.bias = expname
                if write_configs:
                    datafile.save_config(cfg)

        # tests
        for prim in range(10):
            for sec in range(10):
                cfg = config_test((names.kSecondaryTest, primname, prim, expname, sec, rep))
                if write_configs:
                    datafile.save_config(cfg)

    # results
    for prim in range(10):
        jobdep = []
        for sec in range(10):
            for rep in range(repeat):
                jobdep.append(names.key2jobname((names.kSecondaryTest, primname, prim, expname, sec, rep)))
        cfg = config_results((names.kSecondaryResults, primname, prim, expname), jobdep)
        if write_configs:
            datafile.save_config(cfg)

def prim_param_exp(min_orderbabble, repeat = 3):

    if min_orderbabble >= 1000 and min_orderbabble % 1000 == 0:
        n_babble = '{:02d}K'.format(min_orderbabble/1000)
    else:
        n_babble = '{:03d}'.format(min_orderbabble)
    primname = 'mbab{}'.format(n_babble)

    learn_seeds = [7155156840889203871, 5690355778091957505, 4227221844763982751, 1077203299390958199,
                    742764988813620150, 5189664138391362084, 8242855154472905725,  730853595070848367,
                   2536789960665647998, 7200813046020147260, 4676635650031838608, 7064174268753147830,
                   4193293326361042609, 8572800867951405795, 7598963578664304146, 2316684008784354120,
                   9152028930354691119, 7200627669525538061, 4500226611609739185, 4050985011484108118]
    assert repeat <= len(learn_seeds)

    for rep in range(repeat):
        # primary data
        for prim in range(10):
            cfg = config_data((names.kPrimaryData, primname, prim, rep))
            cfg.goals.guide.min_orderbabble = min_orderbabble
            cfg.hardware.seed.primary = learn_seeds[rep]
            if write_configs:
                datafile.save_config(cfg)

        #primary test
        for prim in range(10):
            cfg = config_test((names.kPrimaryTest, primname, prim, rep))
            if write_configs:
                datafile.save_config(cfg)

    # results
    jobdep = []
    for prim in range(10):
        for rep in range(repeat):
            jobdep.append(names.key2jobname((names.kPrimaryTest, primname, prim, rep)))
    cfg = config_results((names.kPrimaryResults, primname), jobdep)
    if write_configs:
        datafile.save_config(cfg)


def sec_param_exp(min_orderbabble, repeat = 3):

    if min_orderbabble >= 1000 and min_orderbabble % 1000 == 0:
        n_babble = '{:02d}K'.format(min_orderbabble/1000)
    else:
        n_babble = '{:03d}'.format(min_orderbabble)
    primname = 'mbab{}'.format(n_babble)
    secname  = '{}{}'.format('imbias', n_babble)

    prim = 0
    for rep in range(repeat):
        # secondary data
        for sec in range(10):
            cfg = config_data((names.kSecondaryData, primname, prim, secname, sec, rep))
            cfg.goals.guide.min_orderbabble = min_orderbabble
            cfg.exp.bias = 'imbias'
            if write_configs:
                datafile.save_config(cfg)

        # secondary test
        for sec in range(10):
            cfg = config_test((names.kSecondaryTest, primname, prim, secname, sec, rep))
            if write_configs:
                datafile.save_config(cfg)

    # results
    jobdep = []
    for sec in range(10):
        for rep in range(repeat):
            jobdep.append(names.key2jobname((names.kSecondaryTest, primname, prim, secname, sec, rep)))
    cfg = config_results((names.kSecondaryResults, primname, prim, secname), jobdep)
    if write_configs:
        datafile.save_config(cfg)

def current_exp(write_config_files = False):
    global write_configs
    write_configs = write_config_files

    prim_param_exp(1000, repeat = 20)
    sec_param_exp(1000, repeat = 20)
#    bias_exp(repeat = 20, primname = 'mbab01K')
    return jobgraph

if __name__ == '__main__':

    current_exp()

    jobgraph.update()
    dtr = jobgraph.to_run()
    for name in dtr:
        print(name)
    print('{} jobs to run'.format(len(dtr)))
