import copy
from dlgo.gotypes import Player

class Move():
    def __init__(self, point=None,is_pass=False,is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign    
        # assert must return True for the code to continue. 
        # ^ is a bitwise exclusive OR operator, XOR, which deals only in 1s / 0s - also read as True / False. 
        # example: a ^ b means that a or b can be True to return a logical True, but they cant both be True. 
        # our assertion means that ONLY one of these can be True
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod # we use the classmethod decorator to define a class method, which means we as defining at class level and not instance level
    def play(cls, point):
        return Move(point=point)
    
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign=True)
    