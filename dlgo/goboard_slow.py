import copy
from dlgo.gotypes import Player

class Move():
    def __init__(self, point=None,is_pass=False,is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign    # assert must return True for the code to continue. 
                                                            # ^ is a bitwise exclusive OR operator, XOR, which deals only in 1s / 0s - also read as True / False. 
                                                            # example: a ^ b means that a or b can be True to return a logical True, but they cant both be True. 
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
