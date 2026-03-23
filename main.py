import json

questions = [
    {
        "id": 1,
        "question": "",
        "options": ["", ""],
        "answer": "",
        "difficulty": "",
        "topic": ""
    }
]

with open("questions.json", "w") as f:
    json.dump(questions, f)