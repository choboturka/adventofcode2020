import re
from collections import Counter
from itertools import chain


test = '''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''.strip().split('\n')


def get_data():
    with open('inputs\\day21.txt') as file:
        return [line.strip() for line in file]


def parse_food_items(data):
    pattern = re.compile(r'^(?P<components>[a-z ]+) \(contains (?P<allergens>[a-z, ]+)\)$')
    for line in data:
        match = pattern.fullmatch(line)
        components = match.group('components').split(' ')
        allergens = match.group('allergens').split(', ')
        yield components, allergens


def get_components_with_allergens(food_item_list):
    allergic_components = {}
    for components, allergens in food_item_list:
        for allergen in allergens:
            candidates = allergic_components.setdefault(allergen, set(components))
            candidates.intersection_update(set(components))
    return allergic_components


def get_first_star(data):
    food_list = list(parse_food_items(data))
    allergic_components = get_components_with_allergens(food_list)
    dangerous_components = set(chain.from_iterable(components for components in allergic_components.values()))
    all_components = list(chain.from_iterable(components for components, _ in food_list))
    all_components_count = Counter(all_components)
    all_components_set = set(all_components)
    safe_components = all_components_set - dangerous_components
    safe_components_count = sum(
        count for component, count in all_components_count.items() if component in safe_components
    )
    return safe_components_count


assert get_first_star(test) == 5
print(get_first_star(get_data()))


def get_second_star(data):
    food_list = list(parse_food_items(data))
    allergic_components = get_components_with_allergens(food_list)
    decoded_components = {}
    while allergic_components:
        for allergen, candidates in allergic_components.items():
            if len(candidates) == 1:
                solved_component = candidates.pop()
                for components in allergic_components.values():
                    components.discard(solved_component)
                decoded_components[allergen] = solved_component
                del allergic_components[allergen]
                break

    sorted_allergen_pairs = sorted(decoded_components.items(), key=lambda item: item[0])
    sorted_components = ",".join([component for _, component in sorted_allergen_pairs])
    return sorted_components


assert get_second_star(test) == 'mxmxvkd,sqjhc,fvjkl'
print(get_second_star(get_data()))
