import chess
import timeit

POINT = (0, 1, 3, 3, 5, 9, 100)

def next_move(board: chess.Board, point, turn):
    nextMove = list(board.legal_moves)
    arr = []
    for move in nextMove:
        tmp = board.copy()
        tmp_point = point
        if board.is_capture(move) and board.piece_type_at(move.to_square) != None:
            tmp_point += turn * POINT[board.piece_type_at(move.to_square)]   
        tmp.push(move)
        arr.append([tmp, move, tmp_point])
    return arr

def alpha_beta_pruning(board, depth, alpha, beta, point, turn):
    if depth == 0 or board.outcome() != None:
        return point, None
    
    if turn == 1:
        max_eval = float('-1000')
        best_move = None
        node = next_move(board, point, turn)
        for move in node:
            eval, _ = alpha_beta_pruning(move[0], depth - 1, alpha, beta, move[2], -1)
            if eval > max_eval:
                max_eval = eval
                best_move = move[1]
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return (max_eval, best_move)
    else:
        min_eval = float('1000')
        best_move = None
        node = next_move(board, point, turn)
        for move in node:
            eval, _ = alpha_beta_pruning(move[0], depth - 1, alpha, beta, move[2], 1)
            if eval < min_eval:
                min_eval = eval
                best_move = move[1]
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return (min_eval, best_move)

board = chess.Board()
# board.push_san("e4")
# board.push_san("e5")
# board.push_san("Nc3")
# board.push_san("Nf6")
# board.push_san("f4")

start = timeit.default_timer()
heu, move = alpha_beta_pruning(board, 4, -float('inf'), float('inf'), 0, 1)
end = timeit.default_timer()
print("time: ", end - start)
print(heu, move)
