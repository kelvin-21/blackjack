from domain.model import Game, Player
from controller import GameStatus
from view import GameViewer
from utilities import Utilities
from configuration import ConfigLoader
import pandas as pd
from typing import List
import os
import logging


class GameRecorder():
    def __init__(self, config_loader: ConfigLoader, game_viewer: GameViewer):
        self.config_loader = config_loader
        self.game_viewer = game_viewer

        self.df = None
        self.file_dest = self.config_loader.data_path + 'data.csv'
        self.init()

    def init(self):
        if os.path.isfile(self.file_dest):
            self.df = pd.read_csv(self.file_dest)
        else:
            self.init_df()
            logging.info(f'Created new data file at {self.file_dest}')

    def init_df(self):
        self.df = pd.DataFrame()
        self.df['sim_date_time'] = None
        self.df['dealer_hand'] = None
        self.df['player_hand'] = None
        self.df['player_status'] = None
        self.df['player_status_reason'] = None
        self.df['dealer_hand_status'] = None
        self.df['num_card_remain'] = None
        self.df['num_player'] = None
        self.df['num_card_set'] = None
        self.df['simulation_trials'] = None

    def record(self, game: Game) -> None:
        if game.status != GameStatus.FINISHED:
            logging.warning(f'Only support record game when status is {GameStatus.FINISHED.value}')
            return
        
        player_me = self.find_player_me(game.players)
        num_card_remain = len(game.card_deck.deck)
        num_card_remain += len(game.dealer.hand.hand)
        for player in game.players:
            num_card_remain += len(player.hand.hand)

        new_row = {
            'sim_date_time'         : Utilities.datetime_str(),
            'dealer_hand'           : self.game_viewer.hand(game.dealer.hand),
            'player_hand'           : self.game_viewer.hand(player_me.hand),
            'player_status'         : player_me.status.value,
            'player_status_reason'  : player_me.status_reason.value,
            'dealer_hand_status'    : game.dealer.hand.status.value,
            'num_card_remain'       : num_card_remain,
            'num_player'            : self.config_loader.num_player,
            'num_card_set'          : self.config_loader.num_card_set,
            'simulation_trials'     : self.config_loader.simulation_trials,
        }
        self.df = self.df.append(new_row, ignore_index=True)
        self.df.to_csv(self.file_dest, index=False)

    def find_player_me(self, players: List[Player]) -> Player:
        for player_i in players:
            if player_i.name == 'Me':
                return player_i
        raise ValueError('Player Me not found in the game players')