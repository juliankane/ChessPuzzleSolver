from minimax import iterative_deepening_minimax,minimax
from Chessboard import Chessboard
import pandas as pd
import re
import logging

def logger_setup(name, log_file, level=logging.DEBUG):
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

problem_logger = logger_setup('ProblemLogger', 'problems.log')
summary_logger = logger_setup('SummarayLogger', 'stockguppy_summary.log')

zero_count, fifty_count , hundred_count , winning_count = 0,0,0,0

def solve_chess_fromcsv(mate_df, pattern = None, depth = 2):
    global zero_count, fifty_count, hundred_count, winning_count 
    w, h, f, z = 0,0,0,0
    hundred, fifty, zero = {}, {}, {}

    problems = mate_df["Problem"]
    solutions = mate_df["Solution"]
    total_points = 0

    for index, (problem, solution) in enumerate(zip(problems, solutions)):
        if '=' in solution:
            problem_logger.info(f"Skipping problem {index + 1}: {problem} with solution {solution} due to pawn promotion")
            continue
        
        problem_logger.info(f"Processing problem {index + 1}: {problem} with expected solution {solution}")

        try:
            chessboard = Chessboard(problem)
            board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=depth)

            matches = re.findall(pattern, solution)
            clean_moves = [move.rstrip('+#') for move in matches]

        except Exception as e:
            problem_logger.error(f"Something went wrong on problem {problem} line {index + 1}")
            board_solution, eval = None, None
            continue

        local_points = 0
        try :
            for move_dict in board_solution:
                generated_move = move_dict['move']
                to_square = generated_move[2:]
                if any(to_square in move for move in clean_moves):
                    local_points += 50

            if local_points == 0:
                zero[index + 1] = {"Line": index + 1}
                z += 1 ; zero_count += 1
            elif local_points == 50:
                fifty[index + 1] = {"Line": index + 1}
                f += 1 ; fifty_count += 1
            elif local_points == 100:
                hundred[index + 1] = {"Line": index + 1}
                h += 1 ; hundred_count += 1
            elif local_points == 150:
                w += 1 ; winning_count += 1

            total_points += 1
            problem_logger.info(f"Returned move : {board_solution}, Eval is: {eval}  points:  {local_points}")
            problem_logger.info(f"Expected solution was : {solution}\n\n")

        except Exception as e:
            problem_logger.error(f"Something went wrong on problem {problem} line {index + 1}")
            board_solution, eval = None, None
            continue

    summary_logger.info(f"zero count : {z} \n Zero indices \n {zero} \n\n")
    summary_logger.info(f"fifty count : {f} \n Fifty indices \n {fifty} \n\n")
    summary_logger.info(f"hundred count : {h} \n hundred indices \n {hundred}\n\n ")
    summary_logger.info(f"Winning count : {w}")
    summary_logger.info(f"Total points: {total_points}")
pattern = r'\b[a-zA-Z]+[a-h][1-8][+#]?\b'


# mate_in_2 = pd.read_csv("matein2.csv")
# solve_chess_fromcsv(mate_in_2, pattern, depth = 3)

# mate_in_3 = pd.read_csv("matein3.csv")
# solve_chess_fromcsv(mate_in_3, pattern, depth = 6)

# mate_in_4 = pd.read_csv("matein4.csv")
# solve_chess_fromcsv(mate_in_4, pattern, depth = 8)

'''
playground
'''

#print("MATE IN 2...s")
#1. Qd8+ Bxd8 2. Re8#
# chessboard = Chessboard('r1b2k1r/ppp1bppp/8/1B1Q4/5q2/2P5/PPP2PPP/R3R1K1 w - - 1 0')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=3)
# print(board_solution, eval)

# #1. Qg4+ Bxg4 2. Bf7# 
# chessboard = Chessboard('r2q1b1r/1pN1n1pp/p1n3k1/4Pb2/2BP4/8/PPP3PP/R1BQ1RK1 w - - 1 0')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=3)
# print(board_solution, eval)

# print("MATE IN 3...s")

'''
mate in 3
'''
#1. Ne7+ Qxe7 2. Qg6+ Qg7 3. Qxg7# 

# 1. Rh8+ Kxh8 2. Qh6+ Kg8 3. Rd8# 
# chessboard = Chessboard('3R4/p1r3rk/1q2P1p1/5p1p/1n6/1B5P/P2Q2P1/3R3K w - - 1 0')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=5)
# print(board_solution, eval)


# # # 1... Qf3+ 2. Kg1 Bc5+ 3. Rxc5 Re1#
# chessboard = Chessboard('4r1k1/pb4pp/1p2p3/4Pp2/1P3N2/P2Qn2P/3n1qPK/RBB1R3 b - - 0 1')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=5)
# print(board_solution, eval)



'''
mate in 4
'''

# print("MATE IN 4...s")

#1. 1... Bxb2+ 2. Qxb2 Qxb2+ 3. Rxb2 Rxc1+ 4. Rb1 Rxb1# 
# chessboard = Chessboard('6k1/1p5p/p2p1q2/3Pb3/1Q2P3/3b1BpP/PPr3P1/KRN5 b - - 0 1')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=8)
# print(board_solution, eval)


# # #2  1... Re3+ 2. fxe3 Rxe3+ 3. Kd2 Nf3+ 4. Kd1 Re1# 
# chessboard = Chessboard('1k2r3/7p/1p6/2p1r1nP/p1Pp1Np1/3K2P1/PPR2P2/2R5 b - - 0 1')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=8)
# print(board_solution, eval)


'''
Quirks
'''

# too early



#1. Rg8+ Kf7 2. Nh6 <--- a second checkmate
# chessboard = Chessboard('4rk2/2pQn2p/p4p2/1p2pN1P/4q3/2P3R1/5PPK/8 w - - 1 0')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=3)
# print(board_solution, eval)

# tooo early
# # 1. Bh7+ Nxh7 2. Qg6+ Kf8 3. Qg7# 
# chessboard = Chessboard('r3rnk1/pp6/1q3B1p/3pP2Q/8/8/PP4PP/1B3b1K w - - 1 0')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=5)
# print(board_solution, eval)

# #  1. Bxh7+ Kxh7 2. Qh5+ Kg8 3. Rxf8+ Kxf8 4. Qf7#
# chessboard = Chessboard('rn3rk1/2qp2pp/p3P3/1p1b4/3b4/3B4/PPP1Q1PP/R1B2R1K w - - 1 0')
# board_solution, eval = iterative_deepening_minimax(chessboard, max_depth=8)
# print(board_solution, eval)



