from functools import reduce
from operator import mul


def is_symbol(c: str):
    return not (c.isalnum() or c == ".")


def get_symbols_pos(input_line: str, line_num: int):
    return [
        (line_num, ix)
        for ix, c in enumerate(input_line)
        if is_symbol(c)
    ]


def get_star_pos(input_line: str, line_num: int):
    return [
        (line_num, ix)
        for ix, c in enumerate(input_line)
        if c == "*"
    ]


def get_values_with_pos(lin: str, line_num):
    result = []
    char_buffer = ""
    pos_buff = []
    for ix, c in enumerate(lin):
        if c.isdigit():
            char_buffer += c
            pos_buff.append((line_num, ix))
        elif char_buffer != "":
            result.append((int(char_buffer), pos_buff))
            char_buffer = ""
            pos_buff = []
    if char_buffer != "":
        result.append((int(char_buffer), pos_buff))
    return result


def get_adjacent_pos(pos):
    lines = [i[0] for i in pos]
    cols = [i[1] for i in pos]
    min_adj_line = min(lines) - 1
    max_adj_line = max(lines) + 1
    min_adj_col = min(cols) - 1
    max_adj_col = max(cols) + 1
    return [
        (x, y)
        for x in [min_adj_line, *lines, max_adj_line]
        for y in [min_adj_col, *cols, max_adj_col]
        if (x, y) not in pos
    ]


def main():
    # parsing stuff
    symbols = []
    values_with_pos = []
    stars = []
    with open("input.txt", 'r') as fh:
        for line_num, lin in enumerate(fh):
            lin = lin.strip()
            symbols.extend(get_symbols_pos(lin, line_num))
            values_with_pos.extend(get_values_with_pos(lin, line_num))
            stars.extend(get_star_pos(lin, line_num))

    task1_sum_of_values_with_adjacent_symbols(symbols, values_with_pos)
    task2_sum_of_gear_ratios(stars, values_with_pos)


def task2_sum_of_gear_ratios(stars, values_with_pos):
    fields_adjacents_to_stars = [
        get_adjacent_pos([p])
        for p in stars
    ]
    values_adjacent_to_stars = [
        [
            v
            for v, v_pos in values_with_pos
            if set(v_pos).intersection(adj)
        ]
        for adj in fields_adjacents_to_stars
    ]
    ratios = [
        reduce(mul, x)
        for x in values_adjacent_to_stars
        if len(x) == 2
    ]
    sum_of_ratios = sum(ratios)
    print(f"{sum_of_ratios=}")


def task1_sum_of_values_with_adjacent_symbols(symbols, values_with_pos):
    values_with_adjacent_pos = [
        (value, get_adjacent_pos(value_pos))
        for value, value_pos in values_with_pos
    ]
    values_with_adjacent_symbols = [
        value
        for value, value_adjacents in values_with_adjacent_pos
        if set(value_adjacents).intersection(symbols)
    ]
    sum_of_values_next_to_symbol = sum(values_with_adjacent_symbols)
    print(f"{sum_of_values_next_to_symbol=}")


if __name__ == '__main__':
    main()
