import serial
import time
import serial.tools.list_ports


class Communication:
    def __init__(self) -> None:
        pass

    def get_move(self, targetBitBoard, currentBitBoard):  # COMMUNICATION
        to = None
        origin = None
        for idx, x in enumerate(targetBitBoard):
            for idy, y in enumerate(x):
                row = 8 - idx
                column = chr(idy + 97)
                if targetBitBoard[idx][idy] == 0 and currentBitBoard[idx][idy] == 1:
                    origin = f"{column}{row}"
                elif targetBitBoard[idx][idy] == 1 and currentBitBoard[idx][idy] == 0:
                    to = f"{column}{row}"

        return f"{origin}{to}"

    def get_next_board(self):  # COMMUNICATION
        # TODO fazer a integracao e recuperar a matriz de bit por aqui
        input("Aguardando proxima jogada (recebimento do proximo bitboard)")
        return [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def fen_to_matrix(self, fen):  # COMMUNICATION
        rows = str(fen.split(" ")[0]).split("/")
        matrix = []
        for row in rows:
            matrix_row = []
            for char in row:
                if char.isnumeric():
                    matrix_row += [" " for _ in range(int(char))]
                else:
                    matrix_row.append(char)
            matrix.append(matrix_row)
        return matrix

    def matrix_to_bitboard(self, matrix):  # COMMUNICATION
        for i in range(8):
            for j in range(8):
                if not matrix[i][j] == " ":
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = 0
        return matrix

    def send_bit_board(self, bitBoard):  # COMMUNICATION
        # TODO devolver o movimento para a eletronica
        return

    def test_serializer_comunication(self, message):
        # extract COM port automatically
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            pathCOMPort = str(p).split("-")[0].strip()
            print(pathCOMPort)

        serializer = serial.Serial(pathCOMPort, 9600)

        time.sleep(2)  # wait for communication to get established

        serializer.write(message.encode())  # messages needs to be sent in binary

        serializer.close()

    def send_endgame_message(self, message):
        # TODO mostrar a mensagem de fim de jogo na telinha
        print(message)
