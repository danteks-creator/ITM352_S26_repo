from flask import Flask, render_template_string
import requests

app = Flask(__name__)


def get_meme():
	url = "https://meme-api.com/gimme/wholesomememes"
	response = requests.request("GET", url)
	response.raise_for_status()
	return response.json()


@app.route("/")
def index():
	try:
		meme = get_meme()
		return render_template_string(
			"""
			<!doctype html>
			<html>
			<head>
				<title>Wholesome Meme</title>
				<style>
					body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; background: #f7f7f7; }
					.card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 6px 24px rgba(0,0,0,0.08); }
					img { max-width: 100%; height: auto; border-radius: 10px; }
					a { color: #0b66c3; }
				</style>
			</head>
			<body>
				<div class="card">
					<h1>{{ title }}</h1>
					<p>Subreddit: {{ subreddit }}</p>
					<img src="{{ image_url }}" alt="{{ title }}">
					<p><a href="{{ post_link }}" target="_blank" rel="noreferrer">Open original post</a></p>
					<p><a href="/">Load another meme</a></p>
				</div>
			</body>
			</html>
			""",
			title=meme.get("title", "Wholesome Meme"),
			subreddit=meme.get("subreddit", "unknown"),
			image_url=meme.get("url", ""),
			post_link=meme.get("postLink", meme.get("url", "#")),
		)
	except requests.RequestException as error:
		return render_template_string(
			"""
			<!doctype html>
			<html>
			<head><title>Error</title></head>
			<body>
				<h1>Could not load meme</h1>
				<p>{{ error }}</p>
			</body>
			</html>
			""",
			error=error,
		), 500


if __name__ == '__main__':
	app.run(debug=True)
