from logic_utils import check_guess, update_score, get_range_for_difficulty, parse_guess

# check_guess returns a (outcome, message) tuple, so we check the outcome [0].

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_high_says_go_lower():
    # The hint direction must match the outcome
    _, message = check_guess(60, 50)
    assert "LOWER" in message

def test_too_low_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message

def test_range_per_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_win_score_has_no_off_by_one():
    # Winning on the 1st guess should award 90 (100 - 10*1), not 80.
    assert update_score(0, "Win", 1) == 90

def test_wrong_guess_never_rewards():
    # A wrong guess always loses points, regardless of attempt parity.
    assert update_score(0, "Too High", 2) == -5
    assert update_score(0, "Too Low", 3) == -5

def test_parse_guess_rejects_non_numbers():
    ok, value, error = parse_guess("abc")
    assert ok is False
    assert value is None
    assert error


# ----------------------------------------------------------------------
# Challenge 1: Advanced edge-case tests
# Each verifies the game handles an unusual input gracefully (no crash).
# ----------------------------------------------------------------------

def test_decimal_input_is_truncated():
    # Edge case: decimals. "3.7" should become the int 3, not crash.
    ok, value, error = parse_guess("3.7")
    assert ok is True
    assert value == 3
    assert error is None

def test_extremely_large_value_does_not_crash():
    # Edge case: huge scientific-notation value. float("1.0e999") is infinity,
    # which used to crash with OverflowError when converted to int.
    ok, value, error = parse_guess("1.0e999")
    assert ok is False
    assert value is None
    assert error  # a friendly message, not an exception

def test_negative_guess_is_out_of_range():
    # Edge case: negative number. With a range given, -5 is rejected gracefully.
    ok, value, error = parse_guess("-5", low=1, high=100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in error

def test_guess_above_range_is_rejected():
    # Edge case: a number larger than the allowed maximum.
    ok, value, error = parse_guess("200", low=1, high=100)
    assert ok is False
    assert "between 1 and 100" in error

def test_in_range_guess_still_accepted():
    # Sanity: a normal guess inside the range still passes.
    ok, value, error = parse_guess("42", low=1, high=100)
    assert ok is True
    assert value == 42
    assert error is None
