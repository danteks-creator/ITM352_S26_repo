"""Flask quiz application for Asst3.

This file loads quiz data from JSON, serves the web pages, and stores scores.
"""

import json
import os
import random
import re
import string
import time
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
SCORES_FILE = os.path.join(BASE_DIR, "scores.json")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.txt")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "itm352-quiz-secret-key")


# Create the data files if they are missing so the app can start cleanly.
def ensure_data_files() -> None:
    if not os.path.exists(USERS_FILE):
        save_json(USERS_FILE, {})
    if not os.path.exists(SCORES_FILE):
        save_json(SCORES_FILE, [])
    if not os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as highscore_file:
            highscore_file.write("0")


def load_json(path: str, default):
    # Read JSON data from disk and fall back to a safe default if needed.
    try:
        with open(path, "r", encoding="utf-8") as data_file:
            return json.load(data_file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        return default


def save_json(path: str, payload) -> None:
    # Save Python data back to a JSON file.
    with open(path, "w", encoding="utf-8") as data_file:
        json.dump(payload, data_file, indent=2)


def read_high_score() -> int:
    # Load the stored high score from the text file.
    try:
        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as score_file:
            return int(score_file.read().strip() or 0)
    except (ValueError, FileNotFoundError):
        return 0


def write_high_score(score: int) -> None:
    # Update the high score file when a new record is reached.
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as score_file:
        score_file.write(str(score))


def validate_question_payload(question: dict) -> bool:
    # Make sure each question has the fields the quiz needs.
    required_keys = {"question", "options", "correct_answers"}
    if not required_keys.issubset(question.keys()):
        return False
    if not isinstance(question.get("question"), str) or not question["question"].strip():
        return False
    if not isinstance(question.get("options"), dict) or len(question["options"]) < 2:
        return False
    if not isinstance(question.get("correct_answers"), list) or not question["correct_answers"]:
        return False
    return True


def load_questions() -> list:
    # Read and validate quiz questions from the JSON file.
    questions = load_json(QUESTIONS_FILE, [])
    if not isinstance(questions, list):
        raise ValueError("Question data must be a list.")

    for question in questions:
        if not isinstance(question, dict) or not validate_question_payload(question):
            raise ValueError("Question data is malformed.")

    return questions


def login_required(route_func):
    # Protect routes that should only be visible after login.
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to access the quiz.", "error")
            return redirect(url_for("login"))
        return route_func(*args, **kwargs)

    return wrapper


def reshuffle_question(question: dict, question_id: int) -> dict:
    # Shuffle the answer order and remap the answer letters.
    option_items = list(question["options"].items())
    random.shuffle(option_items)

    letters = list(string.ascii_lowercase)
    remapped_options = {}
    key_map = {}

    for idx, (old_key, option_text) in enumerate(option_items):
        new_key = letters[idx]
        remapped_options[new_key] = option_text
        key_map[old_key] = new_key

    correct_answers = [
        key_map[old_key]
        for old_key in question["correct_answers"]
        if old_key in key_map
    ]

    return {
        "id": question_id,
        "question": question["question"],
        "options": remapped_options,
        "correct_answers": sorted(correct_answers),
        "match_type": question.get("match_type", "all"),
    }


def initialize_quiz_session() -> None:
    # Start a new standard quiz session.
    questions = load_questions()
    indexed_questions = list(enumerate(questions))
    random.shuffle(indexed_questions)

    shuffled_questions = [
        reshuffle_question(question, question_id)
        for question_id, question in indexed_questions
    ]

    session["quiz_questions"] = shuffled_questions
    session["quiz_progress"] = 0
    session["quiz_score"] = 0
    session["quiz_answers"] = []
    session["quiz_start_time"] = time.time()
    session["question_started_at"] = time.time()
    session["quiz_finished"] = False


def initialize_quiz_session_with_mode(challenge_mode: str, time_limit_seconds: int) -> None:
    # Start a new quiz session and store the selected mode.
    questions = load_questions()
    indexed_questions = list(enumerate(questions))
    random.shuffle(indexed_questions)

    shuffled_questions = [
        reshuffle_question(question, question_id)
        for question_id, question in indexed_questions
    ]

    session["quiz_questions"] = shuffled_questions
    session["quiz_progress"] = 0
    session["quiz_score"] = 0
    session["quiz_answers"] = []
    session["quiz_start_time"] = time.time()
    session["question_started_at"] = time.time()
    session["quiz_finished"] = False
    session["challenge_mode"] = challenge_mode
    session["time_limit_seconds"] = time_limit_seconds if challenge_mode == "timed" else 0


def remaining_question_seconds() -> float:
    # Calculate how much time is left for the current timed question.
    if session.get("challenge_mode") != "timed":
        return 0
    started_at = session.get("question_started_at", time.time())
    limit = session.get("time_limit_seconds", 0)
    return max(float(limit) - (time.time() - float(started_at)), 0.0)


def current_question_payload():
    # Build the current question response that the browser will display.
    questions = session.get("quiz_questions", [])
    progress = session.get("quiz_progress", 0)
    if progress >= len(questions):
        return None

    question = questions[progress]
    timer_seconds_left = round(remaining_question_seconds(), 2)
    return {
        "id": question["id"],
        "question": question["question"],
        "options": question["options"],
        "question_number": progress + 1,
        "total_questions": len(questions),
        "challenge_mode": session.get("challenge_mode", "standard"),
        "time_limit_seconds": session.get("time_limit_seconds", 0),
        "time_left_seconds": timer_seconds_left,
    }


def calculate_result() -> dict:
    # Collect the final score summary shown on the results page.
    total_questions = len(session.get("quiz_questions", []))
    score = session.get("quiz_score", 0)
    incorrect = max(total_questions - score, 0)
    start_time = session.get("quiz_start_time", time.time())
    time_taken = round(max(time.time() - start_time, 0), 2)

    incorrect_questions = [
        answer_record["question"]
        for answer_record in session.get("quiz_answers", [])
        if not answer_record.get("is_correct")
    ]

    return {
        "username": session.get("username", "guest"),
        "display_name": session.get("display_name", session.get("username", "guest")),
        "score": score,
        "total_questions": total_questions,
        "correct": score,
        "incorrect": incorrect,
        "time_taken_seconds": time_taken,
        "areas_for_improvement": incorrect_questions,
        "challenge_mode": session.get("challenge_mode", "standard"),
        "time_limit_seconds": session.get("time_limit_seconds", 0),
        "ended_by_timeout": session.get("ended_by_timeout", False),
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }


def persist_result(result: dict) -> dict:
    # Save the completed quiz result and update the high score if needed.
    scores = load_json(SCORES_FILE, [])
    if not isinstance(scores, list):
        scores = []

    scores.append(result)
    save_json(SCORES_FILE, scores)

    current_high = read_high_score()
    if result["score"] > current_high:
        write_high_score(result["score"])
        result["new_high_score"] = True
    else:
        result["new_high_score"] = False
    result["high_score"] = max(current_high, result["score"])
    return result


def sorted_scores(scores: list) -> list:
    # Sort scores from best to worst for the leaderboard.
    return sorted(
        scores,
        key=lambda row: (
            row.get("score", 0),
            -float(row.get("total_questions", 0) or 1),
            -float(row.get("time_taken_seconds", 0) or 0),
        ),
        reverse=True,
    )


def compute_rankings(scores: list) -> list:
    # Add rank numbers to the sorted leaderboard entries.
    ranked = []
    for idx, row in enumerate(sorted_scores(scores), start=1):
        enriched = dict(row)
        enriched["rank"] = idx
        ranked.append(enriched)
    return ranked


def enrich_result_with_ranking(result: dict) -> dict:
    # Attach the user rank to the final result if we can find it.
    scores = load_json(SCORES_FILE, [])
    ranked_scores = compute_rankings(scores if isinstance(scores, list) else [])

    match_rank = None
    for row in ranked_scores:
        if (
            row.get("submitted_at") == result.get("submitted_at")
            and row.get("username") == result.get("username")
            and row.get("score") == result.get("score")
            and row.get("time_taken_seconds") == result.get("time_taken_seconds")
        ):
            match_rank = row.get("rank")
            break

    result["rank"] = match_rank
    return result


def validate_username(username: str) -> str:
    # Check that the username is short, readable, and safe.
    normalized = (username or "").strip()
    if len(normalized) < 3 or len(normalized) > 20:
        return "Username must be 3-20 characters."
    if not re.fullmatch(r"[A-Za-z0-9_]+", normalized):
        return "Username can only use letters, numbers, and underscore."
    return ""


def validate_password(password: str) -> str:
    # Require a password that is long enough and includes a number.
    if len(password or "") < 6:
        return "Password must be at least 6 characters."
    if not re.search(r"\d", password):
        return "Password must include at least one number."
    return ""


def validate_display_name(display_name: str) -> str:
    # Keep leaderboard names simple and readable.
    normalized = (display_name or "").strip()
    if len(normalized) < 2 or len(normalized) > 30:
        return "Name must be 2-30 characters."
    if not re.fullmatch(r"[A-Za-z0-9_\- ]+", normalized):
        return "Name can only include letters, numbers, spaces, underscore, and hyphen."
    return ""


ensure_data_files()


@app.route("/")
def home():
    # Show the landing page with the stored high score.
    high_score = read_high_score()
    return render_template("index.html", high_score=high_score)


@app.route("/register", methods=["GET", "POST"])
def register():
    # Handle new account creation.
    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    username_error = validate_username(username)
    if username_error:
        flash(username_error, "error")
        return render_template("register.html", username=username), 400

    password_error = validate_password(password)
    if password_error:
        flash(password_error, "error")
        return render_template("register.html", username=username), 400

    if password != confirm_password:
        flash("Passwords do not match.", "error")
        return render_template("register.html", username=username), 400

    users = load_json(USERS_FILE, {})
    if username in users:
        flash("Username already exists.", "error")
        return render_template("register.html", username=username), 400

    users[username] = {
        "password_hash": generate_password_hash(password),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_json(USERS_FILE, users)

    flash("Account created. You can now log in.", "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle user login.
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    users = load_json(USERS_FILE, {})
    user = users.get(username)
    if not user or not check_password_hash(user["password_hash"], password):
        flash("Invalid username or password.", "error")
        return render_template("login.html", username=username), 401

    session.clear()
    session["username"] = username
    flash("Logged in successfully.", "success")
    return redirect(url_for("quiz"))


@app.route("/logout")
def logout():
    # Clear the session when the user logs out.
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/quiz")
@login_required
def quiz():
    # Render the quiz page after login.
    return render_template("quiz.html", username=session.get("username"))


@app.route("/results")
@login_required
def results():
    # Show the latest quiz summary.
    result = session.get("latest_result")
    if not result:
        flash("No quiz result found. Please take a quiz first.", "error")
        return redirect(url_for("quiz"))

    scores = load_json(SCORES_FILE, [])
    ranked_scores = compute_rankings(scores if isinstance(scores, list) else [])
    top_scores = ranked_scores[:10]
    result = enrich_result_with_ranking(result)
    session["latest_result"] = result
    return render_template("results.html", result=result, top_scores=top_scores)


@app.route("/leaderboard")
@login_required
def leaderboard():
    # Show the top 10 scores and the current user's best rank.
    scores = load_json(SCORES_FILE, [])
    ranked_scores = compute_rankings(scores if isinstance(scores, list) else [])
    top_scores = ranked_scores[:10]

    best_user_rank = None
    username = session.get("username")
    for row in ranked_scores:
        if row.get("username") == username:
            best_user_rank = row.get("rank")
            break

    return render_template(
        "leaderboard.html",
        top_scores=top_scores,
        best_user_rank=best_user_rank,
    )


@app.route("/api/quiz/start", methods=["POST"])
@login_required
def api_quiz_start():
    # Start a new quiz session from the browser.
    payload = request.get_json(silent=True) or {}
    challenge_mode = payload.get("challenge_mode", "standard")
    time_limit_seconds = payload.get("time_limit_seconds", 20)

    # Validate mode and timer settings before creating a session.
    if challenge_mode not in {"standard", "timed"}:
        return jsonify({"error": "challenge_mode must be 'standard' or 'timed'."}), 400
    if challenge_mode == "timed":
        if not isinstance(time_limit_seconds, int) or time_limit_seconds < 5 or time_limit_seconds > 120:
            return jsonify({"error": "time_limit_seconds must be an integer between 5 and 120."}), 400

    try:
        initialize_quiz_session_with_mode(challenge_mode, time_limit_seconds)
        question = current_question_payload()
    except ValueError as exc:
        return jsonify({"error": f"Failed to load questions: {exc}"}), 500

    return jsonify(
        {
            "message": "Quiz started.",
            "question": question,
            "score": session.get("quiz_score", 0),
            "challenge_mode": challenge_mode,
            "time_limit_seconds": session.get("time_limit_seconds", 0),
        }
    )


@app.route("/api/quiz/question", methods=["GET"])
@login_required
def api_quiz_question():
    # Return the current question if a quiz is active.
    question = current_question_payload()
    if not question:
        return jsonify({"error": "Quiz session not started or already complete."}), 404
    return jsonify({"question": question, "score": session.get("quiz_score", 0)})


@app.route("/api/quiz/answer", methods=["POST"])
@login_required
def api_quiz_answer():
    # Check the selected answer and move to the next question.
    questions = session.get("quiz_questions", [])
    progress = session.get("quiz_progress", 0)

    if not questions or progress >= len(questions):
        return jsonify({"error": "Quiz is not active. Start a new quiz."}), 400

    # If timed mode has already expired, end the quiz right away.
    if session.get("challenge_mode") == "timed" and remaining_question_seconds() <= 0:
        session["ended_by_timeout"] = True
        current_question = questions[progress]
        quiz_answers = session.get("quiz_answers", [])
        quiz_answers.append(
            {
                "question": current_question["question"],
                "selected": [],
                "correct_answers": sorted(current_question["correct_answers"]),
                "is_correct": False,
            }
        )
        session["quiz_answers"] = quiz_answers
        session["quiz_progress"] = len(questions)
        result = calculate_result()
        result = persist_result(result)
        result = enrich_result_with_ranking(result)
        session["latest_result"] = result
        session["quiz_finished"] = True
        return jsonify(
            {
                "completed": True,
                "timed_out": True,
                "feedback": "Time is up. Quiz ended.",
                "score": session.get("quiz_score", 0),
                "result": result,
                "redirect_url": url_for("results"),
            }
        )

    payload = request.get_json(silent=True) or {}
    selected = payload.get("answers")
    # The browser must send answers as a list like ["a", "c"].
    if not isinstance(selected, list):
        return jsonify({"error": "answers must be a list."}), 400

    selected_normalized = sorted({str(option).lower().strip() for option in selected if option})
    current_question = questions[progress]
    valid_keys = sorted(current_question["options"].keys())

    if not selected_normalized:
        return jsonify({"error": "Please select at least one option."}), 400
    if any(option not in valid_keys for option in selected_normalized):
        return jsonify({"error": "Submitted option is invalid."}), 400

    # Handle "any" match type or exact full-match answers.
    correct_answers = sorted(current_question["correct_answers"])
    if current_question.get("match_type") == "any":
        is_correct = any(option in correct_answers for option in selected_normalized)
    else:
        is_correct = selected_normalized == correct_answers

    if is_correct:
        session["quiz_score"] = session.get("quiz_score", 0) + 1

    quiz_answers = session.get("quiz_answers", [])
    quiz_answers.append(
        {
            "question": current_question["question"],
            "selected": selected_normalized,
            "correct_answers": correct_answers,
            "is_correct": is_correct,
        }
    )
    session["quiz_answers"] = quiz_answers
    session["quiz_progress"] = progress + 1
    session["question_started_at"] = time.time()

    next_question = current_question_payload()
    if next_question:
        # Return the next question without ending the quiz yet.
        return jsonify(
            {
                "is_correct": is_correct,
                "feedback": "Correct!" if is_correct else "Incorrect.",
                "score": session.get("quiz_score", 0),
                "next_question": next_question,
                "completed": False,
            }
        )

    result = calculate_result()
    result = persist_result(result)
    result = enrich_result_with_ranking(result)
    session["latest_result"] = result
    session["quiz_finished"] = True

    # Quiz is complete, so return final data and redirect target.

    return jsonify(
        {
            "is_correct": is_correct,
            "feedback": "Correct!" if is_correct else "Incorrect.",
            "score": session.get("quiz_score", 0),
            "completed": True,
            "result": result,
            "redirect_url": url_for("results"),
        }
    )


@app.route("/api/quiz/timeout", methods=["POST"])
@login_required
def api_quiz_timeout():
    # End the quiz immediately when the timer runs out.
    questions = session.get("quiz_questions", [])
    progress = session.get("quiz_progress", 0)

    if not questions or progress >= len(questions):
        return jsonify({"error": "Quiz is not active. Start a new quiz."}), 400
    if session.get("challenge_mode") != "timed":
        return jsonify({"error": "Timeout endpoint is only available in timed mode."}), 400

    # Record the timed-out question as incorrect before finalizing.
    session["ended_by_timeout"] = True
    current_question = questions[progress]
    quiz_answers = session.get("quiz_answers", [])
    quiz_answers.append(
        {
            "question": current_question["question"],
            "selected": [],
            "correct_answers": sorted(current_question["correct_answers"]),
            "is_correct": False,
        }
    )
    session["quiz_answers"] = quiz_answers
    session["quiz_progress"] = len(questions)

    result = calculate_result()
    result = persist_result(result)
    result = enrich_result_with_ranking(result)
    session["latest_result"] = result
    session["quiz_finished"] = True

    return jsonify(
        {
            "completed": True,
            "timed_out": True,
            "feedback": "Time is up. Quiz ended.",
            "score": session.get("quiz_score", 0),
            "result": result,
            "redirect_url": url_for("results"),
        }
    )


@app.route("/api/quiz/display-name", methods=["POST"])
@login_required
def api_quiz_display_name():
    # Save the name the user wants to show on the leaderboard.
    result = session.get("latest_result")
    if not result:
        return jsonify({"error": "No quiz result is available yet."}), 400

    payload = request.get_json(silent=True) or {}
    display_name = payload.get("display_name", "")

    if display_name:
        # Validate custom leaderboard names.
        name_error = validate_display_name(display_name)
        if name_error:
            return jsonify({"error": name_error}), 400
    else:
        display_name = session.get("username", "guest")

    result["display_name"] = display_name.strip()
    session["display_name"] = result["display_name"]

    scores = load_json(SCORES_FILE, [])
    if isinstance(scores, list):
        # Update the exact stored score row that matches this result.
        updated = False
        for idx, row in enumerate(scores):
            if (
                row.get("submitted_at") == result.get("submitted_at")
                and row.get("username") == result.get("username")
                and row.get("score") == result.get("score")
                and row.get("time_taken_seconds") == result.get("time_taken_seconds")
            ):
                scores[idx]["display_name"] = result["display_name"]
                updated = True
                break
        if updated:
            save_json(SCORES_FILE, scores)

    result = enrich_result_with_ranking(result)
    session["latest_result"] = result

    return jsonify({"message": "Name saved.", "result": result})


@app.route("/api/scores", methods=["GET", "POST"])
@login_required
def api_scores():
    # Let the browser read or save score history.
    if request.method == "GET":
        # Return ranked results plus a quick top-10 slice.
        scores = load_json(SCORES_FILE, [])
        ranked_scores = compute_rankings(scores if isinstance(scores, list) else [])
        top_10 = ranked_scores[:10]
        my_rank = None
        username = session.get("username")
        for row in ranked_scores:
            if row.get("username") == username:
                my_rank = row.get("rank")
                break
        return jsonify({"scores": ranked_scores, "top_10": top_10, "my_rank": my_rank})

    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "").strip()
    score = payload.get("score")
    total_questions = payload.get("total_questions")
    time_taken = payload.get("time_taken_seconds")

    if not username:
        return jsonify({"error": "username is required."}), 400
    if not isinstance(score, int) or score < 0:
        return jsonify({"error": "score must be a non-negative integer."}), 400
    if not isinstance(total_questions, int) or total_questions <= 0:
        return jsonify({"error": "total_questions must be a positive integer."}), 400
    if not isinstance(time_taken, (int, float)) or time_taken < 0:
        return jsonify({"error": "time_taken_seconds must be non-negative."}), 400

    # Build a score record from request data and save it.
    result = {
        "username": username,
        "display_name": payload.get("display_name", username),
        "score": score,
        "total_questions": total_questions,
        "correct": score,
        "incorrect": max(total_questions - score, 0),
        "time_taken_seconds": round(float(time_taken), 2),
        "areas_for_improvement": payload.get("areas_for_improvement", []),
        "challenge_mode": payload.get("challenge_mode", "standard"),
        "time_limit_seconds": payload.get("time_limit_seconds", 0),
        "ended_by_timeout": bool(payload.get("ended_by_timeout", False)),
        "submitted_at": datetime.now(timezone.utc).isoformat(),
    }

    persisted = persist_result(result)
    return jsonify({"message": "Score saved.", "result": persisted}), 201


@app.errorhandler(404)
def not_found(_error):
    # Show a friendly page when a route is missing.
    return render_template("error.html", message="Page not found."), 404


@app.errorhandler(500)
def server_error(_error):
    # Show a friendly page if the server hits an unexpected error.
    return (
        render_template(
            "error.html",
            message="Something went wrong while processing your request.",
        ),
        500,
    )


if __name__ == "__main__":
    ensure_data_files()
    app.run(debug=True)