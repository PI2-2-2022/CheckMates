SQUARE = 1
HALF_SQUARE = SQUARE/2


def squares_to_move(start, end):

    horizontal_diff = ord(end[0]) - ord(start[0])

    vertical_diff = ord(end[1]) - ord(start[1])

    # R = RIGHT
    # D = DOWN
    # L = LEFT
    # U = UP

    first_half_move = str(HALF_SQUARE)+(" L" if horizontal_diff == 0 else " D")

    horizontal_cm = horizontal_diff*SQUARE
    
    vertical_cm = vertical_diff*SQUARE
    
    horizontal_cm = horizontal_cm if horizontal_cm == 0 else horizontal_cm+HALF_SQUARE
    
    vertical_cm = vertical_cm if vertical_cm == 0 else vertical_cm+HALF_SQUARE

    horizontal_move = str(abs(horizontal_cm)) + \
        (" L" if horizontal_diff < 0 else " R")
        
    vertical_move = str(abs(vertical_cm))+(" D" if vertical_diff < 0 else " U")

    return (first_half_move, horizontal_move, vertical_move)


# example usage
print(squares_to_move("c2", "e3"))
