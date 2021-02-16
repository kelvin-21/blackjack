from enum import Enum


class GameStatus(Enum):
    START_NEW_GAME = 'start_new_game'
    START_NEW_ROUND = 'new_round'
    GAME = 'game'
    FINISHED = 'finished'
    EMPTY_DECK = 'empty_deck'
    ERROR = 'error'