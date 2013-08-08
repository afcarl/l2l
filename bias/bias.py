import random
import toolbox

from goals.explorer.effect import cell
from goals.explorer.effect import grid

import meshgrid

class IMBias(object):

    def __init__(self, dataset, effectexplorer = None):
        """"""
        assert effectexplorer is not None
        self.eexplorer = effectexplorer
        self.dataset   = dataset

        self._compute_interest()
        self._order_weights()
        self._compute_order_bias()

    def _compute_interest(self):
        self.interests = {cell.uid:cell.interest_all() for cell in self.eexplorer.cell_list()}

    def _order_weights(self):
        self.orders  = []
        self.weights = []
        for order, effect in self.dataset:
            cell = self.eexplorer.point2cell(effect)
            if self.interests[cell.uid] > 0.0:
                self.orders.append(order)
                self.weights.append(self.interests[cell.uid])

    def _compute_order_bias(self):
        self.order_bias = []
        weights_cpy = list(self.weights)
        assert all(w > 0.0 for w in weights_cpy)
        for _ in xrange(len(self.orders)):
            idx = toolbox.roulette_wheel(weights_cpy)
            weights_cpy[idx] = 0.0
            self.order_bias.append(self.orders[idx])


class DualCellBias(cell.DualCell):

    def __init__(self, bounds, graph, uid, cfg, depth = 0, w = None):
        cell.DualCell.__init__(self, bounds, graph, uid, cfg, depth = 0, w = None)

    def setup(self, bias, bias_duration):
        self.bias = bias
        self.bias_duration = bias_duration

    def interest(self):
        it = cell.DualCell.interest(self)
        d  = float(min(len(self.gcell), self.bias_duration))
        return (it*d + self.bias * (self.bias_duration - d))/self.bias_duration


class GridBias(grid.GridExplorer):

    def __init__(self, bias, bias_duration, s_feats, cfg = grid.defaultcfg, cellclass = DualCellBias):
        self.bias = bias
        self.bias_duration = bias_duration
        grid.GridExplorer.__init__(self, s_feats, cfg = cfg, cellclass = cellclass)
        self.setup()

    def setup(self):
        for cell in self.grid.values():
            cell.setup(self.bias.interests[cell.uid], self.bias_duration)

class MotorBias(object):

    def __init__(self, bias, motorbabble, cfg):
        self.bias = bias
        self.motorbabble = motorbabble
        self.order_cursor = 0
        self.cfg = cfg

    def babble(self):
        if self.order_cursor < len(self.bias.order_bias) and random.random() < self.cfg.motor.motorbias_ratio:
            order = self.bias.order_bias[self.order_cursor]
            self.order_cursor += 1
        else:
            order = self.motorbabble.babble()
        return order

    def add_order(self, order, effect = None):
        return self.motorbabble.add_order(order, effect = effect)

    @property
    def finished(self):
        return True




