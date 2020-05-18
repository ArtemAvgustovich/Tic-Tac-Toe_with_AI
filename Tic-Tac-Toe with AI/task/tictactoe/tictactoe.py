from random import choice

# class TicTacToe_AI:
#
#     def __init__(self, difficulty, side):
#         self.difficulty = difficulty
#         self.side = side

class TicTacToe:

    possible_cell_states = 'XO_'
    cell_map = {(1, 3): 0, (2, 3): 1, (3, 3): 2,
                (1, 2): 3, (2, 2): 4, (3, 2): 5,
                (1, 1): 6, (2, 1): 7, (3, 1): 8}
    lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]
    AI_difficulties = ["easy", "medium", "hard"]

    def __init__(self, cells=""):
        self.field = ['_' for _x in range(9)]
        self.empty_cells = [i for i in range(9)]

        # global variables for hard AI algorithm
        self.AI_side = None
        self.opponent_side = None
        self.empty_cells_choice = None


    def __str__(self):
        return f"""---------
| {' '.join([self.field[i] if self.field[i] in 'XO' else ' ' for i in range(3) ])} |
| {' '.join([self.field[i] if self.field[i] in 'XO' else ' ' for i in range(3, 6)])} |
| {' '.join([self.field[i] if self.field[i] in 'XO' else ' ' for i in range(6, 9)])} |
---------"""

    def __repr__(self):
        res = ''
        for i in range(3):
            for j in range(3):
                res += self.field[i*3+j]
            res += "\n"
        return res

    def move(self, player, side):
        if player in TicTacToe.AI_difficulties:
            return self.AI_move(player, side)
        else:
            return self.player_move(side)

    def AI_move(self, difficulty, side):
        if difficulty == "easy":
            print('Making move level "easy"')
            return self.easy_AI_move(side)
        if difficulty == "medium":
            print('Making move level "medium"')
            return self.medium_AI_move(side)
        if difficulty == "hard":
            print('Making move level "hard"')
            return self.hard_AI_move(side)

    def easy_AI_move(self, side):
        cell = choice(self.empty_cells)
        return self.put_sign(cell, side)

    def medium_AI_move(self, side):
        cell = self.find_pair(side)
        if isinstance(cell, int):
            return self.put_sign(cell, side)
        cell = self.find_pair("XO".replace(side, ""))
        if isinstance(cell, int):
            return self.put_sign(cell, side)
        return self.easy_AI_move(side)

    def hard_AI_move(self, side):
        self.opponent_side = "XO".replace(side, "")
        self.AI_side = side
        temp_field = self.field[:]
        cell = self.minimax(temp_field, side)[0]
        return self.put_sign(cell, side)

    def minimax(self, board, side):
        empty_cells = [i for i in range(9) if board[i] == "_"]

        if self.minimax_winning_check(self, board, self.AI_side):
            score = 10
            return [-1, score]
        elif self.minimax_winning_check(self, board, self.opponent_side):
            score = -10
            return [-1, score]
        elif not empty_cells:
            score = 0
            return [-1, score]

        if side == self.AI_side:
            best = [-1, -9999999]
        else:
            best = [-1, 9999999]

        for i in range(len(empty_cells)):
            cell = empty_cells[i]
            board[cell] = side
            if side == self.AI_side:
                score = self.minimax(board, self.opponent_side)
            else:
                score = self.minimax(board, self.AI_side)
            score[0] = cell
            board[cell] = '_'

            if side == self.AI_side:
                if score[1] > best[1]:
                    best = score
            elif side == self.opponent_side:
                if score[1] < best[1]:
                    best = score

        return best

    @staticmethod
    def minimax_winning_check(self, board, side):
        for line in TicTacToe.lines:
            if all(side == board[i] for i in line):
                return True
        else:
            return False

    def minimax_check_cell(self, board, index, side):
        for line in TicTacToe.lines:
            if index in line:
                if all(side == board[i] for i in line):
                    if side == self.AI_side:
                        self.empty_cells_choice[index] += 10
                    if side == self.opponent_side:
                        self.empty_cells_choice[index] -= 10
                    return True
        else:
            if board.count("_") == 0:
                return True
            else:
                return False

    def find_pair(self, side):
        for line in TicTacToe.lines:
            strip = [self.field[i] for i in line]
            if strip.count(side) == 2 and strip.count("_") == 1:
                return line[strip.index("_")]
        else:
            return None

    def player_move(self, side):
        try:
            coor = tuple(map(int, input("Enter the coordinates:").split(maxsplit=1)))
            cell = TicTacToe.cell_map[coor]
            if cell not in self.empty_cells:
                print("This cell is occupied! Choose another one!")
                return self.player_move(side)
            else:
                return self.put_sign(cell, side)
        except ValueError:
            print("You should enter numbers!")
            return self.player_move(side)
        except KeyError:
            print("Coordinates should be from 1 to 3!")
            return self.player_move(side)

    def put_sign(self, cell, side):
        self.field[cell] = side
        self.empty_cells.remove(cell)
        if self.check_cell(cell, side):
            return True
        else:
            return False

    # check all lines that contain cell with [index], used after adding element
    def check_cell(self, index, side):
        for line in TicTacToe.lines:
            if index in line:
                if all(side == self.field[i] for i in line):
                    print(self)
                    print(f"{side} wins\n")
                    return True
        else:
            print(self)
            if self.field.count("_") == 0:
                print("Draw")
                return True
            else:
                return False

    # Not used in this version
    def check_field(self):
        for line in TicTacToe.lines:
            line = "".join([self.field[i] for i in line])
            if line == "XXX":
                print(self)
                print("X wins\n")
                return
            elif line == "OOO":
                print(self)
                print("O wins\n")
                return
        else:
            print(self)
            print("Draw\n")

    def empty_field(self):
        self.field = self.field = ['_' for _x in range(9)]
        self.empty_cells = [i for i in range(9)]

    def play_game(self, player1, player2):
        print(self)
        while True:
            if self.move(player1, "X"):
                break
            if self.move(player2, "O"):
                break
        self.empty_field()

    def main_menu(self):
        while True:
            command = input("Input command: ")
            try:
                if command == "exit":
                    break
                command = command.split(maxsplit=2)
                if command[0] == "start":
                    if all(player in TicTacToe.AI_difficulties or player == 'user'
                           for player in command[1:3]):
                        player1 = command[1]
                        player2 = command[2]
                        self.play_game(player1, player2)
                    else:
                        raise ValueError
                else:
                    raise ValueError
            except (ValueError, TypeError, IndexError, KeyError):
                print("Bad parameters!")


def main():
    game = TicTacToe()
    game.main_menu()


if __name__ == "__main__":
    main()
