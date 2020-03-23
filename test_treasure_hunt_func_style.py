import pytest

from treasure_hunt_func_style import *

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

MOCKED_TREASURE_IN_CLUES = [
    [55, 14, 25, 52, 21],
    [44, 31, 11, 53, 43],
    [24, 13, 45, 12, 34],
    [42, 22, 43, 32, 41],
    [51, 23, 33, 54, 55]
]

MOCKED_DATA = [
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15],
    [15, 15, 15, 15, 15]
]


@pytest.mark.parametrize(
    "user_input,expected",
    [
        ([43, MOCKED_USER_INPUT], [True, 43, 43]),
        ([21, MOCKED_USER_INPUT], [False, 21, 44])
    ]
)
def test_check_cell(user_input, expected):
    result = check_cell(*user_input)
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
def test_find_treasure_in_clues(user_input, expected):
    result = find_treasure_in_clues(user_input)
    assert result[0] == expected[0]
    assert result[1] == expected[1]
    assert result[2] is expected[2]


def test_find_treasure():
    mocked_steps_to_treasure = [11, 55, 15]
    mocked_clue_place = 21
    mocked_result = [11, 55, 15, 21, 44, 32, 13, 25, 43]
    find_treasure(mocked_steps_to_treasure, mocked_clue_place, MOCKED_USER_INPUT)
    assert mocked_steps_to_treasure == mocked_result


@pytest.mark.parametrize(
    "user_input,expected",
    [
        (77, None),
        (54, True)
    ]
)
def test_validate_value(user_input, expected):
    result = validate_value(user_input)
    assert result is expected


def test_get_user_data(mocker):
    mocker.patch("treasure_hunt_func_style.input", return_value="15")
    result = get_user_data()
    assert result == MOCKED_DATA

    mocker.patch("treasure_hunt_func_style.input", return_value="10")
    result = get_user_data()
    assert result == []


def test_main(mocker):
    mocked_steps_to_treasure = [11, 55, 15]
    mocked_get_user_data = mocker.patch(
        "treasure_hunt_func_style.get_user_data", return_value=MOCKED_USER_INPUT
    )
    mocked_find_treasure_in_clues = mocker.patch(
        "treasure_hunt_func_style.find_treasure_in_clues", return_value=(mocked_steps_to_treasure, 21, False)
    )
    mocked_find_treasure = mocker.patch("treasure_hunt_func_style.find_treasure", return_value=None)
    main()
    mocked_get_user_data.assert_called_once()
    mocked_find_treasure_in_clues.assert_called_once_with(MOCKED_USER_INPUT)
    mocked_find_treasure.assert_called_once_with(mocked_steps_to_treasure, 21, MOCKED_USER_INPUT)


def test_main_wrong_user_input(mocker):
    mocked_get_user_data = mocker.patch(
        "treasure_hunt_func_style.get_user_data", return_value=[]
    )
    main()
    mocked_get_user_data.assert_called_once()


def test_main_treasure_in_clues(mocker):
    mocked_get_user_data = mocker.patch(
        "treasure_hunt_func_style.get_user_data", return_value=MOCKED_TREASURE_IN_CLUES
    )
    mocked_find_treasure_in_clues = mocker.patch(
        "treasure_hunt_func_style.find_treasure_in_clues", return_value=([11, 55], 55, True)
    )
    main()
    mocked_get_user_data.assert_called_once()
    mocked_find_treasure_in_clues.assert_called_once_with(MOCKED_TREASURE_IN_CLUES)
