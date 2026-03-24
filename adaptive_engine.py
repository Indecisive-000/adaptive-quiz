

def calculate_avg(correct, timeTaken, timeLimit):
    if correct == True:
        accuracy_score = 1
    else:
        accuracy_score = 0
    speed_score = max(0, (timeLimit - timeTaken) / timeLimit)
    avg = (0.7 * accuracy_score) + (0.3 * speed_score)
    return round(avg, 2)    


def get_new_difficulty(history, i_difficulty):
    if len(history) == 0:
        return i_difficulty
    avg_score = sum(history) / len(history)