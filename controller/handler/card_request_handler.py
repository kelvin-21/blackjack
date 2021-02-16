class CardRequestResult():
    def __init__(self, request_card: bool):
        self.request_card = request_card

    def __eq__(self, obj):
        if self.__class__ != obj.__class__:
            raise TypeError(f'Cannot compare type - {self.__class__} and {obj.__class__}')
        else:
            return self.request_card == obj.request_card


class CardRequestHandler():
    @staticmethod
    def handle(arg: str) -> CardRequestResult:
        if arg == '':
            return CardRequestResult(False)
        elif any(arg.lower() == _ for _ in ['yes', 'y', 'true', 't']):
            return CardRequestResult(True)
        elif any(arg.lower() == _ for _ in ['no', 'n', 'false', 'f']):
            return CardRequestResult(False)
        else:
            None
            # in this case, we will ask for input again