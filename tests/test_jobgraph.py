import testenv
import random

import treedict
from explib.runs import missing

def test_qsub_options():
    """Test if qsub option are correctly handled"""
    check = True

    cfg = treedict.TreeDict()
    cfg.qsub.resources.mem = '16gb'
    node = missing.DependencyNode('bla', cfg)
    check *= node.qsub_options() == ' -l mem=16gb '

    cfg.qsub.resources.walltime = '5:00:00'
    node = missing.DependencyNode('bla', cfg)
    check *= node.qsub_options() == ' -l mem=16gb,walltime=5:00:00 '

    return check

tests = [test_qsub_options]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))