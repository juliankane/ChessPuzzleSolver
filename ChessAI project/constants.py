import numpy as np

# Chess pieces
KING = 'King'
QUEEN = 'Queen'
ROOK = 'Rook'
BISHOP = 'Bishop'
KNIGHT = 'Knight'
PAWN = 'Pawn'
VALUE = {PAWN: 1, KNIGHT: 3, BISHOP: 3, ROOK: 5, QUEEN: 8}

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['8', '7', '6', '5', '4', '3', '2', '1']
RANKS = [8,7,6,5,4,3,2,1]
FILES = [1,2,3,4,5,6,7,8]
FILES_MAP_NUM_TO_CHAR = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
FILES_MAP_CHAR_TO_NUM = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g':7, 'h': 8}

X,Y = 0,1
N, NE, E, SE, S, SW, W, NW = "NORTH", "NORTHEAST", "EAST", "SOUTHEAST", "SOUTH", "SOUTHWEST", "WEST", "NORTHWEST"

MOVEMENT = {
    N: (0, 1),    
    NE: (1, 1),   
    E: (1, 0),    
    SE: (1, -1),  
    S: (0, -1),   
    SW: (-1, -1), 
    W: (-1, 0),   
    NW: (-1, 1)   
}

WHITE = {
    "PIECES":{
        'P' : PAWN,
        'N' : KNIGHT,
        'B' : BISHOP,
        'R' : ROOK,
        'Q' : QUEEN,
        'K' : KING
    },

    "TO_MOVE": "w",

    "CASTLING": {
        "K": "KINGSIDE",
        "Q": "QUEENSIDE",
    }
}

BLACK = {
    "PIECES":{
    'p' : PAWN,
    'n' : KNIGHT,
    'b' : BISHOP,
    'r' : ROOK,
    'q' : QUEEN,
    'k' : KING,
    },
    "TO_MOVE": "b",
    "CASTLING": {
        "k": "KINGSIDE",
        "q": "QUEENSIDE",
    }
}




