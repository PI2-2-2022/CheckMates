from Communication import Communication
communication = Communication()
from Movements import Movements

moviment  = Movements()

def teste():
    moviment.calibra()
    while True:
        start = input()
        end = input()
        moviment.game_movement(start,end)
        # communication.simple_comm("530",3)

teste()