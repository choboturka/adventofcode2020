def get_data():
    with open("inputs\\day5.txt") as file:
        for line in file:
            rows = line[:7]
            columns = line[7:10]
            rows = rows.replace('F', '0').replace('B', '1')
            columns = columns.replace('L', '0').replace('R', '1')
            yield int(f'0b{rows}', 2), int(f'0b{columns}', 2)


def get_first_star():
    max_id = 0
    for row, column in get_data():
        seat_id = row * 8 + column
        if seat_id > max_id:
            max_id = seat_id
    print(max_id)


def get_second_star():
    seats = [row * 8 + col for row, col in get_data()]
    sorted_seats = sorted(seats)
    for current_seat, next_seat in zip(sorted_seats, sorted_seats[1:]):
        if next_seat - current_seat == 2:
            print(current_seat+1)


get_first_star()
get_second_star()
