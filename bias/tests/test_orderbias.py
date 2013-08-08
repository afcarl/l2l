import testenv
import random

import treedict

from goals.explorer.effect import StaticExplorer
from goals.explorer.effect import grid

import bias

def test_orderbias():
    """Test orderbias methods"""
    cfg = treedict.TreeDict()
    cfg.s_areas = ( ((0.0, 10.0),), ((10.0, 20.0),), ((20.0, 30.0),) )

    se = StaticExplorer((1,), cfg = cfg)

    dataset = []
    for i in xrange(6):
        goal   = (5.0,)
        effect = (float(i),)
        order  = effect
        se.add_effect(effect, goal = goal)
        dataset.append((order, effect))

    for i in xrange(6):
        goal   = (15.0,)
        effect = (10.0 + float(i)/2,)
        order  = effect
        se.add_effect(effect, goal = goal)
        dataset.append((order, effect))

    for i in xrange(6):
        goal   = (25.0,)
        effect = (25.0,)
        order  = effect
        se.add_effect(effect, goal = goal)
        dataset.append((order, effect))

    ob = bias.IMBias(se, dataset)

    #print ", ".join(str(int(x[0])) for x in ob.order_bias)

    return True

def test_cell():
    """Test DualCellBias methods"""

    dc = bias.DualCellBias(((0.0, 10.0), (0.0, 10.0)), None, None)
    dc.setup(3.0, 20)

    check = True

    for i in xrange(100):
        goal   = (5.0, 4.0)
        effect = goal
        dc.add(effect, goal = goal)
        check *= dc.interest() == max(0.0, 3.0*(20-i-1)/20)

    return check

def test_gridbias():
    """Test basic methods of GridBias"""

    cfg = treedict.TreeDict()
    cfg.s_bounds = ((0.0, 1.0), (0.0, 1.0))
    cfg.s_res    = (10, 10)


    ge = grid.GridExplorer((0, 1), cfg = cfg)
    dataset = []

    for _ in xrange(1000):
        effect     = (random.random(), random.random())
        goal       = (random.random(), random.random())
        prediction = (random.random(), random.random())
        ge.add_effect(effect, goal = goal, prediction = prediction)
        order      = (random.random(),)*6
        dataset.append((order, effect))

    ob = bias.IMBias(ge, dataset)
    gb = bias.GridBias(ob, (0, 1), cfg = cfg)
    gb.setup(10)

    for _ in xrange(1000):
        effect     = (random.random(), random.random())
        goal       = (random.random(), random.random())
        prediction = (random.random(), random.random())
        ge.add_effect(effect, goal = goal, prediction = prediction)
        ge.next_goal()

    return True

tests = [test_orderbias,
         test_cell,
         test_gridbias]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))