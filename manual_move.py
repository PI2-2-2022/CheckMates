from Communication import Communication
from Movements import Movements

communication = Communication()
movement = Movements()


def move():
    movement.calibra()
    while True:
        move = input()
        movement.game_movement(move)


move()
