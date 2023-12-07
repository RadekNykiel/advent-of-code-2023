from enum import Enum


class CardTypes(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7


CARD_VALUES = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}
CARD_VALUES.update({str(x): x for x in range(1, 10)})
CARD_VALUES_JOKER = {}
CARD_VALUES_JOKER.update(CARD_VALUES, J=1)


class Cards:
    def __init__(self, cards):
        self.cards = cards
        self.type = self.get_type(self.cards)
        self.cards_after_joker, self.type_joker = self.get_type_joker(self.cards)

    @staticmethod
    def get_type(cards):
        cards_amount = Cards.count_cards(cards)
        match sorted(cards_amount.values(), reverse=True):
            case [5]:
                return CardTypes.FIVE_OF_KIND
            case [4, 1]:
                return CardTypes.FOUR_OF_KIND
            case [3, 2]:
                return CardTypes.FULL_HOUSE
            case [3, *_]:
                return CardTypes.THREE_OF_KIND
            case [2, 2, *_]:
                return CardTypes.TWO_PAIR
            case [2, *_]:
                return CardTypes.ONE_PAIR
            case _:
                return CardTypes.HIGH_CARD

    @staticmethod
    def count_cards(cards):
        cards_amount = {}
        for c in cards:
            cards_amount[c] = cards_amount.get(c, 0) + 1
        return cards_amount

    @classmethod
    def get_type_joker(cls, cards):
        cards_without_joker_amount = Cards.count_cards(cards.replace("J", ""))
        sorted_by_amount_and_value = sorted(cards_without_joker_amount.items(),
                                            key=lambda a: (a[1], CARD_VALUES_JOKER[a[0]]), reverse=True)
        if len(sorted_by_amount_and_value) == 0:
            return "AAAAA", CardTypes.FIVE_OF_KIND
        joker_substitute = sorted_by_amount_and_value[0][0]
        replace = cards.replace("J", joker_substitute)
        return replace, cls.get_type(replace)

    def __str__(self):
        return f"Cards({self.cards}, {self.type.name}, joker: {self.cards_after_joker}, {self.type_joker})"

    def __repr__(self):
        return self.__str__()

    def high_cards_value(self):
        return sum((100 ** ix) * CARD_VALUES[v] for ix, v in enumerate(reversed(self.cards)))

    def high_cards_value_joker(self):
        return sum((100 ** ix) * CARD_VALUES_JOKER[v] for ix, v in enumerate(reversed(self.cards)))


def solve_file(input_file):
    games = []
    with open(input_file, "r") as fh:
        for line in fh:
            cards, bet = line.split()
            cards = Cards(cards)
            games.append((cards, int(bet)))
    games_by_hand_strength = sorted(games, key=lambda a: (a[0].type.value, a[0].high_cards_value()))
    score_no_joker = sum(x[1] * (ix + 1) for ix, x in enumerate(games_by_hand_strength))
    games_by_hand_strength_joker = sorted(games, key=lambda a: (a[0].type_joker.value, a[0].high_cards_value_joker()))
    score_with_joker = sum(x[1] * (ix + 1) for ix, x in enumerate(games_by_hand_strength_joker))
    print(f"{input_file=}: {score_no_joker=}, {score_with_joker=}")


if __name__ == '__main__':
    solve_file("example.txt")
    solve_file("input.txt")
