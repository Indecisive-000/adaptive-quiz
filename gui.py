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
        Label(self.root, text = "Computer science quiz", font = ("Times New Roman", 24, "bold"), bg = "#ffffff", fg="#000000").pack(pady = 30)
        mainframe = Frame(self.root, bg="#ffffff", padx=40, pady = 30)
        mainframe.pack(pady=10)
        Label(mainframe, text = "username", font = ("Times New Roman", 12), bg="#ffffff", fg="#000000").pack(anchor="w")
        self.username_entry = Entry(mainframe, font = ("Times New Roman", 12), width = 30)
        self.username_entry.pack(pady=(0,15))
        Label(mainframe, text = "Select topic", font = ("Times New Roman", 12), bg="#ffffff", fg="#000000").pack(anchor="w")
        #choosing topic
        self.topic_box = ttk.Combobox(mainframe, font = ("Times New Roman", 12), width = 28, state="readonly", values= ["All topics", "OOP", "Algorithms", "Data Structures", "Binary", "Logic Gates"])
        self.topic_box.current(0)
        self.topic_box.pack(pady = (0,20))
        #creating label
        Label(mainframe, text = "Starting difficulty", font = ("Times New Roman", 12), bg = "#ffffff", fg = "#000000").pack(anchor = "w")
        childframe = Frame(self.mainframe, bg="#ffffff")
        childframe.pack(pady = (5, 20))
        self.childbutton = []
        #choose difficulty
        labels = ["Easy", "Medium", "Hard"]
        for i in range(3):
            btn = Button(childframe, text=labels[i], font = ("Times New Roman", 12), width = 8, command=lambda d =i+1: self.set_difficulty(d))
            btn.pack(side = LEFT, padx = 5)
            self.childbutton.append(btn)

        self.set_difficulty(1)

        Button(mainframe, text= "Start", font = ("Times New Roman", 12), width = 20, bg = "#000000", fg = "#ffffff", command = self.start_quiz).pack()
    def set_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        for i in range(3):
            if i+1 == difficulty:
                self.childbutton[i].configure(bg="#000000", fg="#ffffff")
            else:
                self.childbutton[i].configure(bg = "#ffffff", fg="#000000")

    def start_quiz(self):
        pass



root = Tk()
app = QuizApp(root)

root.mainloop()

