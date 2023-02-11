import serial
import time
import ast
import serial.tools.list_ports
from Board import Board

board = Board()

serializer = serial.Serial("/dev/ttyUSB0", 9600)


class Communication:
    def __init__(self) -> None:
        pass

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
        count = 0
        while True:
            response = serializer.readline().decode().split()
            if len(response) > 5:
                final.append(response)
                count += 1
            if count == 8:
                return final

    def simple_comm(self, message, size):
        # extract COM port automatically

        time.sleep(1.5)  # wait for communication to get established

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
        # board.print_list_of_lists(final)
        return final

    def send_message(self, message):
        with open("message.txt", "w") as file:
            file.write(f"'{message}'")

    def request_bitBoard(self):
        # Le a bitboard da eletronica
        raw = self.serializer_comunication("8000")

        # Simula uma leitura de bitboard de um txt
        # raw = self.get_bit_board_txt()

        bitBoard = board.transform_raw_board(raw)
        return bitBoard

    def get_bit_board_txt(self):
        time.sleep(2)
        with open("bitboard_response.txt", "r") as file:
            content = file.read()
        bitBoard = ast.literal_eval(content)
        return bitBoard
