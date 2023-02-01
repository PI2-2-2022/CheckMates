import chess
from Communication import Communication


class Validation:
    # Classe responsável por administrar as regras e violações do jogo

    def __init__(self) -> None:
        pass

    def is_game_over_or_drawn(self, currentFen: str) -> bool:
        board = chess.Board(currentFen)

        if board.is_checkmate():
            # print(
            #                 "Checkmate, Jogador 1 ganhou"
            #                 if chess.Board(currentFen).turn == "w"
            #                 else "Checkmate, Jogador 2 ganhou"
            #             )
            #             break
            message = "Check Mate!"
        if board.is_stalemate():
            message = "Stale Mate!"
        if board.is_insufficient_material():
            message = "Peças insuficientes!"

        if (
            board.is_checkmate()
            or board.is_stalemate()
            or board.is_insufficient_material()
        ):
            Communication.send_message(message)
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
