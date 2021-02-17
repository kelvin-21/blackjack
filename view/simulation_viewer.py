from utilities import Utilities


class SimulationViewer():
    def __init__(self):
        pass

    @staticmethod
    def view(msg: str) -> None:
        if msg:
            print(msg)

    def sim_result(self, sim_result: dict, content='short', display='percentage') -> str:
        return {
            'short': self.sim_result_short(sim_result, display),
            'detail': self.sim_result_detail(sim_result, display)
        }[content]

    @staticmethod
    def sim_result_short(sim_result: dict, display='percentage') -> str:
        tab = '    '
        msg = ''
        for key_i in sim_result:
            sum_i = Utilities.sum_nested_dict(sim_result[key_i])
            msg += f'{key_i.value}: {sum_i}\n'

            for key_j in sim_result[key_i]:
                sum_j = Utilities.sum_nested_dict(sim_result[key_i][key_j])
                if display == 'percentage':
                    sum_j = f'{sum_j/sum_i:.1%}'

                msg += f'{tab}{key_j.value}: {sum_j}\n'
        
        return msg

    @staticmethod
    def sim_result_detail(sim_result: dict, display='percentage') -> str:
        tab = '    '
        msg = ''
        for key_i in sim_result:
            sum_i = Utilities.sum_nested_dict(sim_result[key_i])
            msg += f'{key_i.value}: {sum_i}\n'

            for key_j in sim_result[key_i]:
                sum_j = Utilities.sum_nested_dict(sim_result[key_i][key_j])
                if display == 'percentage':
                    sum_j = f'{sum_j/sum_i:.1%}'

                msg += f'{tab}{key_j.value}: {sum_j}\n'

                for key_k in sim_result[key_i][key_j]:
                    value = sim_result[key_i][key_j][key_k]
                    if display == 'percentage':
                        value = f'{value/sum_i:.1%}'

                    msg += f'{tab}{tab}{key_k.value}: {value}\n'
        
        return msg