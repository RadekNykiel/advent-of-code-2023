from functools import reduce
from operator import mul


def calc_distance(race_time, press):
    speed = press
    time_to_run = (race_time - press) * speed
    return time_to_run


def solve_file(input_file):
    races = parse_input(input_file)
    combinations = calc_combinations(races)
    print(f"For {input_file=} as multiple races got {combinations=}")
    race = parse_input_as_one_race(input_file)
    combinations = calc_single_combinations(race)
    print(f"For {input_file=} as single race got {combinations=}")


def calc_combinations(races):
    ways_to_win = []
    for race in races:
        ways_to_win_current = calc_single_combinations(race)
        ways_to_win.append(ways_to_win_current)
    combinations = reduce(mul, ways_to_win)
    return combinations


def calc_single_combinations(race):
    race_time, race_distance = race
    all_press = list(range(0, race_time))
    valid_press = list(filter(lambda x: calc_distance(race_time, x) > race_distance, all_press))
    ways_to_win_current = len(valid_press)
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
