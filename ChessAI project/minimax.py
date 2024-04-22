from MoveCalculator import *
CHECKMATE = 9999999

def iterative_deepening_minimax(board, max_depth):
    best_move = None
    best_eval = float('-inf')

    for depth in range(1, max_depth + 1):
        current_move, current_eval = minimax(board, float('-inf'),  float('inf'), depth=depth, maximize=True)

        if current_eval > best_eval:
            best_eval = current_eval
            best_move = current_move

        if current_eval == CHECKMATE:
            break

    return best_move, best_eval


def minimax(board, alpha = float('-inf'), beta = float('inf'), depth = 3, maximize = True):

    if depth == 0:
        moves, eval = board.evaluate(maximize)
        # if not board.output:
        #     print(moves)
        return moves, eval
    
    if maximize:
        max_eval = float('-inf')
        best_move = None
        for move in board.get_legal_moves():

            board.push_move(move)
            moves, eval = minimax(board, alpha, beta, depth-1, maximize = False)
            board.undo_move()

            if eval > max_eval:
                max_eval = eval
                best_move = moves

            if eval == CHECKMATE:
                break
            
            alpha = max(alpha, eval)
            if beta <= alpha: 
                break 

        return best_move, max_eval
    
    else:

        min_eval = float('inf')
        best_move = None

        for move in board.get_legal_moves():
            board.push_move(move)
            moves, eval = minimax(board, alpha, beta, depth-1, maximize=True)
            board.undo_move()

            if eval < min_eval:
                min_eval = eval
                best_move = moves

            beta = min(beta, eval)
            if eval == CHECKMATE:
                break

            if beta <= alpha: 
                break

        return best_move, min_eval
        


def alternate_iterative_deepening_minimax(board, max_depth):
    initial = max_depth
    best_move = None
    best_eval = float('-inf') if initial % 2 == 1 else float('inf')

    for depth in range(1, max_depth + 1):
        maximize = True if depth % 2 == 1 else False
        current_move, current_eval = minimax(board, float('-inf'),  float('inf'), depth=depth, maximize=True)


        if current_eval > best_eval:
            best_eval = current_eval
            best_move = current_move

        if current_eval == CHECKMATE:
            break

    return best_move, best_eval
