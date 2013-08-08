import os, sys
import env
from runs import datafile

datadir, filename = os.path.split(sys.argv[1])
datadir = os.path.expanduser(datadir)
results = datafile.load_results(filename, datadir)

print results