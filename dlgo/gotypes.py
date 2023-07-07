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

class point(namedtuple('point', ['row', 'col'])):
    # namedtuple allows us to access the coordinates of our point
    # using point.row and point.col instead of point[0] and point[1]
    def neighbors(self):
        # define the neighbord of the point as those that are directly above,
        # below, left and right of the point
        return [
            point(self.row - 1, self.col),
            point(self.row + 1, self.col),
            point(self.row, self.col - 1),
            point(self.row, self.col + 1)
        ]

