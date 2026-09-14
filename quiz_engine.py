import time
import os
import random

TIME_LIMIT = 15

#clearing screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_question(question, question_number, total, difficulty, score):
    clear_screen()
    
    difficulty_label = {1: "Easy", 2: "Medium", 3: "Hard"}
    #format of printing
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
    start_time = time.time()

    while True:
        try: 
            answer = int(input(f"ur answer: "))
            #protection from user mistake
            if 1 <= answer <= len(question["options"]):
                break
            else:
                print(f"print correct number")
        except ValueError:
            print("invalid number")
    time_taken = round( time.time() - start_time, 2)
    selected_option = question["options"][answer -1]
    is_correct = selected_option == question["answer"]
    return is_correct, time_taken


#just feedback
def display_feedback(is_correct, time_taken, correct_answer, new_difficulty):
    difficulties = {1: "Easy", 2: "Medium", 3: "Hard"}
    print("----------------------")
    if is_correct:
        print("correct")
    else:
        print("wrong, correct answer is: ", correct_answer)
    print(time_taken)
    print(difficulties[new_difficulty])
    print("----------------------")
    
#displaying the result (simple calculation)
def display_results(list_time_taken, list_is_correct):
    sum_correct = 0
    for i in list_is_correct:
        if i:
            sum_correct+=1
    accuracy = round(sum_correct / len(list_is_correct) * 100, 2)
    avg_time = round(sum(list_time_taken) / len(list_time_taken), 2)
    print(sum_correct, "/", len(list_is_correct))
    print(accuracy)
    print(avg_time)



