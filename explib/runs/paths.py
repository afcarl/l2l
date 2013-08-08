import os, platform

if platform.system() == 'Darwin':
    iodir      = '~/Research/local/cluster_io/'
    configdir  = '~/Research/local/l2l/data/configs/'
    datadir    = '~/Research/local/l2l/data/data/'
    pngdir     = '~/Research/local/l2l/data/graphs/'
    resultsdir = '~/Research/local/l2l/data/results/'
    predir     = '~/Research/local/l2l/data/pre/'
else:
    iodir      = '~/io/'
    configdir  = '~/l2l/data/configs/'
    datadir    = '~/l2l/data/data/'
    pngdir     = '~/l2l/data/graphs/'
    resultsdir = '~/l2l/data/results/'
    predir     = '~/l2l/data/pre/'

iodir      = os.path.expanduser(iodir)
configdir  = os.path.expanduser(configdir)
datadir    = os.path.expanduser(datadir)
pngdir     = os.path.expanduser(pngdir)
resultsdir = os.path.expanduser(resultsdir)
predir     = os.path.expanduser(predir)

def set_configdir(new_dir):
    global iodir
    io = new_dir

def set_configdir(new_configdir):
    global configdir
    configdir = new_configdir

def set_datadir(new_datadir):
    global datadir
    datadir = new_datadir

def set_pngdir(new_pngdir):
    global pngdir
    pngdir = new_pngdir

def set_resultsdir(new_resultsdir):
    global resultsdir
    resultsdir = new_resultsdir

def set_predir(new_dir):
    global predir
    predir = new_dir