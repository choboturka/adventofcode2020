from collections import deque
from dataclasses import dataclass


test_input = """
F10
N3
F7
R90
F11
""".strip().split('\n')


@dataclass
class Vector:
    x: int
    y: int

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y
        )

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return Vector(
            self.x * other,
            self.y * other
        )

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def rotate_90_left(self):
        self.x, self.y = -self.y, self.x

    def rotate_90_right(self):
        self.x, self.y = self.y, -self.x

    def rotate_180(self):
        self.x, self.y = -self.x, -self.y
        # return self


def get_input():
    with open('inputs\\day12.txt') as file:
        return [line.strip() for line in file]


BASIS_VECTORS = {
    'N': Vector(0, 1),
    'S': Vector(0, -1),
    'E': Vector(1, 0),
    'W': Vector(-1, 0)
}


class Ship:
    def __init__(self, instructions):
        self.compass = deque(['E', 'S', 'W', 'N'])
        self.position = Vector(0, 0)
        self.waypoint = Vector(10, 1)
        self.instructions = []
        for line in instructions:
            self.instructions.append((line[0], int(line[1:])))

    def get_facing_direction(self):
        return self.compass[0]

    def rotate_ship(self, direction, degrees):
        discrete_turns = degrees // 90
        for _ in range(discrete_turns):
            if direction == 'L':
                self.compass.appendleft(self.compass.pop())
            elif direction == 'R':
                self.compass.append(self.compass.popleft())
            else:
                raise AttributeError('Unknown direction')

    def move_ship(self, direction, amount):
        if direction == 'F':
            direction = self.get_facing_direction()
        self.position += BASIS_VECTORS[direction] * amount

    def get_manhattan_distance(self):
        return abs(self.position)

    def run(self):
        for command, value in self.instructions:
            if command in 'LR':
                self.rotate_ship(command, value)
            elif command in 'FESWN':
                self.move_ship(command, value)
            else:
                raise AttributeError('Unknown command')
        return self.get_manhattan_distance()

    def move_waypoint(self, direction, amount):
        self.waypoint += BASIS_VECTORS[direction] * amount

    def move_to_waypoint(self, distance):
        for _ in range(distance):
            self.position += self.waypoint

    def rotate_waypoint(self, direction, degrees):
        # rotate counter-clockwise around zero
        if degrees == 180:
            self.waypoint.rotate_180()
        elif degrees == 90 and direction == 'R':
            self.waypoint.rotate_90_right()
        elif degrees == 90 and direction == 'L':
            self.waypoint.rotate_90_left()
        elif degrees == 270 and direction == 'R':
            self.waypoint.rotate_90_left()
        elif degrees == 270 and direction == 'L':
            self.waypoint.rotate_90_right()

    def run_waypoint(self):
        for command, value in self.instructions:
            if command in 'LR':
                self.rotate_waypoint(command, value)
            elif command in 'NESW':
                self.move_waypoint(command, value)
            elif command == 'F':
                self.move_to_waypoint(value)
            else:
                raise AttributeError

        return self.get_manhattan_distance()


def get_first_star(data):
    return Ship(data).run()


def get_second_star(data):
    return Ship(data).run_waypoint()


assert get_first_star(test_input) == 25
print(get_first_star(get_input()))

assert get_second_star(test_input) == 286
print(get_second_star(get_input()))


