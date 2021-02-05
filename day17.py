from collections import Counter
from itertools import product

test = """
.#.
..#
###
""".strip().split('\n')


def get_data():
    with open('inputs\\day17.txt') as file:
        return [line.strip() for line in file]


class Conway:

    def __init__(self, config):
        self.state = {}
        for y, line in enumerate(config):
            for x, cell in enumerate(line):
                self.state[(x, y, 0)] = cell
        self.deltas = set(product([-1, 0, 1], repeat=3))
        self.deltas.remove((0, 0, 0))

        x_max = len(config[0])
        y_max = len(config)
        z_max = 1
        self.min_dimensions = (0, 0, 0)
        self.max_dimensions = (x_max, y_max, z_max)

    def active_cells(self):
        return Counter(self.state.values())['#']

    def get_next_state(self, *coordinates):
        neighbors = Counter()
        for delta_coordinates in self.deltas:
            neighbor_coordinates = tuple(
                c + dc for c, dc in zip(coordinates, delta_coordinates)
            )
            neighbor_cell = self.state.setdefault(neighbor_coordinates, '.')
            neighbors.update(neighbor_cell)
        current_cell = self.state.setdefault(coordinates, '.')
        active_neighbors = neighbors['#']
        if current_cell == '#' and (2 <= active_neighbors <= 3):
            return '#'
        elif current_cell == '.' and active_neighbors == 3:
            return '#'
        else:
            return '.'

    def next_step(self):
        x_min, y_min, z_min = [d - 1 for d in self.min_dimensions]
        x_max, y_max, z_max = [d + 1 for d in self.max_dimensions]
        new_state = {}
        for z in range(z_min, z_max):
            for y in range(y_min, y_max):
                for x in range(x_min, x_max):
                    new_cell = self.get_next_state(x, y, z)
                    new_state[(x, y, z)] = new_cell
        self.min_dimensions = (x_min, y_min, z_min)
        self.max_dimensions = (x_max, y_max, z_max)
        self.state = new_state


class Conway4D(Conway):

    def __init__(self, config):
        self.state = {}
        for y, line in enumerate(config):
            for x, cell in enumerate(line):
                self.state[(x, y, 0, 0)] = cell
        self.deltas = set(product([-1, 0, 1], repeat=4))
        self.deltas.remove((0, 0, 0, 0))

        x_max = len(config[0])
        y_max = len(config)
        z_max = w_max = 1
        self.min_dimensions = (0, 0, 0, 0)
        self.max_dimensions = (x_max, y_max, z_max, w_max)
        self.step = 0

    def next_step(self):
        x_min, y_min, z_min, w_min = [d - 1 for d in self.min_dimensions]
        x_max, y_max, z_max, w_max = [d + 1 for d in self.max_dimensions]
        new_state = {}
        for w in range(w_min, w_max):
            for z in range(z_min, z_max):
                for y in range(y_min, y_max):
                    for x in range(x_min, x_max):
                        new_cell = self.get_next_state(x, y, z, w)
                        new_state[(x, y, z, w)] = new_cell
        self.min_dimensions = (x_min, y_min, z_min, w_min)
        self.max_dimensions = (x_max, y_max, z_max, w_max)
        self.state = new_state


def get_first_star(data):
    game = Conway(data)
    for _ in range(6):
        game.next_step()
    return game.active_cells()


def get_second_star(data):
    game = Conway4D(data)
    for _ in range(6):
        game.next_step()
    return game.active_cells()


assert get_first_star(test) == 112
print(get_first_star(get_data()))

assert get_second_star(test) == 848
print(get_second_star(get_data()))
