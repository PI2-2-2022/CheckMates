import os
from Validation import Validation
from Communication import Communication
from Board import Board
from stockfish import Stockfish
from constants import STARTING_FEN, INITIAL_BOARD_BIT
import time

board = Board()
validation = Validation()
communication = Communication()


class Interface:
    # Representa a classe que realiza a a interface com o usuário
    currentBitBoard = [[]]
    currentFen = STARTING_FEN
    isAIMovement = False
    stockfish = None

    def __init__(self):
        pass

    def get_level(self):  # GUI
        level = input("Selecione em qual dificuldade você deseja jogar (0-20): ")
        return int(level)

    def get_color(self):
        color = input(
            "Selecione com qual cor deseja jogar (w para jogar com as brancas ou b para jogar com as pretas): "
        )
        return color

    def make_AI_movement(self):
        self.isAIMovement = True
        self.stockfish.set_fen_position(self.currentFen)
        bestMove = self.stockfish.get_best_move()
        self.stockfish.make_moves_from_current_position([bestMove])
        self.currentFen = self.stockfish.get_fen_position()
        matrix = communication.fen_to_matrix(self.currentFen)
        self.currentBitBoard = communication.matrix_to_bitboard(matrix)
        communication.send_bit_board(self.currentBitBoard)
        board.update_board(self.currentFen)

    def game_loop(self, color):
        if color == "b":
            self.make_AI_movement()

        while not validation.is_game_over_or_drawn(self.currentFen):
            bitBoard = communication.request_bitBoard(self.currentBitBoard)

            if not bitBoard == self.currentBitBoard and self.isAIMovement:
                time.sleep(1)
                continue
            elif bitBoard == self.currentBitBoard and self.isAIMovement:
                self.isAIMovement = False
            # Detecta o movimento do usuario pela diferença das bitBoards
            elif not bitBoard == self.currentBitBoard:
                # Pega o movimento no formato "e2e4" pela diferença da bitboard
                move = board.get_move(bitBoard, self.currentBitBoard)

                if validation.is_valid_move(move, self.currentFen):
                    # Realizando o movimento do usuario na stockfish
                    self.stockfish.make_moves_from_current_position([move])
                    # Verifica se o usuário fez um movimento que resulta no fim do jogo
                    if validation.is_game_over_or_drawn(self.currentFen):
                        break

                    self.make_AI_movement()
                else:
                    print("Movimento inválido, tente novamente.")
                    continue
            time.sleep(1)

    def start_game(self, stockfish: Stockfish, color):
        self.stockfish = stockfish
        # Pega a bit board inicial do jogo
        bitBoard = communication.request_bitBoard(INITIAL_BOARD_BIT)

        # Caso o tabuleiro incial não seja válido, manda uma mensagem para o display
        if not board.is_initial_board(bitBoard):
            communication.send_message("Tabuleiro inicial inválido")
        else:
            self.currentBitBoard = bitBoard
            board.update_board(self.currentFen)
            self.game_loop(color)
