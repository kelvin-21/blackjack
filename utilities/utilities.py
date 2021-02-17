import logging


class Utilities():
    def __init__(self):
        pass
    
    # condition: all values are at same level
    @staticmethod
    def sum_nested_dict(d: dict) -> int:
        if not d:
            return
        if len(d) == 0:
            return

        try:
            depth = Utilities.depth(d)
            if depth == 1:
                return sum(d.values())
            elif depth == 2:
                return sum([sum(d[key].values()) for key in d.keys()])
            else:
                logging.warning(f'sum_nested_dict for depth {depth} is not supported')
                return
        except:
            logging.warning(f'Not supported for this type of nested dict')
            return
    
    @staticmethod
    def depth(d: dict) -> int:
        if isinstance(d, dict):
            return 1 + (max(map(Utilities.depth, d.values())) if d else 0)
        return 0