# Asst3 Quiz App

This folder contains the Flask version of the quiz game.

## What it does

- Loads questions from `questions.json`
- Shuffles questions and answer choices each session
- Supports login and registration
- Shows real-time feedback and final score details
- Saves scores to local JSON files
- Shows a global leaderboard
- Supports standard mode and timed challenge mode

## How to run

1. Open a terminal in the `Asst3` folder.
2. Install Flask if needed: `pip install -r requirements.txt`
3. Start the app: `python Asst3.py`
4. Open `http://127.0.0.1:5000` in your browser.

## How to test

- Register a new user and log in.
- Start a standard quiz and answer questions.
- Start a timed quiz and watch the countdown.
- Check the results page and leaderboard page.
- Try invalid usernames, passwords, or empty answers to see validation messages.

## Notes

- Score history is stored in `scores.json`.
- User accounts are stored in `users.json`.
- The high score is stored in `highscore.txt`.