from stockfish import Stockfish
from Interface import Interface
from constants import STOCKFISH_PATH
from Movements import Movements
from Communication import Communication


interface = Interface()
movements = Movements()
communication = Communication()


def main():
    communication.send_message("Calibrando Motor...")
    movements.calibra()
    communication.send_message("Motor calibrado!")
    level = 1
    stockfish = Stockfish(
        STOCKFISH_PATH,
        depth=level,
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
            "Minimum Thinking Time": level * 1.5,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
        },
    )
    interface.start_game(stockfish)


if __name__ == "__main__":
    main()
