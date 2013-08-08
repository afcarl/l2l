import sys, time
import traceback

import treedict

from toolbox import gfx
from models.learner import Learner

import robots
from .. import exp
from ..runs import datafile

defaultcfg = treedict.TreeDict()
defaultcfg.test.res  = 25
defaultcfg.test.freq = 100
defaultcfg.test.testsetfile = None

def run_tests(cfg):

    start_time = time.time()

    try:
        cfg.update(defaultcfg, overwrite = False)

        data = datafile.load_data(cfg.hardware.datafile)
        date, expcfg, history = data['date'], data['cfg'], data['history']
        cfg.test.setdefault('max', value = len(history))
        cfg.test.max = min(len(history), cfg.test.max)

        cfg.update(expcfg, overwrite = False)

        bot = robots.build_robot(cfg.sim)

        assert cfg.goals.effect.s_feats  == bot.s_feats
        assert cfg.goals.effect.s_bounds == bot.s_bounds
        assert cfg.goals.motor.m_feats   == bot.m_feats
        assert cfg.goals.motor.m_bounds  == bot.m_bounds

        learner  = Learner(bot.m_feats, bot.s_feats, bot.m_bounds, fwd = 'ES-LWLR', inv = 'L-BFGS-B')
        if cfg.test.testsetfile is None:
            testset  = exp.create_tests(bot.s_bounds, cfg.test.res, fixed_dim = cfg.test.fixed_dim)
        else:
            testset  = datafile.load_testset(cfg.test.testsetfile)

        print(cfg.makeReport())

        ticks, results, averages, stds = [], [], [], []
        for counter, (order, goal, _, effect) in enumerate(history):
            if (counter) % cfg.test.freq == 0:
                ticks.append(counter)

                result   = exp.test_results(bot, learner, testset)
                avg, std = exp.test_perfs(testset, result)

                results.append(result)
                averages.append(avg)
                stds.append(std)
                print("{}{:5d}: {}{:6.4f}{}".format(gfx.purple, counter, gfx.cyan, avg, gfx.end))

            if counter > cfg.test.max:
                break

            learner.add_xy(order, effect)

        exp.save_test(cfg, date, tuple(testset), tuple(ticks), tuple(results),
                      tuple(averages), tuple(stds))

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        bot.close()

    print("ran for {}s.".format(int(time.time() - start_time)))
