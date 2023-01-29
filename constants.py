import os
from dotenv import load_dotenv

load_dotenv()

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FILLED_ROW = [1, 1, 1, 1, 1, 1, 1, 1]
EMPTY_ROW = [0, 0, 0, 0, 0, 0, 0, 0]
INITIAL_BOARD_BIT = [
    FILLED_ROW,
    FILLED_ROW,
    EMPTY_ROW,
    EMPTY_ROW,
    EMPTY_ROW,
    EMPTY_ROW,
    FILLED_ROW,
    FILLED_ROW,
]