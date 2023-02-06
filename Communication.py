import serial
import time
import serial.tools.list_ports
from Board import Board

board = Board()
serializer=serial.Serial("/dev/ttyUSB0", 9600)

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


        time.sleep(2)  # wait for communication to get established

        serializer.write(message.encode())  # messages needs to be sent in binary

        # Read multiple lines of data
        final = []
        while True:
            response = serializer.readline().decode().split()
            if response: final.append(response)
            else: break

        # Print the response
        # print(response.decode())

        # final =[
        #     ['800', '0', '8'],
        #     ['8|', '0', '0', '0', '0', '0', '0', '0', '0', '|'],
        #     ['7|', '0', '0', '0', '0', '0', '0', '0', '0', '|'],
        #     ['6|', '1', '1', '1', '1', '1', '1', '1', '1', '|'],
        #     ['5|', '1', '1', '1', '1', '1', '1', '1', '1', '|'],
        #     ['4|', '1', '1', '1', '1', '1', '1', '1', '1', '|'],
        #     ['3|', '1', '1', '1', '1', '1', '1', '1', '1', '|'],
        #     ['2|', '0', '0', '0', '0', '0', '0', '0', '0', '|'],
        #     ['1|', '0', '0', '0', '0', '0', '0', '0', '0', '|']]
        print(final)
        return final

    
    def simple_comm(self, message,size):
        time.sleep(2)
        serializer.write(message.encode())  # messages needs to be sent in binary

        # Read multiple lines of data
        final = []
        while True:
            response = serializer.readline().decode().split()
            print(response)
            if len(response)==int(size): 
                final.append(response) 
                break
        return final


    def send_message(self, message):
        # TODO mostrar as mensagem no display
        print(message)

    def request_bitBoard(self):
        raw = self.test_serializer_comunication("800")
        bitBoard = board.transform_raw_board(raw)
        return bitBoard

    def get_give_up(self):
        # TODO caso o usuario desista do jogo
        return
