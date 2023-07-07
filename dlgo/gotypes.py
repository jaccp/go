# imports
import enum
from collections import namedtuple

# define our player class
class Player(enum.Enum):
    # we are using an enumaration class for our players
    # this means we can have two playeres, 1 and 2, corresponding to black and white
    black = 1
    white = 2

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white

class Point(namedtuple('Point','row col')):
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]

