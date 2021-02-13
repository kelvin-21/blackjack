from typing import List
from enum import Enum


class Suit(Enum):
    DIAMOND = 'diamond'
    CLUB = 'club'
    HEART = 'heart'
    SPADE = 'spade'


class Rank(Enum):
    A = 'A'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    J = 'J'
    Q = 'Q'
    K = 'K'


class Card():
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.__validate()

    def __eq__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError(f'Cannot compare type - {self.__class__} and {obj.__class__}')
        else:
            return self.suit == obj.suit and self.rank == obj.rank

    def __validate(self) -> None:
        if self.suit not in list(item for item in Suit):
            raise ValueError(f'Unknown suit - {self.suit}')
        if self.rank not in list(item for item in Rank):
            raise ValueError(f'Unknown rank - {self.rank}')
        return

    def get_value(self) -> int:
        return {
            Rank.A      : 1,
            Rank.TWO    : 2,
            Rank.THREE  : 3,
            Rank.FOUR   : 4,
            Rank.FIVE   : 5,
            Rank.SIX    : 6,
            Rank.SEVEN  : 7,
            Rank.EIGHT  : 8,
            Rank.NINE   : 9,
            Rank.TEN    : 10,
            Rank.J      : 10,
            Rank.Q      : 10,
            Rank.K      : 10
        }.get(self.rank, -99999)