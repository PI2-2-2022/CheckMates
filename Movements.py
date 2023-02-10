from Communication import Communication

communication = Communication()

class Movements:
    offset = 30

    def __init__(self) -> None:
        pass

    def calibra(self):
        # print("calibrado")
        communication.simple_comm("9000", 2)
        return

    def move_to_coords(self, move):
        if move[0] == 'm':
            num = int(move[1:])
            x = 5 if(num < 9) else 15
            y = (num + 1) * 10 if(num < 9) else (num - 7) * 10 
            return [x, y]

        column = ord(move[0]) - ord('a') + 1
        row = int(move[1])
        x = (5 + column * 10) - 10
        y = (8 - row) * 10
        return [x + self.offset, y]

    def set_cnc_on_piece(self, place_to_go):
        local_now = communication.simple_comm("6000", 2)
        # print("local atual = ", local_now)
        to_go = self.move_to_coords(place_to_go)
        x_to_go = to_go[0]
        Y_to_go = to_go[1]
        # print("quero ir: ", to_go)
        # print("quero ir passos: ", x_to_go, Y_to_go)
        x_to_move = x_to_go - int(local_now[0][0])
        y_to_move = Y_to_go - int(local_now[0][1])
        # print("temos que andar: x", x_to_move, " y", y_to_move)
        x_final = ""
        y_final = ""
        if x_to_move > 0:
            x_final = "3" + str(int(abs(x_to_move))).rjust(3, "0")
        else:
            x_final = "1" + str(int(abs(x_to_move))).rjust(3, "0")

        if y_to_move > 0:
            y_final = "5" + str(
                int(abs(y_to_move) if abs(y_to_move) <= 70 else 70)
            ).rjust(3, "0")
        else:
            y_final = "2" + str(
                int(abs(y_to_move) if abs(y_to_move) <= 70 else 70)
            ).rjust(3, "0")

        # print(to_go)
        # print("tem que andar", x_final, y_final)
        if x_final != "100" and x_final != "300":
            communication.simple_comm(x_final, 3)
        if y_final != "200" and y_final != "500":
            communication.simple_comm(y_final, 3)

    def squares_to_move(self, start, end):
        # set_cnc_on_piece(start)
        current_coordinates = self.move_to_coords(start)
        end_coordinates = self.move_to_coords(end)

        horizontal_diff = end_coordinates[0] - current_coordinates[0]

        vertical_diff = end_coordinates[1] - current_coordinates[1]

        Movements_dict = {"R": "3", "D": "5", "L": "1", "U": "2"}

        # R = RIGHT
        # D = DOWN
        # L = LEFT
        # U = UP

        if horizontal_diff == 0:
            first_half_move = "5 L"
            first_half_move_string = Movements_dict["L"] + "005"
            current_coordinates[0] -= 5
        else:
            if start[1] == "1":
                first_half_move = "5 U"
                first_half_move_string = Movements_dict["U"] + "005"
                current_coordinates[1] -= 5
            else:
                first_half_move = "5 D"
                first_half_move_string = Movements_dict["D"] + "005"
                current_coordinates[1] += 5
        # print(first_half_move)
        # print(current_coordinates)
        # Acaba aqui o primeiro movimento

        if horizontal_diff != 0:
            horizontal_diff = (end_coordinates[0] - current_coordinates[0]) + 5

        vertical_diff = end_coordinates[1] - current_coordinates[1]

        if horizontal_diff < 0:
            horizontal_move = str(abs(horizontal_diff)) + " L"
            horizontal_move_string = Movements_dict["L"] + str(
                abs(horizontal_diff)
            ).rjust(3, "0")
            current_coordinates[0] -= abs(horizontal_diff)
        else:
            horizontal_move = str(abs(horizontal_diff)) + " R"
            horizontal_move_string = Movements_dict["R"] + str(
                abs(horizontal_diff)
            ).rjust(3, "0")
            current_coordinates[0] += abs(horizontal_diff)

        # print(horizontal_move)
        # print(current_coordinates)

        if vertical_diff < 0:
            vertical_move = str(abs(vertical_diff)) + " U"
            vertical_move_string = Movements_dict["U"] + str(abs(vertical_diff)).rjust(
                3, "0"
            )
            current_coordinates[1] -= abs(vertical_diff)
        else:
            vertical_move = str(abs(vertical_diff)) + " D"
            vertical_move_string = Movements_dict["D"] + str(abs(vertical_diff)).rjust(
                3, "0"
            )
            current_coordinates[1] += abs(vertical_diff)

        # print(vertical_move)
        # print(current_coordinates)

        if end_coordinates[0] > current_coordinates[0]:
            last_half_move = "5 R"
            last_half_move_string = Movements_dict["R"] + "005"
            current_coordinates[0] += 5
        else:
            last_half_move = "5 L"
            last_half_move_string = Movements_dict["L"] + "005"
            current_coordinates[0] -= 5

        # print(last_half_move)
        # print(current_coordinates)

        return [
            first_half_move_string,
            horizontal_move_string,
            vertical_move_string,
            last_half_move_string,
        ]

    def game_movement(self, move):
        start = move[:2]
        end = move[2:]
        # print("chegou", start, end)
        self.set_cnc_on_piece(start)
        communication.simple_comm("4000", 2)
        # print("vai ser", start, end)
        squares = self.squares_to_move(start, end)
        # print('squares: ', squares)
        for square in squares:
            if (
                square != "100"
                and square != "200"
                and square != "300"
                and square != "500"
            ):
                resp = communication.simple_comm(square, 3)
        communication.simple_comm("4000", 2)
        return
