from stockfish import Stockfish
from Interface import Interface
from constants import STOCKFISH_PATH


interface = Interface()


def main():
    level = interface.get_level()
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
            "Skill Level": level,
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
        },
    )
    interface.start_game(stockfish, color)


if __name__ == "__main__":
    main()
