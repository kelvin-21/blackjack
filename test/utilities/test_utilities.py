import unittest
from utilities import Utilities


class TestUtilities(unittest.TestCase):
    def setUp(self):
        self.d_none = None
        self.d_empty = {}
        self.d_1 = {'a': 20, 'b': 30}
        self.d_2 = {
            'a': {
                'a_1': 10,
                'a_2': 20,
            },
            'b': {
                'b_1': 6,
                'b_2': 7
            }
        }
        self.d_2_asymmetric = {'a': 3, 'b': {'d': 5}}
        self.d_3_asymmetric = {
            'a': 1,
            'b': {
                'd': 2,
                'e': 3
            },
            'c': {
                'f': {
                    'h': 6,
                    'i': 7
                },
                'g': 8
            }
        }

    def given_none_dict_then_return_depth_0(self):
        depth = Utilities.depth(self.d_none)
        self.assertEqual(depth, 0)

    def given_empty_dict_then_return_depth_1(self):
        depth = Utilities.depth(self.d_empty)
        self.assertEqual(depth, 1)

    def given_dict_with_depth_1_then_return_depth_1(self):
        depth = Utilities.depth(self.d_1)
        self.assertEqual(depth, 1)

    def given_nested_dict_with_depth_2_then_return_depth_2(self):
        depth = Utilities.depth(self.d_2)
        self.assertEqual(depth, 2)

    def given_asymmetric_nested_dict_with_depth_2_then_return_depth_2(self):
        depth = Utilities.depth(self.d_2_asymmetric)
        self.assertEqual(depth, 2)

    def given_asymmetric_nested_dict_with_depth_3_then_return_depth_3(self):
        depth = Utilities.depth(self.d_3_asymmetric)
        self.assertEqual(depth, 3)

    def given_none_dict_then_return_sum_none(self):
        result = Utilities.sum_nested_dict(self.d_none)
        self.assertIsNone(result)

    def given_empty_dict_then_return_sum_none(self):
        result = Utilities.sum_nested_dict(self.d_none)
        self.assertIsNone(result)

    def given_dict_with_depth_1_then_compute_sum(self):
        result = Utilities.sum_nested_dict(self.d_1)
        self.assertEqual(result, 50)

    def given_dict_with_depth_2_then_compute_sum(self):
        result = Utilities.sum_nested_dict(self.d_2)
        self.assertEqual(result, 43)

    def given_asymmetric_dict_with_depth_2_then_return_sum_none(self):
        result = Utilities.sum_nested_dict(self.d_2_asymmetric)
        self.assertIsNone(result)
    
    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestUtilities('given_none_dict_then_return_depth_0'))
        suite.addTest(TestUtilities('given_empty_dict_then_return_depth_1'))
        suite.addTest(TestUtilities('given_dict_with_depth_1_then_return_depth_1'))
        suite.addTest(TestUtilities('given_nested_dict_with_depth_2_then_return_depth_2'))
        suite.addTest(TestUtilities('given_asymmetric_nested_dict_with_depth_2_then_return_depth_2'))
        suite.addTest(TestUtilities('given_asymmetric_nested_dict_with_depth_3_then_return_depth_3'))
        suite.addTest(TestUtilities('given_none_dict_then_return_sum_none'))
        suite.addTest(TestUtilities('given_empty_dict_then_return_sum_none'))
        suite.addTest(TestUtilities('given_dict_with_depth_1_then_compute_sum'))
        suite.addTest(TestUtilities('given_dict_with_depth_2_then_compute_sum'))
        suite.addTest(TestUtilities('given_asymmetric_dict_with_depth_2_then_return_sum_none'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestUtilities.run_all_test()