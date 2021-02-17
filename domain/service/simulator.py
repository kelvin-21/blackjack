from domain.model import Game, Player, PlayerStatus, PlayerStatusReason, HandStatus
from configuration import ConfigLoader
from enum import Enum
from typing import Tuple
import copy
import logging
import traceback


class Decision(Enum):
    REQUEST = 'request_card'
    PASS = 'pass'


class Simulator():
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.simulation_trials = self.config_loader.simulation_trials

    def run_simulation(self, game_input: Game, player_input: Player) -> dict:
        if not self.is_valid_for_simulation(game_input, player_input):
            return

        (game, player) = self.make_copy(game_input, player_input)
        original_cards = len(player_input.hand.hand)

        sim_result = self.init_sim_result()
        for decision in Decision:
            for _ in range(self.simulation_trials):

                try:
                    self.prepare_game_for_simulation(game, player, original_cards)
                    result = self.simulate(game, player, decision)
                    self.update_simulation_result(sim_result, decision, result)
                    
                except Exception as ex:
                    logging.warning(f'Exception while simulating - {ex}')
                    traceback.print_exc()

        return sim_result

    # reuse the game instance
    @staticmethod
    def prepare_game_for_simulation(game: Game, player: Player, original_cards: int) -> None:
        while len(game.dealer.hand.hand) > 1:
            card = game.dealer.hand.hand.pop()
            game.card_deck.deck.append(card)
        game.dealer.update_hand_value()

        for player_i in game.players:
            remain = original_cards if player_i == player else 1
            while len(player_i.hand.hand) > remain:
                card = player_i.hand.hand.pop()
                game.card_deck.deck.append(card)
            player_i.update_hand_value()
            player_i.status, player_i.status_reason = PlayerStatus.GAME, PlayerStatusReason.GAME

    def simulate(self, game: Game, player: Player, decision: Decision) -> Tuple[PlayerStatus, PlayerStatusReason]:
        self.simulate_distribute_first_two_cards(game)
        self.simulate_handle_extra_card_request(game, player, decision)
        game.conclude_player_status(player)
        return (player.status, player.status_reason)
    
    @staticmethod
    def update_simulation_result(sim_result, decision: Decision, result: Tuple[PlayerStatus, PlayerStatusReason]) -> None:
        sim_result[decision][result[0]][result[1]] += 1

    @staticmethod
    def make_copy(game_input: Game, player_input: Player) -> Tuple[Game, Player]:
        game = copy.deepcopy(game_input)
        for player_i in game.players:
            if player_i.name == player_input.name:
                player = player_i
        return (game, player)

    @staticmethod
    def is_valid_for_simulation(game: Game, player: Player) -> bool:
        if player.status != PlayerStatus.GAME or player.hand.status != HandStatus.LIVE or player.is_npc:
            return False
        if len(player.hand.hand) < 2:
            return False
        if len(game.dealer.hand.hand) < 2:
            return False
        for player in game.players:
            if len(player.hand.hand) < 1:
                return False
        return True

    @staticmethod
    def init_sim_result():
        sim_result = {
            Decision.REQUEST: {
                PlayerStatus.WIN: {
                    PlayerStatusReason.DEALER_BUST          : 0,
                    PlayerStatusReason.HAND_VALUE           : 0,
                    PlayerStatusReason.BLACKJACK            : 0,
                    PlayerStatusReason.FIVECARD             : 0
                },
                PlayerStatus.LOSE: {
                    PlayerStatusReason.BUST                 : 0,
                    PlayerStatusReason.DEALER_HAND_VALUE    : 0,
                    PlayerStatusReason.DEALER_BLACKJACK     : 0,
                    PlayerStatusReason.DEALER_FIVECARD      : 0
                }
            },
            Decision.PASS: {
                PlayerStatus.WIN: {
                    PlayerStatusReason.DEALER_BUST          : 0,
                    PlayerStatusReason.HAND_VALUE           : 0,
                    PlayerStatusReason.BLACKJACK            : 0,
                    PlayerStatusReason.FIVECARD             : 0
                },
                PlayerStatus.LOSE: {
                    PlayerStatusReason.BUST                 : 0,
                    PlayerStatusReason.DEALER_HAND_VALUE    : 0,
                    PlayerStatusReason.DEALER_BLACKJACK     : 0,
                    PlayerStatusReason.DEALER_FIVECARD      : 0
                }
            }
        }
        return sim_result


    # ----- game flow reference from GameController -----

    @staticmethod
    def simulate_distribute_first_two_cards(game: Game):
        while len(game.dealer.hand.hand) < 2:
            game.distribute_card(game.dealer)
        for player in game.players:
            while len(player.hand.hand) < 2:
                game.distribute_card(player)

    @staticmethod
    def simulate_handle_extra_card_request(game: Game, player: Player, decision: Decision, position=0) -> None:
        # handle position
        game.players.remove(player)
        game.players.insert(position, player)

        # hand extra card requerst up to my player
        while game.dealer.is_request_card():
            game.distribute_card(game.dealer)

        for player_i in game.players:

            if player_i == player:
                if decision == Decision.REQUEST:
                    game.distribute_card(player_i)
                    return  # ignore the players after 'position'
        
            else:
                while player_i.is_request_card():
                    game.distribute_card(player_i)
        # position is meaning because it can happen that a specific card is the key to win
        # and this card can be taken away by the players in front