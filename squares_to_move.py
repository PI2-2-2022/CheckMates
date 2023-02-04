SQUARE = 5
HALF_SQUARE = SQUARE / 2
MINIMUM_WALK= 0.5
SARTING_POSITION = "a8"
from Communication import Communication
x_atual = 0
y_atual = 0
communication = Communication()

def get_coordinates(position):
    horizontal_diff = ord(SARTING_POSITION[0]) - ord(position[0])
    vertical_diff = int(SARTING_POSITION[1:]) - int(position[1:])

    return [abs(vertical_diff)*SQUARE + HALF_SQUARE, abs(horizontal_diff)*SQUARE + HALF_SQUARE]

def get_position_from_coordinates(x,y):
    x_axis = int(x)*MINIMUM_WALK
    y_axis = int(y)*MINIMUM_WALK
    print(x_axis,y_axis)
    columns = "abcdefgh"
    rows= ['8','7','6','5','4','3','2','1']
    return columns[x] + rows[y]
    

def squares_to_move(start, end):
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
        current_coordinates[1] -= HALF_SQUARE
        print("andadinha", current_coordinates)
    else:
        current_coordinates[0] += HALF_SQUARE
        print("andadinha", current_coordinates)
    final_array.append(current_coordinates)
    
    #Acaba aqui o primeiro movimento
    
    horizontal_cm = horizontal_diff * SQUARE

    vertical_cm = vertical_diff * SQUARE

    horizontal_cm = horizontal_cm if horizontal_cm == 0 else horizontal_cm + HALF_SQUARE

    vertical_cm = HALF_SQUARE if vertical_cm == 0 else vertical_cm + HALF_SQUARE

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

        current_coordinates[1] -= abs(horizontal_cm)
    else:
        current_coordinates[1] += abs(horizontal_cm)

    print("primiro L", current_coordinates)
    
    final_array.append(current_coordinates)
    if (vertical_diff < 0):
        current_coordinates[0] += abs(vertical_cm)
    else:
        current_coordinates[0] -= abs(vertical_cm)

    print("segundo L", current_coordinates)
    final_array.append(current_coordinates)

    if end_coordinates[1] > current_coordinates[1]:
        current_coordinates[1] += HALF_SQUARE
        print("andadinha", current_coordinates)
    else:
        current_coordinates[1] -= HALF_SQUARE
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
    return [
        first_half_move_string, horizontal_move_string, vertical_move_string,
        last_half_move_string
    ]


# example usage
# print(squares_to_move("a7", "d4"))

def calibra():
    communication.simple_comm("900",2)
    print("calibrado")
    x_atual = 0
    y_atual = 0
    return 

def move_piece(start, end):
    
    
    # resp = communication.simple_comm("900",2)
    # resp = communication.simple_comm("530",3)
    # resp = communication.simple_comm("600",2)
    # resp = communication.simple_comm("330",200)
    squares_to_move("a8","d5")
    
def set_cnc_on_piece(place_to_go):
    local_now = communication.simple_comm("600",2)
    print("local atual = ", local_now)
    to_go = get_coordinates(place_to_go)
    x_to_go = to_go[1]/MINIMUM_WALK
    x_to_go = x_to_go if (x_to_go)<=70 else 70
    Y_to_go = to_go[0]/MINIMUM_WALK
    Y_to_go = Y_to_go if (Y_to_go)<=70 else 70
    print("quero ir: ", to_go)
    print("quero ir passos: ", x_to_go,Y_to_go)
    x_to_move = x_to_go - int(local_now[0][0])
    y_to_move = Y_to_go - int(local_now[0][1])
    print("temos que andar: x", x_to_move, " y", y_to_move)
    x_final=''
    y_final=''
    if(x_to_move>0):
        x_final = '3'+str(int(abs(x_to_move))).rjust(2, '0')
    else:
        x_final = '1'+str(int(abs(x_to_move))).rjust(2, '0')
        
    if(y_to_move>0):
        y_final = '5'+str(int(abs(y_to_move) if abs(y_to_move)<=70 else 70)).rjust(2, '0')
    else:
        y_final = '2'+str(int(abs(y_to_move) if abs(y_to_move)<=70 else 70)).rjust(2, '0')
        
    print(to_go)
    print("tem que andar", x_final, y_final)
    communication.simple_comm(x_final,3)
    communication.simple_comm(y_final,3)
    
    
    

def teste():
    calibra()
    set_cnc_on_piece('c8')
    communication.simple_comm("400",2)
    squares = squares_to_move("c8","h8")
    for square in squares:
        resp = communication.simple_comm(square,3)
    communication.simple_comm("400",2)    
    return  
# print(get_coordinates("c6"))]
# print(get_coordinates("b7"))
teste()

