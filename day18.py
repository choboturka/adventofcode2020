from operator import add, mul
from collections import deque
from functools import reduce


def get_data():
    with open('inputs\\day18.txt') as file:
        return [line.strip() for line in file]


def tokenize(line):
    return deque([token for token in line if token != ' '])


def execute_expression(tokens):
    operation_stack = [None]
    number_stack = [None]
    for token in tokens:
        if token in '123456789':
            number = number_stack[-1]
            operation = operation_stack[-1]
            if number is None:
                number = int(token)
            else:
                number = operation(number, int(token))
            number_stack[-1] = number
        elif token == '+':
            operation_stack[-1] = add
        elif token == '*':
            operation_stack[-1] = mul
        elif token == '(':
            number_stack.append(None)
            operation_stack.append(None)
        elif token == ')':
            number = number_stack.pop()
            operation_stack.pop()
            operation = operation_stack[-1]
            if operation:
                number_stack[-1] = operation(number_stack[-1], number)
            else:
                number_stack[-1] = number
    return number_stack[-1]


def execute_with_precedence(tokens):
    op = None
    numbers_to_multiply = [None]
    while True:
        try:
            token = tokens.popleft()
        except IndexError:
            break
        if token in '123456789':
            second_number = int(token)
            number = numbers_to_multiply[-1]
            if number and op == '+':
                numbers_to_multiply[-1] += second_number
            elif number and op == '*':
                numbers_to_multiply.append(second_number)
            else:
                numbers_to_multiply[-1] = second_number
        elif token in '+*':
            op = token
        elif token == '(':
            second_number = execute_with_precedence(tokens)
            number = numbers_to_multiply[-1]
            if number and op == '+':
                numbers_to_multiply[-1] += second_number
            elif number and op == '*':
                numbers_to_multiply.append(second_number)
            else:
                numbers_to_multiply[-1] = second_number
        elif token == ')':
            break
    return reduce(mul, numbers_to_multiply)


def get_first_star(data):
    values_sum = 0
    for expression in data:
        tokens = tokenize(expression)
        value = execute_expression(tokens)
        values_sum += value
    return values_sum


def get_second_star(data):
    values_sum = 0
    for expression in data:
        tokens = tokenize(expression)
        value = execute_with_precedence(tokens)
        values_sum += value
    return values_sum


print(get_first_star(get_data()))
print(get_second_star(get_data()))
