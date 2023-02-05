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
        # TODO verificar o funcionamento
        # Pega as coordenadas da origem do movimento
        originX = ord(move[0]) - 97
        originY = int(move[1])
        # Pega as coordenadas do destino do movimento
        destinationX = ord(move[2]) - 97
        destinationY = int(move[3])

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
        # TODO será necessário testar e fazer ajustes nessa função
        # Verifica se a peça não tem destino, caso tenha é um movimento normal e retorna falso
        if not "None" in move:
            return False

        # Pega qual a cor das peças do usuário
        turn = currentFen[20]

        # Pega as coordenadas da origem do movimento
        x = ord(move[0]) - 97
        y = int(move[1])

        # Pega qual peça foi movimentada a partir daquela origigem
        piece = currentBoard[x][y]
        # Verifica qual grupo de peças serão comparadas dependendo da cor do usuário.
        # Caso sejam peças que não são dele, significa que ele está colocando uma peça na zona morta.
        # Caso contrário siginifica que ele está no meio de um movimento das suas peças.
        pieces = BLACK_PIECES if turn == "w" else WHITE_PIECES
        return piece in pieces
