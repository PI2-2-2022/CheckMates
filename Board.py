import chess
import chess.svg
from pathlib import Path
from constants import INITIAL_BIT_BOARD, WHITE_PIECES, BLACK_PIECES


class Board:
    def __init__(self):
        pass

    def update_SVG(self, currentFen):
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

    def move_to_coords(self, move):
        col_map = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
        row_map = {str(i): 8 - i for i in range(1, 9)}

        start_col = col_map.get(move[0], -1)
        start_row = row_map.get(move[1], -1)
        end_col = col_map.get(move[2], -1)
        end_row = row_map.get(move[3], -1)

        return [[start_row, start_col], [end_row, end_col]]

    def transform_raw_board(self, raw):
        bitBoard = []
        for item in raw:
            row = [1 if x == "0" else 0 for x in item[1:-1]]
            if len(row) == 8:
                bitBoard.append(row)
        return bitBoard

    def is_initial_board(self, bitBoard) -> bool:
        return bitBoard == INITIAL_BIT_BOARD

    def update_board(self, currentBoard, move):
        coords = self.move_to_coords(move)
        # Pega as coordenadas da origem do movimento
        originX = coords[0][0]
        originY = coords[0][1]
        # Pega as coordenadas do destino do movimento
        destinationX = coords[1][0]
        destinationY = coords[1][1]

        # Substitui a peça do destino pela da origem e coloca vazio na origem.
        piece = currentBoard[originX][originY]
        currentBoard[originX][originY] = " "
        currentBoard[destinationX][destinationY] = piece

        return currentBoard

    def print_list_of_lists(self, lst_of_lsts):
        print("\n\n")
        for lst in lst_of_lsts:
            print(lst)

    def is_move_to_eat_piece(self, move, currentBoard, currentFen):
        # TODO comer uma peça errada é um problema!
        # Verifica se a peça não tem destino, caso tenha é um movimento normal e retorna falso
        if not "None" in move:
            return False

        # Pega qual a cor das peças do usuário
        turn = currentFen[-12]

        # Pega as coordenadas da origem do movimento
        coords = self.move_to_coords(move)
        x = coords[0][0]
        y = coords[0][1]

        # Pega qual peça foi movimentada a partir daquela origem
        piece = currentBoard[x][y]
        # Verifica qual grupo de peças serão comparadas dependendo da cor do usuário.
        # Caso sejam peças que não são dele, significa que ele está colocando uma peça na zona morta.
        # Caso contrário siginifica que ele está no meio de um movimento das suas peças.
        pieces = BLACK_PIECES if turn == "w" else WHITE_PIECES
        return piece in pieces
