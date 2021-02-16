import unittest
from domain.model import Suit, Rank
from controller.handler.card_input_handler import CardInputHandler, CardInputResult


class TestCardInputHandler(unittest.TestCase):
    def given_empty_arg_then_return_result_with_both_none(self):
        self.test_handle('', CardInputResult(None, None))

    def given_suit_arg_then_return_result_with_suit(self):
        self.test_handle('diamond', CardInputResult(Suit.DIAMOND, None))
        self.test_handle('club', CardInputResult(Suit.CLUB, None))
        self.test_handle('heart', CardInputResult(Suit.HEART, None))
        self.test_handle('spade', CardInputResult(Suit.SPADE, None))

    def given_cap_suit_arg_then_return_none(self):
        self.test_handle('DIAMOND', None)
        self.test_handle('CLUB', None)
        self.test_handle('HEART', None)
        self.test_handle('SPADE', None)
        pass

    def given_rank_arg_then_return_result_with_rank(self):
        self.test_handle('A', CardInputResult(None, Rank.A))
        self.test_handle('2', CardInputResult(None, Rank.TWO))
        self.test_handle('10', CardInputResult(None, Rank.TEN))
        self.test_handle('J', CardInputResult(None, Rank.J))
        self.test_handle('Q', CardInputResult(None, Rank.Q))
        self.test_handle('K', CardInputResult(None, Rank.K))

    def given_small_rank_arg_then_return_none(self):
        self.test_handle('a', None)
        self.test_handle('j', None)
        self.test_handle('q', None)
        self.test_handle('k', None)

    def given_suit_rank_arg_then_return_result_with_suit_rank(self):
        self.test_handle('diamond A', CardInputResult(Suit.DIAMOND, Rank.A))
        self.test_handle('A diamond', CardInputResult(Suit.DIAMOND, Rank.A))
        self.test_handle('spade 2', CardInputResult(Suit.SPADE, Rank.TWO))
        self.test_handle('2 spade', CardInputResult(Suit.SPADE, Rank.TWO))
        self.test_handle('heart 10', CardInputResult(Suit.HEART, Rank.TEN))
        self.test_handle('10 heart', CardInputResult(Suit.HEART, Rank.TEN))
        self.test_handle('club J', CardInputResult(Suit.CLUB, Rank.J))
        self.test_handle('J club', CardInputResult(Suit.CLUB, Rank.J))
        self.test_handle('diamond Q', CardInputResult(Suit.DIAMOND, Rank.Q))
        self.test_handle('Q diamond', CardInputResult(Suit.DIAMOND, Rank.Q))

    def given_two_items_but_not_suit_rank_pattern_then_return_none(self):
        self.test_handle('diamon A', None)
        self.test_handle('unknown A', None)
        self.test_handle('A diamon', None)
        self.test_handle('A unknown', None)
        self.test_handle('diamond a', None)
        self.test_handle('a diamond', None)

    def given_unknown_arg_then_return_none(self):
        self.test_handle('test', None)
        self.test_handle('test ABC', None)
        self.test_handle('/test', None)
        self.test_handle('/test ABC', None)

    # helper function
    def test_handle(self, arg: str, expected: CardInputResult):
        result = CardInputHandler.handle(arg)
        self.assertEqual(result, expected)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestCardInputHandler('given_empty_arg_then_return_result_with_both_none'))
        suite.addTest(TestCardInputHandler('given_suit_arg_then_return_result_with_suit'))
        suite.addTest(TestCardInputHandler('given_cap_suit_arg_then_return_none'))
        suite.addTest(TestCardInputHandler('given_rank_arg_then_return_result_with_rank'))
        suite.addTest(TestCardInputHandler('given_small_rank_arg_then_return_none'))
        suite.addTest(TestCardInputHandler('given_suit_rank_arg_then_return_result_with_suit_rank'))
        suite.addTest(TestCardInputHandler('given_two_items_but_not_suit_rank_pattern_then_return_none'))
        suite.addTest(TestCardInputHandler('given_unknown_arg_then_return_none'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestCardInputHandler.run_all_test()