import chess
import chess.svg
from pathlib import Path


class Board:

    def __init__(self):
        pass
    
    def get_new_board(self):
    # TODO implementar método que vai gerar um novo tabuleiro no ínicio de um novo jogo
        return 10
        

    def update_board(self, currentFen):
        board = chess.Board(fen=currentFen)
        with open(Path(__file__).parent.joinpath("game.svg"), mode="w") as img:
            img.write(chess.svg.board(board, size=350))
  