import json

#getting the question from json file
def load_questions():
    with open ("questions.json", "r") as f:
        return json.load(f)

#filtering the questions by difficulty
def questions_by_difficulty(questions, difficulty):
    result = []
    for q in questions:
        if q["difficulty"] == difficulty:
            result.append(q)
    return result

    
#filtering the questions by topic
def questions_by_topic(questions, topic):
    result = []
    for q in questions:
        if q["topic"] == topic:
            result.append(q)
    return q
    

def saving_sessions(username, result):
    try:
        with open("sessions.json", "r") as f:
            session = json.load(f)
    except FileNotFoundError:
        session = []
    
    session.append({
        "username": username,
        "result": result
    })
    with open("sessions.json", "w") as f:
        json.dump(session, f, indent=2)


