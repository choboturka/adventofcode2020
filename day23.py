from collections import deque
from dataclasses import dataclass

test = '389125467'


def get_data():
    with open('inputs\\day23.txt') as file:
        return file.read().strip()


class Game:
    def __init__(self, labels):
        numbers = [int(label) for label in labels]
        self.cups = deque(numbers)
        self.current_cup = self.cups[0]
        self.min_cup = min(numbers)
        self.max_cup = max(numbers)
        self.picked_cups = []

    def cycle_one(self):
        self.cups.append(self.cups.popleft())

    def pick_cups(self):
        self.cycle_one()
        for _ in range(3):
            self.picked_cups.append(self.cups.popleft())

    def chose_destination(self):
        cup_to_try = self.current_cup
        while True:
            cup_to_try -= 1
            if cup_to_try < self.min_cup:
                cup_to_try = self.max_cup
            if cup_to_try not in self.picked_cups:
                return cup_to_try

    def push_cups(self, destination):
        while self.cups[-1] != destination:
            self.cycle_one()
        for cup in self.picked_cups:
            self.cups.append(cup)
        self.picked_cups = []
        while self.cups[-1] != self.current_cup:
            self.cycle_one()

    def move(self):
        self.pick_cups()
        destination = self.chose_destination()
        self.push_cups(destination)
        self.current_cup = self.cups[0]

    def final_state(self):
        while self.cups[0] != 1:
            self.cycle_one()
        self.cups.popleft()
        return "".join([str(cup) for cup in self.cups])

    def play(self, moves=100):
        for _ in range(moves):
            self.move()


MEMORY = {}
MAX_RANGE = 101


@dataclass
class Node:
    value: int
    next_address: int


class BigGame:
    def __init__(self, numbers):
        total_cups = 1_000_000
        all_nums = [int(n) for n in numbers] + list(range(10, total_cups + 1))
        self.memory = {
            address: Node(value, (address + 1) % total_cups) for address, value in enumerate(all_nums)
        }
        self.search_index = {node.value: address for address, node in self.memory.items()}
        self.current_pointer = 0

    @property
    def head(self):
        return self.memory[self.current_pointer]

    def next(self, node):
        return self.memory[node.next_address]

    def pick_3(self):
        head_node = self.head
        pointer_to_first = head_node.next_address
        first_node = self.next(head_node)
        second_node = self.next(first_node)
        third_node = self.next(second_node)
        pointer_to_last = second_node.next_address
        head_node.next_address = third_node.next_address
        third_node.next_address = None
        values = (first_node.value, second_node.value, third_node.value)
        return pointer_to_first, pointer_to_last, values

    def chose_destination(self, picked_values):
        destination = self.head.value
        while True:
            destination -= 1
            if destination < 1:
                destination = 1_000_000
            if destination not in picked_values:
                return destination

    def insert_nodes(self, destination, pointer_to_first, pointer_to_last):
        dest_address = self.search_index[destination]
        node = self.memory[dest_address]
        tmp_address = node.next_address
        node.next_address = pointer_to_first
        last_node = self.memory[pointer_to_last]
        last_node.next_address = tmp_address

    def move(self):
        first, last, values = self.pick_3()
        destination = self.chose_destination(values)
        self.insert_nodes(destination, first, last)
        self.current_pointer = self.head.next_address

    def play(self):
        for i in range(10_000_000):
            if i % 1_000_000 == 0:
                print(f'{i} moves made')
            self.move()
        one_node_address = self.search_index[1]
        one_node = self.memory[one_node_address]
        first_star_node = self.next(one_node)
        second_star_node = self.next(first_star_node)
        return first_star_node.value * second_star_node.value


def get_first_star(data):
    game = Game(data)
    game.play()
    return game.final_state()


def get_second_star(data):
    game = BigGame(data)
    return game.play()


assert get_first_star(test) == '67384529'
print(get_first_star(get_data()))
print(get_second_star(get_data()))
