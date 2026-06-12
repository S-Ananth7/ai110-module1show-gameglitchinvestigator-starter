# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:**

```
Probe parse_guess() with unusual inputs (negatives, decimals, very large
values, whitespace, scientific notation) and tell me which ones crash or
behave incorrectly. Then generate pytest cases that verify the game handles
each edge case gracefully instead of raising an exception.
```

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Decimal `3.7` | (above) | `test_decimal_input_is_truncated` | ✅ | Users naturally type fractions; the parser should truncate to an int, not error. |
| Extremely large `1.0e999` | (above) | `test_extremely_large_value_does_not_crash` | ✅ | `float("1.0e999")` is infinity, and `int(infinity)` raised `OverflowError` — a real crash we found and fixed. |
| Negative / out-of-range `-5`, `200` | (above) | `test_negative_guess_is_out_of_range`, `test_guess_above_range_is_rejected` | ✅ | A guess outside the difficulty's range is impossible to win with; it should be rejected with a clear message instead of silently accepted. |

**What the probing revealed:** `1.0e999` crashed with `OverflowError` because, during the refactor, the exception handler had been narrowed from `except Exception` to `except ValueError`. Fix: catch `(ValueError, OverflowError)`, and add an optional range check (`low`/`high`) so out-of-range guesses fail gracefully.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
