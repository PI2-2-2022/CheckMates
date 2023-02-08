from Communication import Communication
communication = Communication()
from Movements import Movements

moviment  = Movements()

def teste():
    moviment.calibra()
    while True:
        move = input()
        moviment.game_movement(move[:2],move[2:])
        # communication.simple_comm("530",3)

teste()