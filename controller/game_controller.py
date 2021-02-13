from domain.model import Game
from domain.service import ConfigLoader, Simulator
from controller import ArgumentHandler


class GameController():
    def __init__(self, config_loader: ConfigLoader):
        self.game = Game(config_loader)

    def start_up(self):
        pass