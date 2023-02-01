SQUARE = 5
HALF_SQUARE = SQUARE / 2
MINIMUM_WALK= 0.5
SARTING_POSITION = "a8"
from Communication import Communication


def get_coordinates(position):
    horizontal_diff = ord(SARTING_POSITION[0]) - ord(position[0])
    vertical_diff = int(SARTING_POSITION[1:]) - int(position[1:])

    return [abs(vertical_diff*2)+1, abs(horizontal_diff*2)+1]


def squares_to_move(start, end):
    communication = Communication()
    current_coordinates = get_coordinates(start)
    print("inicial", current_coordinates)
    end_coordinates = get_coordinates(end)

    horizontal_diff = ord(end[0]) - ord(start[0])

    vertical_diff = int(end[1:]) - int(start[1:])
    final_array = []

    Moviments_dict = {"R": "3", "D": "5", "L": "1", "U": "2"}
    
    # R = RIGHT
    # D = DOWN
    # L = LEFT
    # U = UP

    first_half_move = str(HALF_SQUARE) + (" L"
                                          if horizontal_diff == 0 else " D")
    first_half_move_string = (Moviments_dict["L"] if horizontal_diff == 0 else
                              Moviments_dict["D"]) + str(
                                  int(HALF_SQUARE / MINIMUM_WALK)).rjust(
                                      2, '0')

    if (horizontal_diff == 0):
        current_coordinates[1] -= 1
        print("andadinha", current_coordinates)
    else:
        current_coordinates[0] += 1
        print("andadinha", current_coordinates)
    final_array.append(current_coordinates)
    horizontal_cm = horizontal_diff * SQUARE

    vertical_cm = vertical_diff * SQUARE

    horizontal_cm = horizontal_cm if horizontal_cm == 0 else horizontal_cm + HALF_SQUARE

    vertical_cm = vertical_cm if vertical_cm == 0 else vertical_cm + HALF_SQUARE

    horizontal_move = str(abs(horizontal_cm)) + \
        (" L" if horizontal_diff < 0 else " R")

    horizontal_move_string = (Moviments_dict["L"] if horizontal_diff < 0 else
                              Moviments_dict["R"]) + str(
                                  int(abs(horizontal_cm / MINIMUM_WALK))).rjust(
                                      2, '0')

    vertical_move = str(
        abs(vertical_cm)) + (" D" if vertical_diff < 0 else " U")

    vertical_move_string = (Moviments_dict["D"] if vertical_diff < 0 else
                            Moviments_dict["U"]) + str(
                                int(abs(vertical_cm / MINIMUM_WALK))).rjust(
                                    2, '0')

    if (horizontal_diff < 0):

        current_coordinates[1] -= abs(horizontal_cm) / HALF_SQUARE
    else:
        current_coordinates[1] += abs(horizontal_cm) / HALF_SQUARE

    print("primiro L", current_coordinates)
    final_array.append(current_coordinates)
    if (vertical_diff < 0):
        current_coordinates[0] += abs(vertical_cm) / MINIMUM_WALK
    else:
        current_coordinates[0] -= abs(vertical_cm) / MINIMUM_WALK

    print("segundo L", current_coordinates)
    final_array.append(current_coordinates)

    if end_coordinates[1] > current_coordinates[1]:
        current_coordinates[1] += 1
        print("andadinha", current_coordinates)
    else:
        current_coordinates[1] -= 1
        print("andadinha", current_coordinates)

    last_half_move = str(HALF_SQUARE) + (
        " R" if end_coordinates[1] > current_coordinates[1] else " L")
    last_half_move_string = (Moviments_dict["R"]
                             if end_coordinates[1] > current_coordinates[1]
                             else Moviments_dict["L"]) + str(
                                 int(HALF_SQUARE / MINIMUM_WALK)).rjust(2, '0')

    final_array.append(current_coordinates)
    print(first_half_move, " ", first_half_move_string)
    print(horizontal_move, " ", horizontal_move_string)
    print(vertical_move, " ", vertical_move_string)
    print(last_half_move, " ", last_half_move_string)
    # return final_array
    # print(final_array)
    communication.test_serializer_comunication("502")
    return [
        first_half_move_string, horizontal_move_string, vertical_move_string,
        last_half_move_string
    ]


# example usage
print(squares_to_move("a7", "d4"))
# print(get_coordinates("c6"))
