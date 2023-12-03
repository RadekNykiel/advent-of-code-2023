from typing import Optional, Dict


def get_digit_from_string_beginning(line: str) -> Optional[int]:
    words_to_digits_mapping: Dict[str, int] = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for digit_string, digit_value in words_to_digits_mapping.items():
        if line.startswith(digit_string):
            return digit_value
    first_char = line[0]
    if first_char.isdigit():
        return int(first_char)
    return None


def get_all_digits(line: str):
    digits = []
    while line:
        if (d := get_digit_from_string_beginning(line)) is not None:
            digits.append(d)
        line = line[1:]
    return digits


def get_calibration_value(digits):
    return 10 * digits[0] + digits[-1]


calibration_sum: int = 0
with open("input.txt", 'r') as fh:
    while current_line := fh.readline().strip():
        all_digits_from_line = get_all_digits(current_line)
        calibration = get_calibration_value(all_digits_from_line)
        calibration_sum += calibration
print(f'suma: {calibration_sum}')
