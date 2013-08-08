import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'centerpiece'
cfg.sim.base_pos = 400, 400
