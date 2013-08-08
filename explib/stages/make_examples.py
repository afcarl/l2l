import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../..')))

import time
import traceback

import robots

from ..analysis import compile_tests
from ..runs import datafile, names
from bias import meshgrid

def make_examples(cfg):

    start_time = time.time()

    try:
        bot = robots.build_robot(cfg.sim)

        cat, expname, cfg_id, uid, n = cfg.exp.key
        dataset = compile_tests.create_examples(bot, n)

        filename = names.key2name(cfg.exp.key)
        datafile.save_examples(dataset, cfg.hardware.examplesfile)
    except Exception as e:
        traceback.print_exc()
    finally:
        bot.close()

    print("ran for {}s.".format(int(time.time() - start_time)))


def make_testset(cfg):

    start_time = time.time()

    try:
        bot = robots.build_robot(cfg.sim)

        cat, expname, cfg_id, m = cfg.exp.key
        mg = meshgrid.MeshGrid(bot.s_bounds, cfg.testset.res)

        datafile.update()
        for filename in datafile.examples_available():
            pre_key = names.name2key(filename)
            if pre_key[0] == names.kExamples:
                pre_cat, pre_expname, pre_cfg_id, pre_uid, pre_n = pre_key
                if pre_expname == expname and pre_cfg_id == cfg_id:
                    dataset = datafile.load_examples(filename)
                    for order, effect in dataset:
                        mg.add(effect)

        ts = [mg.draw(replace = False)[0] for _ in range(m)]

        datafile.save_testset(ts, cfg.hardware.testsetfile)

    except Exception as e:
        traceback.print_exc()
    finally:
        bot.close()

    print("ran for {}s.".format(int(time.time() - start_time)))
