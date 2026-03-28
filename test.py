from data_handler import load_questions
from adaptive_engine import calculate_performance, change_difficulty
import os
from quiz_engine import display_question, get_user_answer




questions = load_questions()
print(questions[0]["question"])

history = []
score = calculate_performance(True, 15, 15)
history.append(score)

print(score)

question = {
    "question": "What does OOP stand for?",
    "options": ["Object-Oriented Programming", "Open Operating Process", "Ordered Object Protocol", "Output Oriented Programming"],
    "answer": "Object-Oriented Programming",
    "difficulty": 1,
    "topic": "OOP"
}

display_question(question, 1, 10, 1, 0)
is_correct, time_taken = get_user_answer(question)
print(is_correct)
print(time_taken)
