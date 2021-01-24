test_input = """
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
""".strip().split('\n')


def get_input():
    with open('inputs\\day8.txt') as file:
        for line in file:
            yield line.strip('\n')


class Bootloader:

    @staticmethod
    def _parse_line(line):
        operation, argument = line.split(' ')
        argument = int(argument)
        return operation, argument

    def __init__(self, code_lines):
        self.instructions = {
            num: self._parse_line(line) for num, line in enumerate(code_lines)
        }
        self.accumulator = 0
        self.pointer = 0
        self.called_lines = set()

    def run(self):
        while True:
            if self.pointer in self.called_lines:
                return self.accumulator
            else:
                self.called_lines.add(self.pointer)

            operation, argument = self.instructions[self.pointer]

            if operation == 'acc':
                self.accumulator += argument
                self.pointer += 1
            elif operation == 'jmp':
                self.pointer += argument
            elif operation == 'nop':
                self.pointer += 1

    def run_from_position(self, accumulator, pointer):
        called_lines = self.called_lines.copy()
        while True:
            if pointer in called_lines:
                return None
            elif pointer == len(self.instructions):
                return accumulator
            else:
                called_lines.add(pointer)

            operation, argument = self.instructions[pointer]
            if operation == 'acc':
                accumulator += argument
                pointer += 1
            elif operation == 'jmp':
                pointer += argument
            elif operation == 'nop':
                pointer += 1

    def fix_error(self):
        while True:
            operation, argument = self.instructions[self.pointer]
            if operation == 'acc':
                self.called_lines.add(self.pointer)
                self.accumulator += argument
                self.pointer += 1
            elif operation == 'jmp':
                self.called_lines.add(self.pointer)
                nop_pointer = self.pointer+1
                result = self.run_from_position(self.accumulator, nop_pointer)
                if result is None:
                    self.pointer += argument
                else:
                    return result
            elif operation == 'nop':
                self.called_lines.add(self.pointer)
                jmp_pointer = self.pointer + argument
                result = self.run_from_position(self.accumulator, jmp_pointer)
                if result is None:
                    self.pointer += 1
                else:
                    return result


def get_first_star(code_lines):
    boot = Bootloader(code_lines)
    return boot.run()


def get_second_star(code_lines):
    boot = Bootloader(code_lines)
    return boot.fix_error()


assert get_first_star(test_input) == 5
print(get_first_star(get_input()))

assert get_second_star(test_input) == 8
print(get_second_star(get_input()))
