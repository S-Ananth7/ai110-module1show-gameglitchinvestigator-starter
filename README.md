# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game's purpose
A Streamlit number-guessing game. The app picks a secret number within a range
that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50). You
guess until you find it or run out of attempts, getting "Higher/Lower" hints and
a score along the way.

### Bugs found & fixes applied

| # | Bug (symptom) | Root cause | Fix |
|---|---------------|-----------|-----|
| 1 | Hints lied — guessing too low said "Go LOWER!" | The secret was cast to a string on even turns, so the int/str comparison crashed into a broken fallback branch with swapped messages | Removed the `str()` flip; `check_guess` now compares ints and returns the correct direction |
| 2 | Secret out of range (e.g. 54 while on Hard 1–50) | The secret was generated only once and never regenerated when difficulty changed | Regenerate the secret when the difficulty changes, and remember which difficulty it belongs to |
| 3 | Stale guesses/score carried over when switching difficulty | The round state was never reset on a difficulty change | Reset attempts/score/status/history whenever the secret is regenerated |
| 4 | Attempt counter was one too high | Counter started at `1` instead of `0` | Start attempts at `0` (now consistent with the New Game button) |
| 5 | Debug panel showed state one step behind | The panel was rendered at the top, before the guess was processed | Moved the debug panel to the bottom of the script |
| 6 | Range text always said "between 1 and 100" | The numbers were hardcoded | Use the `low`/`high` variables so the text matches the real range |
| 7 | You could keep guessing after winning | `st.stop()` was indented under the `else`, so it only ran when you lost | De-indented `st.stop()` so it halts on both win and loss |
| 8 | Win on the 1st guess gave 80 instead of 90 | Off-by-one `+ 1` in the points formula | Removed the `+ 1` |
| 9 | Wrong guesses could *add* points | A parity check rewarded "Too High" on even turns, and the two wrong outcomes were scored inconsistently | Every wrong guess now loses 5 points, no parity trick |

### Refactor & tests
- Moved all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`,
  `update_score`) out of `app.py` into `logic_utils.py`. `app.py` now imports them
  and contains only the Streamlit UI — one source of truth, no duplication.
- Updated `tests/test_game_logic.py` to match the `(outcome, message)` contract and
  added tests covering hint direction, per-difficulty range, the win-score off-by-one,
  and the "wrong guess never rewards" rule.

## 📸 Demo Walkthrough

1. Launch the app with `python -m streamlit run app.py` and open the sidebar to pick a difficulty.
2. Expand **Developer Debug Info** (now at the bottom) to see the live secret, attempts, score, and history.
3. Make a guess that is too low — the hint correctly says **"Go HIGHER!"**; guess too high and it says **"Go LOWER!"**.
4. Switch difficulty mid-game — the secret regenerates inside the new range and the round resets cleanly (history clears, score back to 0).
5. Keep guessing until you win — you get points based on how few guesses you used, and after winning the game won't accept more guesses until you press **New Game**.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest -v
============================= test session starts =============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
tests/test_game_logic.py::test_too_high_says_go_lower PASSED             [ 28%]
tests/test_game_logic.py::test_too_low_says_go_higher PASSED             [ 35%]
tests/test_game_logic.py::test_range_per_difficulty PASSED               [ 42%]
tests/test_game_logic.py::test_win_score_has_no_off_by_one PASSED        [ 50%]
tests/test_game_logic.py::test_wrong_guess_never_rewards PASSED          [ 57%]
tests/test_game_logic.py::test_parse_guess_rejects_non_numbers PASSED    [ 64%]
tests/test_game_logic.py::test_decimal_input_is_truncated PASSED         [ 71%]
tests/test_game_logic.py::test_extremely_large_value_does_not_crash PASSED [ 78%]
tests/test_game_logic.py::test_negative_guess_is_out_of_range PASSED     [ 85%]
tests/test_game_logic.py::test_guess_above_range_is_rejected PASSED      [ 92%]
tests/test_game_logic.py::test_in_range_guess_still_accepted PASSED      [100%]

============================= 14 passed in 0.17s ==============================
```

### Edge cases covered (Challenge 1)

| Edge case | Why it matters | Handling |
|-----------|----------------|----------|
| Decimal (`3.7`) | Users may type fractions | Truncated to an int (`3`) |
| Extremely large (`1.0e999`) | Becomes infinity → used to crash with `OverflowError` | Caught and rejected with a friendly message |
| Negative / out-of-range (`-5`, `200`) | Outside the valid 1–N range | Rejected with "Guess must be between low and high" |

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
