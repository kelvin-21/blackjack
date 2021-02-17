import unittest
from domain.model import Card, Suit, Rank, Player, PlayerStatus, Dealer, Game, HandStatus, PlayerStatusReason
from domain.service import Simulator, Decision
from configuration import ConfigLoader

class TestSimulator(unittest.TestCase):
    def setUp(self):
        self.card_A = Card(Suit.SPADE, Rank.A)
        self.card_10 = Card(Suit.SPADE, Rank.TEN)
        self.player_me = Player('me', is_npc=False)
        self.player_npc = Player('npc')
        self.dealer = Dealer(16)
        self.player_me.add_card(self.card_10), self.player_me.add_card(self.card_10)
        self.player_npc.add_card(self.card_10), self.player_npc.add_card(self.card_10)
        self.dealer.add_card(self.card_10), self.dealer.add_card(self.card_10)
        
        self.game = Game(ConfigLoader())
        self.game.init()
        self.game.players = [self.player_me, self.player_npc]
        self.game.dealer = self.dealer

        self.simulator = Simulator(ConfigLoader())

    def given_player_is_not_game_status_then_not_valid_for_simulation(self):
        self.player_status_helper(PlayerStatus.DEALER, False)
        self.player_status_helper(PlayerStatus.WIN, False)
        self.player_status_helper(PlayerStatus.LOSE, False)
        self.player_status_helper(PlayerStatus.UNKNOWN, False)

    def given_player_hand_is_not_live_then_not_valid_for_simulation(self):
        self.hand_status_helper(HandStatus.BUST, False)
        self.hand_status_helper(HandStatus.BLACKJACK, False)
        self.hand_status_helper(HandStatus.FIVECARD, False)

    def given_target_player_less_than_two_cards_then_not_valid_for_simulation(self):
        self.player_me.hand.init()
        self.player_me.add_card(self.card_10)
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertFalse(result)

    def given_non_target_player_less_than_one_card_then_not_valid_for_simulation(self):
        self.player_npc.hand.init()
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertFalse(result)

    def given_dealer_less_than_one_card_then_not_valid_for_simulation(self):
        self.dealer.hand.init()
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertFalse(result)

    def given_target_player_is_npc_then_not_valid_for_simulation(self):
        self.player_me.is_npc = True
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertFalse(result)


    def test_init_sim_result(self):
        sim_result = self.simulator.init_sim_result()
        for decision in Decision:
            for reason in [PlayerStatusReason.DEALER_BUST, PlayerStatusReason.HAND_VALUE, PlayerStatusReason.BLACKJACK, PlayerStatusReason.FIVECARD]:
                v = sim_result[decision][PlayerStatus.WIN][reason]
                self.assertEqual(v, 0)
            for reason in [PlayerStatusReason.BUST, PlayerStatusReason.DEALER_HAND_VALUE, PlayerStatusReason.DEALER_BLACKJACK, PlayerStatusReason.DEALER_FIVECARD]:
                v = sim_result[decision][PlayerStatus.LOSE][reason]
                self.assertEqual(v, 0)
    
    def set_up_is_valid_for_simulation(self):
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertTrue(result)

    def test_make_copy(self):
        game_copy, player_copy = self.simulator.make_copy(self.game, self.player_me)

        self.assertNotEqual(game_copy, self.game)
        self.assertNotEqual(player_copy, self.player_me)
        self.assertEqual(game_copy.__class__, self.game.__class__)
        self.assertEqual(player_copy.__class__, self.player_me.__class__)
        self.assertEqual(player_copy.name, self.player_me.name)
        # card equality is defined by value not reference
        self.assertEqual(game_copy.dealer.hand.hand[0], self.game.dealer.hand.hand[0])
        self.assertEqual(game_copy.dealer.hand.hand[1], self.game.dealer.hand.hand[1])
        for i in range(len(self.game.players)):
            original_player_i = self.game.players[i]
            copy_player_i = game_copy.players[i]
            self.assertNotEqual(original_player_i, copy_player_i)
            self.assertEqual(original_player_i.hand.hand[0], copy_player_i.hand.hand[0])
            self.assertEqual(original_player_i.hand.hand[1], copy_player_i.hand.hand[1])
        self.assertTrue(player_copy in game_copy.players)

    def test_prepare_game_for_simulation(self):
        dealer = self.game.dealer
        players = self.game.players
        initial_total_cards = len(self.game.card_deck.deck) + len(dealer.hand.hand) + sum([len(player.hand.hand) for player in players])
        self.simulator.prepare_game_for_simulation(self.game, self.player_me, 2)

        total_cards = len(self.game.card_deck.deck) + len(dealer.hand.hand) + sum([len(player.hand.hand) for player in players])
        self.assertEqual(len(dealer.hand.hand), 1)
        self.assertEqual(len(self.player_me.hand.hand), 2)
        self.assertEqual(len(self.player_npc.hand.hand), 1)
        self.assertEqual(initial_total_cards, total_cards)

    def given_3_card_in_hand_and_prepare_game_for_simulation_then_still_3_card(self):
        self.player_me.add_card(self.card_A)
        self.simulator.prepare_game_for_simulation(self.game, self.player_me, 3)

        self.assertEqual(len(self.player_me.hand.hand), 3)

    def test_update_simulation_result(self):
        sim_result = self.simulator.init_sim_result()
        result = (PlayerStatus.WIN, PlayerStatusReason.DEALER_BUST)
        self.simulator.update_simulation_result(sim_result, Decision.REQUEST, result)

        v = sim_result[Decision.REQUEST][PlayerStatus.WIN][PlayerStatusReason.DEALER_BUST]
        self.assertEqual(v, 1)

    def test_simulate_distribute_first_two_cards(self):
        self.game.dealer.init()
        self.player_npc.init()
        self.simulator.simulate_distribute_first_two_cards(self.game)

        self.assertEqual(len(self.game.dealer.hand.hand), 2)
        self.assertEqual(len(self.player_me.hand.hand), 2)
        self.assertEqual(len(self.player_npc.hand.hand), 2)

    def test_simulate_card_request_posite_target_correctly(self):
        original_size = len(self.game.players)
        self.simulator.simulate_handle_extra_card_request(self.game, self.player_me, Decision.PASS, 1)
        self.assertEqual(self.game.players[1], self.player_me)
        self.assertEqual(len(self.game.players), original_size)

    def test_simulate_handle_extra_card_request(self):
        self.simulator.simulate_handle_extra_card_request(self.game, self.player_me, Decision.PASS, 1)
        self.assertFalse(self.game.dealer.is_request_card())
        self.assertFalse(self.player_npc.is_request_card())

    def integration_test_simulate(self):
        (status, status_reason) = self.simulator.simulate(self.game, self.player_me, Decision.PASS)
        self.assertTrue(status in [PlayerStatus.WIN, PlayerStatus.LOSE])
        self.assertEqual(status_reason.__class__, PlayerStatusReason)

    def integration_test_run_simulation(self):
        self.simulator.simulation_trials = 1000
        sim_result = self.simulator.run_simulation(self.game, self.player_me)
        total_count = 0
        for i in sim_result.keys():
            for j in sim_result[i].keys():
                for k in sim_result[i][j].keys():
                    total_count += sim_result[i][j][k]
        self.assertEqual(total_count, self.simulator.simulation_trials * 2)

    # helper function
    def player_status_helper(self, status: PlayerStatus, expected: bool):
        self.player_me.status = status
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertEqual(result, expected)

    # helper function
    def hand_status_helper(self, status: HandStatus, expected: bool):
        self.player_me.hand.status = status
        result = self.simulator.is_valid_for_simulation(self.game, self.player_me)
        self.assertEqual(result, expected)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestSimulator('given_player_is_not_game_status_then_not_valid_for_simulation'))
        suite.addTest(TestSimulator('given_player_hand_is_not_live_then_not_valid_for_simulation'))
        suite.addTest(TestSimulator('given_target_player_less_than_two_cards_then_not_valid_for_simulation'))
        suite.addTest(TestSimulator('given_non_target_player_less_than_one_card_then_not_valid_for_simulation'))
        suite.addTest(TestSimulator('given_dealer_less_than_one_card_then_not_valid_for_simulation'))
        suite.addTest(TestSimulator('given_target_player_is_npc_then_not_valid_for_simulation'))
        suite.addTest(TestSimulator('test_init_sim_result'))
        suite.addTest(TestSimulator('set_up_is_valid_for_simulation'))
        suite.addTest(TestSimulator('test_make_copy'))
        suite.addTest(TestSimulator('test_prepare_game_for_simulation'))
        suite.addTest(TestSimulator('given_3_card_in_hand_and_prepare_game_for_simulation_then_still_3_card'))
        suite.addTest(TestSimulator('test_update_simulation_result'))
        suite.addTest(TestSimulator('test_simulate_distribute_first_two_cards'))
        suite.addTest(TestSimulator('test_simulate_card_request_posite_target_correctly'))
        suite.addTest(TestSimulator('test_simulate_handle_extra_card_request'))
        suite.addTest(TestSimulator('integration_test_simulate'))
        suite.addTest(TestSimulator('integration_test_run_simulation'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestSimulator.run_all_test()