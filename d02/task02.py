from functools import reduce
from operator import mul


class Game:
    def __init__(self, input_line):
        game_name, game_log = input_line.split(":")
        self.id = self.get_id(game_name)
        self.reveals = self.get_reveals(game_log)

    @staticmethod
    def get_id(game_name):
        _, game_id = game_name.split(" ")
        return int(game_id)

    @staticmethod
    def parse_cubes_set(cubes_line):
        return {
            (s := single_reveal.strip().split(" "))[1]: int(s[0])
            for single_reveal in cubes_line.strip().split(",")
        }

    def get_reveals(self, game_log):
        return [
            self.parse_cubes_set(cubes_line)
            for cubes_line in game_log.strip().split(";")
        ]

    def power(self):
        minimal_dices = self.get_minimal_dices()
        return reduce(mul, minimal_dices.values())

    def is_possible(self):
        return all(self.is_single_reveal_possible(r) for r in self.reveals)

    @staticmethod
    def is_single_reveal_possible(reveal):
        return reveal.get("red", 0) <= 12 and reveal.get("green", 0) <= 13 and reveal.get("blue", 0) <= 14

    def get_minimal_dices(self):
        minimal_dices = {}
        for r in self.reveals:
            for color, amount in r.items():
                if minimal_dices.get(color, 0) < amount:
                    minimal_dices[color] = amount
        return minimal_dices


def main():
    ids_sum = 0
    power_sum = 0
    with open("input.txt", 'r') as fh:
        while lin := fh.readline().strip():
            if lin.isspace():
                continue
            game = Game(lin)
            if game.is_possible():
                ids_sum += game.id
            power_sum += game.power()
    print(f"Sum of possible games id's is {ids_sum}")
    print(f"Sum of power is {power_sum}")


if __name__ == '__main__':
    main()
