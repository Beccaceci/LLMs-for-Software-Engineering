import pytest

@pytest.mark.parametrize("grades, expected", [
    ([18,25,30,33,22,28],26.25),
    ([20,25,30,33,29,28],28.0),
    ([18,19,20,30,33,25],23.5),
    ([18]*6,18.0), ([30]*6,30.0), ([33]*6,33.0),
    ([25]*6,25.0), ([18,18,18,33,33,33],25.5),
    ([18.5,20,22,24,26,30],23.0),
])
def test_valid_grades(grades, expected):
    original = grades.copy()
    assert compute_average(grades) == pytest.approx(expected, abs=1e-10)
    assert grades == original

@pytest.mark.parametrize("grades", [[18]*5,[18]*7,[],[17,20,22,24,26,30],
    [34,20,22,24,26,30],[31,20,22,24,26,30],[32,20,22,24,26,30],
    [float("nan"),20,22,24,26,30],[float("inf"),20,22,24,26,30],
    [True,20,22,24,26,30]])
def test_invalid_grades(grades):
    with pytest.raises(ValueError): compute_average(grades)

@pytest.mark.parametrize("value", ["25",None,complex(25,0)])
def test_non_numeric_grades(value):
    with pytest.raises(TypeError): compute_average([value,20,22,24,26,30])
