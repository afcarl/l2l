import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'bigger'
cfg.sim.arm_lengths = [350.0/cfg.sim.armsize]*cfg.sim.armsize

