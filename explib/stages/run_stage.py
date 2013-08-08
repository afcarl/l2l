import first_learn
import second_learn
import test_perf
import make_examples

from ..runs import datafile
from ..runs import names

from ..analysis import compile_results

def run_stage(configfile):
    cfg = datafile.load_config(configfile)

    key = cfg.exp.key
    keytype = names.split_key(key)

    if keytype == names.kPrimaryData:
        first_learn.run_first(cfg)
    elif keytype == names.kPrimaryTest:
        test_perf.run_tests(cfg)
    elif keytype == names.kSecondaryData:
        second_learn.run_second(cfg)
    elif keytype == names.kSecondaryTest:
        test_perf.run_tests(cfg)
    elif keytype == names.kPrimaryResults:
        cat, expname = key
        compile_results.compile_primary(expname)
    elif keytype == names.kSecondaryResults:
        cat, primname, source, secname = key
        compile_results.compile_secondary(primname, source, secname)
    elif keytype == names.kExamples:
        make_examples.make_examples(cfg)
    elif keytype == names.kTestset:
        make_examples.make_testset(cfg)
    else:
        assert False