from controller import GameController
from domain.model import Card, Suit, Rank, Hand
from domain.service import Simulator, GameRecorder
from view import GameViewer, SimulationViewer
from configuration import ConfigLoader


config_loader = ConfigLoader()
config_loader.config_logger()

simulator = Simulator(config_loader)
game_viewer = GameViewer()
sim_viewer = SimulationViewer()
game_recorder = GameRecorder(config_loader, game_viewer)

game_controller = GameController(config_loader, simulator, game_viewer, sim_viewer, game_recorder)
game_controller.control = False
game_controller.pause = False
game_controller.use_advice = True
game_controller.start_up()