import pytest
from lab10.function_01 import racer_disqualified

@pytest.mark.parametrize("times, penalties, expected", [
    ([100, 100, 100], [], False),
    ([150, 150, 150], [], False),
    ([151, 100, 100], [], True),
    ([100, 151, 100], [], True),
    ([100, 100, 151], [], True),
    ([100, 100, 100], [100], False),
    ([100, 100, 100], [101], True),
    ([100, 100, 100], [50, 50], False),
    ([100, 100, 100], [50, 51], True),
    ([100, 100, 100], [10] * 5, False),
    ([100, 100, 100], [10] * 6, True),
])
def test_disqualification_rules(times, penalties, expected):
    assert racer_disqualified(times, [100, 100, 100], len(penalties), penalties) is expected

@pytest.mark.parametrize("args", [
    ("100,100,100", [100, 100, 100], 0, []),
    ([100, 100], [100, 100, 100], 0, []),
    ([100, 100, 1.5], [100, 100, 100], 0, []),
    ([100, 100, 100], "100,100,100", 0, []),
    ([100, 100, 100], [100, 100], 0, []),
    ([100, 100, 100], [100, 100, "100"], 0, []),
    ([100, 100, 100], [100, 100, 100], "0", []),
    ([100, 100, 100], [100, 100, 100], 0, ""),
    ([100, 100, 100], [100, 100, 100], 1, [1.5]),
    ([100, 100, 100], [100, 100, 100], 2, [10]),
])
def test_invalid_inputs(args):
    with pytest.raises(ValueError):
        racer_disqualified(*args)
