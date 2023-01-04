import os
import chess
import chess.svg
from stockfish import Stockfish
from pathlib import Path
from dotenv import load_dotenv


def update(board):
    with open(Path(__file__).parent.joinpath("game.svg"), mode="w") as img:
        img.write(chess.svg.board(board, size=350))


load_dotenv()
stockfishPath = os.getenv("STOCKFISH_PATH")

# Prompt the user to enter a level
level = input("Enter a level (1-20): ")

# Validate the user input
if level not in map(str, range(21)):
    print("Invalid level. Please enter a number between 1 and 20.")
    exit()

# Create a chess board
board = chess.Board()
update(board)

# Print the FEN string for the initial position
print(board.fen())

stockfish = Stockfish(
    stockfishPath,
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
        "Skill Level": int(level),
        "Move Overhead": 10,
        "Minimum Thinking Time": 20,
        "Slow Mover": 100,
        "UCI_Chess960": "false",
        "UCI_LimitStrength": "false",
        "UCI_Elo": 1350,
    },
)

# Loop until the game is over
while not board.is_game_over():
    # Wait for the user to make a move
    move = input("Enter your move: ")

    try:
        uciMove = chess.Move.from_uci(move)
        if uciMove not in board.legal_moves:
            raise
    except:
        print("Invalid move. Please try again.\n\n")
        continue

    # Make the move
    board.push_uci(move)
    # Print the FEN string after the move
    print(board.fen())
    update(board=board)

    # Set the position of the board in the Stockfish engine
    stockfish.set_fen_position(board.fen())

    # Tell the Stockfish engine to find the best move
    best_move = stockfish.get_best_move()

    # Make the best move
    board.push_uci(best_move)
    # Print the FEN string after the move
    print("Computer move:", end=' ')
    print(best_move)
    print(board.fen())
    update(board=board)

# Print the result of the game
result = board.result()
print(result)

# # Close the Stockfish engine
stockfish.stdin.close()
stockfish.kill()
