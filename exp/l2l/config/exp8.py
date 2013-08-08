import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

cfg.exp.name = 'arm'
cfg.sim.sensors = 'arm'
