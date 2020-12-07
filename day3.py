def get_input():
    with open('inputs\\day3.txt') as file:
        forest_map = [line.strip() for line in file]
    return forest_map


def _traverse_slope(forest_map, steps_right, steps_down):
    trees_encoutered = 0
    max_width = len(forest_map[0])
    max_height = len(forest_map)
    current_width = steps_right
    current_height = steps_down
    while current_height < max_height:
        if forest_map[current_height][current_width] == "#":
            trees_encoutered += 1
        current_height += steps_down
        current_width = (current_width + steps_right) % max_width
    return trees_encoutered


def get_first_star(forest_map):
    # right 3 down one
    # cyclical buffer?
    return _traverse_slope(forest_map, 3, 1)


def get_second_star(forest_map):
    slopes_to_check = [
        (1, 1),
        (3,  1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    current_multiplier = 1
    for slope in slopes_to_check:
        trees_encountered = _traverse_slope(forest_map, *slope)
        current_multiplier *= trees_encountered
    return current_multiplier


test_forest = """
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
""".strip().split("\n")

assert get_first_star(test_forest) == 7
assert get_second_star(test_forest) == 336

print(get_first_star(get_input()))
print(get_second_star(get_input()))

