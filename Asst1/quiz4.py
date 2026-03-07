#quiz gme, second version
#name: Dante Saito
#date: Feb 24, 2026
#make a list wih the questions and correct answers
#make QUESTIONS a dictionary, to include other pptions with th e correct choiece.
#allow users to select an answer by a label

QUESTIONS = {
    "what is the airspeed of an unladen swallow in miles per hour?": ["12", "10", "15", "8"],
    "what is the capital of texas?": ["austin", "houston", "dallas", "san antonio"],
    "the Last Supper was painted by which artist?": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"]
}

for question, options in QUESTIONS.items():
    correct_answer = options[0]  # the first option is the correct answer
    for i, alternative in enumerate(sorted(options)):
        print(f"{i + 1}. {alternative}")

    answer = input(question + " ")
    if answer == correct_answer.lower():
        print("correct")
    else:
        print(f"The answer is '{correct_answer}', not '{answer}'")
        