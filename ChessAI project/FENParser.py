import pandas as pd
import numpy as np
from Piece import Piece
from constants import *

SEPERATOR = '/' 

@staticmethod
def fen_to_board(board_state, f_move = None):
    splt_ranks = board_state.split('/')

    if f_move is not None:
        piece_square = f_move
        piece = (FILES_MAP_CHAR_TO_NUM[piece_square[0]] , 8 - int(piece_square[1]))
        square = (FILES_MAP_CHAR_TO_NUM[piece_square[2]] , 8 - int(piece_square[3])) 
        moving_piece, moving_rank = delete_piece_from_FEN(piece, splt_ranks[piece[1]], piece[0])
        moved_to_rank = add_piece_to_fen(moving_piece, splt_ranks[square[1]], square[0])
        splt_ranks[piece[1]] = moving_rank
        splt_ranks[square[1]] = moved_to_rank

    str_Board = pd.DataFrame(columns=FILES, index = RANKS).fillna("-") 
    for rank, r in zip(RANKS, splt_ranks): 
        i = 0
        for f in r:                   
            if f.isdigit():
                i+=int(f)
                continue
            else:
                str_Board.at[rank, FILES[i]] = f    
                i+=1
    return str_Board

@staticmethod
def move_tuple_to_string(came_from, went_to):
    from_str = FILES_MAP_NUM_TO_CHAR[came_from[Y]] + str(came_from[X])
    went_str = FILES_MAP_NUM_TO_CHAR[went_to[Y]] + str(went_to[X])
    move_str = from_str + went_str
    return move_str

@staticmethod
def add_piece_to_fen(piece, rank, file_position):
    new_rank = ""  
    current_position = 1  
    piece_added = False
    for pc in rank:
        if pc.isdigit():
            num_empty = int(pc)
            if current_position <= file_position < current_position + num_empty:
                left_gap = file_position - current_position
                right_gap = num_empty - left_gap - 1
                if left_gap > 0:
                    new_rank += str(left_gap)
                new_rank += piece  
                if right_gap > 0:
                    new_rank += str(right_gap)
                piece_added = True
                current_position += num_empty
            else:
                new_rank += pc
                current_position += num_empty
        else:
            if current_position == file_position:
                new_rank += piece
                piece_added = True
            else:
                new_rank += pc
            current_position += 1
    if not piece_added and file_position >= current_position:
        new_rank += piece
    return new_rank

@staticmethod
def delete_piece_from_FEN(rank, file_position):
    new_file = ""
    file_keeper = []
    piece_found = ""
    i=0
    index = 1
    index_piece_found = 0
    pop_right, pop_left = False, False
    for pc in rank:
        if index == file_position: # file
            piece_found = pc
            index_piece_found = i
            if i != 0 and file_keeper[i-1].isdigit():
                pop_left = True
            index += 1

        elif pc.isdigit():
            index += int(pc)   
        else:
            index += 1
        file_keeper.append(pc)
        i += 1
    if index_piece_found == -1:
        raise IndexError
    standard_set = 1

    if pop_left:
        standard_set += int(file_keeper[index_piece_found-1])
        file_keeper.pop(index_piece_found-1)
        index_piece_found -= 1
    if index_piece_found != len(rank) and file_keeper[index_piece_found+1].isdigit():
        standard_set += int(file_keeper[index_piece_found+1])
        file_keeper.pop(index_piece_found+1)    
    file_keeper[index_piece_found] = str(standard_set)
    new_file = ''.join(file_keeper)
    return piece_found, new_file

@staticmethod
def algebraParser(algebra_notation:str):
    _splt = algebra_notation.split(SEPERATOR)
    moved_piece = _splt[0]
    new_square = _splt[1]

    return moved_piece, new_square

def board_to_fen(fen, piece, square, ):
    splt = fen[0].split('/')
    delete_square = delete_piece_from_FEN(splt[square[Y]-1], square[X])
    added_file = add_piece_to_fen(piece.fen_char, splt[square[piece.position[Y]-1]], piece.position[X])
    splt[square[Y]-1] = delete_square
    splt[piece.position[Y]-1] = added_file
    rejoined = '/'.join(splt)
    fen[0] = rejoined   
    return rejoined





    
