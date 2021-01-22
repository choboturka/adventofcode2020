import re

test_input = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".strip().split('\n')

another_test_input = """
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""".strip().split('\n')


def get_input():
    with open('inputs\\day7.txt') as file:
        for line in file:
            yield line.strip('\n')


def process_colors(data):
    colors = dict()
    for rule in data:
        m = re.match(r"^(?P<key>.+) bags contain (?P<values>.+)\.$", rule)
        key = m.group('key')
        values = m.group('values')
        if values == 'no other bags':
            colors[key] = []
        else:
            color_values = []
            raw_values = values.split(', ')
            for value in raw_values:
                m = re.match(r"^(?P<number>[0-9]+) (?P<color>.+) bags?$", value)
                color_values.append(
                    (int(m.group('number')), m.group('color'))
                )
            colors[key] = color_values
    return colors


def get_first_star(data):
    colors = process_colors(data)
    list_to_check = ['shiny gold']
    answers = []
    while True:
        current_color = list_to_check.pop()
        for key, values in colors.items():
            color_values = [t[1] for t in values]
            if current_color in color_values:
                if key not in answers:
                    answers.append(key)
                    list_to_check.append(key)
        if not list_to_check:
            break
    return len(answers)


def get_second_star(data):
    colors = process_colors(data)
    accum = -1
    bags = ['shiny gold']
    while True:
        current_bag = bags.pop()
        accum += 1
        for item in colors[current_bag]:
            for _ in range(item[0]):
                bags.append(item[1])
        if not bags:
            break
    return accum


assert get_first_star(test_input) == 4
assert get_second_star(test_input) == 32
assert get_second_star(another_test_input) == 126

print(get_first_star(get_input()))
print(get_second_star(get_input()))
