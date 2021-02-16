from domain.model import Suit, Rank


class CardInputResult():
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError(f'Cannot compare type - {self.__class__} and {obj.__class__}')
        else:
            return self.suit == obj.suit and self.rank == obj.rank


class CardInputHandler():
    @staticmethod
    def handle(arg: str) -> CardInputResult:
        suit, rank = None, None
        if arg == '':
            return CardInputResult(suit, rank)

        my_list = arg.split(' ')
        for my_item in my_list:
            if not suit:
                for item in Suit:
                    if my_item == item.value:
                        suit = item
            if not rank:
                for item in Rank:
                    if my_item == item.value:
                        rank = item
        
        if len(my_list) == 1:
            if suit is not None or rank is not None:
                return CardInputResult(suit, rank)
        elif len(my_list) == 2:
            if suit is not None and rank is not None:
                return CardInputResult(suit, rank)
        return None
        # if both suit and rank are None, then return None, will ask for input again