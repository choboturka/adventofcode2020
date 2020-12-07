from collections import Counter


def get_input():
    with open("inputs\\day2.txt") as file:
        for line in file:
            line = line.strip()
            policy, password = line.split(":")
            password = password.strip()
            uses_range, letter = policy.split()
            min_uses, max_uses = uses_range.split("-")
            min_uses, max_uses = int(min_uses), int(max_uses)
            yield min_uses, max_uses, letter, password


def get_first_star():
    valid_count = 0
    for min_uses, max_uses, letter, password in get_input():
        password_letter_count = Counter(password).get(letter, 0)
        if min_uses <= password_letter_count <= max_uses:
            valid_count += 1
    return valid_count


def get_second_star():
    valid_count = 0
    for first_pos, second_pos, letter, password in get_input():
        first_pos, second_pos = first_pos - 1, second_pos - 1  # convert to zero-based index
        if bool(password[first_pos] == letter) != bool(password[second_pos] == letter):  # != is xor for boolean values
            valid_count += 1
    return valid_count


print(get_first_star())
print(get_second_star())
