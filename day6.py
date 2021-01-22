def get_data():
    with open('inputs\\day6.txt') as file:
        chunk = []
        for line in file:
            line = line.strip('\n')
            if line:
                chunk.append(set(line))
            else:
                yield chunk
                chunk = []
        yield chunk


def get_first_star():
    total = 0
    for chunk in get_data():
        first = chunk[0]
        total += len(first.union(*chunk[1:]))
    print(total)


def get_second_star():
    total = 0
    for chunk in get_data():
        first = chunk[0]
        total += len(first.intersection(*chunk[1:]))
    print(total)


get_first_star()
get_second_star()
