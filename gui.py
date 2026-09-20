from tkinter import *
from tkinter import ttk
from data_handler import load_questions, questions_by_difficulty, questions_by_topic
from adaptive_engine import calculate_performance, change_difficulty
import os, random, time


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer science quiz")
        self.root.geometry("800x600")
        self.root.configure(bg="#d5f4f9")

        self.questions = load_questions()
        self.current_difficulty = 1
        self.history = []
        self.list_time_taken = []
        self.list_is_correct = []
        self.used_id = []
        self.score = 0
        self.topic_results = {}
        self.question_number = 0
        self.start_time = 0

        self.username = ""
        self.current_question = None
        self.total_questions =10
        
    

    
    
    
    


root = Tk()
app = QuizApp(root)

root.mainloop()

