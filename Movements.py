from Communication import Communication

communication = Communication()

chessboard = {
    "a8": [5, 0],
    "b8": [15, 0],
    "c8": [25, 0],
    "d8": [35, 0],
    "e8": [45, 0],
    "f8": [55, 0],
    "g8": [65, 0],
    "h8": [75, 0],
    "a7": [5, 10],
    "b7": [15, 10],
    "c7": [25, 10],
    "d7": [35, 10],
    "e7": [45, 10],
    "f7": [55, 10],
    "g7": [65, 10],
    "h7": [75, 10],
    "a6": [5, 20],
    "b6": [15, 20],
    "c6": [25, 20],
    "d6": [35, 20],
    "e6": [45, 20],
    "f6": [55, 20],
    "g6": [65, 20],
    "h6": [75, 20],
    "a5": [5, 30],
    "b5": [15, 30],
    "c5": [25, 30],
    "d5": [35, 30],
    "e5": [45, 30],
    "f5": [55, 30],
    "g5": [65, 30],
    "h5": [75, 30],
    "a4": [5, 40],
    "b4": [15, 40],
    "c4": [25, 40],
    "d4": [35, 40],
    "e4": [45, 40],
    "f4": [55, 40],
    "g4": [65, 40],
    "h4": [75, 40],
    "a3": [5, 50],
    "b3": [15, 50],
    "c3": [25, 50],
    "d3": [35, 50],
    "e3": [45, 50],
    "f3": [55, 50],
    "g3": [65, 50],
    "h3": [75, 50],
    "a2": [5, 60],
    "b2": [15, 60],
    "c2": [25, 60],
    "d2": [35, 60],
    "e2": [45, 60],
    "f2": [55, 60],
    "g2": [65, 60],
    "h2": [75, 60],
    "a1": [5, 70],
    "b1": [15, 70],
    "c1": [25, 70],
    "d1": [35, 70],
    "e1": [45, 70],
    "f1": [55, 70],
    "g1": [65, 70],
    "h1": [75, 70],
    "h1": [75, 70],
}
offset = 30
chessboard_with_offset = {
    "a8": [5 + offset, 0],
    "b8": [15 + offset, 0],
    "c8": [25 + offset, 0],
    "d8": [35 + offset, 0],
    "e8": [45 + offset, 0],
    "f8": [55 + offset, 0],
    "g8": [65 + offset, 0],
    "h8": [75 + offset, 0],
    "a7": [5 + offset, 10],
    "b7": [15 + offset, 10],
    "c7": [25 + offset, 10],
    "d7": [35 + offset, 10],
    "e7": [45 + offset, 10],
    "f7": [55 + offset, 10],
    "g7": [65 + offset, 10],
    "h7": [75 + offset, 10],
    "a6": [5 + offset, 20],
    "b6": [15 + offset, 20],
    "c6": [25 + offset, 20],
    "d6": [35 + offset, 20],
    "e6": [45 + offset, 20],
    "f6": [55 + offset, 20],
    "g6": [65 + offset, 20],
    "h6": [75 + offset, 20],
    "a5": [5 + offset, 30],
    "b5": [15 + offset, 30],
    "c5": [25 + offset, 30],
    "d5": [35 + offset, 30],
    "e5": [45 + offset, 30],
    "f5": [55 + offset, 30],
    "g5": [65 + offset, 30],
    "h5": [75 + offset, 30],
    "a4": [5 + offset, 40],
    "b4": [15 + offset, 40],
    "c4": [25 + offset, 40],
    "d4": [35 + offset, 40],
    "e4": [45 + offset, 40],
    "f4": [55 + offset, 40],
    "g4": [65 + offset, 40],
    "h4": [75 + offset, 40],
    "a3": [5 + offset, 50],
    "b3": [15 + offset, 50],
    "c3": [25 + offset, 50],
    "d3": [35 + offset, 50],
    "e3": [45 + offset, 50],
    "f3": [55 + offset, 50],
    "g3": [65 + offset, 50],
    "h3": [75 + offset, 50],
    "a2": [5 + offset, 60],
    "b2": [15 + offset, 60],
    "c2": [25 + offset, 60],
    "d2": [35 + offset, 60],
    "e2": [45 + offset, 60],
    "f2": [55 + offset, 60],
    "g2": [65 + offset, 60],
    "h2": [75 + offset, 60],
    "a1": [5 + offset, 70],
    "b1": [15 + offset, 70],
    "c1": [25 + offset, 70],
    "d1": [35 + offset, 70],
    "e1": [45 + offset, 70],
    "f1": [55 + offset, 70],
    "g1": [65 + offset, 70],
    "h1": [75 + offset, 70],
    "m01": [5, 0],
    "m02": [5, 10],
    "m03": [5, 20],
    "m04": [5, 30],
    "m05": [5, 40],
    "m06": [5, 50],
    "m07": [5, 60],
    "m08": [5, 70],
    "m09": [15, 0],
    "m10": [15, 10],
    "m11": [15, 20],
    "m12": [15, 30],
    "m13": [15, 40],
    "m14": [15, 50],
    "m15": [15, 60],
    "m16": [15, 70],
}

chessboard = chessboard_with_offset


class Movements:
    def __init__(self) -> None:
        pass

    def calibra(self):
        # print("calibrado")
        communication.simple_comm("9000", 2)
        return

    def set_cnc_on_piece(self, place_to_go):
        local_now = communication.simple_comm("6000", 2)
        # print("local atual = ", local_now)
        to_go = chessboard[place_to_go]
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
        # print(start, end)
        current_coordinates = chessboard[start]
        # print("inicial", current_coordinates)
        end_coordinates = chessboard[end]
        # print("final", end_coordinates)

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
