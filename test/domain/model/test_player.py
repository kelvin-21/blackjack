import unittest
from domain.model import Player, PlayerStatus, Card, Suit, Rank


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player('Test')
        self.card_A = Card(Suit.SPADE, Rank.A)
        self.card_9 = Card(Suit.SPADE, Rank.NINE)

    def given_player_in_game_status_then_can_add_card(self):
        self.player.status = PlayerStatus.GAME
        self.player.add_card(self.card_A)

        self.assertEqual(len(self.player.hand.hand), 1)
        self.assertEqual(self.player.hand.hand[0], self.card_A)

    def given_win_player_then_cannot_add_card(self):
        self.player.status = PlayerStatus.WIN
        self.player.add_card(self.card_A)

        self.assertEqual(self.player.hand.hand, [])

    def given_lose_player_then_cannot_add_card(self):
        self.player.status = PlayerStatus.LOSE
        self.player.add_card(self.card_A)

        self.assertEqual(self.player.hand.hand, [])

    def given_player_bust_then_status_is_lose(self):
        self.player.add_card(self.card_9)
        self.player.add_card(self.card_9)
        self.player.add_card(self.card_9)

        self.assertEqual(self.player.status, PlayerStatus.LOSE)

    def given_hand_value_less_then_or_equal_to_11_then_request_card(self):
        for hand_value in range(2, 12):
            self.test_is_request_card(hand_value, True)

    def given_hand_value_greater_then_or_equal_to_21_then_not_request_card(self):
        for hand_value in range(21, 32):
            self.test_is_request_card(hand_value, False)
    
    # helper function
    def test_is_request_card(self, hand_value: int, is_request_card: bool) -> None:
        self.player.hand.hand_value = [hand_value]
        result = self.player.is_request_card()

        self.assertEqual(result, is_request_card)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestPlayer('given_player_in_game_status_then_can_add_card'))
        suite.addTest(TestPlayer('given_win_player_then_cannot_add_card'))
        suite.addTest(TestPlayer('given_lose_player_then_cannot_add_card'))
        suite.addTest(TestPlayer('given_player_bust_then_status_is_lose'))
        suite.addTest(TestPlayer('given_hand_value_less_then_or_equal_to_11_then_request_card'))
        suite.addTest(TestPlayer('given_hand_value_greater_then_or_equal_to_21_then_not_request_card'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestPlayer.run_all_test()