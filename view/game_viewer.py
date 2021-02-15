from domain.model import Player, CardDeck, Card, Suit, Rank, Hand, Dealer
from typing import List


class GameViewer():
    def __init__(self):
        self.suit_to_symbol = {
            Suit.DIAMOND    : '♦',
            Suit.CLUB       : '♣',
            Suit.HEART      : '♥️',
            Suit.SPADE      : '♠'
        }

    @staticmethod
    def view(msg: str) -> None:
        print(msg)

    def all_cards(self, card_deck: CardDeck) -> str:
        count = dict()
        for rank in Rank:
            count[rank] = 0
        for card in card_deck.deck:
            count[card.rank] += 1
        msg = ''
        for rank in Rank:
            msg += f'{rank.value:2}: {count[rank]}\n'
        return msg

    def all_hands(self, dealer: Dealer, players: List[Player]) -> str:
        people = [dealer] + players
        msg = ''
        for person in people:
            name = self.player_name(person, dealer, players)
            hand = self.hand(person.hand)
            msg += f'[{name}]: {hand}\n'
        return msg

    def players_details(self, dealer: Dealer, players: List[Player]) -> str:
        people = [dealer] + players
        msg = ''
        for person in people:
            name = self.player_name(person, dealer, players)
            status = self.player_status(person, dealer, players)
            hand = self.hand(person.hand)
            msg += f'[{name}]: {status} - {hand}\n'
        return msg

    def card(self, card: Card) -> str:
        return f'{self.suit_to_symbol[card.suit]} {card.rank.value}'

    def hand(self, hand: Hand) -> str:
        msg = ''
        for card in hand.hand:
            msg += f'({self.card(card)}) '
        return msg.strip()

    def player_name(self, target: Player, dealer: Dealer, players: List[Player]) -> str:
        l = [len(dealer.name)] + [len(player.name) for player in players]
        maximum = max(l)
        return '{:{m}}'.format(target.name, m=maximum)

    def player_status(self, target: Player, dealer: Dealer, players: List[Player]) -> str:
        l = [len(dealer.status.value)] + [len(player.status.value) for player in players]
        maximum = max(l)
        return '{:{m}}'.format(target.status.value, m=maximum)

    