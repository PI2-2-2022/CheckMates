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
    lastValidBitBoard = INITIAL_BIT_BOARD
    lastValidBoard = INITIAL_BOARD
    currentBitBoard = INITIAL_BIT_BOARD
    currentBoard = INITIAL_BOARD
    currentFen = STARTING_FEN
    isAIMovement = False
    AIEatenPieces = 0
    stockfish = None

    def __init__(self):
        pass

    def move_to_zona_morta(self, AIMove):
        # Pega qual a cor das peças da IA
        turn = self.currentFen[-12]
        offset = (17 if turn == "b" else 0) + self.AIEatenPieces
        zonaMortaMove = AIMove[2:] + "m" + str(int(abs(offset))).rjust(2, "0")

        communication.send_message("Movimento para zona morta: " + zonaMortaMove)
        movements.game_movement(zonaMortaMove)
        self.AIEatenPieces = self.AIEatenPieces + 1

    def make_AI_movement(self):
        self.isAIMovement = True
        self.stockfish.set_fen_position(self.currentFen)
        AIMove = self.stockfish.get_best_move()
        communication.send_message("Movimento IA: " + AIMove)

        if board.destination_has_piece(AIMove, self.currentBoard):
            self.move_to_zona_morta(AIMove)

        movements.game_movement(AIMove)
        self.stockfish.make_moves_from_current_position([AIMove])
        self.currentFen = self.stockfish.get_fen_position()
        self.currentBitBoard = board.update_board(self.currentBitBoard, AIMove, 0)
        self.currentBoard = board.update_board(self.currentBoard, AIMove)
        board.update_SVG(self.currentFen)

        # Se a jogada do usuário e da IA forem válidas, salva os tabuleiros válidos que poderão ser utilizados no modo de recuperação
        self.lastValidBitBoard = self.currentBitBoard
        self.lastValidBoard = self.currentBoard

    def game_loop(self):
        while not validation.validate_game_status(self.currentFen):
            bitBoard = communication.request_bitBoard()

            # Caso os tabuleiros sejam diferentes e a flag da IA seja true, significa que o motor está movimentando a peça
            if not bitBoard == self.currentBitBoard and self.isAIMovement:
                communication.send_message("IA se movimentando...")
            # Caso os tabuleiros sejam iguais e a flag da IA seja true, significa que o motor terminou de movimentar a peça e a próxima iteração deve ser o movimento do usuário
            elif bitBoard == self.currentBitBoard and self.isAIMovement:
                communication.send_message("IA se movimentou! Sua vez de jogar!")
                self.isAIMovement = False
            # Detecta o movimento do usuario pela diferença das bitBoards
            elif not bitBoard == self.currentBitBoard:
                # Pega o movimento no formato "e2e4" pela diferença da bitboard
                move = board.coords_to_move(bitBoard, self.currentBitBoard)
                communication.send_message("Movimento do usuário: " + move)

                # Verifica se o movimento foi um "pré-movimento" para comer uma peça (movimentar uma peça que não é do usuário para fora do tabuleiro)
                if board.is_move_to_eat_piece(move, self.currentBoard, self.currentFen):
                    communication.send_message("Usuário comendo uma peça!")
                    self.currentBitBoard = bitBoard
                elif validation.is_valid_move(move, self.currentFen):
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
                elif move[2:] == "None":
                    communication.send_message("Usuário se movimentando!")
                elif move[:4] == "None":
                    communication.send_message(
                        "Modo de recuperação, volte o tabuleiro para o estado anterior!"
                    )
                    while True:
                        self.currentBitBoard = self.lastValidBitBoard
                        self.currentBoard = self.lastValidBoard
                        bitBoard = communication.request_bitBoard()
                        if bitBoard == self.lastValidBitBoard:
                            break
                else:
                    communication.send_message(
                        "Movimento inválido! Realize o movimento correto ou volte a peça para a posição inicial"
                    )

    def start_game(self, stockfish: Stockfish):
        # Pega a bit board inicial do jogo
        bitBoard = communication.request_bitBoard()
        self.stockfish = stockfish

        # Caso o tabuleiro incial não seja válido, manda uma mensagem para o display
        if not board.is_initial_board(bitBoard):
            communication.send_message(
                "Tabuleiro inicial inválido! Verifique ou reorganize as peças."
            )
            self.start_game(stockfish)
        else:
            communication.send_message("Jogo iniciado!")
            board.update_SVG(self.currentFen)
            self.game_loop()
