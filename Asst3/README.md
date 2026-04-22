# Asst3_NoJS - No JavaScript, No CSS Quiz App

This is a simplified version of the Asst3 quiz application built **without JavaScript or external CSS**.

## Key Differences from Asst3

- **No JavaScript** – All interactions are traditional HTML form submissions with page reloads
- **No external CSS** – Basic inline styles only (embedded in `base.html`)
- **No timed mode** – Only standard quiz mode is available (timed countdown requires JavaScript)
- **Simpler flow** – Each answer submission reloads the page to show the next question
- **Same core features**:
  - User registration and login with password hashing
  - Quiz question shuffling and answer choice shuffling
  - Score tracking and persistence
  - Leaderboard with ranking
  - Performance results summary

## What Works

✓ User registration and login  
✓ Quiz with shuffled questions and answers  
✓ Score calculation (single/multiple correct answers)  
✓ Results page with score breakdown  
✓ Leaderboard with ranking  
✓ File-based data persistence (users.json, scores.json, highscore.txt)  

## What's Different

✗ No client-side timer (timed mode removed)  
✗ No AJAX – full page reload on each answer  
✗ No fancy animations or styling  
✗ Slower UX due to page reloads  

## How to Run

1. Install Flask:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:
   ```bash
   python Asst3_NoJS.py
   ```

3. Open `http://127.0.0.1:5000` in your browser

4. Register a new account, log in, and start the quiz

## File Structure

```
Asst3_NoJS/
├── Asst3_NoJS.py          # Main Flask application
├── requirements.txt        # Python dependencies
├── questions.json          # Quiz questions (sample)
├── users.json              # User accounts (created on first run)
├── scores.json             # Quiz scores (created on first run)
├── highscore.txt           # Global high score (created on first run)
└── templates/
    ├── base.html           # Base template with navigation
    ├── index.html          # Home page
    ├── quiz.html           # Quiz start page
    ├── quiz_question.html  # Question display with form
    ├── results.html        # Quiz results page
    ├── leaderboard.html    # Top scores leaderboard
    ├── login.html          # Login form
    ├── register.html       # Registration form
    └── error.html          # Error page
```

## Validation

- **Username**: 3-20 characters, alphanumeric + underscore
- **Password**: At least 6 characters, must include a number
- **Answer selection**: Checkboxes allow single or multiple selections

## Question Types

- **Standard (all)**: All correct answers must be selected
- **Any**: At least one correct answer must be selected

## Notes

- This version is ideal for learning Flask form handling without modern JavaScript frameworks
- All data is stored locally in JSON files (not a production database)
- No client-side validation, only server-side
