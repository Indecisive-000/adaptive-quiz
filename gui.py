from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from data_handler import load_questions, questions_by_difficulty, questions_by_topic
from adaptive_engine import calculate_performance, change_difficulty
import random, time


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
        self.total_questions = 10
        self.active_questions = []
        self.time_limit = 0
        self.timer_id = None

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
        childframe = Frame(mainframe, bg="#ffffff")
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
        username = self.username_entry.get().strip()
        if username == "":
            messagebox.showerror("Missing username", "Please enter a username.")
            return

        self.username = username
        self.topic = self.topic_box.get()

        all_questions = load_questions()
        if self.topic == "All topics":
            self.active_questions = all_questions
        else:
            self.active_questions = questions_by_topic(all_questions, self.topic)

        # reset session state so a second quiz starts clean
        self.history = []
        self.list_time_taken = []
        self.list_is_correct = []
        self.used_id = []
        self.score = 0
        self.topic_results = {}
        self.question_number = 0
        self.show_question()

    def pick_question(self):
        pool = questions_by_difficulty(self.active_questions, self.current_difficulty)
        filtered_pool = []
        for q in pool:
            if q["id"] not in self.used_id:
                filtered_pool.append(q)
        if len(filtered_pool) == 0:
            return None
        return random.choice(filtered_pool)

    def show_question(self):
        if self.question_number >= self.total_questions:
            self.show_results()
            return

        question = self.pick_question()
        if question is None:
            self.show_results()
            return

        self.current_question = question
        self.used_id.append(question["id"])
        self.question_number += 1
        self.time_limit = self.current_difficulty * 10 + 10

        self.clear_screen()

        # top bar: counter, difficulty, timer
        top = Frame(self.root, bg="#ffffff")
        top.pack(fill=X, padx=40, pady=(30, 10))

        Label(top, text=f"Question {self.question_number}/{self.total_questions}",
              font=("Times New Roman", 12), bg="#ffffff", fg="#000000").pack(side=LEFT)

        self.timer_label = Label(top, text="0s", font=("Times New Roman", 12),
                                 bg="#ffffff", fg="#000000")
        self.timer_label.pack(side=RIGHT)

        difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
        Label(top, text=difficulty_labels[self.current_difficulty],
              font=("Times New Roman", 12), bg="#ffffff", fg="#000000").pack(side=RIGHT, padx=15)

        # question card
        card = Frame(self.root, bg="#ffffff", padx=40, pady=20)
        card.pack(fill=BOTH, expand=True)

        Label(card, text=question["topic"], font=("Times New Roman", 11),
              bg="#ffffff", fg="#555555").pack(anchor="w")
        Label(card, text=question["question"], font=("Times New Roman", 16),
              bg="#ffffff", fg="#000000", wraplength=700, justify=LEFT).pack(anchor="w", pady=(5, 20))

        letters = ["A", "B", "C", "D"]
        options = question["options"]
        for i in range(len(options)):
            Button(card, text=f"{letters[i]}. {options[i]}", font=("Times New Roman", 12),
                   anchor="w", width=60, bg="#ffffff", fg="#000000",
                   command=lambda idx=i: self.check_answer(idx)).pack(pady=5)

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.configure(text=f"{elapsed}s / {self.time_limit}s")
        self.timer_id = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def check_answer(self, selected_index):
        self.stop_timer()
        pass

    def show_results(self):
        self.stop_timer()
        pass


root = Tk()
app = QuizApp(root)

root.mainloop()