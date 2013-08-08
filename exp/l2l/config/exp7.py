import treedict
import common

cfg = treedict.TreeDict()
cfg.update(common.cfg)

lengths = [1.3**(cfg.sim.armsize-i) for i in xrange(cfg.sim.armsize)]
total_l = sum(lengths)
lengths = [l_i/total_l*300.0 for l_i in lengths]

cfg.exp.name = 'irregular'
cfg.sim.arm_lengths = lengths
