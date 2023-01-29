SQUARE = 1
HALF_SQUARE = SQUARE/2
SARTING_POSITION = "a8"


def get_coordinates(position):
    horizontal_diff = ord(SARTING_POSITION[0]) - ord(position[0])
    vertical_diff = int(SARTING_POSITION[1:]) - int(position[1:])

    return [abs(vertical_diff*2)+1, abs(horizontal_diff*2)+1]


def squares_to_move(start, end):

    current_coordinates = get_coordinates(start)
    print("inicial", current_coordinates)
    end_coordinates = get_coordinates(end)

    horizontal_diff = ord(end[0]) - ord(start[0])

    vertical_diff = int(end[1:]) - int(start[1:])
    final_array = []

    # R = RIGHT
    # D = DOWN
    # L = LEFT
    # U = UP

    first_half_move = str(HALF_SQUARE)+(" L" if horizontal_diff == 0 else " D")

    if (horizontal_diff == 0):
        current_coordinates[1] -= 1
        print("andadinha", current_coordinates)
    else:
        current_coordinates[0] += 1
        print("andadinha", current_coordinates)
    final_array.append(current_coordinates)
    horizontal_cm = horizontal_diff*SQUARE

    vertical_cm = vertical_diff*SQUARE

    horizontal_cm = horizontal_cm if horizontal_cm == 0 else horizontal_cm+HALF_SQUARE

    vertical_cm = vertical_cm if vertical_cm == 0 else vertical_cm+HALF_SQUARE

    horizontal_move = str(abs(horizontal_cm)) + \
        (" L" if horizontal_diff < 0 else " R")

    vertical_move = str(abs(vertical_cm))+(" D" if vertical_diff < 0 else " U")

    if (horizontal_diff < 0):

        current_coordinates[1] -= abs(horizontal_cm)/HALF_SQUARE
    else:
        current_coordinates[1] += abs(horizontal_cm)/HALF_SQUARE

    print("primiro L", current_coordinates)
    final_array.append(current_coordinates)
    if (vertical_diff < 0):
        current_coordinates[0] += abs(vertical_cm)/HALF_SQUARE
    else:
        current_coordinates[0] -= abs(vertical_cm)/HALF_SQUARE

    print("segundo L", current_coordinates)
    final_array.append(current_coordinates)
    if end_coordinates[1] > current_coordinates[1]:
        current_coordinates[1] += 1
        print("andadinha", current_coordinates)
    else:
        current_coordinates[1] -= 1
        print("andadinha", current_coordinates)

    final_array.append(current_coordinates)
    # return (first_half_move, horizontal_move, vertical_move)
    return final_array


# example usage
print(squares_to_move("b1", "d3"))
# print(get_coordinates("c6"))
