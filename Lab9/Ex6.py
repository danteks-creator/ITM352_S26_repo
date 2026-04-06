import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(base_dir, "quiz_questions.json")

if os.path.exists(json_file_path):
	with open(json_file_path, "r") as json_file:
		quiz_questions = json.load(json_file)

	print(json.dumps(quiz_questions, indent=2))
else:
	print(f"Error: The file '{json_file_path}' does not exist.")
