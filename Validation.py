import chess
from Communication import Communication

communication = Communication()


class Validation:
    # Classe responsável por administrar as regras e violações do jogo

    def __init__(self) -> None:
        pass

    def validate_game_status(self, currentFen: str) -> bool:
        board = chess.Board(currentFen)
        message = None

        if board.is_check():
            message = (
                "Você está em Check!"
                if chess.Board(currentFen).turn == "b"
                else "Inteligência Artificial em Check!"
            )
        elif board.is_checkmate():
            message = (
                "Checkmate, você ganhou"
                if chess.Board(currentFen).turn == "b"
                else "Checkmate, Inteligência Artificial ganhou"
            )
        elif board.is_stalemate():
            message = "Stale Mate! Empatou..."
        elif board.is_insufficient_material():
            message = "Peças insuficientes! Empatou..."

        if message:
            communication.send_message(message)

        return (
            board.is_checkmate()
            or board.is_stalemate()
            or board.is_insufficient_material()
        )

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
