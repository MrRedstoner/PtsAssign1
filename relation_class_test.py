import unittest

from relation_class import get_relation_class


class MyTestCase(unittest.TestCase):
    def test_rel_class(self):
        res = get_relation_class({1, 2, 3})

        obj0 = res()
        self.assertNotIn((1, 2), obj0)

        obj1 = obj0 + (1, 2)
        self.assertIn((1, 2), obj1)
        # check immutability
        self.assertNotIn((1, 2), obj0)

        # double add an element
        obj2 = (obj1 + (1, 3)) + (1, 2)
        self.assertIn((1, 2), obj2)
        self.assertIn((1, 3), obj2)

        obj3 = obj2 - (1, 2)
        self.assertNotIn((1, 2), obj3)
        self.assertIn((1, 3), obj3)
        # check immutability
        self.assertIn((1, 2), obj2)

    def test_exceptions(self):
        res = get_relation_class({1, 2, 3})

        obj0 = res()
        with self.assertRaises(AssertionError):
            _ = obj0 + (0, 1)
        with self.assertRaises(AssertionError):
            _ = obj0 - (0, 1)
        with self.assertRaises(AssertionError):
            _ = (0, 1) in obj0


if __name__ == '__main__':
    unittest.main()
