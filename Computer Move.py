import chess
import timeit

from heuristic import *

def next_move(board: chess.Board):
    legal_moves = list(board.legal_moves)
    return legal_moves

def negamax(board: chess.Board, depth, alpha, beta, turn, do_null):
    if depth == 0 or board.outcome() != None:
        return turn * score(board)
    
    if board.is_check():
        depth += 1

    if do_null and not board.is_check() and depth >= 3:
        board.push(chess.Move.null())
        null_score = -negamax(board, depth - 3, -beta, -beta + 1, -turn, False)
        board.pop()
        if null_score >= beta:
            return beta

    value = -10000
    n = next_move(board)
    for move in n:
        board.push(move)
        value = max(value, -negamax(board, depth - 1, -beta, -alpha, -turn, True))
        board.pop()
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value

def get_best_move(board: chess.Board, depth):
    legal_moves = list(board.legal_moves)
    best_move = chess.Move.null()
    best_eval = -10000
    alpha = -10000
    beta = 10000
    for move in legal_moves:
        board.push(move)
        eval = -negamax(board, depth - 1, -beta, -alpha, 1 if board.turn else -1, True)
        # print(move, eval)
        if(eval > best_eval):
            best_eval = eval
            best_move = move
        board.pop()
        alpha = max(alpha, best_eval)
    return best_move, best_eval

board = chess.Board()

# Scholar mate
# board.push_san("e4")
# board.push_san("e5")
# board.push_san("Qf3")
# board.push_san("Nc6")
# board.push_san("Bc4")

# Puzzle 1: 2-move checkmate (Queen Sac) => 3 move 

# Puzzle 2: 2-move checkmate (Rook Sac)
board = chess.Board("6k1/pp4p1/2p5/2bp4/8/P5Pb/1P3rrP/2BRRN1K b - - 0 1")

# Puzzle 3: 3-move checkmate
# board = chess.Board("3r4/pR2N3/2pkb3/5p2/8/2B5/qP3PPP/4R1K1 w - - 1 0")

start = timeit.default_timer()
print(get_best_move(board, 6))
end = timeit.default_timer()
print("time: ", end - start)
