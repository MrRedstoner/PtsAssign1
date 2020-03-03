import unittest

from relation_class import get_relation_class


class MyTestCase(unittest.TestCase):
    def test_rel_class(self):
        res = get_relation_class({1, 2, 3})

        obj0 = res()
        self.assertEqual("{}", str(obj0))
        self.assertEqual(False, (1, 2) in obj0)

        obj1 = obj0 + (1, 2)
        self.assertEqual("{1: {2}}", str(obj1))
        self.assertEqual(False, (1, 2) in obj0)
        self.assertEqual(True, (1, 2) in obj1)

    def test_exceptions(self):
        res = get_relation_class({1, 2, 3})

        obj0 = res()
        with self.assertRaises(AssertionError):
            obj0 + (0, 1)
        with self.assertRaises(AssertionError):
            (0, 1) in obj0


if __name__ == '__main__':
    unittest.main()
