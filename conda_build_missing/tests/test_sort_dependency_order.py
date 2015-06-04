import unittest

from conda_build_missing.tests import DummyPackage
from conda_build_missing import sort_dependency_order


class Test_sort_dependency_order(unittest.TestCase):
    def test_basic_with_missing(self):
        a = DummyPackage('a', ['b'])
        b = DummyPackage('b', ['c'], ['d'])
        d = DummyPackage('d')
        self.assertEqual(sort_dependency_order([a, d, b]),
                         [d, b, a])

    def test_duplicate(self):
        a = DummyPackage('a', ['b'])
        simple_a = DummyPackage('a')
        b = DummyPackage('b', ['c'], ['d'])
        d = DummyPackage('d')
        self.assertEqual(sort_dependency_order([a, simple_a, d, b]),
                         [d, b, a, simple_a])


if __name__ == '__main__':
    unittest.main()
