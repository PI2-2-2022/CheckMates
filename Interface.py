from Validation import Validation
from Communication import Communication
from Board import Board
from stockfish import Stockfish
from constants import STARTING_FEN, INITIAL_BIT_BOARD, INITIAL_BOARD
from Movements import Movements

board = Board()
validation = Validation()
communication = Communication()
movements = Movements()



class Interface:
    # Representa a classe que realiza a a interface com o usuário
    currentBitBoard = INITIAL_BIT_BOARD
    currentBoard = INITIAL_BOARD
    currentFen = STARTING_FEN
    isAIMovement = False
    stockfish = None
    AIEatenPieces = 0

    def __init__(self):
        pass

    def move_to_zona_morta(self, AIMove):
        #Pega qual a cor das peças da IA
        turn = self.currentFen[-12]
        offset =  (17 if turn == "b" else 0) + self.AIEatenPieces 
        zonaMortaMove = AIMove[2] + AIMove[3] + 'm' + str(int(abs(offset))).rjust(2, "0")

        print('zona morta move: ', zonaMortaMove)
        movements.game_movement(zonaMortaMove[:2],zonaMortaMove [2:])

    def make_AI_movement(self):
        self.isAIMovement = True
        self.stockfish.set_fen_position(self.currentFen)
        bestMove = self.stockfish.get_best_move()
        print("Movimento IA: ", bestMove)

        if board.destination_has_piece(bestMove, self.currentBoard):
          self.move_to_zona_morta(bestMove)

        movements.game_movement(bestMove[:2],bestMove [2:])
        self.stockfish.make_moves_from_current_position([bestMove])
        self.currentFen = self.stockfish.get_fen_position()
        matrix = communication.fen_to_matrix(self.currentFen)
        self.currentBitBoard = communication.matrix_to_bitboard(matrix)
        self.currentBoard = board.update_board(self.currentBoard, bestMove)
        board.update_SVG(self.currentFen)

    def game_loop(self):
        while not validation.validate_game_status(self.currentFen):
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
                    self.currentBitBoard = bitBoard
                    continue

                if validation.is_valid_move(move, self.currentFen):
                    # Realizando o movimento do usuario na stockfish
                    self.stockfish.make_moves_from_current_position([move])
                    self.currentFen = self.stockfish.get_fen_position()
                    self.currentBitBoard = bitBoard
                    self.currentBoard = board.update_board(self.currentBoard, move)
                    board.update_SVG(self.currentFen)

                    # Verifica se o usuário fez um movimento que resulta no fim do jogo
                    if validation.validate_game_status(self.currentFen):
                        break
                    else:
                        self.make_AI_movement()
                else:
                    print("Usuário se movimentando ou movimento inválido.")
                    continue

    def start_game(self, stockfish: Stockfish):
        # Pega a bit board inicial do jogo
        bitBoard = communication.request_bitBoard()
        self.stockfish = stockfish

        # Caso o tabuleiro incial não seja válido, manda uma mensagem para o display
        if not board.is_initial_board(bitBoard):
            communication.send_message("Tabuleiro inicial inválido")
        else:
            board.update_SVG(self.currentFen)
            self.game_loop()
