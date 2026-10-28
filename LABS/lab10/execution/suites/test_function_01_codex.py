"""Fresh Codex-authored tests generated for this laboratory execution."""
import pytest
from lab10.function_01 import racer_disqualified

@pytest.mark.parametrize("event", range(3))
@pytest.mark.parametrize("offset, expected", [(-1, False), (0, False), (1, True)])
def test_time_limit_for_each_event(event, offset, expected):
    winner = [100, 200, 300]
    times = winner.copy()
    times[event] = int(1.5 * winner[event]) + offset
    assert racer_disqualified(times, winner, 0, []) is expected

@pytest.mark.parametrize("penalties, expected", [
    ([], False), ([99], False), ([100], False), ([101], True),
    ([50, 50], False), ([50, 51], True), ([1] * 5, False), ([1] * 6, True),
])
def test_penalty_limits(penalties, expected):
    assert racer_disqualified([10, 20, 30], [10, 20, 30], len(penalties), penalties) is expected

@pytest.mark.parametrize("position, invalid", [
    (0, (10, 20, 30)), (0, [10, 20]), (0, [10, 20, "30"]),
    (1, None), (1, [10, 20]), (1, [10, 20, 30.5]),
    (2, "0"), (3, ()), (3, ["10"]), (3, [10]),
])
def test_reference_input_contract(position, invalid):
    args = [[10, 20, 30], [10, 20, 30], 0, []]
    args[position] = invalid
    with pytest.raises(ValueError):
        racer_disqualified(*args)
