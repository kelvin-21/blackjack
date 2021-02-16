import unittest
from controller.handler.card_request_handler import CardRequestHandler, CardRequestResult


class TestCardRequestHandler(unittest.TestCase):
    def given_empty_arg_then_return_result_false(self):
        self.test_handle('', CardRequestResult(False))

    def given_positive_arg_then_return_result_true(self):
        self.test_handle('yes', CardRequestResult(True))
        self.test_handle('Yes', CardRequestResult(True))
        self.test_handle('YES', CardRequestResult(True))
        self.test_handle('y', CardRequestResult(True))
        self.test_handle('Y', CardRequestResult(True))
        self.test_handle('true', CardRequestResult(True))
        self.test_handle('True', CardRequestResult(True))
        self.test_handle('TRUE', CardRequestResult(True))
        self.test_handle('t', CardRequestResult(True))
        self.test_handle('T', CardRequestResult(True))

    def given_negative_arg_then_return_result_false(self):
        self.test_handle('no', CardRequestResult(False))
        self.test_handle('No', CardRequestResult(False))
        self.test_handle('NO', CardRequestResult(False))
        self.test_handle('n', CardRequestResult(False))
        self.test_handle('N', CardRequestResult(False))
        self.test_handle('false', CardRequestResult(False))
        self.test_handle('False', CardRequestResult(False))
        self.test_handle('FALSE', CardRequestResult(False))
        self.test_handle('f', CardRequestResult(False))
        self.test_handle('F', CardRequestResult(False))

    # helper function
    def test_handle(self, arg: str, expected: CardRequestResult):
        result = CardRequestHandler.handle(arg)
        self.assertEqual(result, expected)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestCardRequestHandler('given_empty_arg_then_return_result_false'))
        suite.addTest(TestCardRequestHandler('given_positive_arg_then_return_result_true'))
        suite.addTest(TestCardRequestHandler('given_negative_arg_then_return_result_false'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestCardRequestHandler.run_all_test()