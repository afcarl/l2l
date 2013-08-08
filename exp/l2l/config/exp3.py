import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'heavycube'
cfg.sim.toys.toy.type = 'cube'
cfg.sim.toys.toy.restitution = 0.35
cfg.sim.toys.toy.density     = 3.0
