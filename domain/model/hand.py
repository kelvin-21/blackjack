from domain.model import Card, Rank
from typing import List
from enum import Enum
import logging


class HandStatus(Enum):
    LIVE = 'live'
    BUST = 'bust'
    BLACKJACK = 'blackjack'
    FIVECARD = 'five_card'


class Hand():
    def __init__(self):
        self.hand = list()
        self.hand_value = list()
        self.status = HandStatus.LIVE

    def init(self):
        self.__init__()

    def add_card(self, card: Card):
        if self.status != HandStatus.LIVE:
            logging.warning('Prohibited to add card to non-live hand')
            return
        self.hand.append(card)
        self.update_hand_value(card)
        self.update_status()

    def update_hand_value(self, card: Card) -> None:

        # handle special case of A
        if card.rank == Rank.A:

            if len(self.hand_value) == 0:
                self.hand_value.append(1)
                self.hand_value.append(11)

            elif len(self.hand_value) == 1:
                self.hand_value.append(self.hand_value[0] + 11)
                self.hand_value[0] += 1

            elif len(self.hand_value) == 2:
                self.add_hand_value(1)
            
        else:
            card_value = card.get_value()
            self.add_hand_value(card_value)

        # handle bust
        for value in self.hand_value:
            if value > 21:
                self.hand_value.remove(value)

    def add_hand_value(self, card_value: int) -> None:
        if len(self.hand_value) == 0:
            self.hand_value.append(card_value)
        else:
            for i in range(len(self.hand_value)):
                self.hand_value[i] += card_value

    def update_status(self) -> None:
        if len(self.hand_value) == 0:
            self.status = HandStatus.BUST

        elif len(self.hand_value) == 1 and self.hand_value[0] > 21:
            self.status = HandStatus.BUST
        
        elif len(self.hand) == 2 and max(self.hand_value) == 21:
            self.status = HandStatus.BLACKJACK

        elif self.status == HandStatus.LIVE and len(self.hand) >= 5:
            self.status = HandStatus.FIVECARD

        else:
            self.status = HandStatus.LIVE

    def calculate_update_hand_value(self) -> None:
        temp = []
        while self.hand:
            temp.append(self.hand.pop())
        self.init()
        while temp:
            self.add_card(temp.pop())