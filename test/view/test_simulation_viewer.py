import unittest
from domain.model import PlayerStatus, PlayerStatusReason
from domain.service import Decision
from view import SimulationViewer


class TestSimulationViewer(unittest.TestCase):
    def setUp(self):
        self.simulation_viewer = SimulationViewer()
        self.sim_result = {
            Decision.REQUEST: {
                PlayerStatus.WIN: {
                    PlayerStatusReason.DEALER_BUST          : 10,
                    PlayerStatusReason.HAND_VALUE           : 20,
                    PlayerStatusReason.BLACKJACK            : 25,
                    PlayerStatusReason.FIVECARD             : 15
                },
                PlayerStatus.LOSE: {
                    PlayerStatusReason.BUST                 : 5,
                    PlayerStatusReason.DEALER_HAND_VALUE    : 10,
                    PlayerStatusReason.DEALER_BLACKJACK     : 10,
                    PlayerStatusReason.DEALER_FIVECARD      : 5
                }
            },
            Decision.PASS: {
                PlayerStatus.WIN: {
                    PlayerStatusReason.DEALER_BUST          : 35,
                    PlayerStatusReason.HAND_VALUE           : 15,
                    PlayerStatusReason.BLACKJACK            : 15,
                    PlayerStatusReason.FIVECARD             : 0
                },
                PlayerStatus.LOSE: {
                    PlayerStatusReason.BUST                 : 7,
                    PlayerStatusReason.DEALER_HAND_VALUE    : 9,
                    PlayerStatusReason.DEALER_BLACKJACK     : 8,
                    PlayerStatusReason.DEALER_FIVECARD      : 11
                }
            }
        }

    def test_sim_result_short_num(self):
        tab = '    '
        expected = ''
        expected += f'{Decision.REQUEST.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 70\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 30\n'
        expected += f'{Decision.PASS.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 65\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 35\n'

        result = self.simulation_viewer.sim_result_short(self.sim_result, display='num')

        self.assertEqual(result, expected)

    def test_sim_result_detail_num(self):
        tab = '    '
        expected = ''
        expected += f'{Decision.REQUEST.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 70\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BUST.value}: 10\n'
        expected += f'{tab}{tab}{PlayerStatusReason.HAND_VALUE.value}: 20\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BLACKJACK.value}: 25\n'
        expected += f'{tab}{tab}{PlayerStatusReason.FIVECARD.value}: 15\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 30\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BUST.value}: 5\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_HAND_VALUE.value}: 10\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BLACKJACK.value}: 10\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_FIVECARD.value}: 5\n'
        expected += f'{Decision.PASS.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 65\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BUST.value}: 35\n'
        expected += f'{tab}{tab}{PlayerStatusReason.HAND_VALUE.value}: 15\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BLACKJACK.value}: 15\n'
        expected += f'{tab}{tab}{PlayerStatusReason.FIVECARD.value}: 0\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 35\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BUST.value}: 7\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_HAND_VALUE.value}: 9\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BLACKJACK.value}: 8\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_FIVECARD.value}: 11\n'
        
        result = self.simulation_viewer.sim_result_detail(self.sim_result, display='num')

        self.assertEqual(result, expected)

    def test_sim_result_short_percentage(self):
        tab = '    '
        expected = ''
        expected += f'{Decision.REQUEST.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 70.0%\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 30.0%\n'
        expected += f'{Decision.PASS.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 65.0%\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 35.0%\n'

        result = self.simulation_viewer.sim_result_short(self.sim_result, display='percentage')

        self.assertEqual(result, expected)

    def test_sim_result_detail_percentage(self):
        tab = '    '
        expected = ''
        expected += f'{Decision.REQUEST.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 70.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BUST.value}: 10.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.HAND_VALUE.value}: 20.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BLACKJACK.value}: 25.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.FIVECARD.value}: 15.0%\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 30.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BUST.value}: 5.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_HAND_VALUE.value}: 10.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BLACKJACK.value}: 10.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_FIVECARD.value}: 5.0%\n'
        expected += f'{Decision.PASS.value}: 100\n'
        expected += f'{tab}{PlayerStatus.WIN.value}: 65.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BUST.value}: 35.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.HAND_VALUE.value}: 15.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BLACKJACK.value}: 15.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.FIVECARD.value}: 0.0%\n'
        expected += f'{tab}{PlayerStatus.LOSE.value}: 35.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.BUST.value}: 7.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_HAND_VALUE.value}: 9.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_BLACKJACK.value}: 8.0%\n'
        expected += f'{tab}{tab}{PlayerStatusReason.DEALER_FIVECARD.value}: 11.0%\n'
        
        result = self.simulation_viewer.sim_result_detail(self.sim_result, display='percentage')

        self.assertEqual(result, expected)

    def test_advice(self):
        expected = ''
        expected += f'P({PlayerStatus.WIN.value}|{Decision.REQUEST.value}) = 0.700\n'
        expected += f'P({PlayerStatus.WIN.value}|{Decision.PASS.value}) = 0.650\n'
        expected += f'Advice: {Decision.REQUEST.value} -> 70.0% {PlayerStatus.WIN.value}\n'

        result = self.simulation_viewer.advice(self.sim_result)

        self.assertEqual(result, expected)

    @staticmethod
    def run_all_test():
        suite = unittest.TestSuite()
        suite.addTest(TestSimulationViewer('test_sim_result_short_num'))
        suite.addTest(TestSimulationViewer('test_sim_result_detail_num'))
        suite.addTest(TestSimulationViewer('test_sim_result_short_percentage'))
        suite.addTest(TestSimulationViewer('test_sim_result_detail_percentage'))
        suite.addTest(TestSimulationViewer('test_advice'))

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    TestSimulationViewer.run_all_test()