# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
=> Fix the bugs in the Streamlit app, refactor logic into a shared module, add app-level tests, and make sure the game works correctly across new games and guess validation.
<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**
=> The agent reviewed `app.py`, identified logic issues, moved core game functions into `logic_utils.py`, updated `app.py` to import and use the shared logic, added inline `FIXME` comments, and created new pytest files for both helper logic and app behavior. It also added `tests/conftest.py` to fix pytest import resolution.

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->
=> I manually reviewed the proposed changes, verified the new tests, and confirmed the game behavior and bug fixes with pytest. I also checked the commit/remote status because the repo push required a separate Git workflow fix.
---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Invalid guess input | "Create tests for parse_guess input validation" | blank input, null input, non-numeric string | Yes | These cover bad user input and verify error handling stays consistent. |
| Guess outcome mapping | "Create tests for check_guess outcomes" | correct, too high, too low guesses | Yes | Ensures core feedback logic matches expected strings and avoids tuple mismatch. |
| App state reset | "Create tests for new game reset behavior" | new game resets history and status | Yes | Verifies the app clears previous guesses and starts fresh on new game. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
Refactor app.py logic into logic_utils.py, keep changes minimal, and preserve existing style.
```

**Linting output before:**

```
No formal linter output was generated during this session.
```

**Changes applied:**

- Kept the code style consistent with existing app structure.
- Added comments and `FIXME` annotations at known bug locations.
- Avoided unnecessary refactors beyond the requested logic and test fixes.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

Fix the Streamlit game logic bugs and add pytest coverage for helper logic and app behavior.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Copilot / VS Code agent | N/A |
| **Response summary** | Identified logic issues, wrote tests, and suggested fixes | Not used in this session |
| **More Pythonic?** | Yes | N/A |
| **Clearer explanation?** | Yes | N/A |

**Which did you prefer and why?**

I used the VS Code agent workflow for this session because it integrated directly with the workspace and produced practical code edits and tests. Since only one model was used, no direct comparison was made.

