import os, sys
import env
from runs import datafile

datadir, filename = os.path.split(sys.argv[1])
datadir = os.path.expanduser(datadir)
testset = datafile.load_testset(filename, datadir)

sorted_sig = sorted([[p[i+2] for i in range(0, len(p), 3) ] for p in testset])
for e in sorted_sig:
    print(''.join('{:d}'.format(int(e_i)) for e_i in e))

# for p in testset:
#     print(', '.join('{:d}'.format(int(p[i+2])) for i in range(0, len(p), 3)))
#     #print('{}'.format(', '.join('{:3.2f}'.format(p_i) for p_i in p)))
print('{} tests'.format(len(testset)))