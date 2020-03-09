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
        obj2 = ((obj1 + (1, 3)) + (1, 2)) + (2, 3)
        self.assertIn((1, 2), obj2)
        self.assertIn((1, 3), obj2)
        self.assertIn((2, 3), obj2)

        obj3 = obj2 - (1, 2)
        self.assertNotIn((1, 2), obj3)
        self.assertIn((1, 3), obj3)
        self.assertIn((2, 3), obj3)
        # check immutability
        self.assertIn((1, 2), obj2)

        obj4 = obj3 | obj1
        self.assertIn((1, 2), obj4)
        self.assertIn((1, 3), obj4)
        self.assertIn((2, 3), obj4)
        # check immutability
        self.assertNotIn((1, 2), obj3)
        self.assertNotIn((1, 3), obj1)

        obj5 = obj3 & obj1
        self.assertNotIn((1, 2), obj5)
        self.assertNotIn((1, 3), obj5)
        self.assertNotIn((2, 3), obj5)
        # check immutability
        self.assertIn((1, 2), obj1)
        self.assertIn((1, 3), obj3)
        self.assertIn((2, 3), obj3)

        obj6 = ~ obj4
        self.assertIn((2, 1), obj6)
        self.assertIn((3, 1), obj6)
        self.assertIn((3, 2), obj6)
        # check immutability
        self.assertIn((1, 2), obj4)
        self.assertIn((1, 3), obj4)
        self.assertIn((2, 3), obj4)

        obj7 = obj4 - obj1
        self.assertNotIn((1, 2), obj7)
        self.assertIn((1, 3), obj7)
        self.assertIn((2, 3), obj7)
        # check immutability
        self.assertIn((1, 2), obj1)
        self.assertIn((1, 2), obj4)
        self.assertIn((1, 3), obj4)
        self.assertIn((2, 3), obj4)

        obj8 = obj4.compose(obj6)
        self.assertIn((1, 1), obj8)  # 1->2,2->1
        self.assertIn((2, 2), obj8)  # 2->3,3->2
        self.assertIn((1, 2), obj8)  # 1->3,3->2
        self.assertIn((2, 1), obj8)  # 2->3,3->1
        # check immutability
        self.assertIn((2, 1), obj6)
        self.assertIn((3, 1), obj6)
        self.assertIn((3, 2), obj6)
        self.assertIn((1, 2), obj4)
        self.assertIn((1, 3), obj4)
        self.assertIn((2, 3), obj4)

    def test_exceptions(self):
        res = get_relation_class({1, 2, 3})

        obj0 = res()
        with self.assertRaises(AssertionError):
            _ = obj0 + (0, 1)
        with self.assertRaises(AssertionError):
            _ = obj0 - (0, 1)
        with self.assertRaises(AssertionError):
            _ = (0, 1) in obj0
        with self.assertRaises(AssertionError):
            bad_obj = get_relation_class({1, 2, 3, 4})()
            _ = obj0 | bad_obj
        with self.assertRaises(AssertionError):
            bad_obj = get_relation_class({1, 2, 3, 4})()
            _ = obj0 & bad_obj
        with self.assertRaises(AssertionError):
            bad_obj = get_relation_class({1, 2, 3, 4})()
            _ = obj0 - bad_obj


if __name__ == '__main__':
    unittest.main()
