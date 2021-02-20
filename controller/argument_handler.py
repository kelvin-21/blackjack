from domain.model import Game
from domain.service import Simulator
from controller import GameStatus
from controller.handler import CardInputHandler, CardInputResult, CardRequestHandler, CardRequestResult, CommandHandler
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
        self.bypass = None
        self.is_task = None
        self.sim_result = None

        # service
        self.simulator = simulator
        self.game_viewer = game_viewer
        self.sim_viewer = sim_viewer
        self.card_input_handler = CardInputHandler()
        self.card_request_handler = CardRequestHandler()
        self.command_handler = CommandHandler(self.simulator, self.game_viewer, self.sim_viewer)
        
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
        self.bypass = False
        self.command_handler.sim_result_clear_cache()

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
        self.bypass = self.command_handler.handle(arg, self.is_task, self.game)

    def task(self, arg: str, arg_task: ArgumentTask):
        return self.task_handler_mapper[arg_task].handle(arg)

    @staticmethod
    def formatted_input(msg: str = '') -> str:
        if msg == '':
            return input('> ')
        else:
            return input(msg + '\n> ')