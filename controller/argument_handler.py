from domain.model import Game
from domain.service import Simulator
from controller import GameStatus
from controller.handler import CardInputHandler, CardInputResult, CardRequestHandler, CardRequestResult
from view import GameViewer, SimulationViewer
from enum import Enum
import logging


class ArgumentTask(Enum):
    CARD_INPUT = 'card_input'
    CARD_REQUEST = 'card_request'

class ArgumentHandler():
    def __init__(
            self, 
            game: Game, 
            simulator: Simulator, 
            game_viewer: GameViewer, 
            sim_viewer: SimulationViewer
        ):
        self.game = game
        self.player_me = None
        self.bypass = None
        self.is_task = None
        self.sim_result = None

        # service
        self.simulator = simulator
        self.game_viewer = game_viewer
        self.sim_viewer = sim_viewer
        self.card_input_handler = CardInputHandler()
        self.card_request_handler = CardRequestHandler()
        
        # mapper
        self.task_result_mapper = {
            ArgumentTask.CARD_INPUT    : CardInputResult,
            ArgumentTask.CARD_REQUEST  : CardRequestResult
        }
        self.task_handler_mapper = {
            ArgumentTask.CARD_INPUT    : self.card_input_handler,
            ArgumentTask.CARD_REQUEST  : self.card_request_handler
        }

    # return generic result
    def handle(self, arg_task: ArgumentTask = None, msg: str ='Please input:'):
        if not self.player_me:
            for player in self.game.players:
                if player.name == 'Me':
                    self.player_me = player
                    break

        self.bypass = False
        self.sim_result = None
        if not arg_task:  # handle non-task
            self.is_task = False
            self.handle_non_task(msg)           
        else:  # handle task
            self.is_task = True
            return self.handle_task(arg_task, msg)

    def handle_non_task(self, msg: str) -> None:
        arg = self.formatted_input(msg)
        while not self.bypass:
            self.command(arg)
            arg = self.formatted_input()

    def handle_task(self, arg_task: ArgumentTask, msg: str):
        flag = 0
        while not self.bypass:
            if flag == 0:
                arg = self.formatted_input(msg)
                flag = 1
            else:
                arg = self.formatted_input(f'Please input again: ({msg})')
            result = self.handle_argument(arg, arg_task)
            if arg_task and '/' not in arg:
                if self.check_result_type(arg_task, result):
                    return result

    def handle_argument(self, arg: str, arg_task: ArgumentTask):
        if '/' in arg:
            self.command(arg)
        else:
            return self.task(arg, arg_task)

    def check_result_type(self, arg_task: ArgumentTask, result=None) -> bool:
        if not arg_task:
            return True
        else:
            if type(result) is self.task_result_mapper[arg_task]:
                return True
            else:
                logging.warning(f'Wrong input for {arg_task.value}')
                return False

    def command(self, arg: str) -> None:
        if arg == '/go':  # force go
            self.bypass = True
            
        elif arg == '' and not self.is_task:  # force go if not a task
            self.bypass = True

        elif arg == '/re':  # restart round
            self.game.status = GameStatus.RESTART_ROUND
            self.bypass = True

        elif arg == '/RE':  # restart game
            self.game.status = GameStatus.START_NEW_GAME
            self.bypass = True

        elif arg[:6] == '/hands':  # view all hands
            limited_visible = None if '-f' in arg else self.player_me
            msg = self.game_viewer.all_hands(self.game.dealer, self.game.players, limited_visible)
            self.game_viewer.view(msg)

        elif arg[:5] == '/info': # view name, status, status_reason
            limited_visible = None if '-f' in arg else self.player_me
            msg = self.game_viewer.players_info(self.game.dealer, self.game.players, limited_visible)
            self.game_viewer.view(msg)

        elif arg == '/cards':  # view all cards and stat
            msg = self.game_viewer.all_cards(self.game.card_deck)
            self.game_viewer.view(msg)

        elif arg[:4] == '/sim':  # run simulation
            if not self.sim_result or '-r' in arg:
                for player_i in self.game.players:
                    if player_i.name == 'Me':
                        player = player_i
                        break
                self.sim_result = self.simulator.run_simulation(self.game, player)

            if not self.sim_result:
                logging.info('Not valid yet for simulation')
                return

            content = 'detail' if '-l' in arg else 'short'
            display = 'num' if '-n' in arg else 'percentage'
            msg = self.sim_viewer.sim_result(self.sim_result, content, display)
            self.sim_viewer.view(msg)
            
        elif arg == '/ad':  # seek advice on whether to request an extra card
            if not self.sim_result or '-r' in arg:
                for player_i in self.game.players:
                    if player_i.name == 'Me':
                        player = player_i
                        break
                self.sim_result = self.simulator.run_simulation(self.game, player)

            if not self.sim_result:
                logging.info('Not valid yet for simulation')
                return

            msg = self.sim_viewer.advice(self.sim_result)
            self.sim_viewer.view(msg)

        else:
            logging.warning(f'Unknown command arg - [{arg}]')

    def task(self, arg: str, arg_task: ArgumentTask):
        return self.task_handler_mapper[arg_task].handle(arg)

    @staticmethod
    def formatted_input(msg: str = '') -> str:
        if msg == '':
            return input('> ')
        else:
            return input(msg + '\n> ')