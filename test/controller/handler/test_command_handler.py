import unittest
from unittest.mock import MagicMock
from domain.model import Game, Card, Suit, Rank
from domain.service import Simulator
from controller import GameStatus
from controller.handler import CommandHandler
from view import GameViewer, SimulationViewer
from configuration import ConfigLoader


class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.simulator = Simulator(ConfigLoader())
        self.game_viewer = GameViewer()
        self.sim_viewer = SimulationViewer()
        self.command_handler = CommandHandler(self.simulator, self.game_viewer, self.sim_viewer)

        # game setup
        self.game = Game(ConfigLoader())
        self.game.init()
        self.game.distribute_card(self.game.dealer, rank=Rank.NINE)
        self.game.distribute_card(self.game.dealer, rank=Rank.NINE)
        for player in self.game.players:
            self.game.distribute_card(player, rank=Rank.TEN)
            self.game.distribute_card(player, rank=Rank.EIGHT)

        # override view function
        self.game_viewer.view = MagicMock(return_value=0)
        self.sim_viewer.view = MagicMock(return_value=0)

    def test_handle_return_correct_bool(self):
        self.test_handle('/go', True, expected=True)
        self.test_handle('', True, expected=False)
        self.test_handle('/re', True, expected=True)
        self.test_handle('/RE', True, expected=True)
        self.test_handle('/hands', True, expected=False)
        self.test_handle('/info', True, expected=False)
        self.test_handle('/cards', True, expected=False)
        self.test_handle('/sim', True, expected=False)
        self.test_handle('/ad', True, expected=False)
        self.test_handle('', False, expected=True)

    def given_arg_re_then_restart_game_round(self):
        self.command_handler.handle('/re', True, self.game)
        self.assertEqual(self.game.status, GameStatus.RESTART_ROUND)

    def given_arg_RE_then_restart_game(self):
        self.command_handler.handle('/RE', True, self.game)
        self.assertEqual(self.game.status, GameStatus.START_NEW_GAME)

    def test_handle_msg_return_non_empty_str(self):
        self.test_handle_msg('/hands')
        self.test_handle_msg('/info')
        self.test_handle_msg('/cards')
        self.test_handle_msg('/sim')
        self.test_handle_msg('/ad')

    def given_arg_hands_with_visibility_then_return_full_info(self):
        result = self.command_handler.handle_msg('/hands -f', self.game)
        self.assertTrue('( - )' not in result)

    def given_arg_hands_without_visibility_then_return_partial_info(self):
        result = self.command_handler.handle_msg('/hands', self.game)
        self.assertTrue('( - )' in result)

    def given_arg_info_with_visibility_then_return_full_info(self):
        result = self.command_handler.handle_msg('/info -f', self.game)
        self.assertTrue('( - )' not in result)

    def given_arg_info_without_visibility_then_return_partial_info(self):
        result = self.command_handler.handle_msg('/info', self.game)
        self.assertTrue('( - )' in result)

    # helper function
    def test_handle(self, arg: str, is_task: bool, expected: bool):
        result = self.command_handler.handle(arg, is_task, self.game)
        self.assertEqual(result, expected)

    # helper function
    def test_handle_msg(self, arg: str):
        result = self.command_handler.handle_msg(arg, self.game)
        self.assertIsNotNone(result)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestCommandHandler('test_handle_return_correct_bool'))
        suite.addTest(TestCommandHandler('given_arg_re_then_restart_game_round'))
        suite.addTest(TestCommandHandler('given_arg_RE_then_restart_game'))
        suite.addTest(TestCommandHandler('test_handle_msg_return_non_empty_str'))
        suite.addTest(TestCommandHandler('given_arg_hands_with_visibility_then_return_full_info'))
        suite.addTest(TestCommandHandler('given_arg_hands_without_visibility_then_return_partial_info'))
        suite.addTest(TestCommandHandler('given_arg_info_with_visibility_then_return_full_info'))
        suite.addTest(TestCommandHandler('given_arg_info_without_visibility_then_return_partial_info'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestCommandHandler.run_all_test()