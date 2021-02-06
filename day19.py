import re

test = '''
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
'''.strip()

test2 = '''
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''.strip()


def get_data():
    with open('inputs\\day19.txt') as file:
        return file.read()


class Messages:
    def __init__(self, data):
        rules_section, messages_section = data.split('\n\n')
        self.messages = messages_section.split('\n')
        self.rules = {}
        for rule_line in rules_section.split('\n'):
            key, values = rule_line.split(': ')
            if 'a' in values:
                values = 'a'
            elif 'b' in values:
                values = 'b'
            else:
                values = values.split(' ')
            self.rules[key] = values

    def regex_char_list(self, index='0'):
        rules = self.rules[index]
        for rule in rules:
            if rule == '|':
                yield '|'
            elif self.rules[rule] == 'a':
                yield 'a'
            elif self.rules[rule] == 'b':
                yield 'b'
            else:
                yield '('
                yield from self.regex_char_list(index=rule)
                yield ')'

    def rule_regex(self, index='0'):
        return "".join([c for c in self.regex_char_list(index)])

    def match_messages(self):
        pattern = re.compile(self.rule_regex())
        count = 0
        for message in self.messages:
            if pattern.fullmatch(message) is not None:
                count += 1
        return count


def get_first_star(data):
    messages = Messages(data)
    return messages.match_messages()


def get_second_star(data):
    messages = Messages(data)
    pattern_42 = messages.rule_regex('42')
    pattern_31 = messages.rule_regex('31')
    pattern_8 = f'({pattern_42})+'
    pattern_11 = [
        f'({pattern_42}){{{n}}}({pattern_31}){{{n}}}' for n in range(1, 10)
    ]
    pattern_0 = [
        f'{pattern_8}{p11}' for p11 in pattern_11
    ]
    matched_strings = set()
    for pattern in pattern_0:
        compiled = re.compile(pattern)
        for message in messages.messages:
            matched = compiled.fullmatch(message)
            if matched:
                matched_strings.add(matched[0])
    return len(matched_strings)


assert get_first_star(test) == 2
assert get_second_star(test2) == 12

print(get_first_star(get_data()))
print(get_second_star(get_data()))

