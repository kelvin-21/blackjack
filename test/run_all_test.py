from test.domain.model.test_card_deck import TestCardDeck
from test.domain.model.test_card import TestCard
from test.domain.model.test_dealer import TestDealer
from test.domain.model.test_game import TestGame
from test.domain.model.test_hand import TestHand
from test.domain.model.test_player import TestPlayer

from test.domain.service.test_simulator import TestSimulator

from test.controller.handler.test_card_input_handler import TestCardInputHandler
from test.controller.handler.test_card_request_handler import TestCardRequestHandler

from test.view.test_game_viewer import TestGameViewer
from test.view.test_simulation_viewer import TestSimulationViewer

from test.utilities.test_utilities import TestUtilities


def run_all_test():

    TestCardDeck.run_all_test()
    TestCard.run_all_test()
    TestDealer.run_all_test()
    TestGame.run_all_test()
    TestHand.run_all_test()
    TestPlayer.run_all_test()

    TestSimulator.run_all_test()

    TestCardInputHandler.run_all_test()
    TestCardRequestHandler.run_all_test()
        
    TestGameViewer.run_all_test()
    TestSimulationViewer.run_all_test()

    TestUtilities.run_all_test()
    
    print('----------------------------------------------------------------------')
    print('[ALL] Finished\n\n')


if __name__ == '__main__':
    run_all_test()