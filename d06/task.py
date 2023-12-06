from _operator import mul
from functools import reduce, partial
from operator import mul


def solve_file(input_file):
    races = parse_input(input_file)
    combinations = reduce(mul, (calc_single_combinations(race1) for race1 in races))
    print(f"For {input_file=} as multiple races got {combinations=}")
    race = parse_input_as_one_race(input_file)
    combinations = calc_single_combinations(race)
    print(f"For {input_file=} as single race got {combinations=}")


def race_won(race, press_time):
    race_time, race_distance = race
    my_distance = (race_time - press_time) * press_time
    return my_distance > race_distance


def calc_single_combinations(race):
    this_race_won = partial(race_won, race)
    race_time, _ = race
    valid_press_lower_bound = next(filter(this_race_won, range(0, race_time)))
    valid_press_upper_bound = next(filter(this_race_won, range(race_time, 0, -1)))
    ways_to_win_current = valid_press_upper_bound - valid_press_lower_bound + 1
    return ways_to_win_current


def parse_input(input_file):
    with open(input_file, 'r') as fh:
        times = map(int, fh.readline().split(":")[1].split())
        distances = map(int, fh.readline().split(":")[1].split())
        return zip(times, distances)


def parse_input_as_one_race(input_file):
    with open(input_file, 'r') as fh:
        times = int(fh.readline().split(":")[1].replace(" ", ""))
        distances = int(fh.readline().split(":")[1].replace(" ", ""))
        return times, distances


if __name__ == '__main__':
    solve_file("example.txt")
    solve_file("input.txt")
