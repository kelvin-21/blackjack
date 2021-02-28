import logging
import sys
import os


Config = {
    'num_player'                : 5,
    'num_card_set'              : 2,
    'dealer_min'                : 16,
    'max_num_card_in_hand'      : 5,
    'simulation_trials'         : 1000,
    'data_path'                 : ''
}


class ConfigLoader():
    def __init__(self):
        self.num_player = None
        self.num_card_set = None
        self.dealer_min = None
        self.simulation_trials = None
        self.data_path = None
        self.load()

    def load(self):
        for key in self.__dict__.keys():
            try:
                self.__dict__[key] = Config[key]
            except Exception as ex:
                logging.warning(f'Unable to load configuration - {key}, {ex}')

    @staticmethod
    def config_logger():
        # create log if not exist
        log_filename = "logs/blackjack.log"
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)

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