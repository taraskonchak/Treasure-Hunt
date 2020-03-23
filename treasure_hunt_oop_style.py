from collections import namedtuple


class TreasureFinder(object):
    __user_input = [[], [], [], [], []]
    __CLUES = [11, 55, 15]

    def get_user_inputs(self):
        for current_list in self.__user_input:
            for item_index in range(5):
                list_index = self.__user_input.index(current_list)
                user_input = input(f"Enter the {item_index + 1} value for {list_index + 1} list: ")
                if user_input.isdigit() and self._validate_user_input(int(user_input)):
                    current_list.append(int(user_input))
                else:
                    print("Wrong input!")
                    return []
        return self.__user_input

    @staticmethod
    def _validate_user_input(number):
        if 11 <= number <= 55:
            return True

    def find_treasure(self, steps_to_treasure, clue_place, user_input):
        counter = 1
        while counter < 1000:
            cell_data = self.check_cell(clue_place, user_input)
            if cell_data.is_treasure:
                steps_to_treasure.append(cell_data.cell_coordinates)
                return True

            steps_to_treasure.append(cell_data.cell_coordinates)
            clue_place = cell_data.cell_value
            counter += 1
        return False

    @staticmethod
    def check_cell(clue_place, user_input):
        cell_data = namedtuple("result", ["is_treasure", "cell_coordinates", "cell_value"])
        row = int(str(clue_place)[0])
        column = int(str(clue_place)[1])
        cell_value = user_input[row - 1][column - 1]
        if cell_value == clue_place:
            result = cell_data(True, clue_place, cell_value)
        else:
            result = cell_data(False, clue_place, cell_value)
        return result

    def find_treasure_in_clues(self, user_input):
        way_to_treasure = []
        for clue in self.__CLUES:
            cell_data = self.check_cell(clue, user_input)
            way_to_treasure.append(cell_data.cell_coordinates)
            if cell_data.is_treasure:
                return way_to_treasure, cell_data.cell_value, True
        return way_to_treasure, cell_data.cell_value, False

    def start_searching(self):
        user_inputs = self.get_user_inputs()
        if not user_inputs:
            return
        steps_to_treasure, last_cell_value, is_treasure = self.find_treasure_in_clues(user_inputs)
        if is_treasure:
            print(steps_to_treasure)
            return
        treasure_exists = self.find_treasure(steps_to_treasure, last_cell_value, user_inputs)
        if treasure_exists:
            print(steps_to_treasure)
        else:
            print("There is no treasure :(")


if __name__ == "__main__":
    finder = TreasureFinder()
    finder.start_searching()