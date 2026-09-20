import json

#small function to add the questions, making my life a bit easier
def add_newQuestion(new_question):
    with open("questions.json", "r") as f:
        questions = json.load(f)
    questions.append(new_question)
    with open("questions.json", "w") as f:
        json.dump(questions, f, indent = 2)


#standard format of question in json(for me to put the questions in json easily)
questions = {
        "id": 1,
        "question": "",
        "options": ["", ""],
        "answer": "",
        "difficulty": "",
        "topic": ""
}

