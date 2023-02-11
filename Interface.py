import time
from Validation import Validation
from Communication import Communication
from Board import Board
from stockfish import Stockfish
from constants import STARTING_FEN, INITIAL_BIT_BOARD, INITIAL_BOARD, STOCKFISH_PATH
from Movements import Movements

board = Board()
validation = Validation()
communication = Communication()
movements = Movements()


class Interface:
    def __init__(self, color, level):
        self.lastValidBitBoard = INITIAL_BIT_BOARD
        self.lastValidBoard = INITIAL_BOARD
        self.currentBitBoard = INITIAL_BIT_BOARD
        self.currentBoard = INITIAL_BOARD
        self.currentFen = STARTING_FEN
        self.isAIMovement = False
        self.AIEatenPieces = 1
        self.stockfish = None
        self.stopGame = False
        self.color = color
        self.level = level

    def recover_mode(self):
        while True:
            self.currentBitBoard = self.lastValidBitBoard
            self.currentBoard = self.lastValidBoard
            bitBoard = communication.request_bitBoard()
            if bitBoard == self.lastValidBitBoard:
                return

    def move_to_zona_morta(self, AIMove):
        # Pega qual a cor das peças da IA
        zonaMortaMove = AIMove[2:] + "m" + str(self.AIEatenPieces)
        communication.send_message("Movimento para zona morta: " + zonaMortaMove)
        # movements.game_movement(zonaMortaMove)
        self.AIEatenPieces = self.AIEatenPieces + 1

    def user_castling_move(self, castleMove):
        self.UserCastlingAvailable = False
        self.currentBitBoard = board.update_board(self.currentBitBoard, castleMove, 0)
        self.currentBoard = board.update_board(self.currentBoard, castleMove)
        communication.send_message("Mova a torre para completar o hawk!")
        while True:
            expectedBitBoard = communication.request_bitBoard()
            if expectedBitBoard == self.currentBitBoard:
                break
        return

    def AI_castling_move(self, castleMove, message):
        self.AICastlingAvailable = False
        self.currentBitBoard = board.update_board(self.currentBitBoard, castleMove, 0)
        self.currentBoard = board.update_board(self.currentBoard, castleMove)
        # movements.game_movement(castleMove)
        communication.send_message(message)

    def make_AI_movement(self):
        self.isAIMovement = True
        self.stockfish.set_fen_position(self.currentFen)
        bestMove = self.stockfish.get_best_move()

        # Castling logic
        if self.AICastlingAvailable and board.is_AI_castling_right(
            bestMove, self.currentBoard
        ):
            self.AI_castling_move("h8f8", "Hawk direito concluído!")
        elif self.AICastlingAvailable and board.is_AI_castling_left(
            bestMove, self.currentBoard
        ):
            self.AI_castling_move("a8d8", "Hawk esquerdo concluído!")

        # Zona morta logic
        if board.destination_has_piece(bestMove, self.currentBoard):
            self.move_to_zona_morta(bestMove)
            communication.send_message("Movimento para zona morta concluido!")

        communication.send_message("Movimento IA: " + bestMove)
        # movements.game_movement(bestMove)
        self.stockfish.make_moves_from_current_position([bestMove])
        self.currentFen = self.stockfish.get_fen_position()
        self.currentBitBoard = board.update_board(self.currentBitBoard, bestMove, 0)
        self.currentBoard = board.update_board(self.currentBoard, bestMove)
        board.update_SVG(self.currentFen)

        # Se a jogada do usuário e da IA forem válidas, salva os tabuleiros válidos que poderão ser utilizados no modo de recuperação
        self.lastValidBitBoard = self.currentBitBoard
        self.lastValidBoard = self.currentBoard
        # movements.calibra()

    def game_loop(self):
        while (
            not validation.validate_game_status(self.currentFen) and not self.stopGame
        ):
            bitBoard = communication.request_bitBoard()
            with open("bitboard.txt", "w") as file:
                file.write(str(bitBoard))

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

                    if self.UserCastlingAvailable and board.is_user_castling_right(
                        move, self.currentBoard
                    ):
                        self.user_castling_move("h1f1")
                    elif self.UserCastlingAvailable and board.is_user_castling_left(
                        move, self.currentBoard
                    ):
                        self.user_castling_move("a1d1")

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
                    self.recover_mode()
                else:
                    communication.send_message(
                        "Movimento inválido! Realize o movimento correto ou volte a peça para a posição inicial"
                    )

    def start_game(self):
        self.stockfish = Stockfish(
            STOCKFISH_PATH,
            depth=self.level,
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
                "Skill Level": self.level,
                "Move Overhead": 10,
                "Minimum Thinking Time": self.level * 1.5,
                "Slow Mover": 100,
                "UCI_Chess960": "false",
                "UCI_LimitStrength": "false",
                "UCI_Elo": 1350,
            },
        )
        # Pega a bit board inicial do jogo
        bitBoard = communication.request_bitBoard()
        self.currentBitBoard = bitBoard
        with open("bitboard.txt", "w") as file:
            file.write(str(bitBoard))

        board.update_SVG(self.currentFen)

        while not board.is_initial_board(bitBoard) and not self.stopGame:
            communication.send_message("Tabuleiro inicial inválido!")
            bitBoard = communication.request_bitBoard()
            self.currentBitBoard = bitBoard
            with open("bitboard.txt", "w") as file:
                file.write(str(bitBoard))

        communication.send_message("Jogo iniciado!")
        self.game_loop()
