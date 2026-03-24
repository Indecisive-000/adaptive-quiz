import json

def add_newQuestion(new_question):
    with open("questions.json", "r") as f:
        questions = json.load(f)
    questions.append(new_question)
    with open("questions.json", "w") as f:
        json.dump(questions, f, indent = 2)


# questions = {
#         "id": 1,
#         "question": "",
#         "options": ["", ""],
#         "answer": "",
#         "difficulty": "",
#         "topic": ""
# }

# add_newQuestion(question)
