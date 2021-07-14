import json
import copy

# noinspection PyTypeChecker
class State:
    def __init__(self, state_matrix, walls, t_cords, non_terminal):
        self.non_terminal = non_terminal
        self.matrix = state_matrix
        self.maxX = len(self.matrix[0])
        self.maxY = len(self.matrix)
        self.cord = (0, 0)
        self.walls = walls
        self.t_cords = t_cords

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.matrix == self.matrix
        return False

    def __str__(self):
        return str(self.matrix)

    def value_at(self, n_cord):
        if n_cord[0] < 0 or n_cord[0] >= self.maxX or n_cord[1] < 0 or n_cord[1] >= self.maxY:
            return 0.0
        elif n_cord in self.walls:
            return 0.0
        else:
            return self.matrix[n_cord[1]][n_cord[0]]

    def up_val(self):
        return self.value_at((self.cord[0], self.cord[1] + 1))

    def down_val(self):
        return self.value_at((self.cord[0], self.cord[1] - 1))

    def right_val(self):
        return self.value_at((self.cord[0] + 1, self.cord[1]))

    def left_val(self):
        return self.value_at((self.cord[0] - 1, self.cord[1]))

    def move_up(self,):
        up_prob = 0.8 * self.up_val()
        left_prob = 0.1 * self.left_val()
        right_prob = 0.1 * self.right_val()
        return up_prob + left_prob + right_prob

    def move_down(self,):
        down_prob = 0.8 * self.down_val()
        left_prob = 0.1 * self.left_val()
        right_prob = 0.1 * self.right_val()
        return down_prob + left_prob + right_prob

    def move_right(self,):
        right_prob = 0.8 * self.right_val()
        up_prob = 0.1 * self.up_val()
        down_prob = 0.1 * self.down_val()
        return right_prob + up_prob + down_prob

    def move_left(self,):
        left_prob = 0.8 * self.left_val()
        up_prob = 0.1 * self.up_val()
        down_prob = 0.1 * self.down_val()
        return left_prob + up_prob + down_prob

    def is_terminal_cord(self, cords):
        for t_cord in self.t_cords:
            if cords[0] == t_cord[0] and cords[1] == t_cord[1]:
                return True
        return False

    def eval(self):
        x = 0
        y = 0
        delta = 0
        for y in range(0, self.maxY):
            for x in range(0, self.maxX):
                self.cord = (x, y)
                if self.is_terminal_cord(self.cord) or (self.cord in self.walls):
                    pass
                else:
                    moves_val = [self.move_up(), self.move_down(), self.move_right(), self.move_left(),
                                self.value_at(self.cord)]
                    new_val = max(moves_val) - self.non_terminal
                    delta = max([delta, new_val - self.matrix[y][x]])
                    self.matrix[y][x] = new_val
        return delta

def adjust_cords(cords):
    if len(cords) == 3:
        return (cords[0]-1, cords[1]-1, cords[2])
    else:
        return (cords[0]-1, cords[1]-1)


class Grid:
    def __init__(self, board_config):
        self.grid_size_x = board_config["size"]["x"]
        self.grid_size_y = board_config["size"]["y"]
        self.wall_space = [adjust_cords((wall["x"], wall["y"])) for wall in board_config["walls"]]
        self.terminal_cords = [adjust_cords((state['x'], state['y'], state["value"])) for state in board_config["terminal_cords"]]
        self.non_terminal = board_config["reward"]
        self.transitions = board_config["transitions"]
        self.discount_rate = board_config["discount_rate"]
        self.epsilon = board_config["epsilon"]
        self.states = []
        grid = [[0 for x in range(0, self.grid_size_x)] for y in range(0, self.grid_size_y)]

        for wall in self.wall_space:
            grid[wall[1]][wall[0]] = "w"

        for t_cord in self.terminal_cords:
            grid[t_cord[1]][t_cord[0]] = float(t_cord[2])

        self.states.append(State(grid, self.wall_space, self.terminal_cords, self.non_terminal))

    def __str__(self):

        for state in self.states:
            for row in reversed(state.matrix):
                print(row)
            print("-")
        return str((self.grid_size_x, self.grid_size_y)) + ", states: " + str(len(self.states))

    def mdp(self):
        delta = 0
        while True:
            candidate_state = copy.deepcopy(self.states[-1])
            if delta == candidate_state.eval():
                break
            delta = candidate_state.eval()
            self.states.append(candidate_state)
        print("mdp Complete")


with open("input.json", "r") as read_file:
    data = json.load(read_file)

test = Grid(data)
test.mdp()

print(test)