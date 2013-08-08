import random, sys
import treedict

cfg = treedict.TreeDict()

cfg.sim.robotclass = 'boxsim.BoxSim'
cfg.sim.visu = False

cfg.sim.steps           = 12*60
cfg.sim.armsize         = 6
cfg.sim.arm_lengths     = [300.0/cfg.sim.armsize]*cfg.sim.armsize
cfg.sim.base_pos        = 400, 80
cfg.sim.angle_limit     = 2.0
cfg.sim.max_speed       = 2.0

cfg.sim.verbose         = False

cfg.sim.filters.uniformize = True
cfg.sim.filters.s_feats = None
cfg.sim.filters.s_bounds_factor = None

cfg.sim.toys.toy.pos         = (550, 350)
cfg.sim.toys.toy.width       = 40
cfg.sim.toys.toy.type        = 'ball'
cfg.sim.toys.toy.friction    = 1.0
cfg.sim.toys.toy.restitution = 0.7
cfg.sim.toys.toy.density     = 1.0

cfg.sim.toy_order            = ['toy']
cfg.sim.sensors              = 'toy'
cfg.sim.motors               = 'commonvelocity'


cfg.goals.guide.min_orderbabble   = 500
cfg.goals.guide.ratio_orderbabble = 0.3
cfg.goals.motor.motorbias_ratio   = 0.8

cfg.goals.effect.s_res               = 10
cfg.goals.effect.competence.function = 'log'
cfg.goals.effect.interest.max_deriv  = 10
cfg.goals.effect.competence.min_d    = 0.01

cfg.exp.trials = 10000
