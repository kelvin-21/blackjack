from domain.model import Player, PlayerStatus, PlayerStatusReason, Hand


class Dealer(Player):
    def __init__(self, dealer_min: int):
        super(Dealer, self).__init__('Dealer')
        self.dealer_min = dealer_min  # minimum hand value to attain in each round
        self.status = PlayerStatus.DEALER
        self.status_reason = PlayerStatusReason.DEALER

    def init(self):
        self.hand.init()
        self.status_reason = PlayerStatusReason.DEALER
    
    def is_request_card(self) -> bool:
        if not self.can_request_card():
            return False
        hand_value = max(self.hand.hand_value) # if the Dealer has A, it must be used as 11
        return True if hand_value < self.dealer_min else False

    def update_status(self):
        self.status = PlayerStatus.DEALER
        self.status_reason = PlayerStatusReason.DEALER