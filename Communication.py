import serial
import time
import ast
import serial.tools.list_ports
from Board import Board

board = Board()

serializer = serial.Serial("/dev/ttyUSB0", 9600)


class Communication:
    def __init__(self) -> None:
        self.message = [" ", " ", " "]
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

    def update_message(self):
        print("Status do jogo: ", self.message[0])
        print("Movimento IA: ", self.message[1])
        print("Movimento Usuário: ", self.message[2])

    def update_status_message(self, message):
        self.message[0] = message
        self.update_message()

    def update_AI_move(self, message):
        self.message[1] = message
        self.update_message()

    def update_user_move(self, message):
        self.message[2] = message
        self.update_message()
