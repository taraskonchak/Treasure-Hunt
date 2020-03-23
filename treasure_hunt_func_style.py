from collections import namedtuple

CLUES = [11, 55, 15]


def check_cell(clue_place, user_input):
    cell_data = namedtuple("result", ["is_treasure", "cell_coordinates", "cell_value"])
    row, column = int(str(clue_place)[0]), int(str(clue_place)[1])

    cell_value = user_input[row - 1][column - 1]
    if cell_value == clue_place:
        result = cell_data(True, clue_place, cell_value)
    else:
        result = cell_data(False, clue_place, cell_value)
    return result


def find_treasure_in_clues(user_input):
    steps_to_treasure = []
    for clue in CLUES:
        cell_data = check_cell(clue, user_input)
        steps_to_treasure.append(cell_data.cell_coordinates)
        if cell_data.is_treasure:
            return steps_to_treasure, cell_data.cell_value, True
    return steps_to_treasure, cell_data.cell_value, False


def find_treasure(steps_to_treasure, clue_place, user_input):
    cell_data = check_cell(clue_place, user_input)
    if cell_data.is_treasure:
        return steps_to_treasure.append(cell_data.cell_coordinates)

    steps_to_treasure.append(cell_data.cell_coordinates)
    clue_place = cell_data.cell_value
    return find_treasure(steps_to_treasure, clue_place, user_input)


def validate_value(number):
    if 11 <= number <= 55:
        return True


def get_user_data():
    user_input = []
    for index in range(5):
        numbers = []
        for list_value in range(5):
            number = input(f"Enter the {list_value+1} value for {index+1} list: ")
            if number.isdigit() and validate_value(int(number)):
                numbers.append(int(number))
            else:
                print("Wrong input!")
                return []
        user_input.append(numbers)
    return user_input


def main():
    user_input = get_user_data()
    if not user_input:
        return
    steps_to_treasure, last_cell_value, is_treasure = find_treasure_in_clues(user_input)
    if is_treasure:
        print(steps_to_treasure)
        return
    try:
        find_treasure(steps_to_treasure, last_cell_value, user_input)
        print(steps_to_treasure)
    except RecursionError:
        print("There is no treasure :(")


if __name__ == "__main__":
    main()