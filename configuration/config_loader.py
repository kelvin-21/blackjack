import logging
import sys


Config = {
    'num_player'                : 5,
    'num_card_set'              : 2,
    'dealer_min'                : 16,
    'max_num_card_in_hand'      : 5,
    'simulation_trials'         : 100
}


class ConfigLoader():
    def __init__(self):
        self.num_player = None
        self.num_card_set = None
        self.dealer_min = None
        self.simulation_trials = None
        self.load()

    def load(self):
        for key in self.__dict__.keys():
            try:
                self.__dict__[key] = Config[key]
            except Exception as ex:
                logging.warning(f'Unable to load configuration - {key}, {ex}')

    @staticmethod
    def config_logger():
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        fh = logging.FileHandler('logs/blackjack.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(formatter)

        root.addHandler(fh)
        root.addHandler(sh)