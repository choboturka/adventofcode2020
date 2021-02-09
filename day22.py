from collections import deque
from itertools import islice

test = '''
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''.strip()

infinite_test = '''
Player 1:
43
19

Player 2:
2
29
14
'''.strip()


def get_data():
    with open('inputs\\day22.txt') as file:
        return file.read()


def parse_decks(data):
    players_data = data.split('\n\n')
    decks = []
    for player_data in players_data:
        deck = deque(int(card) for card in player_data.split('\n')[1:])
        decks.append(deck)
    return tuple(decks)


def score_deck(deck):
    score = 0
    for multiplier, card in enumerate(reversed(deck), start=1):
        score += card * multiplier
    return score


def play_game(first_deck, second_deck):
    while first_deck and second_deck:
        first_card = first_deck.popleft()
        second_card = second_deck.popleft()
        if first_card > second_card:
            first_deck.append(first_card)
            first_deck.append(second_card)
        elif second_card > first_card:
            second_deck.append(second_card)
            second_deck.append(first_card)
        else:
            raise ValueError('Ties are not allowed!')
    winning_deck = first_deck or second_deck
    return winning_deck


def play_recursive_game(first_deck, second_deck):
    played_games = set()
    while first_deck and second_deck:
        game_state = tuple(first_deck), tuple(second_deck)
        if game_state in played_games:
            return True
        else:
            played_games.add(game_state)
        first_card, second_card = first_deck.popleft(), second_deck.popleft()
        continue_recursion = (len(first_deck) >= first_card) and (len(second_deck) >= second_card)
        if continue_recursion:
            first_copy = deque(islice(first_deck, 0, first_card))
            second_copy = deque(islice(second_deck, 0, second_card))
            first_player_won = play_recursive_game(first_copy, second_copy)
        else:
            first_player_won = first_card > second_card
        if first_player_won:
            first_deck.append(first_card)
            first_deck.append(second_card)
        else:
            second_deck.append(second_card)
            second_deck.append(first_card)
    return bool(first_deck)


def get_first_star(data):
    first_deck, second_deck = parse_decks(data)
    winning_deck = play_game(first_deck, second_deck)
    return score_deck(winning_deck)


def get_second_star(data):
    first_deck, second_deck = parse_decks(data)
    first_player_won = play_recursive_game(first_deck, second_deck)
    return score_deck(first_deck) if first_player_won else score_deck(second_deck)


assert get_first_star(test) == 306
print(get_first_star(get_data()))
assert get_second_star(test) == 291
print(get_second_star(get_data()))
