import chess
import chess.polyglot
import timeit
import numpy as np
import random
import time

from heuristic import *
from TranspositionTable import *

#KILLER MOVE & HISTORY HEURISTIC
killer_move = np.zeros((20, 2), dtype=chess.Move)  # killer_move[0/1][ply]
history_move = np.zeros((7, 2, 64), dtype=int)

#MVV-LVA TABLE
MVV_LVA = np.array([
    [0,  0,  0,  0,  0,  0,  0],    # victim None,  attacker None, P, N, B, R, Q, K
    [0, 15, 14, 13, 12, 11, 10],    # victim P,     attacker None, P, N, B, R, Q, K
    [0, 25, 24, 23, 22, 21, 20],    # victim N,     attacker None, P, N, B, R, Q, K
    [0, 35, 34, 33, 32, 31, 30],    # victim B,     attacker None, P, N, B, R, Q, K
    [0, 45, 44, 43, 42, 41, 40],    # victim R,     attacker None, P, N, B, R, Q, K
    [0, 55, 54, 53, 52, 51, 50],    # victim Q,     attacker None, P, N, B, R, Q, K
    [0,  0,  0,  0,  0,  0,  0],    # victim K,     attacker None, P, N, B, R, Q, K
])
MVV_LVA_OFFSET = 1000000

def move_ordering(board: chess.Board, move: chess.Move, tt_move: chess.Move, depth):
    if move == tt_move:
        return 2000000
    move_score = 0
    to_square = move.to_square
    from_square = move.from_square  
    
    if board.is_capture(move):
        move_score += MVV_LVA_OFFSET 
        if board.is_en_passant(move):
            victim = 1
        else:
            victim = board.piece_at(to_square).piece_type
        attacker = board.piece_at(from_square).piece_type
        move_score += MVV_LVA[victim][attacker]

    else:
        if move == killer_move[depth][0]:
            move_score = MVV_LVA_OFFSET - 100
        elif move == killer_move[depth][1]:
            move_score = MVV_LVA_OFFSET - 200
        else:
            from_piece = board.piece_at(from_square)
            pieceF = from_piece.piece_type
            colorF = from_piece.color
            move_score += history_move[pieceF][int(colorF)][to_square]

    return move_score
    
#Transposition Table Consts
EXACT = 0
LOWER = 1
UPPER = 2

zobrist_keys = [[[random.getrandbits(64) for i in range(64)] for j in range(2)] for k in range(7)]


black_hash = random.getrandbits(64)
transposition_table = TranspositionTable()

def update_key(board: chess.Board, move: chess.Move, cur_key):
    new_key = cur_key ^ black_hash
    from_square, to_square = move.from_square, move.to_square
    from_piece = board.piece_at(from_square)
    to_piece = board.piece_at(to_square)

    if from_piece is not None:
        pieceF = from_piece.piece_type
        colorF = from_piece.color
        new_key = new_key ^ zobrist_keys[pieceF][int(colorF)][from_square] ^ zobrist_keys[pieceF][int(colorF)][to_square]
        if to_piece is not None:
            pieceT = to_piece.piece_type
            colorT = to_piece.color
            new_key ^= zobrist_keys[pieceT][int(colorT)][to_square]

    if board.is_castling(move):
        # Also xor in the rook
        if board.turn:
            if board.is_queenside_castling(move):
                new_key = new_key ^ zobrist_keys[4][1][0] ^ zobrist_keys[4][1][3]
            elif board.is_kingside_castling(move):
                new_key = new_key ^ zobrist_keys[4][1][7] ^ zobrist_keys[4][1][5]
        else:
            if board.is_queenside_castling(move):
                new_key = new_key ^ zobrist_keys[4][0][56] ^ zobrist_keys[4][0][59]
            elif board.is_kingside_castling(move):
                new_key = new_key ^ zobrist_keys[4][0][63] ^ zobrist_keys[4][0][61]

    elif board.is_en_passant(move):
        if board.turn:
            if to_square - from_square == 9:
                new_key ^= zobrist_keys[1][0][from_square + 1]
            elif to_square - from_square == 7:
                new_key ^= zobrist_keys[1][0][from_square - 1]
        else:
            if from_square - to_square == 9:
                new_key ^= zobrist_keys[1][1][from_square - 1]
            elif from_square - to_square == 7:
                new_key ^= zobrist_keys[1][1][from_square + 1]
                
    elif move.promotion is not None:
        pieceF = from_piece.piece_type
        colorF = from_piece.color
        new_key ^= zobrist_keys[pieceF][int(colorF)][to_square] # xor out the pawn
        new_key ^= zobrist_keys[move.promotion][int(colorF)][to_square] # xor in the promotion piece

    return new_key

def next_move(board: chess.Board):
    return list(board.legal_moves)

