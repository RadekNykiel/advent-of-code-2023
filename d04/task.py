def main():
    all_games_score = 0
    scratchcards = {}
    with open("input.txt", "r") as fh:
        for line in fh:
            current_game_id = int(line.split(":")[0].split()[1])
            all_numbers = line.split(":")[1].split("|")
            my_numbers = all_numbers[1].split()
            winning_numbers = all_numbers[0].split()
            common_numbers = set(my_numbers).intersection(winning_numbers)
            numbers_matching = len(common_numbers)

            game_score = 2 ** (numbers_matching-1) if numbers_matching != 0 else 0
            all_games_score += game_score

            if current_game_id not in scratchcards:
                scratchcards[current_game_id] = 1
            for won_card_id in range(current_game_id + 1, current_game_id + numbers_matching + 1):
                extra_copies = scratchcards[current_game_id]
                scratchcards[won_card_id] = scratchcards.get(won_card_id, 1) + extra_copies
    print(f"{all_games_score=}")

    all_scratchcards_amount = sum(scratchcards.values())
    # todo - it may be that current implementation adds scratchcards with indexes above last game from input
    #        however it's not the case for my input xD
    print(f"{all_scratchcards_amount=}")


if __name__ == '__main__':
    main()
