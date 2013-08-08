import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'cornercase'
cfg.sim.base_pos = 80, 80
cfg.sim.toys.toy.pos  = 180, 350
