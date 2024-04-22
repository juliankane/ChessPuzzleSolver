
import pandas as pd
from constants import *
from FENParser import fen_to_board, move_tuple_to_string
from MoveCalculator import legal_moves
from Piece import Piece
import copy

class Chessboard:
    class State:
        def __init__(self, fen):
            self.is_checked = False
            self.inital_order = fen[0] 
            self.white_attacking = fen[1] == 'w'
            self.enpassant, self.clock, self.num_moves = fen[3], fen[4], fen[5] 
            self.str_board = fen_to_board(fen[0])
            self.previous_states = []

        def save_state(self, move:Piece, frm:tuple, taken, turn, eval, checks):
            state = { "move":move, "frm":frm, "taken": taken, "turn":turn, "eval":eval,"checks":checks}
            self.previous_states.append(state)        

        def load_state(self):
            return self.previous_states.pop()
        
    def __init__ (self, fen, output = False):
        self.output = output
        self.state = self.State(fen.split(' '))
        self.fen = fen
        self.evaluation = 0
        self.Board = pd.DataFrame(columns=FILES, index = RANKS).fillna("-")
        self.current = 0 if self.state.white_attacking else 1 
        self.move_list = []
        self._initBoard()

    def _initBoard(self):
        b = self.state.str_board
        self.pieces = {0:[],1:[]} ; self.open_squares = {0:[],1:[]} 

        for i, rank in b.iterrows(): 
            for file in b.columns:
                piece = b.loc[file, i]
                if piece in WHITE["PIECES"]: 
                    piece = Piece.create_piece(type = WHITE["PIECES"][piece], color="white", position=(file,i), fen_char = piece) 
                    self.pieces[0].append(piece)
                    self.Board.at[file, i] = piece 
                    if not self.state.white_attacking and piece.name != KING: 
                        self.open_squares[1].append((file, i))
                elif piece in BLACK["PIECES"]:
                    piece = Piece.create_piece(BLACK["PIECES"][piece], color="black", position=(file,i), fen_char = piece)
                    self.pieces[1].append(piece)
                    self.Board.at[file, i] = piece 
                    if self.state.white_attacking and piece.name != KING: 
                        self.open_squares[0].append((file, i)) 
                else:
                    self.Board.at[file, i] = (file,i)
                    self.open_squares[0].append((file, i))
                    self.open_squares[1].append((file, i))

    def toggle_turn(self):
        self.current = 1 - self.current

    def get_legal_moves(self):
        move_dictionary = legal_moves(self)
        return move_dictionary
    
    def push_move(self, move):
        piece = move['piece']
        square = move['moved_to']
        value = move['value']
        self.state.is_checked = move['check']
        self.evaluation = value
        leaving_square = piece.position
        piece.move(square)
        _attacked_square = self.Board.at[square[X], square[Y]]
        opponent_index = 1 - self.current

        if isinstance(_attacked_square, Piece):
            self.pieces[opponent_index].remove(_attacked_square) 
            self.open_squares[opponent_index].append(square)

        self.open_squares[self.current].remove(square) 
        self.open_squares[self.current].append(leaving_square)

        self.state.save_state(piece, leaving_square, _attacked_square, self.current, value, move['check'])
        self.Board.at[leaving_square[X], leaving_square[Y]] = leaving_square
        self.Board.at[square[X], square[Y]] = piece
        self.move = move_tuple_to_string(leaving_square, square)
        self.move_list.append({'value':value, 'move': move_tuple_to_string(leaving_square, square)})

        if self.output:
            self.print_board()
        self.toggle_turn()
        return True
    
    def undo_move(self):
        state = self.state.load_state()
        piece = state['move']
        frm = state['frm']
        taken = state['taken']
        self.current = state['turn']
        self.evaluation = state['eval']
        self.move_list.pop()
        if state['checks']:
            self.state.is_checked = False
        piece.move(frm)

        if isinstance(taken, Piece):
            self.pieces[1-self.current].append(taken) 
            self.open_squares[1-self.current].remove(taken.position) 
            self.Board.at[taken.position[X], taken.position[Y]] = taken
            self.open_squares[self.current].append(taken.position)  
        else:
            self.open_squares[self.current].append(taken) 
            self.Board.at[taken[X],taken[Y]] = taken

        self.open_squares[self.current].remove(piece.position)
        self.Board.at[piece.position[X], piece.position[Y]] = piece
        return True

    def evaluate(self, maximizing):
        if self.is_checkmate():
            if maximizing:
                return copy.deepcopy(self.move_list), -9999999
            else:
                return copy.deepcopy(self.move_list), 9999999
        else:
            eval = 0
            for i, move_info in enumerate(self.move_list):
                sign = 1 if i % 2 == 0 else -1
                eval += sign * move_info['value']
            return copy.deepcopy(self.move_list), eval
        
    def is_checkmate(self):
        if self.state.is_checked:
            moves = legal_moves(self)
            if len(moves) == 0:
                return True
        return False
    
    def getState(self):
        return self.State
    
    def getPieces(self):
        return self.pieces
    
    def getOpenSquares(self):
        return self.open_squares
    
    def print_board(self):
        print(f"To move : {self.current}")
        board = self.Board.map(lambda x: x.name if isinstance(x, Piece) and x != "-" else x)
        print(board)
        print("\n")
        

    


    


    