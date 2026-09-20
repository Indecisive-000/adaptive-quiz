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
        self.root.configure(bg="#ffffff")

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
        self.show_login()
    def clear_screen(self):
        #destroying every widget that list winfo_children return
        for widget in self.root.winfo_children():
            widget.destroy()
    def show_login(self):
        self.clear_screen()
        Label(self.root, text = "Computer science quiz", font = ("Times New Roman", 40, "bold"), bg = "#ffffff", fg="#000000").pack(pady = 60)
        mainframe = Frame(self.root, bg="#ffffff", padx=100, pady = 30)
        mainframe.pack(pady=10)
        Label(mainframe, text = "username", font = ("Times New Roman", 12), bg="#ffffff", fg="#000000").pack(anchor="w")
        self.username_entry = Entry(mainframe, width = 30)
        self.username_entry.pack(pady=15)
        


        
    

    
    
    
    


root = Tk()
app = QuizApp(root)

root.mainloop()

