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
