from domain.service import ConfigLoader
from domain.model import Player, PlayerStatus, Dealer, Card, Suit, Rank, CardDeck, HandStatus
import random
import logging


class Game():
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.players = None
        self.dealer = None
        self.card_deck = None
        self.cards_required_each_round = None

    def init(self):
        num_player = self.config_loader.num_player
        dealer_min = self.config_loader.dealer_min
        num_card_set = self.config_loader.num_card_set

        self.create_players(num_player)
        self.dealer = Dealer(dealer_min)
        self.card_deck = CardDeck(num_card_set)
        self.cards_required_each_round = (num_player + 1) * 3

        self.init_game()

    def init_game(self) -> None:
        for player in self.players:
            player.init()
        self.dealer.init()
        self.card_deck.init()

    def init_round(self) -> None:
        while self.dealer.hand.hand:
            card = self.dealer.hand.hand.pop()
            self.card_deck.add_card(card)
        for player in self.players:
            while player.hand.hand:
                card = player.hand.hand.pop()
                self.card_deck.add_card(card)

    def create_players(self, num_player: int) -> None:
        self.players = list()
        self.players.append(Player('Me'))
        for i in range(num_player - 1):
            self.players.append(Player(f'Player_{i+2}'))
    
    def distribute_card(self, target: Player, suit: Suit = None, rank: Rank = None) -> bool:
        # this check should be in game controller

        # # restart game if card deck is empty
        # if self.card_deck.is_card_deck_empty():
        #     self.init()
        #     logging.info('Restarting game because the card deck is empty')
        #     return False

        # # restart game if remaining cards are not enough for a round
        # if self.card_deck.cards_remaining() < self.cards_required_each_round:
        #     self.init()
        #     logging.info('Restarting game because the card deck does not have enough cards')
        #     return False
        
        if suit is not None or rank is not None:
            # distribute a certain card
            card = self.card_deck.search_card(suit, rank)
            return self.send_card(target, card)

        else:
            # distribute randomly
            card = self.card_deck.get_random_card()
            return self.send_card(target, card)

    def send_card(self, target: Player, card: Card) -> bool:
        if card:
            target.add_card(card)
            self.card_deck.remove_card(card)
            return True
        else:
            return False

    def conclude_players_status(self) -> None:
        for player in self.players:
            self.conclude_player_status(player)

    def conclude_player_status(self, player: Player) -> None:
        if player.hand.status == HandStatus.BUST:
            player.status = PlayerStatus.LOSE

        elif player.hand.status in (HandStatus.BLACKJACK, HandStatus.BLACKJACK):
            if self.dealer.hand.status in (HandStatus.BLACKJACK, HandStatus.BLACKJACK):
                player.status = PlayerStatus.LOSE
            else:
                player.status = PlayerStatus.WIN

        elif player.hand.status == HandStatus.LIVE:
            if self.dealer.hand.status == HandStatus.BUST:
                return True
            elif max(player.hand.hand_value) > max(self.dealer.hand.hand_value):
                return True
            else:
                return False

        else:
            raise ValueError(f'Unknown HandStatus ({player.hand.status}) for player {player.name}')