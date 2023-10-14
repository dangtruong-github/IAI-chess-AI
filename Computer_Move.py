import chess
import chess.polyglot
import timeit
import random

from heuristic import *
from TranspositionTable import *

#KILLER MOVE & HISTORY HEURISTIC
killer_move = [[0, 0] for i in range(10)] # killer_move[0/1][ply]
history_move = [[[0 for i in range(64)] for j in range(2)] for k in range(7)]
move = []

#MVV-LVA TABLE
MVV_LVA = [
    [0, 0 , 0 , 0 , 0 , 0 , 0 ],    # victim None, attacker None, P, N, B, R, Q, K
    [0, 150, 140, 130, 120, 110, 100],    # victim P, attacker None, P, N, B, R, Q, K
    [0, 250, 240, 230, 220, 210, 200],    # victim N, attacker None, P, N, B, R, Q, K
    [0, 350, 340, 330, 320, 310, 300],    # victim B, attacker None, P, N, B, R, Q, K
    [0, 450, 440, 430, 420, 410, 400],    # victim R, attacker None, P, N, B, R, Q, K
    [0, 550, 540, 530, 520, 510, 500],    # victim Q, attacker None, P, N, B, R, Q, K
    [0, 0 , 0 , 0 , 0 , 0 , 0 ],    # victim K, attacker None, P, N, B, R, Q, K
]

def move_ordering(board: chess.Board, move: chess.Move, depth):
    move_score = 0
    to_square = move.to_square
    from_square = move.from_square  

    if board.is_capture(move):
        move_score += 10000 
        if board.is_en_passant(move):
            victim = 1
        else:
            victim = board.piece_at(to_square).piece_type
        attacker = board.piece_at(from_square).piece_type
        move_score += MVV_LVA[victim][attacker]

    else:
        if move == killer_move[depth][0]:
            move_score += 9000
        elif move == killer_move[depth][1]:
            move_score += 8000
        else:
            from_piece = board.piece_at(from_square)
            pieceF = from_piece.piece_type
            colorF = from_piece.color
            move_score += 5000 + history_move[pieceF][colorF][to_square]

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
        new_key = new_key ^ zobrist_keys[pieceF][colorF][from_square] ^ zobrist_keys[pieceF][colorF][to_square]
        if to_piece is not None:
            pieceT = to_piece.piece_type
            colorT = to_piece.color
            new_key ^= zobrist_keys[pieceT][colorT][to_square]

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
        new_key ^= zobrist_keys[pieceF][colorF][to_square] # xor out the pawn
        new_key ^= zobrist_keys[move.promotion][colorF][to_square] # xor in the promotion piece

    return new_key

def next_move(board: chess.Board):
    return list(board.legal_moves)

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
    
    # Reach leaf node
    if depth == 0 or board.outcome() != None:
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
    moves.sort(key = lambda move: move_ordering(board, move, depth), reverse = True)

    for move in moves:
        new_key = update_key(board, move, key)
        board.push(move)
        eval = -negamax(board, depth - 1, -beta, -alpha, -turn, True, new_key)
        board.pop()

        max_eval = max(max_eval, eval)
        if max_eval > alpha:
            alpha = max_eval
            # add point to history move
            if not board.is_capture(move):
                from_square, to_square = move.from_square, move.to_square
                from_piece = board.piece_at(from_square)
                piece = from_piece.piece_type
                color = from_piece.color
                history_move[piece][color][to_square] += depth * depth

        if alpha >= beta:
            # save killer move that cut off beta
            if not board.is_capture(move):
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

def get_best_move(board: chess.Board, depth):
    start = timeit.default_timer()
    # Looking for opening move
    best_move = None
    with chess.polyglot.open_reader("data/opening_book.bin") as reader:
        root = list(reader.find_all(board))
        if len(root) != 0:
            op_move = root[0]
            best_move = op_move.move
            return best_move, "opening"
        
    # Not in opening theory
    current_key = 0 # Initialize a key for Zobrist hash
    for square, piece in board.piece_map().items():
        current_key ^= zobrist_keys[piece.piece_type][piece.color][square]
    if not board.turn: 
        current_key ^= black_hash

    print("\n\nThinking...")
    legal_moves = list(board.legal_moves)
    moves = legal_moves
    moves.sort(key = lambda move: move_ordering(board, move, depth), reverse = True)
    best_eval = -1000000
    alpha = -1000000
    beta = 1000000
    for move in moves:   
        new_key = update_key(board, move, current_key)
        board.push(move)
        eval = -negamax(board, depth - 1, -beta, -alpha, 1 if board.turn else -1, True, new_key)
        if(eval > best_eval):
            best_eval = eval
            best_move = move
            print("\nmove: ", best_move, "\neval: ", eval)
        board.pop()
        alpha = max(alpha, best_eval)
    end = timeit.default_timer()
    print("\nruntime: ", round(end - start, 2), "\bs")
    return best_move, best_eval

# board = chess.Board("rn1qnrk1/pppbppbp/6p1/4p3/2PP4/2N1BP2/PP2Q1PP/R3KBNR w KQ - 0 9")

# start = timeit.default_timer()
# print(get_best_move(board, 6))
# end = timeit.default_timer()
# print("time: ", end - start)