import abc


class Heuristics(abc.ABC):

    @staticmethod
    @abc.abstractmethod
    def evaluate(game_state, choosing_player, depth):
        pass
