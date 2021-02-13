import logging
from config import Config


class ConfigLoader():
    def __init__(self):
        self.num_player = None
        self.num_card_set = None
        self.dealer_min = None

    def load(self):
        for key in self.__dict__.keys():
            try:
                self.__dict__[key] = Config[key]
            except Exception as ex:
                logging.warning(f'Unable to load configuration - {key}, {ex}')