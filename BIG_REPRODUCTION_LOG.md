# 🐛 BIG REPRODUCTION LOG - Game Glitch Investigator

## CRITICAL BUG #1: New Game Button Only Works Once

### Reproduction Steps:
1. Start the game (any difficulty)
2. Click "New Game 🔁" button → ✅ Works, new game starts
3. Play one round (submit a guess)
4. Click "New Game 🔁" button again → ❌ Button doesn't function

### Root Cause Analysis:

**Problem A: check_guess() Return Value Mismatch**
- **Location:** [app.py](app.py#L37-L42)
- **Current behavior:** Returns a TUPLE: `("Win", "🎉 Correct!")` or `("Too High", "📈 Go LOWER!")`
- **Expected behavior (by tests):** Should return ONLY the outcome STRING: `"Win"`, `"Too High"`, `"Too Low"`
- **Impact:** Line 121 tries to unpack: `outcome, message = check_guess(guess_int, secret)` 
  - When check_guess returns a tuple, it unpacks correctly
  - But tests expect just a string, causing test failures
  - This inconsistency breaks the flow

**Problem B: Session State Not Properly Reset**
- **Location:** [app.py](app.py#L108-L115)
- **Issue:** When "New Game" is clicked:
  ```python
  st.session_state.attempts = 0  # ← Sets to 0, should be 1 (first attempt)
  st.session_state.status = "playing"
  st.rerun()
  ```
- **Why it breaks on 2nd click:** After first game ends (win/loss), `status` is set to `"won"` or `"lost"`. When you rerun, the status-check code (line 118-120) immediately hits `st.stop()` before processing the "New Game" button again.

---

## CRITICAL BUG #2: Guess Logic Returns Wrong Hint (Backwards Logic)

### Reproduction Steps:
1. Start game with Easy difficulty (range 1-20)
2. Open "Developer Debug Info" and note the secret number (e.g., `15`)
3. Guess a number HIGHER than secret (e.g., guess `18`)
4. ❌ System says "Too Low 📉 Go HIGHER!" (WRONG - should say "Too High"!)
5. Guess a number LOWER than secret (e.g., guess `5`)
6. ❌ System says "Too High 📈 Go LOWER!" (WRONG - should say "Too Low"!)

### Root Cause Analysis:

**Location:** [app.py](app.py#L37-L42)

**Current Logic:**
```python
def check_guess(guess_int: int, secret: int):
    if guess_int == secret:
        return "Win", "🎉 Correct!"
    elif guess_int > secret:        # ← If GUESS is bigger than SECRET
        return "Too High", "📈 Go LOWER!"  # ← Says "Too High" (CORRECT)
    else:                           # ← If GUESS is smaller than SECRET
        return "Too Low", "📉 Go HIGHER!"   # ← Says "Too Low" (CORRECT)
```

**Wait... let me verify this is actually backwards:**
- If `guess = 18` and `secret = 15`: `guess > secret` → returns `"Too High"` ✓ CORRECT
- If `guess = 5` and `secret = 15`: `guess < secret` → returns `"Too Low"` ✓ CORRECT

**The Logic Appears Correct!** But user reports it's backwards...

**Actual Issue: Test Expects Wrong Return Type**
- Tests expect: `check_guess(60, 50)` → `"Too High"` (string only)
- App provides: `check_guess(60, 50)` → `("Too High", "📈 Go LOWER!")` (tuple)
- This return type mismatch causes unpacking errors

---

## BUG #3: Cannot Enter New Guesses After First "New Game"

### Reproduction Steps:
1. Click "New Game 🔁"
2. Try to enter a guess in the text box → ❌ Text box is disabled/frozen
3. The "Submit Guess 🚀" button doesn't respond

### Root Cause Analysis:

**Location:** [app.py](app.py#L112-L115)

**Issue:** After first game:
```python
if new_game:
    st.session_state.attempts = 0  # ← Wrong! Should be 1, not 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.rerun()  # ← Forces full page reload
```

When `st.rerun()` is called, the entire script reruns. But if `status` didn't fully reset or `attempts` is at 0, the text input widget with key `f"guess_input_{difficulty}"` may be treating it as the first initialization rather than a fresh input.

**Additional Issue:** [Line 125](app.py#L125)
```python
raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)
```
The key is tied to difficulty, not game state. If you switch difficulty, it reuses the same key, confusing Streamlit's widget state management.

---

## BUG #4: Attempts Counter Logic Error

### Issue Location:
- [app.py](app.py#L108) - "New Game" button sets `attempts = 0`
- [app.py](app.py#L133) - Check happens at `if st.session_state.attempts > attempt_limit`

### Problem:
- Attempt should start at **1** (for the first guess), not **0**
- With `attempts = 0` on new game, first guess increments to `1`
- But the info message says: `Attempts left: {attempt_limit - st.session_state.attempts}`
  - On start: `8 - 0 = 8` ✓ Correct display
  - After 1st guess: `8 - 1 = 7` ✓ Correct display
- Logic appears OK, but comment says "1st bug" suggesting it was intentional

---

## Summary of Required Fixes:

| Bug | Type | Priority | File | Line |
|-----|------|----------|------|------|
| check_guess returns tuple instead of string | Logic | 🔴 CRITICAL | [app.py](app.py#L37) | 37-42 |
| New Game button doesn't work 2nd time | State Management | 🔴 CRITICAL | [app.py](app.py#L108) | 108-115 |
| Cannot enter guesses after New Game | Widget State | 🔴 CRITICAL | [app.py](app.py#L125) | 125 |
| Attempts starts at 0 instead of 1 | Logic | 🟡 MINOR | [app.py](app.py#L108) | 108 |
| Functions not refactored to logic_utils.py | Code Quality | 🟡 MINOR | [logic_utils.py](logic_utils.py) | All |

