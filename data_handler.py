import json, os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
SESSIONS_FILE = os.path.join(BASE_DIR, "sessions.json")


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def questions_by_difficulty(questions, difficulty):
    result = []
    for q in questions:
        if q["difficulty"] == difficulty:
            result.append(q)
    return result


def questions_by_topic(questions, topic):
    result = []
    for q in questions:
        if q["topic"] == topic:
            result.append(q)
    return result


def load_sessions():
    try:
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def saving_sessions(username, result):
    sessions = load_sessions()
    sessions.append({
        "username": username,
        "result": result
    })
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=2, ensure_ascii=False)