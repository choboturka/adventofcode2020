import math
import re

from collections import Counter

test = str('''
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
 
'''[1:-2]).split('\n')


def get_data():
    with open('inputs\\day20.txt') as file:
        return [line.strip('\n') for line in file]


def flip_lookup_populate():
    flip_lookup = {}
    for n in range(1024):
        binary = "".join(reversed(f'{n:#012b}'[2:]))
        flip_lookup[n] = int(f'0b{binary}', 2)
    return flip_lookup


def parse_tiles(text):
    current_number = None
    current_tile = []
    for line in text:
        line = line.strip()
        if not line:
            yield current_number, current_tile
            current_number = None
            current_tile = []
        elif 'Tile' in line:
            current_number = int(re.search('[0-9]+', line).group(0))
        else:
            current_tile.append(line)


NUMBERS = flip_lookup_populate()


def convert(line):
    binary_line = line.replace('#', '1').replace('.', '0')
    num = int(f'0b{binary_line}', 2)
    return min(num, NUMBERS[num])


def get_sides(tile):
    return (
        tile[0],
        "".join([row[-1] for row in tile]),
        tile[-1],
        "".join([row[0] for row in tile])
    )


def get_corner_tiles(tiles):
    side_count = Counter()
    side_to_tile = {}
    for tile_id, tile in tiles:
        tile_sides = get_sides(tile)
        side_ids = [convert(side) for side in tile_sides]
        side_count.update(side_ids)
        side_to_tile.update({side_id: tile_id for side_id in side_ids})
    edge_tile_sides = Counter()
    for side_id, count in side_count.items():
        if count == 1:
            tile_id = side_to_tile[side_id]
            edge_tile_sides.update([tile_id])
    for tile_id, count in edge_tile_sides.items():
        if count == 2:
            yield tile_id
    return edge_tile_sides


def get_first_star(data):
    tiles = parse_tiles(data)
    result = 1
    for tile_id in get_corner_tiles(tiles):
        result *= tile_id
    return result


assert get_first_star(test) == 20899048083289
print(get_first_star(get_data()))


class Image:
    def __init__(self, rows):
        self.matrix = {}
        for y, row in enumerate(rows):
            for x, char in enumerate(row):
                num = 1 if char == '#' else 0
                self.matrix[x, y] = num

        self.x_size = len(rows[0])
        self.y_size = len(rows)

    @property
    def up(self):
        y = 0
        return tuple(self.matrix[x, y] for x in range(self.x_size))

    @property
    def down(self):
        y = self.y_size - 1
        return tuple(self.matrix[x, y] for x in range(self.x_size))

    @property
    def left(self):
        x = 0
        return tuple(self.matrix[x, y] for y in range(self.y_size))

    @property
    def right(self):
        x = self.x_size - 1
        return tuple(self.matrix[x, y] for y in range(self.y_size))

    def print(self):
        text = []
        for y in range(self.y_size):
            for x in range(self.x_size):
                char = '#' if self.matrix[x, y] else ' '
                text.append(char)
            text.append('\n')
        print("".join(text))

    def rotate(self):
        new_matrix = {}
        for old_y, new_x in enumerate(reversed(range(self.x_size))):
            for old_x, new_y in enumerate(range(self.y_size)):
                new_matrix[new_x, new_y] = self.matrix[old_x, old_y]
        self.x_size, self.y_size = self.y_size, self.x_size
        self.matrix = new_matrix

    def flip(self):
        new_matrix = {}
        for old_y, new_y in enumerate(range(self.y_size)):
            for old_x, new_x in enumerate(reversed(range(self.x_size))):
                new_matrix[new_x, new_y] = self.matrix[old_x, old_y]
        self.matrix = new_matrix

    def cycle(self):
        for _ in range(2):
            for _ in range(4):
                yield self
                self.rotate()
            self.flip()

    def mask(self, mask):
        delta_x = self.x_size - mask.x_size + 1
        delta_y = self.y_size - mask.y_size + 1
        if delta_x <= 0 or delta_y <= 0:
            return False
        mask_count = 0
        mask_xy = [key for key, value in mask.matrix.items() if value]
        for dy in range(delta_y):
            for dx in range(delta_x):
                if all(self.matrix[mx + dx, my + dy] for mx, my in mask_xy):
                    mask_count += 1
        return mask_count

    def match_right(self, other):
        if self.right == other.left:
            return True
        else:
            return False

    def match_down(self, other):
        if self.down == other.up:
            return True
        else:
            return False

    def crop(self):
        new_matrix = {}
        for new_y, y in enumerate(range(1, self.y_size - 1)):
            for new_x, x in enumerate(range(1, self.x_size - 1)):
                new_matrix[new_x, new_y] = self.matrix[x, y]
        self.x_size -= 2
        self.y_size -= 2
        self.matrix = new_matrix


monster = '''
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
'''.strip('\n').split('\n')


def find_right_match(image, other):
    for other_variation in other.cycle():
        if image.match_right(other_variation):
            return True
    return False


def find_down_match(image, other):
    for other_variation in other.cycle():
        if image.match_down(other_variation):
            return True
    return False


def find_top_left(candidates, images):
    for top_left_id in candidates:
        top_left = images[top_left_id]
        right_id = None
        for image_id, image in images.items():
            if image_id == top_left_id:
                continue
            if find_right_match(top_left, image):
                right_id = image_id
                break
        if right_id:
            for image_id, image in images.items():
                if image_id == top_left_id or image_id == right_id:
                    continue
                if find_down_match(top_left, image):
                    return top_left_id, top_left


def get_correct_images(data):
    images = {}
    for tile_id, tile in parse_tiles(data):
        images[tile_id] = Image(tile)
    corner_tile_ids = get_corner_tiles(parse_tiles(data))
    size = int(math.sqrt(len(images)))
    current_id, current_image = find_top_left(corner_tile_ids, images)
    del images[current_id]
    correct_images = dict()
    correct_images[0, 0] = current_image
    for y in range(size):
        for x in range(1, size):
            for image_id, image in images.items():
                if find_right_match(current_image, image):
                    current_image = image
                    correct_images[x, y] = image
                    del images[image_id]
                    break
        current_image = correct_images[0, y]
        for image_id, image in images.items():
            if find_down_match(current_image, image):
                current_image = image
                correct_images[0, y + 1] = image
                del images[image_id]
                break
    return correct_images


def image_from_data(data):
    correct_images = get_correct_images(data)
    size = int(math.sqrt(len(correct_images)))
    y_size = correct_images[0, 0].y_size - 2
    x_size = correct_images[0, 0].x_size - 2
    new_image_matrix = {}
    for y in range(size):
        for x in range(size):
            image = correct_images[x, y]
            image.crop()
            for (xm, ym), char in image.matrix.items():
                x_new = x*x_size + xm
                y_new = y*y_size + ym
                new_image_matrix[x_new, y_new] = '#' if char else '.'

    image_size = int(math.sqrt(len(new_image_matrix)))
    return Image([
        "".join([
            new_image_matrix[x, y]
            for x in range(image_size)
        ])
        for y in range(image_size)
    ])


def get_second_star(data):
    image = image_from_data(data)
    monster_image = Image(monster)
    monster_count = 0
    for _ in image.cycle():
        monster_count = image.mask(monster_image)
        if monster_count:
            break
    return sum(image.matrix.values()) - monster_count * sum(monster_image.matrix.values())


assert get_second_star(test) == 273
print(get_second_star(get_data()))
