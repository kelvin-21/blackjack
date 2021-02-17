import unittest
from domain.model import Game, Card, Hand, Suit, Rank, PlayerStatus, PlayerStatusReason, HandStatus
from configuration import ConfigLoader
from typing import List


class TestGame(unittest.TestCase):
    def setUp(self):
        self.config_loader = ConfigLoader()
        self.config_loader.load()
        self.num_player = self.config_loader.num_player
        self.num_card = self.config_loader.num_card_set * 52

        self.game = Game(self.config_loader)
        self.game.init()

    def test_create_players(self):
        self.game.create_players(10)

        self.assertEqual(len(self.game.players), 10)

    def test_init(self):
        self.assertEqual(len(self.game.players), self.num_player)
        self.assertIsNotNone(self.game.dealer)
        self.assertIsNotNone(self.game.card_deck)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card)
    
    def test_init_game(self):
        self.game.players[0].status = PlayerStatus.LOSE
        self.game.init_game()

        for player in self.game.players:
            self.assertEqual(len(player.hand.hand), 0)
            self.assertEqual(player.status, PlayerStatus.GAME)
        self.assertEqual(len(self.game.dealer.hand.hand), 0)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card)        

    def test_restart_round(self):
        # arrange
        num_used_card = 10
        for _ in range(num_used_card):
            self.game.card_deck.deck.pop()
        for player in self.game.players:
            player.add_card(self.game.card_deck.deck.pop())    
        self.game.dealer.add_card(self.game.card_deck.deck.pop())

        # assert arrange
        for player in self.game.players:
            self.assertEqual(len(player.hand.hand), 1)
        self.assertEqual(len(self.game.dealer.hand.hand), 1)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - num_used_card - self.num_player - 1)

        # action
        self.game.restart_round()

        # assert
        for player in self.game.players:
            self.assertEqual(len(player.hand.hand), 0)
        self.assertEqual(len(self.game.dealer.hand.hand), 0)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - num_used_card)        

    def send_card_that_exist(self):
        player = self.game.players[0]
        card = self.game.card_deck.deck[0]
        flag = self.game.send_card(player, card)

        self.assertTrue(flag)
        self.assertEqual(len(player.hand.hand), 1)
        self.assertEqual(player.hand.hand[0], card)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)
        
    def send_card_that_not_exist_then_return_none(self):
        player = self.game.players[0]
        card = None
        flag = self.game.send_card(player, card)

        self.assertFalse(flag)
        self.assertEqual(len(player.hand.hand), 0)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card)

    def send_card_to_dealer(self):
        card = self.game.card_deck.deck[0]
        flag = self.game.send_card(self.game.dealer, card)

        self.assertTrue(flag)
        self.assertEqual(len(self.game.dealer.hand.hand), 1)
        self.assertEqual(self.game.dealer.hand.hand[0], card)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)


    def distribute_card_that_exist_with_specified_suit_and_rank(self):
        player = self.game.players[0]
        flag = self.game.distribute_card(player, Suit.SPADE, Rank.TWO)

        self.assertTrue(flag)
        self.assertEqual(len(player.hand.hand), 1)
        self.assertEqual(player.hand.hand[0], Card(Suit.SPADE, Rank.TWO))
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)

    def distribute_card_to_dealer(self):
        flag = self.game.distribute_card(self.game.dealer, Suit.SPADE, Rank.TWO)

        self.assertTrue(flag)
        self.assertEqual(len(self.game.dealer.hand.hand), 1)
        self.assertEqual(self.game.dealer.hand.hand[0], Card(Suit.SPADE, Rank.TWO))
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)


    def distribute_card_that_exist_with_specified_suit(self):
        player = self.game.players[0]
        flag = self.game.distribute_card(player, suit=Suit.SPADE)

        self.assertTrue(flag)
        self.assertEqual(len(player.hand.hand), 1)
        self.assertEqual(player.hand.hand[0].suit, Suit.SPADE)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)

    def distribute_card_that_exist_with_specified_rank(self):
        player = self.game.players[0]
        flag = self.game.distribute_card(player, rank=Rank.TWO)

        self.assertTrue(flag)
        self.assertEqual(len(player.hand.hand), 1)
        self.assertEqual(player.hand.hand[0].rank, Rank.TWO)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)

    def distribute_card_that_not_exist_then_return_false(self):
        player = self.game.players[0]
        self.game.card_deck.deck = list()
        flag = self.game.distribute_card(player, rank=Rank.TWO)

        self.assertFalse(flag)
        self.assertEqual(len(player.hand.hand), 0)
        self.assertEqual(len(self.game.card_deck.deck), 0)

    def distribute_random_card_from_nonempty_card_deck(self):
        player = self.game.players[0]
        flag = self.game.distribute_card(player)

        self.assertTrue(flag)
        self.assertEqual(len(player.hand.hand), 1)
        self.assertEqual(len(self.game.card_deck.deck), self.num_card - 1)

    def distribute_random_card_from_empty_card_deck_then_return_false(self):
        player = self.game.players[0]
        self.game.card_deck.deck = list()
        flag = self.game.distribute_card(player)

        self.assertFalse(flag)
        self.assertEqual(len(player.hand.hand), 0)
        self.assertEqual(len(self.game.card_deck.deck), 0)

    def test_conclude_player_status(self):
        self.player_status_helper(HandStatus.BUST, HandStatus.LIVE, PlayerStatus.WIN, PlayerStatusReason.DEALER_BUST)
        self.player_status_helper(HandStatus.BUST, HandStatus.BLACKJACK, PlayerStatus.WIN, PlayerStatusReason.DEALER_BUST)
        self.player_status_helper(HandStatus.BUST, HandStatus.FIVECARD, PlayerStatus.WIN, PlayerStatusReason.DEALER_BUST)
        self.player_status_helper(HandStatus.BUST, HandStatus.BUST, PlayerStatus.LOSE, PlayerStatusReason.BUST)
        self.player_status_helper(HandStatus.BLACKJACK, HandStatus.LIVE, PlayerStatus.LOSE, PlayerStatusReason.DEALER_BLACKJACK)
        self.player_status_helper(HandStatus.BLACKJACK, HandStatus.BUST, PlayerStatus.LOSE, PlayerStatusReason.DEALER_BLACKJACK)
        self.player_status_helper(HandStatus.BLACKJACK, HandStatus.BLACKJACK, PlayerStatus.LOSE, PlayerStatusReason.DEALER_BLACKJACK)
        self.player_status_helper(HandStatus.BLACKJACK, HandStatus.FIVECARD, PlayerStatus.LOSE, PlayerStatusReason.DEALER_BLACKJACK)
        self.player_status_helper(HandStatus.FIVECARD, HandStatus.LIVE, PlayerStatus.LOSE, PlayerStatusReason.DEALER_FIVECARD)
        self.player_status_helper(HandStatus.FIVECARD, HandStatus.BUST, PlayerStatus.LOSE, PlayerStatusReason.DEALER_FIVECARD)
        self.player_status_helper(HandStatus.FIVECARD, HandStatus.BLACKJACK, PlayerStatus.LOSE, PlayerStatusReason.DEALER_FIVECARD)
        self.player_status_helper(HandStatus.FIVECARD, HandStatus.FIVECARD, PlayerStatus.LOSE, PlayerStatusReason.DEALER_FIVECARD)
        self.player_status_helper(HandStatus.LIVE, HandStatus.BUST, PlayerStatus.LOSE, PlayerStatusReason.BUST)
        self.player_status_helper(HandStatus.LIVE, HandStatus.BLACKJACK, PlayerStatus.WIN, PlayerStatusReason.BLACKJACK)
        self.player_status_helper(HandStatus.LIVE, HandStatus.FIVECARD, PlayerStatus.WIN, PlayerStatusReason.FIVECARD)

    def test_conclude_player_status_hand_value(self):
        hand_16 = [Card(Suit.SPADE, Rank.TEN), Card(Suit.SPADE, Rank.SIX)]
        hand_17 = [Card(Suit.SPADE, Rank.TEN), Card(Suit.SPADE, Rank.SEVEN)]
        hand_21 = [Card(Suit.SPADE, Rank.TEN), Card(Suit.SPADE, Rank.SEVEN), Card(Suit.SPADE, Rank.FOUR)]
        hand_blackjack = [Card(Suit.SPADE, Rank.TEN), Card(Suit.SPADE, Rank.A)]
        hand_fivecard = [Card(Suit.SPADE, Rank.TWO), Card(Suit.SPADE, Rank.THREE), Card(Suit.SPADE, Rank.THREE), Card(Suit.SPADE, Rank.FOUR), Card(Suit.SPADE, Rank.FOUR)]

        self.hand_value_helper(hand_16, hand_16, PlayerStatus.LOSE, PlayerStatusReason.DEALER_HAND_VALUE)
        self.hand_value_helper(hand_16, hand_17, PlayerStatus.WIN, PlayerStatusReason.HAND_VALUE)
        self.hand_value_helper(hand_17, hand_16, PlayerStatus.LOSE, PlayerStatusReason.DEALER_HAND_VALUE)
        self.hand_value_helper(hand_21, hand_blackjack, PlayerStatus.WIN, PlayerStatusReason.BLACKJACK)
        self.hand_value_helper(hand_21, hand_fivecard, PlayerStatus.WIN, PlayerStatusReason.FIVECARD)

    # helper function
    def player_status_helper(
        self, 
        dealer_hand_status: HandStatus, 
        player_hand_status: HandStatus, 
        expected_status: PlayerStatus,
        expected_status_reason: PlayerStatusReason
    ):
        self.game.dealer.hand.status = dealer_hand_status
        self.game.players[0].hand.status = player_hand_status
        self.game.conclude_player_status(self.game.players[0])
        status = self.game.players[0].status
        status_reason = self.game.players[0].status_reason
        self.assertEqual(status, expected_status)
        self.assertEqual(status_reason, expected_status_reason)

    # helper function
    def hand_value_helper(
        self, 
        dealer_cards: List[Hand], 
        player_cards: List[Hand], 
        expected_status: PlayerStatus, 
        expected_status_reason: PlayerStatusReason
    ):
        dealer = self.game.dealer
        player = self.game.players[0]
        dealer.hand.init(), player.hand.init()
        for card in dealer_cards:
            dealer.hand.add_card(card)
        for card in player_cards:
            player.hand.add_card(card)
        self.game.conclude_player_status(player)
        
        status = player.status
        status_reason = player.status_reason
        self.assertEqual(status, expected_status)
        self.assertEqual(status_reason, expected_status_reason)
        

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestGame('test_create_players'))
        suite.addTest(TestGame('test_init'))
        suite.addTest(TestGame('test_init_game'))
        suite.addTest(TestGame('test_restart_round'))
        suite.addTest(TestGame('send_card_that_exist'))
        suite.addTest(TestGame('send_card_that_not_exist_then_return_none'))
        suite.addTest(TestGame('send_card_to_dealer'))
        suite.addTest(TestGame('distribute_card_that_exist_with_specified_suit_and_rank'))
        suite.addTest(TestGame('distribute_card_to_dealer'))
        suite.addTest(TestGame('distribute_card_that_exist_with_specified_suit'))
        suite.addTest(TestGame('distribute_card_that_exist_with_specified_rank'))
        suite.addTest(TestGame('distribute_card_that_not_exist_then_return_false'))
        suite.addTest(TestGame('distribute_random_card_from_nonempty_card_deck'))
        suite.addTest(TestGame('distribute_random_card_from_empty_card_deck_then_return_false'))
        suite.addTest(TestGame('test_conclude_player_status'))
        suite.addTest(TestGame('test_conclude_player_status_hand_value'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestGame.run_all_test()