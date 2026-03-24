import json

def load_questions():
    with open ("questions.json", "r") as f:
        return json.load(f)
    
def questions_by_difficulty(questions, difficulty):
    return [q for q in questions if q["difficulty"] == difficulty]

def questions_by_topic(questions, topic):
    return [q for q in questions if q["topic"] == topic]

def saving_sessions(username, result):
    try:
        with open("questions.json", "r") as f:
            session = json.load(f)
    except FileNotFoundError:
        session = []
    
    session.append({
        "username": username,
        "result": result
    })
    with open("session.json", "w") as f:
        json.dump(session, f, indent=2)


