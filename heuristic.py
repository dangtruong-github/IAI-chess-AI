import chess

MATERIAL_POINT = (0, 1, 3, 3, 5, 9, 1000)
MATE_SCORE = 1000

def score(board: chess.Board):
    value = 0
    if(board.is_checkmate()):
        value += MATE_SCORE * (-1 if board.turn else 1)
    value += mat_diff(board)
    return value

def mat_diff(board: chess.Board):
    material_difference = 0
    for piece in board.piece_map():
        material_difference += MATERIAL_POINT[board.piece_type_at(piece)] * (1 if board.piece_at(piece).color else -1)
    return material_difference