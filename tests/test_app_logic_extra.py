from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    update_score,
    check_guess,
)

# Extended tests for helper functions — I requested additional test coverage, agent built test suite

def test_get_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)
    # Unknown difficulty falls back to Normal-range behavior
    assert get_range_for_difficulty("Unknown") == (1, 100)


def test_parse_guess_valid_integers():
    ok, val, err = parse_guess("42")
    assert ok is True and val == 42 and err is None


def test_parse_guess_float_and_decimal():
    ok, val, err = parse_guess("42.0")
    assert ok is True and val == 42 and err is None

    ok2, val2, err2 = parse_guess("3.9")
    assert ok2 is True and val2 == 3 and err2 is None


def test_parse_guess_invalid_inputs():
    ok, val, err = parse_guess("")
    assert ok is False and val is None and "Enter a guess" in err

    ok2, val2, err2 = parse_guess(None)
    assert ok2 is False and val2 is None and "Enter a guess" in err2

    ok3, val3, err3 = parse_guess("not-a-number")
    assert ok3 is False and val3 is None and "not a number" in err3.lower()


def test_update_score_win_and_loss():
    # Winning should not subtract points
    s = update_score(100, "Win", 1)
    assert s == 100

    # Losing should subtract 10 but grant a 10 bonus when current_score < 10
    s2 = update_score(50, "Lose", 2)
    assert s2 == 40

    s3 = update_score(5, "Lose", 1)
    # current_score < 10 so points = -10 + 10 -> 0 change
    assert s3 == 5


def test_check_guess_mapping_consistency():
    # Ensure check_guess returns the canonical outcomes used by the app
    assert check_guess(10, 10) == "Win"
    assert check_guess(20, 10) == "Too High"
    assert check_guess(5, 10) == "Too Low"
