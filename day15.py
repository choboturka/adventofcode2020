from collections import defaultdict, deque
from functools import partial


def get_input():
    with open('inputs\\day15.txt') as file:
        return [int(num) for num in file.readline().strip().split(',')]


def play_game(data, last_turn):
    turn_history = defaultdict(partial(deque, maxlen=2))
    for turn, num in enumerate(data, start=1):
        turn_history[num].append(turn)
    start = len(data) + 1
    end = last_turn + 1
    last_number = data[-1]

    for turn in range(start, end):
        number_history = turn_history[last_number]
        if len(number_history) == 1:
            last_number = 0
        else:
            last_number = number_history[1] - number_history[0]
        turn_history[last_number].append(turn)
    return last_number


def get_first_star(data):
    return play_game(data, last_turn=2020)


def get_second_star(data):
    return play_game(data, last_turn=30000000)


print(get_first_star(get_input()))
print(get_second_star(get_input()))
