import re


def get_input():
    with open("inputs\\day4.txt") as file:
        for line in file:
            yield line.strip('\n')


def parse_input(lines):
    passport = {}
    for line in lines:
        if line:
            fields = [field.split(":") for field in line.split()]
            for key, value in fields:
                passport[key] = value
        else:
            yield passport
            passport = {}
    yield passport  # yield the last passport before EOF


test_input = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""".strip().split('\n')


def get_first_star(passports):
    mandatory_fields = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid'
    }
    valid_passports = 0
    for passport in passports:
        passport.pop('cid', None)
        if set(passport.keys()) == mandatory_fields:
            valid_passports += 1
    return valid_passports


def _validate_byr(data):
    if data is not None and len(data) == 4 and (1920 <= int(data) <= 2002):
        return True
    return False


def _validate_iyr(data):
    if data is not None and len(data) == 4 and (2010 <= int(data) <= 2020):
        return True
    return False


def _validate_eyr(data):
    if data is not None and len(data) == 4 and (2020 <= int(data) <= 2030):
        return True
    return False


def _validate_hgt(data):
    if data is not None and (match := re.fullmatch(r'(?P<number>[0-9]+)(?P<suffix>in|cm)', data)):
        if match.group('suffix') == 'in' and 59 <= int(match.group('number')) <= 76:
            return True
        elif match.group('suffix') == 'cm' and 150 <= int(match.group('number')) <= 193:
            return True
    return False


def _validate_hcl(data):
    if data is not None and re.fullmatch(r'#[0-9a-f]{6}', data):
        return True
    return False


def _validate_ecl(data):
    if data is not None and re.fullmatch(r'(amb|blu|brn|gry|grn|hzl|oth)', data):
        return True
    return False


def _validate_pid(data):
    if data is not None and re.fullmatch(r'[0-9]{9}', data):
        return True
    else:
        return False


def get_second_star(passports):
    validators = {
        'byr': _validate_byr,
        'iyr': _validate_iyr,
        'eyr': _validate_eyr,
        'hgt': _validate_hgt,
        'hcl': _validate_hcl,
        'ecl': _validate_ecl,
        'pid': _validate_pid
    }
    validated_fields = set(validators.keys())
    valid_passports = 0
    for passport in passports:
        passport.pop('cid', None)
        if set(passport.keys()) != validated_fields:
            continue
        if all([validators[key](value) for key, value in passport.items()]):
            valid_passports += 1
    return valid_passports


assert get_first_star(parse_input(test_input)) == 2

print(get_first_star(parse_input(get_input())))
print(get_second_star(parse_input(get_input())))
