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
    def num_liberties(self): # returns the number of liberties
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
        assert self._grid.get(point) is None # check stone is not already on the board at that point - defined below
        
        adjacent_same_colour = [] # create list to track adjacent points of the same colour
        adjacent_opposite_colour = [] # create list to track adjacent points of the opposite colour
        liberties = [] # create list to track liberties of the placed stone
        
        for neighbour in point.neighbours(): # for all 4 neighbouring points...
            if not self.is_on_grid(neighbour): # check the neighbour is not on grid
                continue # if it is not on grid then continue with loop, i.e. skip to the next neighbour
            neighbour_string = self._grid.get(neighbour) # define string using current point on grid using our get method. this can return either None or the player colour
            if neighbour_string is None:
                liberties.append(neighbour) # add this point to the placed stone liberties if there is no other stone at this point
            elif neighbour_string.colour == player:
                if neighbour_string not in adjacent_same_colour:
                    adjacent_same_colour.append(neighbour_string) # add current player colour to adjacent_same_colour list if its not already there
            else:
                if neighbour_string not in adjacent_opposite_colour:
                    adjacent_opposite_colour.append(neighbour_string) # add opposite player colour to adjacent_opposite_colour list if its not already there
        
        new_string = GoString(player, [point], liberties) 

        for same_colour_string in adjacent_same_colour: # merge  any adjacent string of the same colour
            new_string = new_string.merged_with(same_colour_string)

        for new_string_point in new_string.stones: # map each stone in new_string to the _grid dictionary
            self._grid[new_string_point] = new_string
        
        for other_colour_string in adjacent_opposite_colour: #reduce liberties of any adjacent string of the opposite colour
            other_colour_string.remove_liberty(point)

        for other_colour_string in adjacent_opposite_colour: # if any opposite colour stings now have zero liberties then remove them
            if other_colour_string.num_liberties == 0:
                self._remove_string(other_colour_string)

    def is_on_grid(self, point):
        # this checks that a point is within the limits of the board
        return 1 <= point.row <= self.num_rows and \
        1 <= point.col <= self.num_cols
    
    def get(self, point):
        # returns the content of a point on the board: a player is a stone is on that point, else None
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color

    def get_go_string(self, point):
        # similar to above get method, but with the distinction that we are now 
        # returning the entire string of stones at a point: a GoString if a stone is on that point, else None
        string = self._grid.get(point)
        if string is None:
            return None
        return string
    
    def _remove_string(self, string):
        for point in string.stones:
            for neighbour in point.neighbours():
                neighbour_string = self._grid.get(neighbour)
                if neighbour_string is None:
                    continue
                if neighbour_string is not string:
                    neighbour_string.add_liberty(point)
            self._grid[point] = None

class GameState():
    # the GameState class tracks the board position, the next player, the previous game state and last move played
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    def apply_move(self, move): # this returns the new GameState after applying the move
        if move.is_play: # if the move is to place a stone then copy the board and place the stone on the new copy for the next player - since the current board state will be for the previous player
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)
        else: # if move is not to place stone then the next board state is just the same as the current board state
            next_board = self.board
        return GameState(board=next_board, next_player=self.next_player.other, previous_state=self, last_move=move)
    
    @classmethod
    def new_game(cls, board_size): # create a new game with a specified board size
        if isinstance(board_size, int): # check that board_size in an integer
            board_size = (board_size, board_size)
        board = Board(*board_size) # create instance of Board class with our specified board size
        return GameState(board=board, next_player=Player.black, previous_state=None, last_move=None) # returns the starting gamestate with the new board. black is next to play, there is no previous player and there is no last move
    
    def is_over(self): # work out if the game is over
        if self.last_move is None:
            return False
        if self.last_move.is_resign: # resigning will cause the game to end
            return True
        second_last_move = self.previous_state.last_move # second last move is defined using the previous game state's last move - now it is obvious why we capture it in this way
        if second_last_move is None:
            '''
            don't undestand the point of this part? 
            '''
            return False
        return self.last_move.is_pass and second_last_move.is_pass 
    
    