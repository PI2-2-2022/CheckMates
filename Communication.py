import serial
import time
import serial.tools.list_ports


class Communication:
    def __init__(self) -> None:
        pass

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

    def send_message(self, message):
        # TODO mostrar as mensagem no display
        print(message)

    def request_bitBoard(self, bitboard):
        # TODO comunicação com a eletrônica que retorna a bitBoard Atual
        temp = input("Movimento da IA ou movimento do usuario (e2e4)")
        if temp == "skip":
            return bitboard
        else:
            # TODO receber 'e2e4', transformar em bitboard para simular o retorno da eletronica
            return bitboard

    def get_give_up(self):
        # TODO caso o usuario desista do jogo
        return
