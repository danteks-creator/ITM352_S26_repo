# Asst3 Quiz App

This folder contains the current Flask quiz app for Asst3.

## Features

- User registration and login with hashed passwords
- Shuffled question order and shuffled answer options each quiz
- Standard mode and timed challenge mode
- Timed challenge is 60 seconds for the whole quiz
- Server-side timeout enforcement when the timer expires
- Results summary with score, accuracy, and improvement areas
- Persistent leaderboard and high score tracking

## How Timed Mode Works

- Timed mode starts with a 60-second quiz timer
- A visible countdown appears on the question page
- If time reaches 0, the quiz ends immediately
- Results are marked with `ended_by_timeout: true`

## How to Run

1. Open a terminal in the `Asst3` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python Asst3.py
   ```
4. Open `http://127.0.0.1:5000` in your browser.

## Data Files

- `questions.json`: Quiz question bank
- `users.json`: Registered users and password hashes
- `scores.json`: Saved quiz results
- `highscore.txt`: Global high score

## Project Structure

```
Asst3/
|- Asst3.py
|- README.md
|- requirements.txt
|- questions.json
|- users.json
|- scores.json
|- highscore.txt
|- templates/
|  |- base.html
|  |- index.html
|  |- login.html
|  |- register.html
|  |- quiz.html
|  |- quiz_question.html
|  |- results.html
|  |- leaderboard.html
|  |- error.html
|- static/
   |- app.js
   |- style.css
```

## Validation Rules

- Username: 3-20 characters, letters/numbers/underscore only
- Password: at least 6 characters and must include a number
- Display name: 2-30 characters, letters/numbers/spaces/underscore/hyphen

## Notes

- Data is stored locally in JSON/text files.
- Quiz logic and timer enforcement are handled server-side.
