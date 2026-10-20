D_MAX = 3
D_MIN = 1
A_WEIGHT = 0.7      # correctness matters most
T_WEIGHT = 0.3      # speed rewards confidence, but can't outweigh a wrong answer
WIN_SIZE = 5     # only the most recent answers are judged
MIN_ANSWERS = 3     # need this many answers at a level before changing it


def calculate_performance(accuracy, timeTaken, timeLimit):
    if accuracy == True:
        accuracy_score = 1
    else:
        accuracy_score = 0
    time_score = (timeLimit - timeTaken) / timeLimit
    if time_score < 0:
        time_score = 0
    avg = (A_WEIGHT * accuracy_score) + (time_score * T_WEIGHT)
    return round(avg, 2)


def change_difficulty(history, initialDifficulty):
    window = history[-WIN_SIZE:]
    if len(window) < MIN_ANSWERS:
        return initialDifficulty

    avg_score = sum(window) / len(window)

    if avg_score >= 0.75:
        return min(initialDifficulty + 1, D_MAX)
    elif avg_score < 0.4:
        return max(initialDifficulty - 1, D_MIN)
    else:
        return initialDifficulty