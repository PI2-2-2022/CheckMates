import os
import chess
import chess.svg
from pathlib import Path
from stockfish import Stockfish
from dotenv import load_dotenv

load_dotenv()

STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
FILLED_ROW = [1, 1, 1, 1, 1, 1, 1, 1]
EMPTY_ROW = [0, 0, 0, 0, 0, 0, 0, 0]
INITIAL_BOARD_BIT = [
    FILLED_ROW,
    FILLED_ROW,
    EMPTY_ROW,
    EMPTY_ROW,
    EMPTY_ROW,
    EMPTY_ROW,
    FILLED_ROW,
    FILLED_ROW,
]
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def get_level():
    # TODO pegar o nivel do display de niveis
    return 10


def get_move(targetBitBoard, currentBitBoard):
    to = None
    origin = None
    for idx, x in enumerate(targetBitBoard):
        for idy, y in enumerate(x):
            row = 8 - idx
            column = chr(idy + 97)
            if (targetBitBoard[idx][idy] == 0 and currentBitBoard[idx][idy] == 1):
                origin = f'{column}{row}'
            elif (targetBitBoard[idx][idy] == 1 and currentBitBoard[idx][idy] == 0):
                to = f'{column}{row}'

    return f'{origin}{to}'


def get_next_board():
    # TODO fazer a integracao e recuperar a matriz de bit por aqui
    input("Aguardando proxima jogada (recebimento do proximo bitboard)")
    return [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]


def fen_to_matrix(fen):
    rows = str(fen.split(' ')[0]).split("/")
    matrix = []
    for row in rows:
        matrix_row = []
        for char in row:
            if char.isnumeric():
                matrix_row += [' ' for _ in range(int(char))]
            else:
                matrix_row.append(char)
        matrix.append(matrix_row)
    return matrix


def matrix_to_bitboard(matrix):
    for i in range(8):
        for j in range(8):
            if (not matrix[i][j] == ' '):
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(row)


def send_bit_board(bitBoard):
    # TODO devolver o movimento para a eletronica
    return


def is_game_over():
    # TODO verificar checkmate, empate, vitoria, etc...
    return False


def update_board(currentFen):
    board = chess.Board(fen=currentFen)
    with open(Path(__file__).parent.joinpath("game.svg"), mode="w") as img:
        img.write(chess.svg.board(board, size=350))


def start_game(stockfish: Stockfish, currentFen, currentBitBoard):
    while not is_game_over():
        # TODO descomentar quando o recebimento da bit board estiver funcionando
        # targetBoard = get_next_board()
        # move = get_move(targetBoard, currentBitBoard)

        move = input('Insira sua jogada(ex.: e2e4): ')
        # print('Movimento usuario:', move)

        stockfish.set_fen_position(currentFen)
        # print('FEN inicio rodada:', stockfish.get_fen_position())

        # TODO fazer as validacoes do movimento
        stockfish.make_moves_from_current_position([move])
        # print('FEN apos movimento usuario:', stockfish.get_fen_position())

        bestMove = stockfish.get_best_move()
        # print('Movimento da IA:', bestMove)
        stockfish.make_moves_from_current_position([bestMove])
        # print('FEN apos movimento IA:', stockfish.get_fen_position())

        currentFen = stockfish.get_fen_position()
        matrix = fen_to_matrix(currentFen)
        # print('\n\nmatriz: ')
        # print_matrix(matrix)
        currentBitBoard = matrix_to_bitboard(matrix)
        # print('\n\nbit board: ')
        # print_matrix(currentBitBoard)
        send_bit_board(currentBitBoard)
        update_board(currentFen)


def main():
    # TODO verificar se o bit board inicial mandado pela eletronica é equivalente ao INITIAL_BOARD_BIT para iniciar o jogo
    level = get_level()
    stockfish = Stockfish(
        STOCKFISH_PATH,
        depth=20,
        parameters={
            "Debug Log File": "",
            "Contempt": 0,
            "Min Split Depth": 0,
            # More threads will make the engine stronger, but should be kept at less than the number of logical processors on your computer.
            "Threads": 1,
            "Ponder": "false",
            # Default size is 16 MB. It's recommended that you increase this value, but keep it as some power of 2. E.g., if you're fine using 2 GB of RAM, set Hash to 2048 (11th power of 2).
            "Hash": 512,
            "MultiPV": 1,
            "Skill Level": int(level),
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 1350,
        },
    )
    update_board(STARTING_FEN)
    start_game(stockfish, STARTING_FEN, INITIAL_BOARD_BIT)


if __name__ == '__main__':
    main()
