from domain.model import Game, Player
from domain.service import Simulator
from controller import GameStatus
from view import GameViewer, SimulationViewer

from typing import List
import logging


class CommandHandler():
    def __init__(
            self, 
            simulator: Simulator, 
            game_viewer: GameViewer, 
            sim_viewer: SimulationViewer
        ):
        self.simulator = simulator
        self.game_viewer = game_viewer
        self.sim_viewer = sim_viewer

        self.sim_result = None
        self.player_me = None

    def handle(self, arg: str, is_task: bool, game: Game) -> bool: # return bool: bypass

        self.find_player_me(game.players)

        if arg == '/go':  # force go
            return True
            
        elif arg == '' and not is_task:  # force go if not a task
            return True

        elif arg == '/re':  # restart round
            game.status = GameStatus.RESTART_ROUND
            return True

        elif arg == '/RE':  # restart game
            game.status = GameStatus.START_NEW_GAME
            return True

        elif any(item in arg for item in ['/hands', '/info', 'cards']):
            msg = self.handle_msg(arg, game)
            self.game_viewer.view(msg)
            return False

        elif any(item in arg for item in ['/sim', '/ad']):
            msg = self.handle_msg(arg, game)
            self.sim_viewer.view(msg)
            return False

        else:
            logging.warning(f'Unknown command arg - [{arg}]')

        return False

    def handle_msg(self, arg: str, game: Game) -> str:
        msg = None

        if arg[:6] == '/hands':  # view all hands
            limited_visible = None if '-f' in arg else self.player_me
            msg = self.game_viewer.all_hands(game.dealer, game.players, limited_visible)

        elif arg[:5] == '/info': # view name, status, status_reason
            limited_visible = None if '-f' in arg else self.player_me
            msg = self.game_viewer.players_info(game.dealer, game.players, limited_visible)

        elif arg == '/cards':  # view all cards and stat
            msg = self.game_viewer.all_cards(game.card_deck)

        elif arg[:4] == '/sim':  # run simulation
            if not self.sim_result or '-r' in arg:
                self.sim_result = self.simulator.run_simulation(game, self.player_me)

            if self.sim_result:
                content = 'detail' if '-l' in arg else 'short'
                display = 'num' if '-n' in arg else 'percentage'
                msg = self.sim_viewer.sim_result(self.sim_result, content, display)
            else:
                logging.info('Not valid yet for simulation')
            
        elif arg == '/ad':  # seek advice on whether to request an extra card
            if not self.sim_result or '-r' in arg:
                self.sim_result = self.simulator.run_simulation(game, self.player_me)

            if self.sim_result:
                msg = self.sim_viewer.advice(self.sim_result)
            else:
                logging.info('Not valid yet for simulation')

        return msg

    def sim_result_clear_cache(self) -> None:
        self.sim_result = None

    def find_player_me(self, players: List[Player]) -> None:
        for player_i in players:
            if player_i.name == 'Me':
                self.player_me = player_i
                return
        raise ValueError('Player Me not found in the game players')