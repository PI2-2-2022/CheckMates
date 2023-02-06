import serial
import time
import ast
import serial.tools.list_ports
from Board import Board

board = Board()

serializer = serial.Serial("/dev/ttyACM0", 9600)


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

    def serializer_comunication(self, message):
        # extract COM port automatically
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            pathCOMPort = str(p).split("-")[0].strip()
            print(pathCOMPort)

        time.sleep(2)  # wait for communication to get established

        serializer.write(message.encode())
         # messages needs to be sent in binary
        # Read multiple lines of data
        final = []
        count= 0 
        while True:
            response = serializer.readline().decode().split()
            print(response)
            if len(response) > 5:
                final.append(response)
                count+=1
            if count==8:
                return final

    def simple_comm(self, message, size):
        # extract COM port automatically

        time.sleep(2)  # wait for communication to get established

        serializer.write(message.encode())  # messages needs to be sent in binary

        # Read multiple lines of data
        final = []
        while True:
            response = serializer.readline().decode().split()
            print(response)
            if len(response) == int(size):
                final.append(response)
                break
            # else: break

        # serializer.close()

        return final

    def send_message(self, message):
        # TODO mostrar as mensagem no display
        print(message)

    def request_bitBoard(self):
        # TODO descomentar quando for testar com a eletronica
        # Le a bitboard da eletronica
        raw = self.serializer_comunication("800")

        # TODO comentar quando for testar com a eletronica
        # Simula uma leitura de bitboard de um txt
        # raw = self.get_bit_board_txt()

        bitBoard = board.transform_raw_board(raw)
        return bitBoard

    def get_give_up(self):
        # TODO caso o usuario desista do jogo
        return

    def get_bit_board_txt(self):
        time.sleep(2)
        with open("bitboard.txt", "r") as file:
            content = file.read()
        bitBoard = ast.literal_eval(content)
        return bitBoard
