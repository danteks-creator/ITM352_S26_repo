import json
import os

from flask import Flask, redirect, render_template_string, request, session, url_for


app = Flask(__name__)
app.secret_key = "quiz-skeleton-secret-key"

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUIZ_DIR = os.path.join(REPO_DIR, "Asst1")
QUESTIONS_PATH = os.path.join(QUIZ_DIR, "questions.json")
HIGH_SCORE_PATH = os.path.join(QUIZ_DIR, "highscore.txt")


def load_questions():
	with open(QUESTIONS_PATH, "r", encoding="utf-8") as file:
		return json.load(file)


def load_high_score():
	if not os.path.exists(HIGH_SCORE_PATH):
		return 0
	with open(HIGH_SCORE_PATH, "r", encoding="utf-8") as file:
		try:
			return int(file.read().strip())
		except ValueError:
			return 0


def save_high_score(score):
	with open(HIGH_SCORE_PATH, "w", encoding="utf-8") as file:
		file.write(str(score))


def is_correct_answer(question, selected_answers):
	correct_answers = question["correct_answers"]
	if question.get("match_type") == "any":
		return any(answer in correct_answers for answer in selected_answers)
	return sorted(selected_answers) == sorted(correct_answers)


@app.route("/")
def index():
	questions = load_questions()
	high_score = load_high_score()
	return render_template_string(
		"""
		<!doctype html>
		<html>
		<head>
			<title>Quiz Game Skeleton</title>
			<style>
				body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; background: #f4f6f8; }
				.card { background: white; border-radius: 14px; padding: 24px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); }
				a.button { display: inline-block; padding: 12px 18px; border-radius: 10px; text-decoration: none; background: #1f6feb; color: white; margin-right: 10px; }
				ul { line-height: 1.7; }
			</style>
		</head>
		<body>
			<div class="card">
				<h1>Assignment 1 Quiz Game</h1>
				<p>This is a Flask skeleton based on the real quiz data in <strong>Asst1/questions.json</strong>.</p>
				<p><strong>Total questions:</strong> {{ total_questions }}</p>
				<p><strong>High score:</strong> {{ high_score }}</p>
				<p>
					<a class="button" href="{{ url_for('start_quiz') }}">Start Quiz</a>
					<a class="button" href="{{ url_for('instructions') }}">How It Works</a>
				</p>
				<h2>Planned Pages</h2>
				<ul>
					<li>Home page with navigation</li>
					<li>Instructions page</li>
					<li>Question page</li>
					<li>Results page</li>
				</ul>
			</div>
		</body>
		</html>
		""",
		total_questions=len(questions),
		high_score=high_score,
	)


@app.route("/instructions")
def instructions():
	return render_template_string(
		"""
		<!doctype html>
		<html>
		<head><title>Instructions</title></head>
		<body>
			<h1>How the Quiz Works</h1>
			<p>Answer each question one at a time. Some questions allow more than one correct choice.</p>
			<p><a href="{{ url_for('index') }}">Back Home</a></p>
		</body>
		</html>
		"""
	)


@app.route("/start")
def start_quiz():
	session["question_index"] = 0
	session["score"] = 0
	session["answers"] = []
	return redirect(url_for("quiz"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
	questions = load_questions()
	question_index = session.get("question_index", 0)

	if question_index >= len(questions):
		return redirect(url_for("results"))

	question = questions[question_index]

	if request.method == "POST":
		selected_answers = request.form.getlist("answer")
		session.setdefault("answers", []).append(
			{
				"question": question["question"],
				"selected": selected_answers,
				"correct": question["correct_answers"],
			}
		)

		if is_correct_answer(question, selected_answers):
			session["score"] = session.get("score", 0) + 1

		session["question_index"] = question_index + 1
		return redirect(url_for("quiz"))

	return render_template_string(
		"""
		<!doctype html>
		<html>
		<head>
			<title>Quiz Question</title>
			<style>
				body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; background: #f4f6f8; }
				.card { background: white; border-radius: 14px; padding: 24px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); }
				.option { margin: 10px 0; }
				button { padding: 10px 16px; border: 0; border-radius: 10px; background: #1f6feb; color: white; cursor: pointer; }
			</style>
		</head>
		<body>
			<div class="card">
				<p>Question {{ current_number }} of {{ total_questions }}</p>
				<h1>{{ question.question }}</h1>
				<form method="post">
					{% for key, value in question.options.items() %}
						<div class="option">
							<label>
								<input type="checkbox" name="answer" value="{{ key }}">
								{{ key }}) {{ value }}
							</label>
						</div>
					{% endfor %}
					<p><button type="submit">Submit Answer</button></p>
				</form>
			</div>
		</body>
		</html>
		""",
		question=question,
		current_number=question_index + 1,
		total_questions=len(questions),
	)


@app.route("/results")
def results():
	questions = load_questions()
	score = session.get("score", 0)
	high_score = load_high_score()
	if score > high_score:
		save_high_score(score)
		high_score = score

	return render_template_string(
		"""
		<!doctype html>
		<html>
		<head>
			<title>Results</title>
			<style>
				body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; background: #f4f6f8; }
				.card { background: white; border-radius: 14px; padding: 24px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); }
			</style>
		</head>
		<body>
			<div class="card">
				<h1>Quiz Complete</h1>
				<p><strong>Final Score:</strong> {{ score }} / {{ total_questions }}</p>
				<p><strong>High Score:</strong> {{ high_score }}</p>
				<p><a href="{{ url_for('start_quiz') }}">Play Again</a></p>
				<p><a href="{{ url_for('index') }}">Back Home</a></p>
			</div>
		</body>
		</html>
		""",
		score=score,
		total_questions=len(questions),
		high_score=high_score,
	)


if __name__ == "__main__":
	app.run(debug=True)
