from data_handler import load_questions, questions_by_difficulty, questions_by_topic
from adaptive_engine import calculate_performance, change_difficulty
import os, random
from quiz_engine import display_question, get_user_answer, display_feedback, display_results

def main():
    questions = load_questions()
    current_difficulty = 1
    history = []
    list_time_taken = []
    list_is_correct = []
    score = 0
    
    
    for i in range(1, 10):
         pool = questions_by_difficulty(questions, current_difficulty)
         time_limit = current_difficulty*10 +10
         a = random.choice(pool)
         display_question(a, i, 10, current_difficulty, score)
         is_correct, time_taken = get_user_answer(a)
         score = calculate_performance(is_correct, time_taken, time_limit)
         history.append(score)
         current_difficulty = change_difficulty(history, current_difficulty)
         list_time_taken.append(time_taken)
         list_is_correct.append(is_correct)
         display_feedback(is_correct, time_taken, a["answer"], current_difficulty)
    display_results(list_time_taken, list_is_correct)




         

         
main()

