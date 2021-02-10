test = [5764801, 17807724]


def get_data():
    with open('inputs\\day25.txt') as file:
        return [int(line.strip()) for line in file]


DIVISOR = 20201227
INITIAL_SUBJECT_NUMBER = 7


def transform(subject_number, loop_size):
    value = 1
    for _ in range(loop_size):
        value = value * subject_number
        value = value % DIVISOR
    return value


def find_loop_size(public_key):
    loop_size = 1
    value = 1
    while True:
        value = value * INITIAL_SUBJECT_NUMBER
        value = value % DIVISOR
        if value == public_key:
            return loop_size
        else:
            loop_size += 1


def find_keys(data):
    first, second = data
    loop = find_loop_size(second)
    encryption_key = transform(first, loop)
    return encryption_key


assert find_keys(test) == 14897079
print(find_keys(get_data()))
