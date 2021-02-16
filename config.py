import logging
import sys


Config = {
    'num_player'                : 5,
    'num_card_set'              : 2,
    'dealer_min'                : 16,
    'max_num_card_in_hand'      : 5
}


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