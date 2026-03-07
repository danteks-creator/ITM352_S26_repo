#quiz gme, second version
#name: Dante Saito
#date: Feb 24, 2026
#make a list wih the questions and correct answers

QUESTIONS = [
    ( "what is the airspeed of an unladen swallow in miles per hour?", "12"),
    ("what is the capital of texas?", "austin")
    ("the Last Supper was painted by which artist?", "Leonardo da Vinci")
]

for question, correct_answer in QUESTIONS:
    answer = input(question *  "2")
    if answer.lower() == correct_answer.lower():
        print("correct")
    else:
        print(f"The answer is '{correct_answer}', not '{answer}'")