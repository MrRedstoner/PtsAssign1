import unittest

from relation_class import get_relation_class


class MyTestCase(unittest.TestCase):
    def test_rel_class(self):
        res=get_relation_class({1,2,3})

    def test_exceptions(self):
        pass

if __name__ == '__main__':
    unittest.main()
