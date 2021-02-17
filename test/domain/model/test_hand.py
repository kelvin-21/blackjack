import unittest
from domain.model import Hand, HandStatus, Card, Suit, Rank

class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = Hand()
        self.card_8 = Card(Suit.SPADE, Rank.EIGHT)
        self.card_9 = Card(Suit.SPADE, Rank.NINE)
        self.card_10 = Card(Suit.SPADE, Rank.TEN)
        self.card_J = Card(Suit.SPADE, Rank.J)
        self.card_A = Card(Suit.SPADE, Rank.A)
        self.card_A_2 = Card(Suit.SPADE, Rank.A)

    # ----- one card -----

    def test_add_card(self):
        self.hand.add_card(self.card_8)

        self.assertEqual(len(self.hand.hand_value), 1)
        self.assertEqual(self.hand.hand_value, [8])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    def test_add_card_A(self):
        self.hand.add_card(self.card_A)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [1, 11])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    # ----- two cards -----

    def test_add_two_card(self):
        self.hand.add_card(self.card_9)
        self.hand.add_card(self.card_10)

        self.assertEqual(len(self.hand.hand_value), 1)
        self.assertEqual(self.hand.hand_value, [19])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    def test_add_A_and_add_another_card(self):
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_J)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [11, 21])
        self.assertEqual(self.hand.status, HandStatus.BLACKJACK)

    def test_add_card_and_add_A(self):
        card_A = Card(Suit.SPADE, Rank.A)
        card = Card(Suit.SPADE, Rank.J)
        self.hand.add_card(card)
        self.hand.add_card(card_A)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [11, 21])
        self.assertEqual(self.hand.status, HandStatus.BLACKJACK)

    def test_two_A(self):
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [2, 12])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    def test_two_A_different_reference(self):
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A_2)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [2, 12])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    # ----- three cards -----

    def test_three_A(self):
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [3, 13])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    def test_add_card_and_two_A(self):
        self.hand.add_card(self.card_9)
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)

        self.assertEqual(len(self.hand.hand_value), 2)
        self.assertEqual(self.hand.hand_value, [11, 21])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    # ----- handle bust -----
    
    def given_bust_then_return_empty_hand_value(self):
        self.hand.add_card(self.card_9)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_8)

        self.assertEqual(self.hand.hand_value, [])
        self.assertEqual(self.hand.status, HandStatus.BUST)

    def given_A_as_11_bust_then_use_it_as_1_only(self):
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_8)

        self.assertEqual(self.hand.hand_value, [17])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    def given_two_A_as_11_bust_then_use_it_as_1_only(self):
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_A)

        self.assertEqual(self.hand.hand_value, [18])
        self.assertEqual(self.hand.status, HandStatus.LIVE)

    def given_five_cards_and_not_bust_then_status_is_fivecard(self):
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)

        self.assertEqual(self.hand.hand_value, [19])
        self.assertEqual(self.hand.status, HandStatus.FIVECARD)

    def given_five_cards_and_bust_then_status_is_bust(self):
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_A)
        self.hand.add_card(self.card_A)

        self.assertEqual(self.hand.hand_value, [])
        self.assertEqual(self.hand.status, HandStatus.BUST)

    # ----- hand value -----

    def test_calculate_update_hand_value(self):
        self.hand.add_card(self.card_8)
        self.hand.add_card(self.card_9)
        self.hand.add_card(self.card_A)
        original = self.hand.hand_value
        self.hand.hand_value = [-1]
        self.hand.calculate_update_hand_value()

        self.assertEqual(self.hand.hand_value, original)
        self.assertEqual(self.hand.hand[0], self.card_8)
        self.assertEqual(self.hand.hand[1], self.card_9)
        self.assertEqual(self.hand.hand[2], self.card_A)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestHand('test_add_card'))
        suite.addTest(TestHand('test_add_card_A'))
        suite.addTest(TestHand('test_add_two_card'))
        suite.addTest(TestHand('test_add_A_and_add_another_card'))
        suite.addTest(TestHand('test_add_card_and_add_A'))
        suite.addTest(TestHand('test_two_A'))
        suite.addTest(TestHand('test_two_A_different_reference'))
        suite.addTest(TestHand('test_three_A'))
        suite.addTest(TestHand('test_add_card_and_two_A'))
        suite.addTest(TestHand('given_bust_then_return_empty_hand_value'))
        suite.addTest(TestHand('given_A_as_11_bust_then_use_it_as_1_only'))
        suite.addTest(TestHand('given_two_A_as_11_bust_then_use_it_as_1_only'))
        suite.addTest(TestHand('given_five_cards_and_not_bust_then_status_is_fivecard'))
        suite.addTest(TestHand('given_five_cards_and_bust_then_status_is_bust'))
        suite.addTest(TestHand('test_calculate_update_hand_value'))

        runner = unittest.TextTestRunner()
        runner.run(suite)

    
if __name__ == '__main__':
    TestHand.run_all_test()