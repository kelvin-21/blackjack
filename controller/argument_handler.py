from domain.model import Game
from domain.service import Simulator


class ArgumentHandler():
    def __init__(self, game: Game, simulator: Simulator):
        self.game = game
        self.simulator = simulator

    def handle(self, input: str) -> None:
        while not self.arg(input):
            pass

    def arg(self, input: str) -> bool:

        if input == '/re':
            self.game.init_round()
            return False

        elif input == '/RE':
            self.game.init_game()
            # restart game
            return False

        elif input == '/cards':
            # view all cards and stat
            return False

        elif input == '/sim':
            # run simulation
            return False

        else:
            # good to go
            return True        