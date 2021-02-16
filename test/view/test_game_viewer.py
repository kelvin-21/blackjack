import unittest
from domain.model import Card, Suit, Rank, Hand, Player, Dealer, CardDeck
from view import GameViewer


class TestGameViewer(unittest.TestCase):
    def setUp(self):
        self.game_viewer = GameViewer()
        self.card_A = Card(Suit.SPADE, Rank.A)
        self.card_10 = Card(Suit.SPADE, Rank.TEN)
        self.hand_1, self.hand_2, self.hand_3 = Hand(), Hand(), Hand()
        self.hand_1.add_card(self.card_A)
        self.hand_2.add_card(self.card_10)
        self.hand_2.add_card(self.card_A)
        self.hand_3.add_card(self.card_10)
        self.hand_3.add_card(self.card_10)
        self.dealer = Dealer(16)
        self.dealer.hand = self.hand_3
        self.players = [Player('test_1'), Player('testing_2')]
        self.players[0].hand = self.hand_1
        self.players[1].hand = self.hand_2
        
    def test_card(self):
        self.view_card_helper(Card(Suit.SPADE, Rank.A), '♠ A')
        self.view_card_helper(Card(Suit.HEART, Rank.A), '♥️ A')
        self.view_card_helper(Card(Suit.CLUB, Rank.A), '♣ A')
        self.view_card_helper(Card(Suit.DIAMOND, Rank.A), '♦ A')
        self.view_card_helper(Card(Suit.SPADE, Rank.TWO), '♠ 2')
        self.view_card_helper(Card(Suit.SPADE, Rank.TEN), '♠ 10')
        self.view_card_helper(Card(Suit.SPADE, Rank.J), '♠ J')
        self.view_card_helper(Card(Suit.SPADE, Rank.Q), '♠ Q')
        self.view_card_helper(Card(Suit.SPADE, Rank.K), '♠ K')
    
    def test_hand(self):
        self.view_hand_helper(self.hand_1, '(♠ A)')
        self.view_hand_helper(self.hand_2, '(♠ 10) (♠ A)')

    def test_all_hands(self):
        result = self.game_viewer.all_hands(self.dealer, self.players)
        expected = '[Dealer   ]: (♠ 10) (♠ 10)\n[test_1   ]: (♠ A)\n[testing_2]: (♠ 10) (♠ A)\n'
        self.assertEqual(result, expected)

    def test_players_details(self):
        result = self.game_viewer.players_details(self.dealer, self.players)
        expected = '[Dealer   ]:      - (♠ 10) (♠ 10)\n[test_1   ]: game - (♠ A)\n[testing_2]: game - (♠ 10) (♠ A)\n'
        self.assertEqual(result, expected)

    def test_all_cards(self):
        card_deck = CardDeck(2)
        card_deck.init()
        result = self.game_viewer.all_cards(card_deck)
        expected = 'A : 8\n2 : 8\n3 : 8\n4 : 8\n5 : 8\n6 : 8\n7 : 8\n8 : 8\n9 : 8\n10: 8\nJ : 8\nQ : 8\nK : 8\n'
        self.assertEqual(result, expected)

    # helper function
    def view_card_helper(self, card: Card, expected: str):
        result = self.game_viewer.card(card)
        self.assertEqual(result, expected)

    # helper function
    def view_hand_helper(self, hand: Hand, expected: str):
        result = self.game_viewer.hand(hand)
        self.assertEqual(result, expected)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestGameViewer('test_card'))
        suite.addTest(TestGameViewer('test_hand'))
        suite.addTest(TestGameViewer('test_all_hands'))
        suite.addTest(TestGameViewer('test_players_details'))
        suite.addTest(TestGameViewer('test_all_cards'))

        runner = unittest.TextTestRunner()
        runner.run(suite)
        # print('♠ ♥️ ♣ ♦')


if __name__ == '__main__':
    TestGameViewer.run_all_test()