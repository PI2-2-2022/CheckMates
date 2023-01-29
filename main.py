from stockfish import Stockfish
from Board import Board
from Interface import Interface
from constants import STARTING_FEN, INITIAL_BOARD_BIT, STOCKFISH_PATH


interface = Interface()
board = Board()


def main():
    color = interface.get_color()
    stockfish = Stockfish(
        STOCKFISH_PATH,
        depth=20,
        parameters={
            "Debug Log File": "",
            "Contempt": 0,
            "Min Split Depth": 0,
            # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
            "Threads": 1,
            "Ponder": "false",
            # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
            "Hash": 512,
            "MultiPV": 1,
            "Skill Level": interface.get_level(),
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
        },
    )
    board.update_board(STARTING_FEN)
    interface.start_game(stockfish, STARTING_FEN, INITIAL_BOARD_BIT, color)


if __name__ == "__main__":
    main()
