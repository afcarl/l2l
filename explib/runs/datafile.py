import os, re, sys
import cPickle
import platform

import treedict

import toolbox
from toolbox import gfx

import names
import paths

    ## available files ##

_datafiles  = set()
_categories = set(), set(), set(), set(), set(), set(), set(), set()

def update():
    global _datafiles, _categories
    _datafiles  = set()
    _categories = set(), set(), set(), set(), set(), set(), set(), set()
    filenames = os.listdir(paths.configdir)
    filenames += os.listdir(paths.datadir)
    filenames += os.listdir(paths.resultsdir)
    filenames += os.listdir(paths.pngdir)
    filenames += os.listdir(paths.predir)
    for filename in filenames:
        idx = names.split_jobname(filename)
        if idx is not None:
            _datafiles.add(filename)
            _categories[idx].add(filename)

def prim_data_available():
    return _categories[names.kPrimaryData]

def prim_test_available():
    return _categories[names.kPrimaryTest]

def sec_data_available():
    return _categories[names.kSecondaryData]

def sec_test_available():
    return _categories[names.kSecondaryTest]

def prim_res_available():
    return _categories[names.kPrimaryResults]

def sec_res_available():
    return _categories[names.kSecondaryResults]

def examples_available():
    return _categories[names.kExamples]

def testset_available():
    return _categories[names.kTestset]

def data_available():
    return _datafiles


    ## load & save ##

def _load_file(filename, directory, typename):
    filepath = "{}/{}".format(directory, filename)
    with open(filepath, 'r') as f:
        data = cPickle.load(f)
    print('{}exp:{} compiled {} loaded in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))
    return data

def _save_file(data, filename, directory, typename):
    filepath = '{}/{}'.format(directory, filename)
    with open(filepath,'w') as f:
        cPickle.dump(data, f)
    print('{}exp:{} compiled {} saved in {}{}{}'.format(gfx.purple, gfx.grey, typename, gfx.cyan, filepath, gfx.end))

def load_results(filename, resultsdir = paths.resultsdir):
    return _load_file(filename, resultsdir, 'results')
def save_results(data, filename, resultsdir = paths.resultsdir):
    _save_file(data, filename, resultsdir, 'results')

def load_examples(filename, predir = paths.predir):
    return _load_file(filename, predir, 'examples')
def save_examples(data, filename, predir = paths.predir):
    _save_file(data, filename, predir, 'examples')

def load_testset(filename, predir = paths.predir):
    return _load_file(filename, predir, 'testset')
def save_testset(data, filename, predir = paths.predir):
    _save_file(data, filename, predir, 'testset')

def load_test(filename, datadir = paths.datadir):
    return _load_file(filename, datadir, 'test')
def save_test(data, filename, datadir = paths.datadir):
    _save_file(data, filename, datadir, 'test')

def load_data(filename, datadir = paths.datadir):
    return _load_file(filename, datadir, 'history')
def save_data(data, filename, datadir = paths.datadir):
    _save_file(data, filename, datadir, 'history')

def load_config(filename, configdir = paths.configdir):
    if filename[-4:] != '.cfg':
        filename = filename + '.cfg'
    filepath = os.path.join(configdir, filename)
    filepath = os.path.expanduser(filepath)

    with open(filepath,'r') as f:
        s = f.read()

    d = {}
    for line in s.split('\n'):
        key, value = line.split('=')
        key = key.strip()
        value = eval(value.strip(), {}, {})
        d[key] = value

    return treedict.TreeDict().fromdict(d)

def save_config(cfg, configdir = paths.configdir):
    filepath = os.path.join(configdir, cfg.hardware.configfile)
    filepath = os.path.expanduser(filepath)

    with open(filepath,'w') as f:
        f.write(cfg.makeReport())
