import os
from Validation import Validation
from Communication import Communication
from Board import Board
from stockfish import Stockfish
from constants import STARTING_FEN, INITIAL_BIT_BOARD, INITIAL_BOARD
import time

board = Board()
validation = Validation()
communication = Communication()


class Interface:
    # Representa a classe que realiza a a interface com o usuário
    currentBitBoard = INITIAL_BIT_BOARD
    currentBoard = INITIAL_BOARD
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
        print("Movimento IA: ", bestMove)
        self.stockfish.make_moves_from_current_position([bestMove])
        self.currentFen = self.stockfish.get_fen_position()
        matrix = communication.fen_to_matrix(self.currentFen)
        self.currentBitBoard = communication.matrix_to_bitboard(matrix)
        self.currentBoard = board.update_board(self.currentBoard, bestMove)
        board.update_SVG(self.currentFen)

    def game_loop(self):
        while not validation.is_game_over_or_drawn(self.currentFen):
            bitBoard = communication.request_bitBoard()

            # Caso os tabuleiros sejam diferentes e a flag da IA seja true, significa que o motor está movimentando a peça
            if not bitBoard == self.currentBitBoard and self.isAIMovement:
                print("IA se movimentando...")
            # Caso os tabuleiros sejam iguais e a flag da IA seja true, significa que o motor terminou de movimentar a peça e a próxima iteração deve ser o movimento do usuário
            elif bitBoard == self.currentBitBoard and self.isAIMovement:
                print("IA se movimentou!")
                self.isAIMovement = False
            # Detecta o movimento do usuario pela diferença das bitBoards
            elif not bitBoard == self.currentBitBoard:
                # Pega o movimento no formato "e2e4" pela diferença da bitboard
                move = board.get_move(bitBoard, self.currentBitBoard)
                print("Movimento do usuário: ", move)

                # Verifica se o movimento foi um "pré-movimento" para comer uma peça (movimentar uma peça que não é do usuário para fora do tabuleiro)
                if board.is_move_to_eat_piece(move, self.currentBoard, self.currentFen):
                    # TODO verificar se essa atribuição gera problemas
                    self.currentBitBoard = bitBoard
                    continue

                if validation.is_valid_move(move, self.currentFen):
                    # Realizando o movimento do usuario na stockfish
                    self.stockfish.make_moves_from_current_position([move])
                    self.currentFen = self.stockfish.get_fen_position()
                    self.currentBitBoard = bitBoard
                    self.currentBoard = board.update_board(self.currentBoard, move)

                    # Verifica se o usuário fez um movimento que resulta no fim do jogo
                    if validation.is_game_over_or_drawn(self.currentFen):
                        break
                    else:
                        self.make_AI_movement()
                else:
                    # TODO mostrar vermelho na telinha
                    print("Movimento inválido, tente novamente.")
                    continue

    def start_game(self, stockfish: Stockfish, color):
        # Pega a bit board inicial do jogo
        bitBoard = communication.request_bitBoard()
        self.stockfish = stockfish

        # Caso o tabuleiro incial não seja válido, manda uma mensagem para o display
        if not board.is_initial_board(bitBoard):
            communication.send_message("Tabuleiro inicial inválido")
        else:
            board.update_SVG(self.currentFen)
            self.game_loop()
            if color == "b":
                self.make_AI_movement()
