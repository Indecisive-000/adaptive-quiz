
D_MAX = 3
D_MIN = 1
A_WEIGHT = 0.7
T_WEIGHT = 0.3


def calculate_performance(accuracy, timeTaken, timeLimit):
    if accuracy == True:
        accuracy_score  = 1
    else:
        accuracy_score = 0
    time_score = (timeLimit - timeTaken) / timeLimit
    avg = (A_WEIGHT * accuracy_score) + (time_score * T_WEIGHT)
    return avg

def change_difficulty(history, initialDifficulty):
    if len(history) == 0:
        return initialDifficulty
    avg_score = sum(history) / len(history)
    if avg_score >=0.75:
        return min(initialDifficulty+1, D_MAX)
    elif avg_score < 0.4:
        return max(initialDifficulty - 1, D_MIN)
    else:
        return initialDifficulty