# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Click "New Game 🔁" button (second time) | New game starts, secret resets, attempts reset to 1, can enter new guesses | Button doesn't function; game state remains in "won"/"lost" status; st.stop() prevents further execution | Session state `status` stuck on "won"/"lost"; st.rerun() called but status not fully cleared |
| Submit guess higher than secret (e.g., guess 18 when secret is 15) | Display "Too High 📈 Go LOWER!" hint | Display "Too Low 📉 Go HIGHER!" hint (backwards logic) | check_guess() returns tuple ("Too High", message) instead of string "Too High"; unpacking fails |
| After New Game clicked, try to enter a guess in text input | Text input accepts new guess; "Submit Guess 🚀" button responds | Text input is frozen/disabled; button unresponsive | Widget key `guess_input_{difficulty}` state confused; attempts initialized to 0 instead of 1 |
| Start new game | Display "Attempts left: 8" (for Normal difficulty with 8 allowed) | Display "Attempts left: 8" then "Attempts left: 7" after 1st guess | attempts set to 0 instead of 1 on line 108; off-by-one error in attempt tracking |
| Click "New Game 🔁" | History should clear (empty list) | Previous guesses persist in history from last game | st.session_state.history not reset in new_game block; old guesses show in Developer Debug Info |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
=> I use Claude Haiku 4.5

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
