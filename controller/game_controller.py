from domain.model import Game, Player, Card, Suit, Rank
from domain.service import Simulator, Decision, GameRecorder
from controller import ArgumentHandler, ArgumentTask, GameStatus
from view import GameViewer, SimulationViewer
from configuration import ConfigLoader
import logging
import traceback


class GameController():
    def __init__(
            self, 
            config_loader: ConfigLoader, 
            simulator: Simulator, 
            game_viewer: GameViewer,
            sim_viewer: SimulationViewer,
            game_recorder: GameRecorder
        ):
        self.game = Game(config_loader)
        self.simulator = simulator
        self.argument_handler = ArgumentHandler(self.game, simulator, game_viewer, sim_viewer)
        self.game_viewer = game_viewer
        self.sim_viewer = sim_viewer
        self.game_recorder = game_recorder

        # control param
        self.control = True
        self.pause = True
        self.use_advice = True

    def init(self):
        self.game.init()

    def start_up(self):
        self.game.status = GameStatus.START_NEW_GAME
        while 1:
            self.action()

    def action(self):
        if self.game.status == GameStatus.START_NEW_GAME:
            self.start_game()

        elif self.game.status == GameStatus.START_NEW_ROUND:
            self.game.init_round()
            self.start_round()

        elif self.game.status == GameStatus.RESTART_ROUND:
            self.game.restart_round()
            self.start_round()

        elif self.game.status == GameStatus.GAME:
            pass

        elif self.game.status == GameStatus.FINISHED:
            msg = self.game_viewer.players_info(self.game.dealer, self.game.players)
            self.game_viewer.view(msg)
            self.game_recorder.record(self.game)
            self.game.status = GameStatus.START_NEW_ROUND
            if self.pause:
                pause_msg = 'Press any key to continue...'
                self.argument_handler.handle(msg=pause_msg)

        elif self.game.status == GameStatus.EMPTY_DECK:
            self.game.status = GameStatus.START_NEW_GAME
            logging.debug('Restart game because card deck does not have enough cards')

        elif self.game.status == GameStatus.ERROR:
            logging.error('Error status, exitting program')
            quit()

    def start_game(self):
        self.init()
        self.game.status = GameStatus.START_NEW_ROUND

    def start_round(self):
        if self.game.card_deck.cards_remaining() < self.game.cards_required_each_round:
            self.game.status = GameStatus.EMPTY_DECK
            return

        self.game.status = GameStatus.GAME

        try:
            self.distribute_first_two_cards()
            self.handle_extra_card_request()
            self.conclude_players_status()

            self.game.status = GameStatus.FINISHED
        except Exception as ex:
            if self.game.status == GameStatus.START_NEW_GAME:
                logging.info('This round is ended because start new game')
            elif self.game.status == GameStatus.RESTART_ROUND:
                logging.info('This round is ended because start new round')
            else:
                logging.error(f'Unexpected error in a round - {ex}')
                traceback.print_exc()
                self.game.status = GameStatus.ERROR

    def distribute_first_two_cards(self):
        while len(self.game.dealer.hand.hand) < 2:
            self.controller_distribute_card(self.game.dealer)
        for player in self.game.players:
            while len(player.hand.hand) < 2:
                self.controller_distribute_card(player)

    def handle_extra_card_request(self):
        for player in self.game.players:
            self.controller_ask_card_request(player)
        self.controller_ask_card_request(self.game.dealer)

    def conclude_players_status(self):
        for player in self.game.players:
            self.game.conclude_player_status(player)

    def controller_distribute_card(self, target: Player) -> None:
        if self.game.status != GameStatus.GAME:
            return
        
        suit, rank = None, None
        if self.control:
            msg = f'Input the {self.order_str(len(target.hand.hand)+1)} card of {target.name}:'
            result = self.argument_handler.handle(ArgumentTask.CARD_INPUT, msg)
            suit, rank = result.suit, result.rank
        
        success = self.game.distribute_card(target, suit, rank)
        if not success:
            if self.game.card_deck.is_empty():
                self.game.status = GameStatus.EMPTY_DECK

    def controller_ask_card_request(self, target: Player) -> None:
        if target.is_npc:
            while(self.game.status == GameStatus.GAME and target.is_request_card()):
                self.controller_distribute_card(target)
        else:
            while 1:
                if self.game.status != GameStatus.GAME or not target.can_request_card():
                    return

                if self.control:
                    msg = f'Input whether {target.name} would like 1 more card:'
                    result = self.argument_handler.handle(ArgumentTask.CARD_REQUEST, msg)
                    request_card = result.request_card
                else:
                    if self.use_advice:
                        sim_result = self.simulator.run_simulation(self.game, target)
                        advice = self.simulator.get_advice(sim_result)
                        if advice:
                            request_card = True if advice == Decision.REQUEST else False
                            logging.debug(f'\n{self.sim_viewer.sim_result_short(sim_result)}\n{advice.value}\n')
                        else:  # equality between request and pass
                            request_card = False
                            logging.debug('Choose default - not request card')

                    else:
                        request_card = target.is_request_card()

                if request_card:
                    self.controller_distribute_card(target)
                else:
                    return

    @staticmethod
    def order_str(order: int) -> str:
        return {
            1: '1st',
            2: '2nd',
            3: '3rd',
            4: '4th',
            5: '5th'
        }[order]