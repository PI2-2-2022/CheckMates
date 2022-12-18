from stockfish import Stockfish

stockfish = Stockfish(path="./stockfish_15/stockfish-ubuntu-20.04-x86-64")

class Game:
    def __init__(self):
        stockfish.get_board_visual()
        # stockfish.set_position(["e2e4", "e7e6"])
        # stockfish.make_moves_from_current_position(["g4d7", "a8b8", "f1d1"])
        # stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
        # stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -") # will return False, in this case because the FEN is missing two of the six required fields.
        # stockfish.get_best_move()
        # stockfish.get_best_move_time(1000)
        # stockfish.is_move_correct('a2a3')
        # stockfish.get_top_moves(3)
        # stockfish.get_board_visual()
        # stockfish.send_quit_command()

    def getStatus(self):
        print(stockfish.get_board_visual())

    def getBestMove(self):
        print(stockfish.get_best_move_time(1000))

game = Game()
game.getStatus()
game.getBestMove()
