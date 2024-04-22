
from constants import *
import copy

class Piece:
    def __init__(self, color = "", position = "", fen_char = ""):
        self.color = color 
        self.position = position 
        self.fen_char = fen_char   
        self.attacks_board = False  

    def __deepcopy__(self, memo):
        new_piece = type(self)(
            color=self.color,
            position=copy.deepcopy(self.position, memo),
            fen_char=self.fen_char
        )
        return new_piece
    
    def create_piece(type = "", color = "", position = "", fen_char = ""): 
        if type == PAWN:
            return Pawn(color, position, fen_char)
        elif type == KNIGHT:
            return Knight(color, position, fen_char)
        elif type == BISHOP:
            return Bishop(color, position, fen_char)
        elif type == ROOK:
            return Rook(color, position, fen_char)
        elif type == QUEEN:
            return Queen(color, position, fen_char)
        elif type == KING:
            return King(color, position, fen_char)
        else:
            raise ValueError("Unknown Piece Type")
        
    def move(self, square):
        self.position = square

    def absolute_position(self, square, from_square = None):
        if from_square is None:
            x = abs(square[X] - self.position[X]) # self to square ->
            y = abs(square[Y] - self.position[Y])
        else:
            x = abs(square[X] - from_square[X]) # self to square ->
            y = abs(square[Y] - from_square[Y])
        return x,y
    
    def relative_direction(self, square, from_square = None):
        if from_square is None:
            dir_x = (square[X] - self.position[X]) // max(abs(square[X] - self.position[X]), 1)
            dir_y = (square[Y] - self.position[Y]) // max(abs(square[Y] - self.position[Y]), 1)
        else:
            dir_x = (square[X] - from_square[X]) // max(abs(square[X] - from_square[X]), 1)
            dir_y = (square[Y] - from_square[Y]) // max(abs(square[Y] - from_square[Y]), 1)
        return dir_x, dir_y
    
    def steps_to_square(self, square, frm = None):
        x,y = self.absolute_position(square, from_square = frm)
        x_direction, y_direction = self.relative_direction(square, from_square=frm)
        steps_to_square = max(x,y)
        steps = []

        if frm is None:
            for step in range(1, steps_to_square): 
                square = (self.position[X] + (step * x_direction), self.position[Y] + (step * y_direction))
                steps.append(square)
        else:
            for step in range(1, steps_to_square): 
                square = (frm[X] + (step * x_direction), frm[Y] + (step * y_direction))
                steps.append(square)
        return steps

    def clear_path(self, square, pieces, frm=None, **kwargs):
        ignore_king = kwargs.get("ignore_king", False)
        steps = self.steps_to_square(square, frm = frm) 
        for step in steps:
            if step == square:
                return True
            for p in pieces:
                if p.position == step:
                    if ignore_king and p.name == "King":
                        continue
                    return False
        return True

class Pawn(Piece):
    def __init__(self, color, position, fen_char):
        super().__init__(color, position, fen_char)
        self.name = PAWN
        self.value = 1
        self.isValueable = False
        self.can_pin = False

    def can_reach_square(self, square, att = [], dff = [], frm = None, to_attack = True, to_move = True, **kwargs) -> bool: 
        if square == self.position or (frm is not None and frm == self.position):
            return False
        direction = 1 if self.color == 'white' else -1 
        x,y = self.position     

        takes_position = [(x + direction, y-1), (x + direction, y + 1 )] if (1 <= x + direction <= 8 and (1 <= y - 1 <= 8 or 1 <= y + 1 <= 8)) else []
        if square in takes_position and any(p.position == square for p in dff):
            return True
        if not to_move:
            if square in takes_position:
                return True
        if to_move:
            forward_position = [(x + direction, y)] if 1 <= x + direction <= 8 else []
            if square in forward_position:
                return True
        return False
    

class Knight(Piece):
    def __init__(self, color, position, fen_char):
        super().__init__(color, position, fen_char)
        self.name = KNIGHT
        self.value = 3
        self.can_pin = False

    def can_reach_square(self, square, att = [], dff = [], frm=None,  **kwargs) -> bool: 
        if square == self.position or (frm is not None and frm == self.position):
            return False
        x,y = self.absolute_position(square, from_square=frm)
        if ((x==2 and y == 1) or (x == 1 and y == 2)):
            return True
        return False
    
    def steps_to_square(self, square, **kwargs):
        return []


class Bishop(Piece):
    def __init__(self, color, position, fen_char):
        super().__init__(color, position, fen_char)
        self.name = BISHOP
        self.value = 3 

    def can_reach_square(self, square, att = [], dff = [], frm = None, **kwargs):
        if square == self.position or (frm is not None and frm == self.position):
            return False
        x,y = self.absolute_position(square, from_square = frm)
        if (x==y):
            return self.clear_path(square, att+dff, frm=frm, **kwargs)
        return False
        
class Rook(Piece):
    def __init__(self, color, position, fen_char):
        super().__init__(color, position, fen_char)
        self.name = ROOK
        self.value = 5

    def can_reach_square(self, square, att = [], dff = [], frm = None, **kwargs) -> bool:
        if square == self.position or (frm is not None and frm == self.position):
            return False
        x,y = self.absolute_position(square, from_square=frm)
        if ( (x==0) or (y==0) ):
            det = self.clear_path(square, att+dff, frm=frm, **kwargs)
            return det
        return False

class Queen(Piece):
    def __init__(self, color, position, fen_char):
        super().__init__(color, position, fen_char)
        self.name = QUEEN
        self.value = 8

    def can_reach_square(self, square, att = [], dff = [], frm=None, **kwargs) -> bool:
        if square == self.position or (frm is not None and frm == self.position):
            return False
        x,y = self.absolute_position(square, from_square=frm)
        if ((x == y) or (x == 0) or (y == 0)):
            return self.clear_path(square, att+dff, frm=frm,  **kwargs)
        return False
    
class King(Piece):
    def __init__(self, color, position, fen_char):
        super().__init__(color, position, fen_char)
        self.name = KING
        self.value = 15
        self.range = 1
        self.moves = [MOVEMENT[N], MOVEMENT[NE], MOVEMENT[E], MOVEMENT[SE], MOVEMENT[S], MOVEMENT[SW], MOVEMENT[W], MOVEMENT[NW]]

    def can_reach_square(self, square, att = [], dff = [], frm=None, **kwargs) -> bool:
        if square == self.position or (frm is not None and frm == self.position):
            return False
        
        x,y = self.absolute_position(square, from_square=frm)
        if ((x == 1 and y == 0) or (y == 1 and x == 0) or (x == 1 and y == 1)) and \
            not any(p.can_reach_square(square, att=dff, dff=att, frm=frm) for p in dff if p.name != "King"):
                return True
        return False
    
    def kings_adjacent_squares(self, open_squares, attacking, defending = [], Moves = {}):
        kings_adjacent = []
        for square in self.moves:
            x = square[X] + self.position[X] 
            y = square[Y] + self.position[Y]

            if not (1 <= x <= 8 and 1 <= y <= 8):
                continue

            potential_position = (x,y) 
            if potential_position in open_squares and not any(piece.position == potential_position for piece in attacking):
                kings_adjacent.append(potential_position)

        return kings_adjacent
        
                    
                
            




            


        
        


       









