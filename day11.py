from collections import Counter

test_input = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
""".strip().split('\n')


def get_input():
    with open('inputs\\day11.txt') as file:
        return [line.strip() for line in file]


class Layout:
    def __init__(self, seats):
        self.layout = {}
        self.max_row = len(seats)
        self.max_column = len(seats[0])
        for row_number, row in enumerate(seats):
            for seat_number, seat in enumerate(row):
                self.layout[(row_number, seat_number)] = seat

    def get_next_generation(self, row, column):
        neighbors = Counter()
        for r in [row - 1, row, row + 1]:
            for c in [column - 1, column, column + 1]:
                if (r, c) == (row, column):
                    continue
                if r < 0 or r >= self.max_row:
                    continue
                if c < 0 or c >= self.max_column:
                    continue
                neighbors.update(self.layout[(r, c)])

        current_seat = self.layout[(row, column)]
        if current_seat == 'L' and neighbors['#'] == 0:
            return '#'
        elif current_seat == '#' and neighbors['#'] >= 4:
            return 'L'
        else:
            return current_seat

    def _get_direction(self, row, column, row_increment, column_increment):
        while True:
            next_row, next_column = row+row_increment, column+column_increment
            visible_seat = self.layout.get((next_row, next_column))
            if visible_seat == 'L' or visible_seat == '#':
                return visible_seat
            elif visible_seat is None:
                return '.'
            else:
                row, column = next_row, next_column

    def get_next_gen_by_visibility(self, row, column):
        visible_counter = Counter()
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if (x, y) == (0, 0):
                    continue
                visible_counter.update(self._get_direction(row, column, x, y))

        current_seat = self.layout[(row, column)]
        if current_seat == 'L' and visible_counter['#'] == 0:
            return '#'
        elif current_seat == '#' and visible_counter['#'] >= 5:
            return 'L'
        else:
            return current_seat

    def run(self, visibility_rules=False):
        if visibility_rules:
            get_next_gen = self.get_next_gen_by_visibility
        else:
            get_next_gen = self.get_next_generation

        while True:
            next_layout = {}
            for row in range(self.max_row):
                for column in range(self.max_column):
                    next_layout[(row, column)] = get_next_gen(row, column)

            if next_layout == self.layout:
                break
            else:
                self.layout = next_layout

        count_seats = Counter()
        for seat in self.layout.values():
            count_seats.update(seat)
        return count_seats['#']


def get_first_star(data):
    return Layout(data).run()


def get_second_star(data):
    return Layout(data).run(visibility_rules=True)


assert get_first_star(test_input) == 37
assert get_second_star(test_input) == 26

print(get_first_star(get_input()))
print(get_second_star(get_input()))
