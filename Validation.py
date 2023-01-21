from constants import STOCKFISH_PATH
from stockfish import Stockfish
import chess

class Validation:
    # Classe responsável por administrar as regras e violações do jogo

    def __init__(self) -> None:
        pass    
        
    def is_game_over(self): # VALIDATION
    # TODO verificar checkmate, empate, vitoria, etc...
        return False

    def is_checkmate(self, fen: str) -> bool:
        board = chess.Board(fen)
        return board.is_checkmate()

    def is_valid_move(self, move: str, currentFen: str) -> bool:
        board = chess.Board(currentFen)
        try:
            board.push_uci(move)
            return True
        except ValueError:
            return False
