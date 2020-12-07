def get_input():
    with open("inputs\\day1.txt") as file:
        nums = [int(line.strip()) for line in file]
    return nums


def get_first_star():
    nums = get_input()
    for first in nums:
        for second in nums:
            if first + second == 2020:
                return first * second


def get_second_star():
    nums = get_input()
    for first in nums:
        for second in nums:
            for third in nums:
                if first + second + third == 2020:
                    return first * second * third


print(get_first_star())
print(get_second_star())
