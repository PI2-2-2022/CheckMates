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

    def is_game_over_or_drawn(self, currentFen: str) -> bool:
        board = chess.Board(currentFen)
        if board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material():
            return True
        else:
            return False

    def is_stalemate(self, currentFen: str) -> bool:
        board = chess.Board(currentFen)
        return board.is_stalemate()

    def is_insufficient_material(self, currentFen: str) -> bool:
        board = chess.Board(currentFen)
        return board.is_insufficient_material()

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
