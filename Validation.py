import chess
from Communication import Communication

communication = Communication()


class Validation:
    def __init__(self):
        pass

    def validate_game_status(self, currentFen):
        board = chess.Board(currentFen)
        message = None

        if board.is_check():
            message = "Em check!"
        elif board.is_checkmate():
            if board.turn == "w":
                message = "Checkmate! Brancas ganharam."
            else:
                message = "Checkmate! Pretas ganharam."
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

    def is_valid_move(self, move, currentFen):
        board = chess.Board(currentFen)
        try:
            board.push_uci(move)
            return True
        except ValueError:
            return False
