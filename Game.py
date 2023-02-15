import time
from Board import Board
from Constants import STARTING_FEN, STOCKFISH_PATH, INITIAL_BOARD
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
        self.lastValidBoard = INITIAL_BOARD
        self.currentBoard = INITIAL_BOARD
        self.currentFen = STARTING_FEN
        self.AIEatenPieces = 1
        self.stockfish = None
        self.AICastlingAvailable = True
        self.color = color
        self.level = level

    def start_game(self):
        self.config_stockfish()
        self.calibrar_motor()

        board.update_SVG(self.currentFen)
        communication.update_status_message("Jogo iniciado!")

        # Caso a escolha das peças do usuário sejam pretas a IA começa jogando
        if self.color == "b":
            self.make_AI_movement()

        self.game_loop()

    def game_loop(self):
        while not validation.end_game(self.currentFen):
            move = input("Digite seu movimento (Ex.: e2e4): ")
            communication.update_user_move(move)

            # Verifica se o movimento é de um peão e se resulta nele se tornar uma rainha
            if board.is_pawn_to_queen(move, self.currentBoard, self.color):
                move = f"{move}q"

            try:
                # Realizando o movimento do usuario na stockfish
                self.stockfish.make_moves_from_current_position([move])
                self.currentFen = self.stockfish.get_fen_position()
                self.currentBoard = board.update_board(self.currentBoard, move)
                board.update_SVG(self.currentFen)

                # Verifica se o usuário fez um movimento que resulta no fim do jogo
                if validation.end_game(self.currentFen):
                    break

                self.make_AI_movement()
            except:
                communication.update_status_message("Movimento inválido!")

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

    def move_to_zona_morta(self, AIMove):
        # Pega qual a cor das peças da IA
        zonaMortaMove = AIMove[2:] + "m" + str(self.AIEatenPieces)
        communication.update_AI_move(zonaMortaMove)
        movements.game_movement(zonaMortaMove)
        self.AIEatenPieces = self.AIEatenPieces + 1
        communication.update_status_message("Movimento para zona morta concluido!")

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
        self.currentBoard = board.update_board(self.currentBoard, towerMove)
        return towerMove

    def make_AI_movement(self):
        communication.update_status_message("IA se movimentando!")
        self.stockfish.set_fen_position(self.currentFen)
        bestMove = self.stockfish.get_best_move()

        # Zona morta logic
        if board.destination_has_piece(bestMove, self.currentBoard):
            self.move_to_zona_morta(bestMove)

        self.stockfish.make_moves_from_current_position([bestMove])
        self.currentFen = self.stockfish.get_fen_position()
        self.currentBoard = board.update_board(self.currentBoard, bestMove)
        board.update_SVG(self.currentFen)
        # Se a jogada do usuário e da IA forem válidas, salva os tabuleiros válidos que poderão ser utilizados no modo de recuperação
        self.lastValidBoard = self.currentBoard

        # Castling logic
        if self.AICastlingAvailable and board.is_castling(bestMove, self.currentBoard):
            self.AI_castling_move(bestMove)

        communication.update_AI_move(bestMove)
        movements.game_movement(bestMove)
        communication.update_status_message("IA se movimentou! Sua vez.")
        self.calibrar_motor()


if __name__ == "__main__":
    level = input("Digite o nível que deseja jogar: ")
    color = input("Digite a cor que deseja jogar ('w' ou 'b'): ")
    game = Game(color, level)
    game.start_game()
