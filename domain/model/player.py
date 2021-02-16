from domain.model import Card, Hand, HandStatus, RequestCardProbability
from typing import List
from enum import Enum
import random
import logging


class PlayerStatus(Enum):
    GAME = 'game'
    WIN = 'win'
    LOSE = 'lose'
    DEALER = ''
    UNKNOWN = 'unknown'


class PlayerStatusReason(Enum):
    # win
    DEALER_BUST = 'dealer_bust'
    HAND_VALUE = 'hand_value'
    BLACKJACK = 'blackjack'
    FIVECARD = 'five_card'

    # lose
    BUST = 'bust'
    DEALER_HAND_VALUE = 'dealer_hand_value'
    DEALER_BLACKJACK = 'dealer_blackjack'
    DEALER_FIVECARD = 'dealer_five_card'

    # unknown
    UNKNOWN = 'unknown'


class Player():
    def __init__(self, name: str, is_npc: bool = True):
        self.name = name
        self.hand = Hand()
        self.status = PlayerStatus.GAME
        self.status_reason = None
        self.request_card_probi = RequestCardProbability()
        self.is_npc = is_npc

    def init(self):
        self.hand.init()
        self.status = PlayerStatus.GAME 
        self.status_reason = None

    def add_card(self, card: Card) -> None:
        if self.status in (PlayerStatus.WIN, PlayerStatus.LOSE):
            logging.warning(f'Prohibited to add card to player {self.name} whose status is {self.status}')
            return
        self.hand.add_card(card)
        self.update_status()

    def can_request_card(self) -> bool:
        return self.hand.status == HandStatus.LIVE

    def is_request_card(self) -> bool:
        if not self.can_request_card():
            return False

        if len(self.hand.hand_value) == 1:
            hand_value = self.hand.hand_value[0]
        elif len(self.hand.hand_value) == 2:
            hand_value = max(self.hand.hand_value)
        else:
            raise ValueError(f'Hand value list cannot have size {len(self.hand.hand_value)}')

        probi = self.request_card_probi.get_probability(hand_value)
        return self.probi_toss_coin(probi)

    def update_status(self) -> None:
        if self.hand.status == HandStatus.BUST:
            self.status = PlayerStatus.LOSE

    @staticmethod
    def probi_toss_coin(p: float) -> bool:
        if p == 0:
            return False
        elif p == 1:
            return True
        else:
            r = random.uniform(0, 1)
            return True if r <= p else False