import os
from dotenv import load_dotenv

load_dotenv()

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FILLED_BIT_ROW = [1, 1, 1, 1, 1, 1, 1, 1]
EMPTY_BIT_ROW = [0, 0, 0, 0, 0, 0, 0, 0]
INITIAL_BIT_BOARD = [
    FILLED_BIT_ROW,
    FILLED_BIT_ROW,
    EMPTY_BIT_ROW,
    EMPTY_BIT_ROW,
    EMPTY_BIT_ROW,
    EMPTY_BIT_ROW,
    FILLED_BIT_ROW,
    FILLED_BIT_ROW,
]
INITIAL_BOARD = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
]
WHITE_PIECES = ["R", "N", "B", "Q", "K", "B", "N", "R", "P"]
BLACK_PIECES = ["r", "n", "b", "q", "k", "b", "n", "r", "p"]

# TODO pegar as coordenadas exatas da zona morta das peças brancas e das peças pretas
ZONA_MORTA_WHITE = [[10, 30], [20, 30]]
ZONA_MORTA_BLACK = [[10, 30], [20, 30]]
