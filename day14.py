from collections import Counter, deque
from itertools import product


def get_data():
    with open('inputs\\day14.txt') as file:
        return [line.strip() for line in file]


def apply_mask(mask, number):
    digits = f'{number:#038b}'[2:]
    return int("0b" + "".join(mask_digit if mask_digit != 'X' else digit for mask_digit, digit in zip(mask, digits)), 2)


def get_first_star(data):
    mask = None
    mem = {}
    for line in data:
        if line[:4] == 'mask':
            _, mask = line.strip().split(" = ")
        else:
            left, right = line.strip().split(" = ")
            key = left[4:-1]
            value = apply_mask(mask, int(right))
            mem[key] = value
    return sum(mem.values())


def apply_floating_mask(mask, number):
    digits = f'{number:#038b}'[2:]
    x_times = Counter(mask)['X']
    for x_variant in product('01', repeat=x_times):
        next_number = []
        x_variant = deque(x_variant)
        for mask_digit, digit in zip(mask, digits):
            if mask_digit == '0':
                next_number.append(digit)
            elif mask_digit == '1':
                next_number.append('1')
            elif mask_digit == 'X':
                next_number.append(x_variant.popleft())
        yield int(f"0b{''.join(next_number)}", 2)


def get_second_star(data):
    mask = None
    mem = {}
    for line in data:
        if line[:4] == 'mask':
            _, mask = line.strip().split(" = ")
        else:
            left, right = line.strip().split(" = ")
            floating_key = int(left[4:-1])
            value = int(right)
            for key in apply_floating_mask(mask, floating_key):
                mem[key] = value
    return sum(mem.values())


print(get_first_star(get_data()))
print(get_second_star(get_data()))
