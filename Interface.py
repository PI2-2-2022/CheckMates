import os
from Validation import Validation
from Communication import Communication
from Board import Board
from stockfish import Stockfish
from constants import STARTING_FEN

board = Board()
validation = Validation()
communication = Communication()


class Interface:
    # Representa a classe que realiza a a interface com o usuário 
    
    def __init__(self):
        pass

    def get_level(): # GUI
    # TODO pegar o nivel do display de niveis
        return 10

    def get_color():
    # TODO pegar com qual peça o jogador gostaria de jogar
        return 10

    def start_game(self, stockfish: Stockfish, currentFen, currentBitBoard): # 
        if currentFen == None:
            currentFen = STARTING_FEN
        while not validation.is_game_over():
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
            matrix = communication.fen_to_matrix(currentFen)
            # print('\n\nmatriz: ')
            # print_matrix(matrix)
            currentBitBoard = communication.matrix_to_bitboard(matrix)
            # print('\n\nbit board: ')
            # print_matrix(currentBitBoard)
            communication.send_bit_board(currentBitBoard)
            board.update_board(currentFen)