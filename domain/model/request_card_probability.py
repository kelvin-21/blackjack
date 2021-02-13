class RequestCardProbability():
    def __init__(self):
        self.probability = {
            12  : 0.95,
            13  : 0.9,
            14  : 0.8,
            15  : 0.5,
            16  : 0.2,
            17  : 0.1,
            18  : 0,
            19  : 0,
            20  : 0,
        }

    def get_probability(self, hand_value: int):
        if hand_value <= 11:
            return 1
        elif hand_value >= 21:
            return 0
        else:
            return self.probability[hand_value]
