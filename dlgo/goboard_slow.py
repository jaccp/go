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
    
class GoString():
    # this is whree we will track connected groups of stones
    def __init__(self, color, stones, liberties):
        self.color = color
        self.stones = set(stones)
        self.liberties = set(liberties)

    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string):
        # used to track when a string merges with another string by placing a stone
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(
            self.color,
            combined_stones,
            (self.liberties | go_string.liberties) - combined_stones # spacially, this translates to us removing the liberty at the point where we have added the briding stone between the two strings
        )

    @property
    def num_liberties(self):
        return len(self.liberties)
    
    def __eq__(self, other):
        # the __eq__ is a dunder method that allows us to define what python does when comparing two objects of a class when using '=='
        # we want python to perform a thorough check that both strings are part of the same string
        # # we do this by checking that they are both GoString object of the same color, with the same stones and liberties 
        return isinstance(other, GoString) and \
            self.color == other.color and \
            self.stones == other.stones and \
            self.liberties == other.liberties
    
class Board():
    # our board is initialised as an empty grid with the specified number of rows and columns
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {}

    def place_stone(self, player, point):
        # this function allows the placing of stones, where we must check for neighbours 
        assert self.is_on_grid(point) # check stone will be on grid - defined below
        assert self._grid.get(point) is None # check stone is not already on the board at that point
        adjacent_same_colour = []
        adjacent_opposite_colour = []
        liberties = []
        for neighbour in point.neighbours(): # for all 4 neighbouring points...
            if not self.is_on_grid(neighbour): # check the neighbour is not on grid
                continue # if it is not on grid then continue, otherwise break and go to next neighbour
            neighbour_string = self._grid.get(neighbour)
            if neighbour_string is None:
                liberties.append(neighbour)
            elif neighbour_string.colour == player:
                if neighbour_string not in adjacent_same_colour:
                    adjacent_same_colour.append(neighbour_string)
            else:
                if neighbour_string not in adjacent_opposite_colour:
                    adjacent_opposite_colour.append(neighbour_string)
        new_string = GoString(player, [point], liberties)

        def is_on_grid(self, point):
            return 1 <= point.row <= self.num_rows and \
            1 <= point.col <= self.num_cols


