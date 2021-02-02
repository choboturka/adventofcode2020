from collections import defaultdict
from functools import partial


def validate_field(ranges, number):
    return any(left <= number <= right for left, right in ranges)


def validate_ticket(validators, ticket):
    for number in ticket:
        if not any(field_validator(number) for field_validator in validators):
            return False
    return True


def get_data():
    fields = {}
    modes = ['other_tickets', 'my_ticket']
    mode = 'fields'
    other_tickets = []
    with open('inputs\\day16.txt') as file:
        for line in file:
            line = line.strip()
            if not line:
                mode = modes.pop()
                continue
            if mode == 'fields':
                name, ranges = line.split(': ')
                validation_params = []
                for _range in ranges.split(' or '):
                    left, right = _range.split('-')
                    pair = int(left), int(right)
                    validation_params.append(pair)
                fields[name] = partial(validate_field, validation_params)
            elif mode == 'my_ticket':
                if line == 'your ticket:':
                    continue
                my_ticket = [int(num) for num in line.split(',')]
            elif mode == 'other_tickets':
                if line == 'nearby tickets:':
                    continue
                other_tickets.append([int(num) for num in line.split(',')])
    return fields, my_ticket, other_tickets


def get_first_star():
    fields, _, tickets = get_data()
    invalid_values = []
    for ticket in tickets:
        for number in ticket:
            if not any(field_validator(number) for field_validator in fields.values()):
                invalid_values.append(number)
    return sum(invalid_values)


def get_second_star():
    fields, my_ticket, other_tickets = get_data()
    filter_invalid_tickets = partial(validate_ticket, fields.values())
    valid_tickets = list(filter(filter_invalid_tickets, other_tickets))
    valid_tickets.append(my_ticket)

    field_options = defaultdict(set)
    for name, validator in fields.items():
        for position_index, position_values in enumerate(zip(*valid_tickets)):
            if all(validator(num) for num in position_values):
                field_options[position_index].add(name)

    translated_fields = {}
    while True:
        name_to_delete = None
        index_to_delete = None
        for index, names in field_options.items():
            if len(names) == 1:
                name_to_delete = names.pop()
                index_to_delete = index
        for names in field_options.values():
            names.discard(name_to_delete)
        del field_options[index_to_delete]
        translated_fields[name_to_delete] = index_to_delete
        if not field_options:
            break

    product = 1
    for name, index in translated_fields.items():
        if 'departure' in name:
            product *= my_ticket[index]
    return product


print(get_first_star())
print(get_second_star())
