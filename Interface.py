import os
from Validation import Validation
from Communication import Communication
from Board import Board
from stockfish import Stockfish
from constants import STARTING_FEN
import chess

board = Board()
validation = Validation()
communication = Communication()


class Interface:
    # Representa a classe que realiza a a interface com o usuário 
    
    def __init__(self):
        pass

    def get_level(self): # GUI
        level = input("Selecione em qual dificuldade você deseja jogar (0-20): ")
        return int(level)

    def get_color(self):
        color = input("Selecione com qual cor deseja jogar (w para jogar com as brancas ou b para jogar com as pretas): ")
        return color

    def start_game(self, stockfish: Stockfish, currentFen, currentBitBoard, color):
        if currentFen == None:
            currentFen = STARTING_FEN
        if color == 'b':
            stockfish.set_fen_position(currentFen)
            bestMove = stockfish.get_best_move()
            stockfish.make_moves_from_current_position([bestMove])
            currentFen = stockfish.get_fen_position()
        while not validation.is_game_over_or_drawn(currentFen):
            give_up = input('Insira sua jogada(ex.: e2e4) ou digite "give up" para desistir: ')
            if give_up == "give up":
                print("Jogador desistiu, fim de jogo.")
                break
            move = give_up
            if validation.is_valid_move(move, currentFen):
                stockfish.make_moves_from_current_position([move])
                bestMove = stockfish.get_best_move()
                stockfish.make_moves_from_current_position([bestMove])
                currentFen = stockfish.get_fen_position()
                if validation.is_checkmate(currentFen):
                    print("Checkmate, Jogador 1 ganhou" if chess.Board(currentFen).turn == 'w' else "Checkmate, Jogador 2 ganhou")
                    break
                matrix = communication.fen_to_matrix(currentFen)
                currentBitBoard = communication.matrix_to_bitboard(matrix)
                communication.send_bit_board(currentBitBoard)
                board.update_board(currentFen)
            else:
                print("Movimento inválido, tente novamente.")
