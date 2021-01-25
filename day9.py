from collections import deque
from itertools import combinations

test_input = [
    35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102,
    117, 150, 182, 127, 219, 299, 277, 309, 576
]
TEST_PREAMBLE = 5
PRODUCTION_PREAMBLE = 25


def get_input():
    with open('inputs\\day9.txt') as file:
        for line in file:
            yield int(line.strip('\n'))


def _validate_number(preamble, number):
    # number must be the sum of ANY 2 numbers (not repeat):
    pairs = combinations(set(preamble), 2)
    for pair in pairs:
        if sum(pair) == number:
            return True
    return False


def get_first_star(numbers, preamble_size):
    buffer = deque(maxlen=preamble_size)
    for number in numbers:
        # pre-populate the buffer
        if len(buffer) < preamble_size:
            buffer.append(number)
            continue

        if _validate_number(buffer, number):
            buffer.append(number)
        else:
            return number


def get_second_star(numbers, preamble_size):
    numbers = list(numbers)
    target = get_first_star(numbers, preamble_size)
    buffer = deque()
    for number in numbers:
        buffer.append(number)
        if sum(buffer) > target:
            while sum(buffer) > target:
                buffer.popleft()
        if sum(buffer) == target:
            return min(buffer) + max(buffer)


assert get_first_star(test_input, TEST_PREAMBLE) == 127
print(get_first_star(get_input(), PRODUCTION_PREAMBLE))

assert get_second_star(test_input, TEST_PREAMBLE) == 62
print(get_second_star(get_input(), PRODUCTION_PREAMBLE))
