import testenv
import random

from explib import exp

def test_tests():
    """Test if tests are correctly created"""
    check = True

    s_bounds = ((0., 1.), (0., 1.), (0., 4.))
    check *= exp.create_tests(s_bounds, 3, fixed_dim = [None, None, 3.0]) == ((0.0, 0.0, 3.0), (0.0, 0.5, 3.0), (0.0, 1.0, 3.0), (0.5, 0.0, 3.0), (0.5, 0.5, 3.0), (0.5, 1.0, 3.0), (1.0, 0.0, 3.0), (1.0, 0.5, 3.0), (1.0, 1.0, 3.0))

    return check


tests = [test_tests]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))