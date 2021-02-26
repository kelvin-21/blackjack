from domain.model import Player, PlayerStatus, PlayerStatusReason, Dealer, Card, Suit, Rank, CardDeck, HandStatus
from configuration import ConfigLoader
import random
import logging


class Game():
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.config_loader.load()
        self.players = None
        self.dealer = None
        self.card_deck = None
        self.cards_required_each_round = None
        self.status = None  # for GameController

    def init(self):
        num_player = self.config_loader.num_player
        dealer_min = self.config_loader.dealer_min
        num_card_set = self.config_loader.num_card_set

        self.create_players(num_player)
        self.dealer = Dealer(dealer_min)
        self.card_deck = CardDeck(num_card_set)
        self.cards_required_each_round = (num_player + 1) * 4

        self.init_game()

    def init_game(self) -> None:
        self.init_participants()
        self.card_deck.init()

    def init_round(self) -> None:
        self.init_participants()

    def restart_round(self) -> None:
        while self.dealer.hand.hand:
            card = self.dealer.hand.hand.pop()
            self.card_deck.add_card(card)
        for player in self.players:
            while player.hand.hand:
                card = player.hand.hand.pop()
                self.card_deck.add_card(card)
        self.init_participants()

    def init_participants(self) -> None:
        self.dealer.init()
        for player in self.players:
            player.init()

    def create_players(self, num_player: int) -> None:
        self.players = list()
        self.players.append(Player('Me', is_npc=False))
        for i in range(num_player - 1):
            self.players.append(Player(f'Player_{i+2}'))
    
    def distribute_card(self, target: Player, suit: Suit = None, rank: Rank = None) -> bool:
        if not target.can_request_card() or self.card_deck.is_empty():
            return False
            
        if suit is not None or rank is not None:
            # distribute a certain card
            card = self.card_deck.search_card(suit, rank)
            return self.send_card(target, card)

        else:
            # distribute randomly
            card = self.card_deck.get_random_card()
            return self.send_card(target, card)

    def send_card(self, target: Player, card: Card) -> bool:
        if card and target.can_request_card() and not self.card_deck.is_empty():
            target.add_card(card)
            self.card_deck.remove_card(card)
            return True
        else:
            return False

    def conclude_player_status(self, player: Player) -> None:
        if self.dealer.hand.status == HandStatus.BUST:
            if player.hand.status == HandStatus.BUST:
                player.status = PlayerStatus.LOSE
                player.status_reason = PlayerStatusReason.BUST
            else:
                player.status = PlayerStatus.WIN
                player.status_reason = PlayerStatusReason.DEALER_BUST

        elif self.dealer.hand.status == HandStatus.BLACKJACK:
            player.status = PlayerStatus.LOSE
            player.status_reason = PlayerStatusReason.DEALER_BLACKJACK

        elif self.dealer.hand.status == HandStatus.FIVECARD:
            player.status = PlayerStatus.LOSE
            player.status_reason = PlayerStatusReason.DEALER_FIVECARD

        elif self.dealer.hand.status == HandStatus.LIVE:
            if player.hand.status == HandStatus.BLACKJACK:
                player.status = PlayerStatus.WIN
                player.status_reason = PlayerStatusReason.BLACKJACK

            elif player.hand.status == HandStatus.FIVECARD:
                player.status = PlayerStatus.WIN
                player.status_reason = PlayerStatusReason.FIVECARD

            elif player.hand.status == HandStatus.BUST:
                player.status = PlayerStatus.LOSE
                player.status_reason = PlayerStatusReason.BUST

            elif player.hand.status == HandStatus.LIVE:
                if len(player.hand.hand) < 2 or len(self.dealer.hand.hand) < 2: # unexpected flow
                    player.status = PlayerStatus.UNKNOWN
                    player.status_reason = PlayerStatusReason.UNKNOWN
                else:
                    if max(player.hand.hand_value) > max(self.dealer.hand.hand_value):
                        player.status = PlayerStatus.WIN
                        player.status_reason = PlayerStatusReason.HAND_VALUE
                    else:
                        player.status = PlayerStatus.LOSE
                        player.status_reason = PlayerStatusReason.DEALER_HAND_VALUE

            else:
                raise ValueError(f'Unknown HandStatus ({player.hand.status}) for player {player.name}')

        else:
            raise ValueError(f'Unknown HandStatus ({self.dealer.hand.status}) for dealer')