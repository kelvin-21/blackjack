import unittest
from domain.model import Dealer, Card, Suit, Rank, PlayerStatus


class TestDealer(unittest.TestCase):
    def setUp(self):
        self.dealer = Dealer(16)
        self.card_A = Card(Suit.SPADE, Rank.A)
        self.card_9 = Card(Suit.SPADE, Rank.NINE)

    def dealer_is_created_with_dealer_status(self):
        self.assertEqual(self.dealer.status, PlayerStatus.DEALER)

    def given_dealer_bust_then_the_status_is_dealer(self):
        self.dealer.add_card(self.card_9)
        self.dealer.add_card(self.card_9)
        self.dealer.add_card(self.card_9)

        self.assertEqual(self.dealer.status, PlayerStatus.DEALER)

    def given_hand_value_less_then_16_then_request_card(self):
        for hand_value in range(2, 16):
            self.test_is_request_card(hand_value, True)

    def given_hand_value_greater_then_or_equal_to_16_then_not_request_card(self):
        for hand_value in range(16, 32):
            self.test_is_request_card(hand_value, False)
    
    # helper function
    def test_is_request_card(self, hand_value: int, is_request_card: bool) -> None:
        self.dealer.hand.hand_value = [hand_value]
        result = self.dealer.is_request_card()

        self.assertEqual(result, is_request_card)


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestDealer('dealer_is_created_with_dealer_status'))
    suite.addTest(TestDealer('given_dealer_bust_then_the_status_is_dealer'))
    suite.addTest(TestDealer('given_hand_value_less_then_16_then_request_card'))
    suite.addTest(TestDealer('given_hand_value_greater_then_or_equal_to_16_then_not_request_card'))

    runner = unittest.TextTestRunner()
    runner.run(suite)