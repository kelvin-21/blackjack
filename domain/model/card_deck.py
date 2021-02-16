from domain.model import Card, Suit, Rank
import random
import logging


class CardDeck():
    def __init__(self, num_card_set: int):
        self.num_card_set = num_card_set
        self.deck = list()

    def init(self):
        self.deck = list()
        for _ in range(self.num_card_set):
            for suit in Suit:
                for rank in Rank:
                    self.add_card(Card(suit, rank))

    def is_empty(self) -> bool:
        return True if len(self.deck) == 0 else False

    def search_card(self, suit: Suit = None, rank: Rank = None) -> Card:
        # support searching by 1 or 2 criteria
        for i in range(len(self.deck)):
            card = self.deck[i]
            if suit and rank:
                if card.suit == suit and card.rank == rank:
                    return card
            elif suit:
                if card.suit == suit:
                    return card
            elif rank:
                if card.rank == rank:
                    return card
        
        logging.info(f'Card ({suit}, {rank}) not found in card deck')
        return None

    def add_card(self, card: Card) -> None:
        self.deck.append(card)

    def remove_card(self, card: Card) -> None:
        self.deck.remove(card)

    def cards_remaining(self) -> int:
        return len(self.deck)

    def get_random_card(self) -> Card:
        if self.is_empty():
            logging.warning('Unable to get card randomly because the card deck is empty')
            return None
        index = random.randint(0, self.cards_remaining()-1)
        card = self.deck[index]
        return card