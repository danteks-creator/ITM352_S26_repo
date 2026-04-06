import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
source_file = os.path.join(base_dir, "..", "Asst1", "questions.json")
output_file = os.path.join(base_dir, "quiz_questions.json")

if os.path.exists(source_file):
	with open(source_file, "r") as input_file:
		quiz_questions = json.load(input_file)

	with open(output_file, "w") as json_file:
		json.dump(quiz_questions, json_file, indent=2)

	print(f"Quiz questions saved to {output_file}")
else:
	print(f"Error: The file '{source_file}' does not exist.")
