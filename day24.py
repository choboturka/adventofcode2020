from math import sqrt
from collections import Counter


test = '''
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''.strip().split('\n')


def get_data():
    with open('inputs\\day24.txt') as file:
        return [line.strip() for line in file]


DIRECTION_TOKENS = {
    'ne': '1',
    'nw': '2',
    'se': '3',
    'sw': '4',
    'e': '5',
    'w': '6'
}
# w --> e
# s --> n
ROUNDING_CONSTANT = 12

y_unit = round(sqrt(3)/2, ROUNDING_CONSTANT)
x_unit = 0.5

TOKEN_DISTANCES = {
    '1': (x_unit, y_unit),
    '2': (-x_unit, y_unit),
    '3': (x_unit, -y_unit),
    '4': (-x_unit, -y_unit),
    '5': (2*x_unit, 0.0),
    '6': (-2*x_unit, 0.0),
}


def parse_coordinates(line):
    for direction, token in DIRECTION_TOKENS.items():
        line = line.replace(direction, token)
    x, y = 0, 0
    for token in line:
        dx, dy = TOKEN_DISTANCES[token]
        x += dx
        y += dy
    return round(x, ROUNDING_CONSTANT), round(y, ROUNDING_CONSTANT)


def get_first_star(data):
    flipped_tile_count = Counter()
    for line in data:
        tile_coordinates = parse_coordinates(line)
        flipped_tile_count.update([tile_coordinates])
    count = 0
    for times_flipped in flipped_tile_count.values():
        if times_flipped % 2 == 1:
            count += 1
    return count


def get_second_star(data):
    black_tiles = set()
    for line in data:
        tile = parse_coordinates(line)
        if tile not in black_tiles:
            black_tiles.add(tile)
        else:
            black_tiles.remove(tile)

    for turn in range(100):
        black_to_white_flip = set()
        white_tiles_to_check = set()
        for x, y in black_tiles:
            neighbors_count = 0
            for dx, dy in TOKEN_DISTANCES.values():
                neighbor = round(x+dx, ROUNDING_CONSTANT), round(y+dy, ROUNDING_CONSTANT)
                if neighbor in black_tiles:
                    neighbors_count += 1
                else:
                    white_tiles_to_check.add(neighbor)
            if neighbors_count == 0 or neighbors_count > 2:
                black_to_white_flip.add((x, y))
        white_to_black_flip = set()
        for x, y in white_tiles_to_check:
            neighbors_count = 0
            for dx, dy in TOKEN_DISTANCES.values():
                neighbor = round(x+dx, ROUNDING_CONSTANT), round(y+dy, ROUNDING_CONSTANT)
                if neighbor in black_tiles:
                    neighbors_count += 1
            if neighbors_count == 2:
                white_to_black_flip.add((x, y))
        black_tiles = black_tiles - black_to_white_flip
        black_tiles = black_tiles | white_to_black_flip
    return len(black_tiles)


assert get_first_star(test) == 10
print(get_first_star(get_data()))

assert get_second_star(test) == 2208
print(get_second_star(get_data()))
