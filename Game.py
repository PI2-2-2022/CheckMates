import time
from Board import Board
from Constants import INITIAL_BIT_BOARD, STARTING_FEN, STOCKFISH_PATH, INITIAL_BOARD
from Movements import Movements
from Communication import Communication
from Validation import Validation
from stockfish import Stockfish

movements = Movements()
communication = Communication()
board = Board()
validation = Validation()


class Game:
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
        self.userCastlingAvailable = True
        self.AICastlingAvailable = True
        self.color = color
        self.level = level

    def start_game(self):
        self.config_stockfish()
        self.calibrar_motor()

        board.update_SVG(self.currentFen)
        self.currentBitBoard = self.request_bitboard()

        while not board.is_initial_board(self.currentBitBoard) and not self.stopGame:
            communication.update_status_message("Tabuleiro inicial inválido!")
            self.currentBitBoard = self.request_bitboard()

        communication.update_status_message("Jogo iniciado!")

        # Caso a escolha das peças do usuário sejam pretas a IA começa jogando
        if self.color == "b":
            self.make_AI_movement()

        self.game_loop()
        # depois que o jogo é interrompido reseta as variáveis
        communication.message = ["", "", ""]
        self.lastValidBitBoard = INITIAL_BIT_BOARD
        self.currentBitBoard = INITIAL_BIT_BOARD
        self.currentBoard = INITIAL_BOARD
        self.currentFen = STARTING_FEN
        self.isAIMovement = False
        self.AIEatenPieces = 1
        self.stockfish = None
        self.stopGame = False
        self.userCastlingAvailable = True
        self.AICastlingAvailable = True

    def game_loop(self):
        while not validation.end_game(self.currentFen) and not self.stopGame:
            bitBoard = self.request_bitboard()
            # Caso os tabuleiros sejam diferentes e a flag da IA seja true, significa que o motor está movimentando a peça
            if not bitBoard == self.currentBitBoard and self.isAIMovement:
                communication.update_status_message("IA se movimentando...")
            # Caso os tabuleiros sejam iguais e a flag da IA seja true, significa que o motor terminou de movimentar a peça e a próxima iteração deve ser o movimento do usuário
            elif bitBoard == self.currentBitBoard and self.isAIMovement:
                communication.update_status_message("IA se movimentou! Sua vez.")
                self.isAIMovement = False
            # Detecta o movimento do usuario pela diferença das bitBoards
            elif not bitBoard == self.currentBitBoard:
                # Pega o movimento no formato "e2e4" pela diferença da bitboard
                move = board.coords_to_move(bitBoard, self.currentBitBoard)
                communication.update_user_move(move)

                # Verifica se o movimento foi um "pré-movimento" para comer uma peça (movimentar uma peça que não é do usuário para fora do tabuleiro)
                if board.is_move_to_eat_piece(move, self.currentBoard, self.currentFen):
                    communication.update_status_message("Usuário comendo uma peça!")
                    self.currentBitBoard = bitBoard
                    continue

                # Veririca se o movimento é de um peão e se resulta nele se tornar uma rainha
                if board.is_pawn_to_queen(move, self.currentBoard, self.color):
                    move = f"{move}q"

                try:
                    # Realizando o movimento do usuario na stockfish
                    self.stockfish.make_moves_from_current_position([move])
                    self.currentFen = self.stockfish.get_fen_position()
                    self.currentBitBoard = bitBoard
                    self.currentBoard = board.update_board(self.currentBoard, move)
                    board.update_SVG(self.currentFen)

                    if self.userCastlingAvailable and board.is_castling(
                        move, self.currentBoard
                    ):
                        self.user_castling_move(move)

                    # Verifica se o usuário fez um movimento que resulta no fim do jogo
                    if validation.end_game(self.currentFen):
                        break

                    self.make_AI_movement()
                except:
                    if move[2:] == "None":
                        communication.update_status_message("Usuário se movimentando!")
                    else:
                        communication.update_status_message(
                            "Movimento inválido!\nVolte o tabuleiro para o estado anterior."
                        )
                        self.recover_mode()

    def config_stockfish(self):
        hash = 256
        if self.level == 3:
            hash = 512
        elif self.level == 7:
            hash = 768

        self.stockfish = Stockfish(
            STOCKFISH_PATH,
            depth=self.level,
            parameters={
                "Debug Log File": "",
                "Min Split Depth": 0,
                "Threads": 1,
                "Ponder": "false",
                "Hash": hash,
                "MultiPV": 1,
                "Skill Level": self.level,
                "Move Overhead": 10,
                "Slow Mover": 100,
                "UCI_Chess960": "false",
            },
        )

    def calibrar_motor(self):
        communication.update_status_message("Calibrando motor...")
        movements.calibrar_motor()
        communication.update_status_message("Motor calibrado!")

    def request_bitboard(self):
        bitBoard = communication.request_bitBoard()
        with open("bitboard.txt", "w") as file:
            file.write(str(bitBoard))
        return bitBoard

    def recover_mode(self):
        self.currentBitBoard = self.lastValidBitBoard
        self.currentBoard = self.lastValidBoard
        while True:
            bitBoard = communication.request_bitBoard()
            if bitBoard == self.currentBitBoard:
                communication.update_status_message(
                    "Tabuleiro recuperado!\n Jogue novamente"
                )
                break

    def move_to_zona_morta(self, AIMove):
        # Pega qual a cor das peças da IA
        zonaMortaMove = AIMove[2:] + "m" + str(self.AIEatenPieces)
        communication.update_AI_move(zonaMortaMove)
        movements.game_movement(zonaMortaMove)
        self.AIEatenPieces = self.AIEatenPieces + 1
        communication.update_status_message("Movimento para zona morta concluido!")

    def user_castling_move(self, move):
        towerMove = self.castling_move(move)
        self.userCastlingAvailable = False
        while True:
            communication.update_status_message(
                f"Mova a torre para completar o castling! {towerMove}"
            )
            expectedBitBoard = communication.request_bitBoard()
            if expectedBitBoard == self.currentBitBoard:
                break
        communication.update_status_message("Casltling move concluído!")

    def AI_castling_move(self, move):
        towerMove = self.castling_move(move)
        self.AICastlingAvailable = False
        movements.game_movement(towerMove)
        communication.update_status_message(f"IA Castling move concluído! {towerMove}")

    def castling_move(self, move):
        castlingMoves = {
            "e1g1": "h1f1",
            "e1b1": "a1c1",
            "e8g8": "h8f8",
            "e8b8": "a8c8",
        }
        towerMove = castlingMoves.get(move)
        self.currentBitBoard = board.update_board(self.currentBitBoard, towerMove, 0)
        self.currentBoard = board.update_board(self.currentBoard, towerMove)
        return towerMove

    def make_AI_movement(self):
        self.isAIMovement = True
        self.stockfish.set_fen_position(self.currentFen)
        bestMove = self.stockfish.get_best_move()

        # Zona morta logic
        if board.destination_has_piece(bestMove, self.currentBoard):
            self.move_to_zona_morta(bestMove)

        self.stockfish.make_moves_from_current_position([bestMove])
        self.currentFen = self.stockfish.get_fen_position()
        self.currentBitBoard = board.update_board(self.currentBitBoard, bestMove, 0)
        self.currentBoard = board.update_board(self.currentBoard, bestMove)
        board.update_SVG(self.currentFen)
        # Se a jogada do usuário e da IA forem válidas, salva os tabuleiros válidos que poderão ser utilizados no modo de recuperação
        self.lastValidBitBoard = self.currentBitBoard
        self.lastValidBoard = self.currentBoard

        # Castling logic
        if self.AICastlingAvailable and board.is_castling(bestMove, self.currentBoard):
            self.AI_castling_move(bestMove)

        communication.update_AI_move(bestMove)
        movements.game_movement(bestMove)
        self.calibrar_motor()
