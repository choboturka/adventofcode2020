test_input = (939, [7, 13, None, None, 59, None, 31, 19])


def get_input():
    with open('inputs\\day13.txt') as file:
        timestamp = int(file.readline().strip())
        buses = []
        for bus in file.readline().strip().split(','):
            try:
                buses.append(int(bus))
            except ValueError:
                buses.append(None)
        return timestamp, buses


def get_first_star(data):
    start_time, buses = data
    buses = list(filter(None, buses))
    time = start_time
    while True:
        for bus in buses:
            if time % bus == 0:
                return (time - start_time) * bus
        time += 1


assert get_first_star(test_input) == 295
print(get_first_star(get_input()))

tests = [
    (7, 13, None, None, 59, None, 31, 19),
    (17, None, 13, 19),
    (67, 7, 59, 61),
    (67, None, 7, 59, 61),
    (67, 7, None, 59, 61),
    (1789, 37, 47, 1889)
]

answers = [1068781, 3417, 754018, 779210, 1261476, 1202161486]


def get_second_star(data, start=1):
    step = 1
    enumerated_data = [
        (diff, divisor)
        for diff, divisor
        in enumerate(data)
        if divisor is not None
    ]
    for diff, divisor in enumerated_data:
        while True:
            if (start + diff) % divisor == 0:
                step *= divisor
                break
            start += step
    return start


for test, answer in zip(tests, answers):
    assert get_second_star(test) == answer

print(get_second_star(
    data=get_input()[1],
    start=100000000000000
))
