import os, sys
import env
from runs import datafile

datadir, filename = os.path.split(sys.argv[1])
datadir = os.path.expanduser(datadir)
test = datafile.load_test(filename, datadir)

print test.keys()
print len(test['testset'])
print test['testset']
#print test['averages']