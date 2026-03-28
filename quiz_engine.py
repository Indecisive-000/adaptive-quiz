import time
import os
import random

TIME_LIMIT = 15


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_question(question, question_number, total, difficulty, score):
    clear_screen()
    
    difficulty_label = {1: "Easy", 2: "Medium", 3: "Hard"}
    
    print("=" * 50)
    print(f"Question {question_number} of {total}")
    print(f"Difficulty: {difficulty_label[difficulty]}")
    print(f"Topic: {question['topic']}")
    print(f"Score: {score}")
    print("=" * 50)
    print()
    print(question["question"])
    print()
    
    for i, option in enumerate(question["options"]):
        print(f"  {i + 1}. {option}")
    
    print()

def get_user_answer(question):
    start_line = time.time()

    while True:
        try: 
            answer = int(input(f"ur answer: (1-{len(question['options'])}):"))
            if 1 <= answer <= len(question['options']):
                break
            else:
                print(f"print number")
        except ValueError:
            print("invalid number")
    time_taken = round( time.time() - start_line, 2)
    selected_option = question["options"][answer -1]
    is_correct = selected_option == question["answer"]
    return is_correct, time_taken
