import time
from Communication import Communication
from Board import Board

comunication = Communication()
board = Board()

while True:

    board.print_list_of_lists(comunication.request_bitBoard())
    # time.sleep(0.5)