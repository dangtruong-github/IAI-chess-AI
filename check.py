import chess

board = chess.Board()
# Create a chess board
board = chess.Board()

# Specify the square you want to extract the piece from (in this case, g1)
square = chess.parse_square('g1')

# Extract the piece from the specified square
piece = board.piece_at(square)

# Check if there is a piece on the square
if piece is not None:
    print(f"Piece on square g1: {piece}")
else:
    print("No piece on square g1")