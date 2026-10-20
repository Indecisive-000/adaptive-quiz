from data_handler import load_questions, questions_by_difficulty, questions_by_topic, saving_sessions
from adaptive_engine import calculate_performance, change_difficulty
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import random, time, ctypes

COLORS = {
    "bg": "#d5f4f9",          
    "card": "#ffffff",        
    "primary": "#5d395d",     
    "accent": "#639cba",      
    "highlight": "#94e0ee",   
    "muted": "#c19b9a",       
    "text": "#3a2a3a",        
    "text_light": "#ffffff",  
    "correct": "#2e7d32",     
    "wrong": "#c62828"        
}

FONT = "Segoe UI"


class QuizApp:
    #the values set here reset in start_quiz for a new session
    def __init__(self, root):
        self.root = root
        self.root.title("Computer science quiz")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS["bg"])

        # ttk widgets ignore bg/fg, for custom colors
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Topic.Horizontal.TProgressbar",
                        background=COLORS["primary"], troughcolor=COLORS["bg"],
                        bordercolor=COLORS["bg"], lightcolor=COLORS["primary"],
                        darkcolor=COLORS["primary"])

        self.questions = load_questions()
        self.current_difficulty = 1
        self.history = []
        self.list_time_taken = []
        self.list_is_correct = []
        self.used_id = []
        self.score = 0
        self.topic_results = {}
        self.level_history = []

        self.question_number = 0
        self.start_time = 0
        self.username = ""
        self.current_question = None
        self.total_questions = 10
        self.active_questions = []
        self.time_limit = 0
        self.timer_id = None

        #base sizes to change them directly from here without using ctrl+H
        self.font_sizes = {
            "title": 28,
            "big": 24,
            "heading": 18,
            "body": 14,
            "body_bold": 14,
            "small": 13,
            "small_bold": 13
        }
        self.fonts = {
            "title": tkfont.Font(family=FONT, size=28, weight="bold"),
            "big": tkfont.Font(family=FONT, size=24, weight="bold"),
            "heading": tkfont.Font(family=FONT, size=18),
            "body": tkfont.Font(family=FONT, size=14),
            "body_bold": tkfont.Font(family=FONT, size=14, weight="bold"),
            "small": tkfont.Font(family=FONT, size=13),
            "small_bold": tkfont.Font(family=FONT, size=13, weight="bold")
        }
        self.root.option_add("*TCombobox*Listbox.font", self.fonts["body"])
        self.root.bind("<Configure>", self.on_resize)

        self.show_login()

    def clear_screen(self):
        #destroying every widget that list winfo_children return
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_resize(self, event):
        #filter is for which size to calculate from
        if event.widget != self.root:
            return

        #for text to fit in all directions
        scale = min(event.width / 800, event.height / 600)

        for name in self.fonts:
            #scaling from the base size
            new_size = int(round(self.font_sizes[name] * scale))
            if new_size < 8:
                #for text to be readable even if window is small
                new_size = 8
            self.fonts[name].configure(size=new_size)


    def make_card(self, parent):
        # white frame with a thin border
        return Frame(parent, bg=COLORS["card"], highlightbackground=COLORS["muted"],
                     highlightthickness=1)

    def primary_button(self, parent, text, command, width=20):
        return Button(parent, text=text, 	font=self.fonts["body_bold"], width=width,
                      bg=COLORS["primary"], fg=COLORS["text_light"],
                      activebackground=COLORS["accent"], activeforeground=COLORS["text_light"],
                      relief=FLAT, cursor="hand2", command=command)

    def show_login(self):
        self.clear_screen()
        Label(self.root, text="Computer science quiz", 	font=self.fonts["title"],
              bg=COLORS["bg"], fg=COLORS["primary"]).pack(pady=30)

        mainframe = self.make_card(self.root)
        mainframe.configure(padx=40, pady=30)
        mainframe.pack(pady=10)

        Label(mainframe, text="Username", 	font=self.fonts["body"],
              bg=COLORS["card"], fg=COLORS["accent"]).pack(anchor="w")
        self.username_entry = Entry(mainframe, 	font=self.fonts["body"], width=30,
                                    relief=SOLID, bd=1)
        self.username_entry.pack(pady=(0, 15))

        Label(mainframe, text="Select topic", 	font=self.fonts["body"],
              bg=COLORS["card"], fg=COLORS["accent"]).pack(anchor="w")
        #choosing topic
        self.topic_box = ttk.Combobox(mainframe, 	font=self.fonts["body"], width=28, state="readonly",
                                      values=["All topics", "OOP", "Algorithms",
                                              "Data Structures", "Binary", "Logic Gates"])
        self.topic_box.current(0)
        self.topic_box.pack(pady=(0, 20))

        Label(mainframe, text="Starting difficulty", 	font=self.fonts["body"],
              bg=COLORS["card"], fg=COLORS["accent"]).pack(anchor="w")
        childframe = Frame(mainframe, bg=COLORS["card"])
        childframe.pack(pady=(5, 20))
        self.childbutton = []
        #choose difficulty
        labels = ["Easy", "Medium", "Hard"]
        for i in range(3):
            btn = Button(childframe, text=labels[i], 	font=self.fonts["body"], width=8,
                         relief=FLAT, cursor="hand2",
                         #lambda is capturing the value now 
                         command=lambda d=i+1: self.set_difficulty(d))
            btn.pack(side=LEFT, padx=5)
            self.childbutton.append(btn)

        self.set_difficulty(1)

        self.primary_button(mainframe, "Start", self.start_quiz).pack()

    def set_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        for i in range(3):
            if i + 1 == difficulty:
                self.childbutton[i].configure(bg=COLORS["primary"], fg=COLORS["text_light"])
            else:
                self.childbutton[i].configure(bg=COLORS["bg"], fg=COLORS["text"])

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

        # reset for second quiz starts clean
        self.history = []
        self.list_time_taken = []
        self.list_is_correct = []
        self.used_id = []
        self.score = 0
        self.topic_results = {}
        self.question_number = 0
        self.show_question()
        self.level_history = []

    def available_questions(self, difficulty):
        pool = questions_by_difficulty(self.active_questions, difficulty)
        filtered_pool = []
        for q in pool:
            if q["id"] not in self.used_id:
                filtered_pool.append(q)
        return filtered_pool

    def pick_question(self):
        if self.current_difficulty == 1:
            order = [1, 2, 3]
        elif self.current_difficulty == 2:
            order = [2, 1, 3]
        else:
            order = [3, 2, 1]

        for difficulty in order:
            pool = self.available_questions(difficulty)
            if len(pool) > 0:
                return random.choice(pool)

        # every question in the topic has been used
        return None

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
        #harder questions take more time to answer
        self.time_limit = question["difficulty"] * 10 + 10

        self.clear_screen()

        # top bar: counter, difficulty, timer
        top = Frame(self.root, bg=COLORS["bg"])
        top.pack(fill=X, padx=40, pady=(30, 10))

        Label(top, text=f"Question {self.question_number}/{self.total_questions}",
              	font=self.fonts["small_bold"], bg=COLORS["primary"], fg=COLORS["text_light"],
              padx=12, pady=4).pack(side=LEFT)

        self.timer_label = Label(top, text="0s", 	font=self.fonts["small"],
                                 bg=COLORS["card"], fg=COLORS["text"], padx=12, pady=4)
        self.timer_label.pack(side=RIGHT)

        difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}
        Label(top, text=difficulty_labels[question["difficulty"]],
              	font=self.fonts["small_bold"], bg=COLORS["accent"], fg=COLORS["text_light"],
              padx=12, pady=4).pack(side=RIGHT, padx=10)

        # question card
        card = self.make_card(self.root)
        card.configure(padx=30, pady=20)
        card.pack(fill=BOTH, expand=True, padx=40, pady=(0, 30))

        Label(card, text=question["topic"].upper(), 	font=self.fonts["small_bold"],
              bg=COLORS["card"], fg=COLORS["accent"]).pack(anchor="w")
        Label(card, text=question["question"], 	font=self.fonts["heading"],
              bg=COLORS["card"], fg=COLORS["text"], wraplength=650,
              justify=LEFT).pack(anchor="w", pady=(5, 20))

        letters = ["A", "B", "C", "D"]
        options = question["options"]
        for i in range(len(options)):
            Button(card, text=f"{letters[i]}.  {options[i]}", 	font=self.fonts["body"],
                   anchor="w", padx=15, pady=6,
                   bg=COLORS["bg"], fg=COLORS["text"],
                   activebackground=COLORS["highlight"], relief=FLAT, cursor="hand2",
                   command=lambda idx=i: self.check_answer(idx)).pack(fill=X, pady=5)

        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.configure(text=f"{elapsed}s / {self.time_limit}s")
        #loop would freeze the window so i used after
        if elapsed >= self.time_limit:
            self.timer_id = None
            self.check_answer(None)
            return
        self.timer_id = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def check_answer(self, selected_index):
        self.stop_timer()

        if selected_index is None:
            is_correct = False
            time_taken = self.time_limit
        else:
            time_taken = round(time.time() - self.start_time, 2)
            selected_option = self.current_question["options"][selected_index]
            is_correct = selected_option == self.current_question["answer"]

        score = calculate_performance(is_correct, time_taken, self.time_limit)
        self.history.append(score)
        self.level_history.append(score)

        self.list_time_taken.append(time_taken)
        self.list_is_correct.append(is_correct)

        if is_correct:
            self.score += 1

        topic = self.current_question["topic"]
        if topic not in self.topic_results:
            self.topic_results[topic] = []
        self.topic_results[topic].append(is_correct)

        old_difficulty = self.current_difficulty
        self.current_difficulty = change_difficulty(self.level_history, self.current_difficulty)

        if self.current_difficulty != old_difficulty:
            self.level_history = []

        self.show_feedback(is_correct, time_taken, old_difficulty, selected_index is None)

    def show_feedback(self, is_correct, time_taken, old_difficulty, timed_out=False):
        self.clear_screen()
        difficulty_labels = {1: "Easy", 2: "Medium", 3: "Hard"}

        card = self.make_card(self.root)
        card.configure(padx=30, pady=25)
        card.pack(fill=BOTH, expand=True, padx=40, pady=30)

        Label(card, text=f"Question {self.question_number}/{self.total_questions}",
              	font=self.fonts["small"], bg=COLORS["card"], fg=COLORS["accent"]).pack(anchor="w")

        Label(card, text=self.current_question["question"], 	font=self.fonts["heading"],
              bg=COLORS["card"], fg=COLORS["text"], wraplength=650,
              justify=LEFT).pack(anchor="w", pady=(10, 20))

        if is_correct:
            Label(card, text="Correct", 	font=self.fonts["big"],
                  bg=COLORS["card"], fg=COLORS["correct"]).pack(anchor="w")
        else:
            if timed_out:
                result_text = "Time's up"
            else:
                result_text = "Wrong"
            Label(card, text=result_text, font=self.fonts["big"],
                  bg=COLORS["card"], fg=COLORS["wrong"]).pack(anchor="w")

        # adaptive engine info box
        info = Frame(card, bg=COLORS["bg"], padx=15, pady=10)
        info.pack(fill=X, pady=(20, 0))

        Label(info, text=f"Time taken: {time_taken}s / {self.time_limit}s",
              	font=self.fonts["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")
        Label(info, text=f"Difficulty: {difficulty_labels[old_difficulty]} -> {difficulty_labels[self.current_difficulty]}",
              	font=self.fonts["body_bold"], bg=COLORS["bg"], fg=COLORS["primary"]).pack(anchor="w", pady=(5, 0))
        Label(info, text=f"Performance score: {round(self.history[-1], 2)}",
              	font=self.fonts["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(5, 0))

        self.primary_button(card, "Next", self.show_question).pack(pady=25)

    def show_results(self):
        self.stop_timer()
        self.clear_screen()

        answered = len(self.list_is_correct)

        Label(self.root, text="Session complete", 	font=self.fonts["title"],
              bg=COLORS["bg"], fg=COLORS["primary"]).pack(pady=(30, 10))

        #to not devide by zero or program crashes
        if answered == 0:
            Label(self.root, text="No questions available for this topic and difficulty.",
                  	font=self.fonts["body"], bg=COLORS["bg"], fg=COLORS["text"]).pack(pady=10)
            self.primary_button(self.root, "Back", self.show_login).pack(pady=20)
            return

        correct = 0
        for result in self.list_is_correct:
            if result:
                correct += 1
        accuracy = round(correct / answered * 100, 1)
        avg_time = round(sum(self.list_time_taken) / answered, 2)

        # summary row - three white cards
        stats = Frame(self.root, bg=COLORS["bg"])
        stats.pack(pady=10)
        values = [("Score", f"{correct}/{answered}"), ("Accuracy", f"{accuracy}%"), ("Avg time", f"{avg_time}s")]
        for i in range(len(values)):
            box = self.make_card(stats)
            box.configure(padx=25, pady=10)
            box.pack(side=LEFT, padx=10)
            Label(box, text=values[i][0], 	font=self.fonts["small"],
                  bg=COLORS["card"], fg=COLORS["accent"]).pack()
            Label(box, text=values[i][1], 	font=self.fonts["big"],
                  bg=COLORS["card"], fg=COLORS["primary"]).pack()

        # performance by topic
        topics_frame = self.make_card(self.root)
        topics_frame.configure(padx=30, pady=15)
        topics_frame.pack(fill=X, padx=60, pady=(15, 10))
        Label(topics_frame, text="Performance by topic", 	font=self.fonts["body_bold"],
              bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 10))

        weak_topics = []
        for topic in self.topic_results:
            results = self.topic_results[topic]
            topic_correct = 0
            for r in results:
                if r:
                    topic_correct += 1
            topic_accuracy = round(topic_correct / len(results) * 100)

            if topic_accuracy < 50:
                weak_topics.append(topic)

            row = Frame(topics_frame, bg=COLORS["card"])
            row.pack(fill=X, pady=3)
            Label(row, text=f"{topic} ({topic_accuracy}%)", 	font=self.fonts["small"],
                  bg=COLORS["card"], fg=COLORS["text"], width=22, anchor="w").pack(side=LEFT)
            bar = ttk.Progressbar(row, length=350, maximum=100, value=topic_accuracy,
                                  style="Topic.Horizontal.TProgressbar")
            bar.pack(side=LEFT, padx=10)

        if len(weak_topics) > 0:
            Label(self.root, text="Weak topics: " + ", ".join(weak_topics),
                  	font=self.fonts["body_bold"], bg=COLORS["bg"], fg=COLORS["wrong"]).pack(pady=10)

        # save session
        saving_sessions(self.username, {
            "topic": self.topic,
            "correct": self.list_is_correct,
            "times": self.list_time_taken,
            "accuracy": accuracy,
            "topic_results": self.topic_results
        })

        self.primary_button(self.root, "Play again", self.show_login).pack(pady=15)
    

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


root = Tk()
app = QuizApp(root)

root.mainloop()