import chess
import timeit

from heuristic import *

def next_move(board: chess.Board):
    legal_moves = list(board.legal_moves)
    return legal_moves

def negamax(board: chess.Board, depth, alpha, beta, turn, do_null):
    if depth == 0 or board.outcome() != None:
        return turn * score(board)
    
    # if board.is_check():
    #     depth += 1

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
        print(move, eval)
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

start = timeit.default_timer()
print(get_best_move(board, 6))
end = timeit.default_timer()
print("time: ", end - start)
