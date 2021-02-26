from domain.model import PlayerStatus
from domain.service import Simulator, Decision
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

    @staticmethod
    def advice(sim_result: dict) -> str:
        decision = Simulator.get_advice(sim_result)

        sum_dict = Utilities.sum_nested_dict
        if decision:
            maximum = sum_dict(sim_result[decision][PlayerStatus.WIN]) / sum_dict(sim_result[decision])
            advice_msg = decision.value

        else:  # decision is None
            maximum = sum_dict(sim_result[Decision.REQUEST][PlayerStatus.WIN]) / sum_dict(sim_result[Decision.REQUEST])
            advice_msg = 'try your luck'

        request_c = sum_dict(sim_result[Decision.REQUEST])
        pass_c = sum_dict(sim_result[Decision.PASS])
        win_given_request_c = sum_dict(sim_result[Decision.REQUEST][PlayerStatus.WIN])
        win_given_pass_c = sum_dict(sim_result[Decision.PASS][PlayerStatus.WIN])

        win_given_request_p = win_given_request_c / request_c
        win_given_pass_p = win_given_pass_c / pass_c
        
        msg = ''
        msg += f'P({PlayerStatus.WIN.value}|{Decision.REQUEST.value}) = {win_given_request_p:.3f}\n'
        msg += f'P({PlayerStatus.WIN.value}|{Decision.PASS.value}) = {win_given_pass_p:.3f}\n'
        msg += f'Advice: {advice_msg} -> {maximum:.1%} {PlayerStatus.WIN.value}\n'

        return msg