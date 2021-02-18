from domain.model import Card, Suit, Rank, Hand
from domain.service import Simulator
from controller import GameController
from view import GameViewer, SimulationViewer
from configuration import ConfigLoader


config_loader = ConfigLoader()
config_loader.config_logger()

simulator = Simulator(config_loader)
game_viewer = GameViewer()
sim_viewer = SimulationViewer()

game_controller = GameController(config_loader, simulator, game_viewer, sim_viewer)
game_controller.control = True
game_controller.pause = True
game_controller.start_up()