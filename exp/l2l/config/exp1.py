import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'mirror'
cfg.sim.toys.toy.pos = 300, 350