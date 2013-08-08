import os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../../goals')))
import random
import goals
import sys

import treedict

from toolbox import gfx

from models.learner import Learner
from goals.guide import Guide
from goals.explorer.effect import BoundedRandomExplorer, GridExplorer
from goals.explorer.motor  import MotorBabble

import robots

from bias import bias
from .. import exp
from ..runs import datafile

def run_second(cfg):

    start_time = time.time()

    try:
        if cfg.hardware.seed.get('secondary', None) is None:
            seed = random.randint(0, sys.maxint)
            cfg.hardware.seed.secondary   = seed
        random.seed(cfg.hardware.seed.secondary)

        data = datafile.load_data(cfg.hardware.primaryfile)
        date, primcfg, history = data['date'], data['cfg'], data['history']

        cfg.update(primcfg, overwrite = False)
        primcfg = primcfg.copy(deep = True)

        bot = robots.build_robot(cfg.sim)

        # this should not change
        assert cfg.goals.motor.m_feats   == bot.m_feats, 'expected {}, got {}'.format(cfg.goals.motor.m_feats, bot.m_feats)
        assert cfg.goals.motor.m_bounds  == bot.m_bounds
        # sensors might change
        cfg.goals.effect.s_feats  = bot.s_feats
        cfg.goals.effect.s_bounds = bot.s_bounds


            ## Configuration ##

        cfg.goals.effect.res = 10

            ## Bias loading ##

        grid_expl = GridExplorer(primcfg.goals.effect.s_feats, cfg = primcfg.goals)
        dataset   = []
        for order, goal, _, effect in history:
            effect = [min(b_max, max(b_min, e_i)) for e_i, (b_min, b_max) in zip(effect, primcfg.goals.effect.s_bounds)]
            grid_expl.add_effect(effect, goal = goal)
            dataset.append((order, effect))

        bs = bias.IMBias(dataset, effectexplorer = grid_expl)

            ## Instanciation of core modules ##

        #s_explorer = bias.GridBias(bs, cfg.effect.cfg.interest.max_deriv, s_feats, cfg = cfg.effect.cfg)
        s_explorer = BoundedRandomExplorer(bot.s_feats, cfg.goals)
        m_babble   = MotorBabble(bot.m_feats, bot.m_bounds, cfg.goals)
        m_explorer = bias.MotorBias(bs, m_babble, cfg.goals)
        guide      = Guide(bot.m_feats, bot.s_feats, bot.m_bounds, cfg.goals,
                           goalexplorer = s_explorer, motorbabble = m_explorer)

        learner  = Learner(bot.m_feats, bot.s_feats, bot.m_bounds,
                           fwd = 'ES-LWLR', inv = 'L-BFGS-B')

        cfg.freeze()
        print(cfg.makeReport())

            ## Running learning ##

        for i in xrange(cfg.exp.trials):
            exp.learn(bot, guide, learner)
            gfx.print_progress(i+1, cfg.exp.trials,
                               prefix = '{}learning... {}'.format(gfx.purple, gfx.cyan),
                               suffix = gfx.end, eta = 1)
        print ''

        exp.save_data(cfg, guide)

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        bot.close()

    print("ran for {}s.".format(int(time.time() - start_time)))
