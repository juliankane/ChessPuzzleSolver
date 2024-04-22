
from constants import *
from Piece import Piece
from constants import KING

@staticmethod
def legal_moves(board):
    _legal_moves_= None

    open_squares = board.getOpenSquares() 
    pieces = board.getPieces()

    attacking = pieces[board.current]
    defending = pieces[1-board.current]

    att_squars = open_squares[board.current]
    dff_squars = open_squares[1-board.current]
    
    if board.state.is_checked:
        _legal_moves_ = checked_legal_moves(board, attacking, defending, attacking_squares=att_squars, defending_squares=dff_squars)
        _sorted_moves = move_eval(_legal_moves_)
    else:
        _legal_moves_ = get_moves(attacking, defending, att_squars, dff_squars, board)
        _sorted_moves = move_eval(_legal_moves_)
        
    return _sorted_moves

@staticmethod
def get_moves(attackers:Piece, defenders:Piece, open_attacking, open_defending, board, no_king = False, **kwargs):

    Moves = {}  
    dff_king = None
    for piece in defenders:
        if piece.name == KING:
            dff_king = piece
            break

    for square in open_attacking:
        Moves[square] = {"Attackers":[], "Defenders": []}
        if no_king:
            attacking_square = [piece for piece in attackers if piece.can_reach_square(square, attackers, defenders) and piece.name != KING] 
        else:
            attacking_square = [piece for piece in attackers if piece.can_reach_square(square, attackers, defenders)] 
        defending_square = [piece for piece in defenders if piece.can_reach_square(square, attackers, defenders)]

        king_is_defender = any(piece.name == KING for piece in defending_square)
        for piece in attacking_square: 
            if (king_is_defender and piece.name == KING):
                continue

            if square != dff_king.position and piece.can_reach_square(dff_king.position, att=attackers, dff=defenders, frm=square):
                Moves[square]["Attackers"].append({"piece": piece, "check_multiplier": 100}) 
            else:
                Moves[square]["Attackers"].append({"piece": piece, "check_multiplier": 0}) 

        for piece in defending_square:
            Moves[square]["Defenders"].append({"piece": piece})
            if piece.position == square and piece.name != KING:
                for a in attacking_square:
                    if not board.state.is_checked:
                        Moves[square]["multiplier"] = 80       
                    else:
                        Moves[square]["multiplier"] = 150

    return Moves


@staticmethod
def move_eval(Legal, **kwargs):
    move_order = []
    for square, props in Legal.items(): 
        sqr_attacks = props["Attackers"] 
        sqr_defense = props["Defenders"]
        square_multiplier = props.get("multiplier", 0)

        sqr_bonus = 0
        num_attackers = len(sqr_attacks)
        att_cost = sum(attacker_details["piece"].value for attacker_details in sqr_attacks)

        num_defenders = len(sqr_defense)
        dff_cost = sum(defender_details["piece"].value for defender_details in sqr_defense)

        if num_attackers <= num_defenders:
            sqr_bonus -=10
        else:
            sqr_bonus += 10
        for attacker_details in sqr_attacks:

            piece = attacker_details["piece"]
            positional_multiplier = attacker_details.get("positional_multiplier",0)
            sqr_bonus += attacker_details["check_multiplier"] + positional_multiplier
            net_value = (square_multiplier + att_cost + sqr_bonus) - dff_cost

            if attacker_details["check_multiplier"] != 0:
                move_order.append({"piece":piece, "moved_to": square, "value": net_value, "check": True})
            else:
                move_order.append({"piece":piece, "moved_to": square, "value": net_value, "check":False})
                
    sorted_moves = sorted(move_order, key=lambda x:x['value'], reverse=True)
    return sorted_moves




@staticmethod
def checked_legal_moves(board, attacking, defending, attacking_squares, defending_squares):
    def get_kings_moves(king, squares, defenders, moves = {}):
        for square in squares:
            moves[square] = {"Attackers": [], "Defenders": []}
            moves[square]["Attackers"].append({"piece": king, "check_multiplier": 0, "positional_multliplier": 50})
            if any(p.position == square for p in defenders):
                mult = moves[square].get("multiplier",0)    
        return moves
    king = None
    checking_piece = []
    for piece in attacking:
        if piece.name == KING:
            king = piece
            break

    for piece in defending:
        if piece.can_reach_square(king.position, att=defending, dff=attacking, to_move = False):
            checking_piece.append(piece)

    legal_moves = {}
    if len(checking_piece) == 1:
        legal_squares = checking_piece[0].steps_to_square(king.position)
        legal_squares.append(checking_piece[0].position)
        legal_moves = get_moves(attacking, defending, legal_squares, defending_squares, board, no_king = True)

    kings_squares =  king.kings_adjacent_squares(attacking_squares, attacking)                                                                    
    kings_legal = [square for square in kings_squares if not any(piece.can_reach_square(square, att = defending, dff = attacking, to_move = False, ignore_king=True) for piece in defending)] # reverse defending and attacking for this case because we're looking if the defending squares attacking the square
    final_legal = get_kings_moves(king, kings_legal, defending, legal_moves)
    return final_legal










   
