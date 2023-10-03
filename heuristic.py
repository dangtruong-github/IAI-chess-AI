import chess

MATERIAL_POINT = (0, 1, 3, 3, 5, 9, 10000)
MATE_SCORE = 1000000
SQUARE_VALUE = {chess.A8: 0, chess.B8: 0, chess.C8: 0, chess.D8: 0, chess.E8: 0, chess.F8: 0, chess.G8: 0, chess.H8: 0,
                chess.A7: 0, chess.B7: 1, chess.C7: 1, chess.D7: 1, chess.E7: 1, chess.F7: 1, chess.G7: 1, chess.H7: 0,
                chess.A6: 0, chess.B6: 1, chess.C6: 2, chess.D6: 2, chess.E6: 2, chess.F6: 2, chess.G6: 1, chess.H6: 0,
                chess.A5: 0, chess.B5: 1, chess.C5: 2, chess.D5: 4, chess.E5: 4, chess.F5: 2, chess.G5: 1, chess.H5: 0,
                chess.A4: 0, chess.B4: 1, chess.C4: 2, chess.D4: 4, chess.E4: 4, chess.F4: 2, chess.G4: 1, chess.H4: 0,
                chess.A3: 0, chess.B3: 1, chess.C3: 2, chess.D3: 2, chess.E3: 2, chess.F3: 2, chess.G3: 1, chess.H3: 0,
                chess.A2: 0, chess.B2: 1, chess.C2: 1, chess.D2: 1, chess.E2: 1, chess.F2: 1, chess.G2: 1, chess.H2: 0,
                chess.A1: 0, chess.B1: 0, chess.C1: 0, chess.D1: 0, chess.E1: 0, chess.F1: 0, chess.G1: 0, chess.H1: 0,}

def score(board: chess.Board):
    value = 0
    if(board.is_checkmate()):
        value += MATE_SCORE * (-1 if board.turn else 1)
    value += mat_diff(board) * 100

    """
    value += midctrl_diff(board)
    board.push(chess.Move.null())
    value -= midctrl_diff(board)
    board.pop()
    value += mobility(board)
    """

    return value

def mat_diff(board: chess.Board):
    material_difference = 0
    for piece in board.piece_map():
        material_difference += MATERIAL_POINT[board.piece_type_at(piece)] * (1 if board.piece_at(piece).color else -1)
    return material_difference

def midctrl_diff(board: chess.Board):
    legal = list(board.legal_moves)
    controlled_diff = 0
    pawn_pos = []
    for move in legal:
        piece = board.piece_type_at(move.from_square)
        if (piece != 1):
            controlled_diff += SQUARE_VALUE[move.to_square]
        else:
            if move.from_square not in pawn_pos:
                pawn_pos.append(move.from_square)
    pawn_color = board.turn
    if pawn_color == chess.WHITE:
        for pawn in pawn_pos:
            if (pawn % 8 == 0) or (pawn % 8 == 7):
                controlled_diff += 1
            else:
                controlled_diff += SQUARE_VALUE[pawn + 7]
                controlled_diff += SQUARE_VALUE[pawn + 9]
    elif pawn_color == chess.BLACK:
        for pawn in pawn_pos:
            if (pawn % 8 == 0) or (pawn % 8 == 7):
                controlled_diff += 1
            else:
                controlled_diff += SQUARE_VALUE[pawn - 7]
                controlled_diff += SQUARE_VALUE[pawn - 9]
    return controlled_diff

def mobility(board: chess.Board):
    return len(list(board.legal_moves))
