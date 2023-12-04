def get_id(input_line):
    game_name, _ = input_line.split(":")
    _, game_id = game_name.split(" ")
    return int(game_id)


def get_reveals(input_line):
    _, game_log = input_line.split(":")
    games_ = game_log.split(";")
    cubes_got = []
    for game in games_:
        cubes_set = {}
        for single_reveal in game.strip().split(","):
            amount, color = single_reveal.strip().split(" ")
            cubes_set[color] = int(amount)
        cubes_got.append(cubes_set)
    return cubes_got


class Game:
    def __init__(self, input_line):
        self.id = get_id(input_line)
        self.reveals = get_reveals(input_line)


def is_possible(game):
    possible = True
    for g in game.reveals:
        if g.get("red", 0) > 12 or g.get("green", 0) > 13 or g.get("blue", 0) > 14:
            possible = False
    return possible


def main():
    ids_sum = 0
    with open("input.txt", 'r') as fh:
        while lin := fh.readline().strip():
            if lin.isspace():
                continue
            game = Game(lin)
            if is_possible(game):
                ids_sum += game.id
    print(f'Sum of possible games id\'s is {ids_sum}')


if __name__ == '__main__':
    main()
