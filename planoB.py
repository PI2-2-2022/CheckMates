from time import sleep
from stockfish import Stockfish
from constants import STARTING_FEN
from Validation import Validation
# from Communication import Communication
from Board import Board
import chess

# communication = Communication()
validation = Validation()
board = Board()

class PlanB:

    def __init__(self) -> None:
        pass

    def start_game(self, stockfish: Stockfish, currentFen, color):
        if currentFen == None:
            currentFen = STARTING_FEN
        if color == 'b':
            board.update_board(currentFen)
            stockfish.set_fen_position(currentFen)
            bestMove = stockfish.get_best_move()
            stockfish.make_moves_from_current_position([bestMove])
            currentFen = stockfish.get_fen_position()
        while not validation.is_game_over_or_drawn(currentFen):
            board.update_board(currentFen)
            give_up = input('Insira sua jogada(ex.: e2e4) ou digite "give up" para desistir: ')
            if give_up == "give up":
                print("Jogador desistiu, fim de jogo.")
                break
            move = give_up
            if validation.is_valid_move(move, currentFen):
                stockfish.make_moves_from_current_position([move]) # nosso movimento
                currentFen = stockfish.get_fen_position()
                board.update_board(currentFen)
                sleep(1)
                bestMove = stockfish.get_best_move()
                ## Mover peça baseada no movimento do adversário (bestMove)
                stockfish.make_moves_from_current_position([bestMove]) #atualiza fen stockfish
                currentFen = stockfish.get_fen_position() #atualiza nossa fen interna
                if validation.is_checkmate(currentFen):
                    print("Checkmate, Jogador 1 ganhou" if chess.Board(currentFen).turn == 'w' else "Checkmate, Jogador 2 ganhou")
                    break
                board.update_board(currentFen)
            else:
                print("Movimento inválido, tente novamente.")