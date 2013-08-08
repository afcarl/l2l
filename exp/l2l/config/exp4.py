import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'lightcube'
cfg.sim.toys.toy.type = 'cube'
cfg.sim.toys.toy.restitution = 1.0
cfg.sim.toys.toy.density     = 0.2
