# imports
import enum
from collections import namedtuple

# define our player class
class player(enum.Enum):
    # we are using an enumaration class for both of our players
    # this means we have two playeres, 1 and 2, corresponding to black and white, on the same class object
    black = 1
    white = 2

    @property # we use the property decorator to define a method that can be called as an attribute
    def other(self):
        return player.black if self == player.white else player.white
        # this method allows us to see which player is our opponent 
        
class Point(namedtuple('Point','row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]

