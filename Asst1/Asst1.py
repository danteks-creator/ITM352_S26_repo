import json, os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = lambda f: os.path.join(BASE_DIR, f)

def run_quiz():
    

    if not os.path.exists(path('questions.json')): 
        return print("Error: questions.json not found in " + BASE_DIR)
        
    with open(path('questions.json')) as f: 
        questions = json.load(f)


    score, hs_path = 0, path('highscore.txt')
    high_score = 0
    if os.path.exists(hs_path):
        with open(hs_path, 'r') as f:
            try:
                high_score = int(f.read().strip())
            except:
                high_score = 0


    print("WELCOME TO THE QUIZ")
    print("HOW TO ANSWER:")
    print("- Type the letter of your choice (ex: 'a').")
    print("- For multiple answers, separate letters with spaces (ex: 'a b c').")
    print("- Commas and capitalization will be ignored automatically.")
    

    for q in questions:
        print(f"\n{q['question']}")
        options = q['options']
        for k, v in sorted(options.items()):
            print(f"{k}) {v}")
        
        
        user_input = []
        valid_keys = sorted(options.keys())
        while not user_input or not all(c in valid_keys for c in user_input):
            user_input = input(f"Your choice ({valid_keys[0]}-{valid_keys[-1]}): ").lower().replace(',', ' ').split()
            if not user_input or not all(c in valid_keys for c in user_input):
                print(f"Invalid input. Please use letters: {', '.join(valid_keys)}")
                

        if q.get('match_type') == 'any':
            is_correct = any(choice in q['correct_answers'] for choice in user_input)
        else:
            is_correct = sorted(user_input) == sorted(q['correct_answers'])

        if is_correct:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer(s) was: {', '.join(q['correct_answers'])}")

    
    print("\n" + "=" * 20)
    print(f"Quiz Complete! Final Score: {score}/{len(questions)}")
    
    if score > high_score:
        print(f"NEW HIGH SCORE: {score}! (Previous record: {high_score})")
        with open(hs_path, 'w') as f:
            f.write(str(score))
    else:
        print(f"Current high score remains: {high_score}")

if __name__ == "__main__":
    run_quiz()