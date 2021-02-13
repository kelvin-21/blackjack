import unittest
from domain.model import Card, Suit, Rank


class TestCard(unittest.TestCase):
    def setUp(self):
        self.card_A = Card(Suit.SPADE, Rank.A)
        self.card_A_2 = Card(Suit.SPADE, Rank.A)
        self.card_different_suit = Card(Suit.DIAMOND, Rank.A)
        self.card_different_rank = Card(Suit.SPADE, Rank.TWO)

    # operator ==

    def card_is_equal_to_itself(self):
        result = (self.card_A == self.card_A)

        self.assertTrue(result)

    def same_cards_with_different_reference_are_equal(self):
        result = (self.card_A == self.card_A_2)

        self.assertTrue(result)

    def cards_with_different_suit_are_not_equal(self):
        result = (self.card_A == self.card_different_suit)

        self.assertFalse(result)

    def cards_with_different_rank_are_not_equal(self):
        result = (self.card_A == self.card_different_rank)

        self.assertFalse(result)

    # operator !=

    def card_is_not_nonequal_to_itself(self):
        result = (self.card_A != self.card_A)

        self.assertFalse(result)

    def same_cards_with_different_reference_are_not_nonequal(self):
        result = (self.card_A != self.card_A_2)

        self.assertFalse(result)

    def cards_with_different_suit_are_nonequal(self):
        result = (self.card_A != self.card_different_suit)

        self.assertTrue(result)

    def cards_with_different_rank_are_nonequal(self):
        result = (self.card_A != self.card_different_rank)

        self.assertTrue(result)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestCard('card_is_equal_to_itself'))
    suite.addTest(TestCard('same_cards_with_different_reference_are_equal'))
    suite.addTest(TestCard('cards_with_different_suit_are_not_equal'))
    suite.addTest(TestCard('cards_with_different_rank_are_not_equal'))
    suite.addTest(TestCard('card_is_not_nonequal_to_itself'))
    suite.addTest(TestCard('same_cards_with_different_reference_are_not_nonequal'))
    suite.addTest(TestCard('cards_with_different_suit_are_nonequal'))
    suite.addTest(TestCard('cards_with_different_rank_are_nonequal'))

    runner = unittest.TextTestRunner()
    runner.run(suite)