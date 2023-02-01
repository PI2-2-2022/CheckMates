import chess
import chess.svg
from pathlib import Path
from constants import INITIAL_BOARD_BIT


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

    def get_move(self, targetBitBoard, currentBitBoard):
        to = None
        origin = None
        for idx, x in enumerate(targetBitBoard):
            for idy, y in enumerate(x):
                row = 8 - idx
                column = chr(idy + 97)
                if targetBitBoard[idx][idy] == 0 and currentBitBoard[idx][idy] == 1:
                    origin = f"{column}{row}"
                elif targetBitBoard[idx][idy] == 1 and currentBitBoard[idx][idy] == 0:
                    to = f"{column}{row}"

        return f"{origin}{to}"

    def transform_raw_board(self, raw):
        bitBoard = []
        for item in raw:
            row = [1 if x == '0' else 0 for x in item[1:-1]]
            if len(row) == 8: bitBoard.append(row)
        return bitBoard

    def is_initial_board(self, bitBoard) -> bool:
        return bitBoard == INITIAL_BOARD_BIT

    def print_list_of_lists(self, lst_of_lsts):
        print('\n\n')
        for lst in lst_of_lsts:
            print(lst)

    def is_zona_morta(self, move):
        # TODO verificar se o destino do movimento (e2z1 -> segunda parte do movimento) está na zona morta
        return False