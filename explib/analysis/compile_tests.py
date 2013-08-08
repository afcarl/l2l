import random

import bias
from bias import meshgrid

def create_tests(effects, m, res):

    assert m <= n
    box = boxsim.UniformizeSim(boxsim.BoxSim(cfg.sim))

    dataset = create_examples(box, n)

    mg = bias.SensorBias(dataset, box.s_bounds, res)


def create_examples(box, n):

    dataset = []
    for _ in range(n):
        random_order = tuple(random.uniform(o_min, o_max) for o_min, o_max in box.m_bounds)
        effect = box.execute_order(random_order)
        dataset.append((random_order, effect))

    return dataset




if __name__ == '__main__':
    create_examples(box, n)
