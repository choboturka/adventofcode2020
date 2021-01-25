from itertools import combinations


test_data = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
test_data_2 = [
    28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19,
    38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3
]


def get_input():
    with open('inputs\\day10.txt') as file:
        return [int(line.strip()) for line in file]


def get_first_star(adapters):
    outlet = 0
    device = max(adapters) + 3
    all_adapters = sorted([outlet, *adapters, device])

    diff_one = 0
    diff_three = 0

    for previous, current in zip(all_adapters, all_adapters[1:]):
        if current - previous == 1:
            diff_one += 1
        elif current - previous == 3:
            diff_three += 1
    return diff_one * diff_three


def validate_adapter_chain(adapter_chain):
    for previous, current in zip(adapter_chain, adapter_chain[1:]):
        if current-previous > 3:
            return False
    return True


def find_arrangements(adapters):
    valid_adapter_chains = 0
    left_adapter, right_adapter = min(adapters), max(adapters)
    for chain_length in range(2, len(adapters)+1):
        for adapter_chain in combinations(adapters, chain_length):
            adapter_chain = list(adapter_chain)
            if (left_adapter not in adapter_chain) or (right_adapter not in adapter_chain):
                continue
            if validate_adapter_chain(adapter_chain):
                valid_adapter_chains += 1
    return valid_adapter_chains


def split_to_chunks(adapters):
    current_chunk = []
    for previous, current in zip(adapters, adapters[1:]):
        if current - previous == 3:
            current_chunk.append(previous)
            if len(current_chunk) > 2:
                yield current_chunk
            current_chunk = []
        else:
            current_chunk.append(previous)


def get_second_star(adapters):
    outlet = 0
    device = max(adapters) + 3
    adapters = sorted([outlet, *adapters, device])
    arrangements = 1
    for chunk in split_to_chunks(adapters):
        arrangements *= find_arrangements(chunk)
    return arrangements


assert get_first_star(test_data) == 7*5
assert get_first_star(test_data_2) == 22*10
print(get_first_star(get_input()))

assert get_second_star(test_data) == 8
assert get_second_star(test_data_2) == 19208
print(get_second_star(get_input()))
