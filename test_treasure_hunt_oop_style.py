import pytest

from treasure_hunt_oop_style import TreasureFinder


MOCKED_USER_INPUT = [
    [55, 14, 25, 52, 21],
    [44, 31, 11, 53, 43],
    [24, 13, 45, 12, 34],
    [42, 22, 43, 32, 41],
    [51, 23, 33, 54, 15]
]

MOCKED_WRONG_USER_INPUT = [
    [55, 14, 25, 52, 21],
    [44, 31, 11, 53, 43],
    [24, 13, 45, 12, 34],
    [42, 22, 43, 21, 41],
    [51, 23, 33, 54, 11]
]

MOCKED_DATA = [
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15]
]

MOCKED_TREASURE_IN_CLUES = [
    [55, 14, 25, 52, 21],
    [44, 31, 11, 53, 43],
    [24, 13, 45, 12, 34],
    [42, 22, 43, 32, 41],
    [51, 23, 33, 54, 55]
]

CLUES = [11, 55, 15]


class TestTreasureFinder(object):

    def setup_class(cls):
        cls.treasure_finder_instance = TreasureFinder()

    def test_get_user_inputs(self, mocker):
        mocker.patch("treasure_hunt_oop_style.input", return_value="15")
        result = self.treasure_finder_instance.get_user_inputs()
        assert result == MOCKED_DATA

        mocker.patch("treasure_hunt_oop_style.input", return_value="10")
        result = self.treasure_finder_instance.get_user_inputs()
        assert result == []

    @pytest.mark.parametrize(
        "user_input,expected",
        [
            (77, None),
            (54, True)
        ]
    )
    def test_validate_value(self, user_input, expected):
        result = self.treasure_finder_instance._validate_user_input(user_input)
        assert result is expected


    def test_find_treasure(self):
        mocked_steps_to_treasure = [11, 55, 15]
        mocked_clue_place = 21
        mocked_result = [11, 55, 15, 21, 44, 32, 13, 25, 43]
        result = self.treasure_finder_instance.find_treasure(
            mocked_steps_to_treasure, mocked_clue_place, MOCKED_USER_INPUT
        )
        assert result is True
        assert mocked_steps_to_treasure == mocked_result

    @pytest.mark.parametrize(
        "user_input,expected",
        [
            ([43, MOCKED_USER_INPUT], [True, 43, 43]),
            ([21, MOCKED_USER_INPUT], [False, 21, 44])
        ]
    )
    def test_check_cell(self, user_input, expected):
        result = self.treasure_finder_instance.check_cell(*user_input)
        assert result.is_treasure is expected[0]
        assert result.cell_coordinates == expected[1]
        assert result.cell_value == expected[2]

    @pytest.mark.parametrize(
        "user_input,expected",
        [
            (MOCKED_USER_INPUT, (CLUES, 21, False)),
            (MOCKED_TREASURE_IN_CLUES, ([11, 55], 55, True))
        ]
    )
    def test_find_treasure_in_clues(self, user_input, expected):
        result = self.treasure_finder_instance.find_treasure_in_clues(user_input)
        assert result[0] == expected[0]
        assert result[1] == expected[1]
        assert result[2] is expected[2]

    def test_start_searching(self, mocker):
        mocked_steps_to_treasure = [11, 55, 15]
        mocked_cell_value = 21
        mocked_get_user_data = mocker.patch(
            "treasure_hunt_oop_style.TreasureFinder.get_user_inputs", return_value=MOCKED_USER_INPUT
        )
        mocked_find_treasure_in_clues = mocker.patch(
            "treasure_hunt_oop_style.TreasureFinder.find_treasure_in_clues",
            return_value=(mocked_steps_to_treasure, mocked_cell_value, False)
        )
        mocked_find_treasure = mocker.patch("treasure_hunt_oop_style.TreasureFinder.find_treasure", return_value=True)
        self.treasure_finder_instance.start_searching()

        mocked_get_user_data.assert_called_once()
        mocked_find_treasure_in_clues.assert_called_once_with(MOCKED_USER_INPUT)
        mocked_find_treasure.assert_called_once_with(mocked_steps_to_treasure, mocked_cell_value, MOCKED_USER_INPUT)

    def test_start_searching_wrong_user_input(self, mocker):
        mocked_get_user_data = mocker.patch(
            "treasure_hunt_oop_style.TreasureFinder.get_user_inputs", return_value=[]
        )
        self.treasure_finder_instance.start_searching()
        mocked_get_user_data.assert_called_once()

    def test_start_searching_treasure_in_clues(self, mocker):
        mocked_cell_value = 55
        mocked_steps = [11, 55]
        mocked_get_user_data = mocker.patch(
            "treasure_hunt_oop_style.TreasureFinder.get_user_inputs", return_value=MOCKED_TREASURE_IN_CLUES
        )
        mocked_find_treasure_in_clues = mocker.patch(
            "treasure_hunt_oop_style.TreasureFinder.find_treasure_in_clues",
            return_value=(mocked_steps, mocked_cell_value, True)
        )
        self.treasure_finder_instance.start_searching()
        mocked_get_user_data.assert_called_once()
        mocked_find_treasure_in_clues.assert_called_once_with(MOCKED_TREASURE_IN_CLUES)
