import testenv
import random

from explib.runs import names

def test_names():
    """Test if names are correctly transformed into keys"""
    check = True
    check *= names.name2key("origin[0.01]exp[2.01].s.t") == (names.kSecondaryTest, 'origin', 0, 'exp', 2, 1)
    check *= names.name2key("exp[0.01].p.d") == (names.kPrimaryData, 'exp', 0, 1)
    check *= names.name2key("origin[3].exp.s.r") == (names.kSecondaryResults, 'origin', 3, 'exp')
    return check


tests = [test_names]

if __name__ == "__main__":
    print("\033[1m%s\033[0m" % (__file__,))
    for t in tests:
        print('%s %s' % ('\033[1;32mPASS\033[0m' if t() else
                         '\033[1;31mFAIL\033[0m', t.__doc__))