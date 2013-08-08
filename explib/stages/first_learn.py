# Adjusting paths.
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '../../../goals')))
import random
import time

import treedict


from toolbox import gfx

import goals
import robots
from models.learner import Learner
from goals.guide import Guide
from goals.explorer.effect import BoundedRandomExplorer
from goals.explorer.motor  import MotorBabble

import boxsim

from bias import cluster
from .. import exp

    ## Configuration ##

def run_first(cfg):

    start_time = time.time()

    try:
        if cfg.hardware.seed.get('primary', None) is None:
            seed = random.randint(0, sys.maxint)
            cfg.hardware.seed.primary   = seed
        random.seed(cfg.hardware.seed.primary)

        bot = robots.build_robot(cfg.sim)

            ## Configuration ##

        goalscfg = treedict.TreeDict()

        goalscfg.effect.explorer = BoundedRandomExplorer

        cfg.goals.update(goalscfg, overwrite = False)

        cfg.goals.effect.s_feats  = s_feats  = bot.s_feats
        cfg.goals.effect.s_bounds = s_bounds = bot.s_bounds
        cfg.goals.motor.m_feats   = m_feats  = bot.m_feats
        cfg.goals.motor.m_bounds  = m_bounds = bot.m_bounds

            ## Instanciation of core modules ##

        s_explorer = BoundedRandomExplorer(s_feats, cfg.goals)
        if 'explorename' in cfg.goals.effect:
            if cfg.goals.effect.explorername == 'cluster':
                s_explorer = cluster.ClusterExplorer(s_feats, cfg.goals)
            elif cfg.goals.effect.explorername == 'cluster_im':
                s_explorer = cluster.ClusterIMExplorer(s_feats, cfg.goals)

        m_explorer = MotorBabble(bot.m_feats, bot.m_bounds, cfg.goals)
        guide      = Guide(m_feats, s_feats, m_bounds, cfg.goals,
                           goalexplorer = s_explorer, motorbabble = m_explorer)
        learner    = Learner(m_feats, s_feats, m_bounds, fwd = 'ES-LWLR', inv = 'L-BFGS-B')

        cfg.freeze()
        print(cfg.makeReport())

            ## Runing learning ##

        for i in xrange(cfg.exp.trials):
            exp.learn(bot, guide, learner)
            if not cfg.sim.verbose:
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