def qsearch(board: chess.Board, alpha, beta, turn, depth):
    stand_pat = turn * score(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    if depth == 0: return stand_pat
    moves = next_move(board)
    for move in moves:
        if board.is_capture(move):
            board.push(move)
            eval = -qsearch(board, -beta, -alpha, -turn, depth - 1)
            board.pop()
            if eval >= beta:
                return beta
            if eval > alpha:
                alpha = eval
    return alpha

def negamax(board: chess.Board, depth, alpha, beta, turn, do_null, key):
    og_alpha = alpha # Store original alpha value

    # Look up for state saved in transposition table
    cur_entry = transposition_table.lookup(key)
    if cur_entry is not None and cur_entry.depth >= depth:
        if cur_entry.flag == EXACT:
            return cur_entry.score
        elif cur_entry.flag == LOWER:
            alpha = max(alpha, cur_entry.score)
        elif cur_entry.flag == UPPER:
            beta = min(beta, cur_entry.score)
        
        if alpha >= beta:
            return cur_entry.score
        
    # Reach terminate node
    if board.outcome() != None:
        return turn * score(board)
    
    # Reach leaf node
    if depth == 0:
        if not board.is_check():
            return qsearch(board, alpha, beta, turn, 6)
        return turn * score(board)

    # Null-Move pruning
    if do_null and not board.is_check() and depth >= 3:
        new_key = update_key(board, chess.Move.null(), key)
        board.push(chess.Move.null())
        null_score = -negamax(board, depth - 3, -beta, -beta + 1, -turn, False, new_key)
        board.pop()
        if null_score >= beta:
            return beta

    # Normal alpha beta pruning
    max_eval = -1000000
    best_move =  None

    moves = next_move(board)
    moves.sort(key = lambda move: move_ordering(board, move, None, depth), reverse = True)

    for move in moves:
        new_key = update_key(board, move, key)
        board.push(move)
        eval = -negamax(board, depth - 1, -beta, -alpha, -turn, True, new_key)
        board.pop()

        if max_eval < eval:
            max_eval = eval
            best_move = move

        if max_eval > alpha:
            alpha = max_eval
            # add point to history move
            if not board.is_capture(move):
                from_square, to_square = move.from_square, move.to_square
                from_piece = board.piece_at(from_square)
                piece = from_piece.piece_type
                color = from_piece.color
                history_move[piece][int(color)][to_square] += depth * depth

        if alpha >= beta:
            # save killer move that cut off beta
            if not board.is_capture(move) and move != killer_move[depth][0]:
                killer_move[depth][1] = killer_move[depth][0]
                killer_move[depth][0] = move
            break
    
    if max_eval <= og_alpha:
        tt_flag = UPPER
    elif max_eval >= beta:
        tt_flag = LOWER
    else:
        tt_flag = EXACT
    new_entry = Entry(key, depth, max_eval, tt_flag, best_move)
    transposition_table.store(new_entry)

    return max_eval

# Constant for limit runtime
THINKING_TIME = 15
MOVE_TIME = 60

def get_best_move(board: chess.Board, depth):
    print("\n\nThinking...")
    start = timeit.default_timer()

    # Looking for opening move
    best_move = None
    with chess.polyglot.open_reader("data/final-book.bin") as reader:
        root = list(reader.find_all(board))
        if len(root) != 0:
            op_move = root[0]
            best_move = op_move.move
            time.sleep(1)
            return best_move, "opening"
        
    # Not in opening theory
    current_key = 0 # Initialize a key for Zobrist hash
    for square, piece in board.piece_map().items():
        current_key ^= zobrist_keys[piece.piece_type][int(piece.color)][square]
    if not board.turn: 
        current_key ^= black_hash

    ids_start = timeit.default_timer()
    runtime = 0
    cur_depth = 1
    # search until reach max depth or time limit
    while runtime < THINKING_TIME and cur_depth <= depth:
        print("\ndepth: ", cur_depth + 1)
        legal_moves = list(board.legal_moves)
        moves = legal_moves
        moves.sort(key = lambda move: move_ordering(board, move, best_move, cur_depth), reverse = True)

        best_eval = -1000000
        alpha = -1000000
        beta = 1000000

        for move in moves:   
            new_key = update_key(board, move, current_key)
            board.push(move)
            eval = -negamax(board, cur_depth, -beta, -alpha, 1 if board.turn else -1, True, new_key)
            if eval > best_eval:
                best_eval = eval
                best_move = move
                print("\nmove: ", best_move, "\neval: ", eval, "\ndepth: ", cur_depth + 1)
            board.pop()
            alpha = max(alpha, best_eval)
            runtime = timeit.default_timer() - ids_start
            if runtime > MOVE_TIME:
                break
        
        if eval == MATE_SCORE: 
            break
        cur_depth += 1

    end = timeit.default_timer()
    print("\nruntime: ", round(end - start, 2), "\bs")
    return best_move, best_eval

# Test area

board = chess.Board("1Q1Q4/8/k7/4p1p1/5pP1/5K2/8/8 w - - 0 49")
start = timeit.default_timer()
print(get_best_move(board, 6))
end = timeit.default_timer()
print("time: ", end - start)
