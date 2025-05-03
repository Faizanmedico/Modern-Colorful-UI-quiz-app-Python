import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random
import os
from pathlib import Path

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Master Quiz")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')
        
        # Create colorful border
        self.border_frame = tk.Frame(root, bg=self.get_random_color(), bd=5)
        self.border_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Main content frame
        self.main_frame = tk.Frame(self.border_frame, bg='#ecf0f1', padx=20, pady=20)
        self.main_frame.pack(fill='both', expand=True)
        
        # Header
        self.header = tk.Label(
            self.main_frame, 
            text="🐍 Python Master Quiz", 
            font=("Arial", 20, "bold"), 
            bg='#ecf0f1', 
            fg='#2c3e50'
        )
        self.header.pack(pady=(0, 20))
        
        # Question area
        self.question_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.question_frame.pack(fill='x', pady=10)
        
        self.question_label = tk.Label(
            self.question_frame, 
            text="", 
            font=("Arial", 14), 
            bg='#ecf0f1', 
            fg='#2c3e50',
            wraplength=600,
            justify='center'
        )
        self.question_label.pack()
        
        # Image display
        self.image_label = tk.Label(self.main_frame, bg='#ecf0f1')
        self.image_label.pack(pady=10)
        
        # Options
        self.radio_var = tk.StringVar()
        self.option_buttons = []
        for i in range(3):
            btn = tk.Radiobutton(
                self.main_frame, 
                text="", 
                variable=self.radio_var, 
                value="",
                font=("Arial", 12), 
                bg='#ecf0f1',
                activebackground='#bdc3c7',
                selectcolor='#3498db',
                indicatoron=1,
                padx=10,
                pady=5,
                anchor='w'
            )
            self.option_buttons.append(btn)
            btn.pack(fill='x', padx=50, pady=5)
        
        # Timer and progress
        self.timer_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.timer_frame.pack(fill='x', pady=10)
        
        self.timer_label = tk.Label(
            self.timer_frame, 
            text="", 
            font=("Arial", 12, "bold"), 
            bg='#ecf0f1'
        )
        self.timer_label.pack(side='left')
        
        self.score_label = tk.Label(
            self.timer_frame, 
            text="Score: 0", 
            font=("Arial", 12), 
            bg='#ecf0f1'
        )
        self.score_label.pack(side='right')
        
        self.progress_bar = ttk.Progressbar(
            self.main_frame, 
            orient="horizontal", 
            length=500, 
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)
        
        # Navigation buttons
        self.button_frame = tk.Frame(self.main_frame, bg='#ecf0f1')
        self.button_frame.pack(pady=20)
        
        button_style = {
            'font': ("Arial", 12, "bold"),
            'width': 10,
            'padx': 10,
            'pady': 5,
            'bd': 0,
            'activebackground': '#34495e'
        }
        
        self.prev_button = tk.Button(
            self.button_frame, 
            text="← Previous", 
            command=self.prev_question,
            state="disabled", 
            bg='#3498db', 
            fg='white',
            **button_style
        )
        self.prev_button.pack(side='left', padx=20)
        
        self.next_button = tk.Button(
            self.button_frame, 
            text="Next →", 
            command=self.check_answer,
            bg='#2ecc71', 
            fg='white',
            **button_style
        )
        self.next_button.pack(side='right', padx=20)
        
        # Quiz data
        self.questions = self.load_questions()
        random.shuffle(self.questions)
        
        self.current_question = 0
        self.score = 0
        self.time_left = 15
        
        # Start quiz
        self.cycle_border_colors()
        self.load_question()
    
    def get_random_color(self):
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        return random.choice(colors)
    
    def cycle_border_colors(self):
        self.border_frame.config(bg=self.get_random_color())
        self.root.after(3000, self.cycle_border_colors)
    
    def load_questions(self):
        """Load questions with optional images from a questions folder"""
        questions = [
            {
                "question": "Which keyword defines a function in Python?",
                "image": "1.png",  # Relative path to image
                "options": ["def", "function", "lambda"],
                "answer": "def"
            },
            {
                "question": "What is the output of print(type(3.14))?",
                "image": "1.png",
                "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>"],
                "answer": "<class 'float'>"
            },
            # Add more questions here...
    {
        "question": "Which keyword defines a function in Python?",
        "image": "1.png",
        "options": ["def", "function", "lambda"],
        "answer": "def"
    },
    {
        "question": "What is the output of print(type(3.14))?",
        "image": "1.png",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>"],
        "answer": "<class 'float'>"
    },
    {
        "question": "How do you create an empty list in Python?",
        "image": "1.png",
        "options": ["list()", "[]", "Both list() and []"],
        "answer": "Both list() and []"
    },
    {
        "question": "Which method removes and returns the last item from a list?",
        "image": "1.png",
        "options": ["remove()", "pop()", "delete()"],
        "answer": "pop()"
    },
    {
        "question": "What does the 'in' keyword do in Python?",
        "image": "1.png",
        "options": ["Checks for existence", "Creates a loop", "Imports modules"],
        "answer": "Checks for existence"
    },
    {
        "question": "How do you open a file for reading in Python?",
        "image": "1.png",
        "options": ["open(file, 'r')", "open(file, 'read')", "open(file, 'w')"],
        "answer": "open(file, 'r')"
    },
    {
        "question": "What is the correct way to create a dictionary?",
        "image": "1.png",
        "options": ["{key: value}", "dict(key=value)", "Both {key: value} and dict(key=value)"],
        "answer": "Both {key: value} and dict(key=value)"
    },
    {
        "question": "Which module is used for working with dates?",
        "image": "1.png",
        "options": ["time", "datetime", "calendar"],
        "answer": "datetime"
    },
    {
        "question": "What does list comprehension do?",
        "image": "1.png",
        "options": ["Creates a new list", "Filters elements", "Both creates and filters"],
        "answer": "Both creates and filters"
    },
    {
        "question": "How do you handle exceptions in Python?",
        "image": "1.png",
        "options": ["try/except", "catch/throw", "error/handle"],
        "answer": "try/except"
    },
    {
        "question": "What is the output of bool('False')?",
        "image": "1.png",
        "options": ["True", "False", "Error"],
        "answer": "True"
    }




        ]
        
        # Validate images exist or use placeholder
        for q in questions:
            if 'image' in q:
                img_path = Path(__file__).parent / q['image']
                if not img_path.exists():
                    q['image'] = None  # No image if file doesn't exist
        
        return questions
    
    def load_question(self):
        if self.current_question >= len(self.questions):
            self.show_result()
            return
            
        q = self.questions[self.current_question]
        self.question_label.config(text=q["question"])
        
        # Load image if available
        if q.get("image"):
            try:
                img_path = Path(__file__).parent / q["image"]
                pil_img = Image.open(img_path)
                pil_img = pil_img.resize((400, 250), Image.LANCZOS)
                img = ImageTk.PhotoImage(pil_img)
                self.image_label.config(image=img)
                self.image_label.image = img
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_label.config(image='', text='[Image not available]')
        else:
            self.image_label.config(image='', text='')
        
        # Load options
        for i, option in enumerate(q["options"]):
            self.option_buttons[i].config(text=option, value=option)
        self.radio_var.set("")
        
        # Update navigation
        self.prev_button.config(state="normal" if self.current_question > 0 else "disabled")
        self.score_label.config(text=f"Score: {self.score}/{len(self.questions)}")
        
        # Reset timer
        self.time_left = 15
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.progress_bar["value"] = (self.time_left / 15) * 100
            color = "#e74c3c" if self.time_left <= 5 else "#2c3e50"
            self.timer_label.config(
                text=f"⏱️ Time left: {self.time_left}s", 
                fg=color
            )
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.check_answer(auto_submit=True)
    
    def check_answer(self, auto_submit=False):
        if not auto_submit and not self.radio_var.get():
            messagebox.showwarning("No Answer", "Please select an answer!")
            return
            
        correct_answer = self.questions[self.current_question]["answer"]
        user_answer = self.radio_var.get()
        
        if user_answer == correct_answer:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}/{len(self.questions)}")
        
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_question()
        else:
            self.show_result()
    
    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_question()
    
    def show_result(self):
        total = len(self.questions)
        percentage = (self.score / total) * 100
        
        if percentage >= 90:
            msg = "🌟 Python Master! 🌟"
            color = "#f1c40f"
        elif percentage >= 70:
            msg = "👍 Great Job!"
            color = "#2ecc71"
        else:
            msg = "💪 Keep Practicing!"
            color = "#e74c3c"
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Quiz Results")
        result_window.geometry("400x300")
        result_window.configure(bg='#2c3e50')
        
        tk.Label(
            result_window, 
            text="Quiz Completed!", 
            font=("Arial", 20, "bold"), 
            bg='#2c3e50', 
            fg='white'
        ).pack(pady=20)
        
        tk.Label(
            result_window, 
            text=f"Your Score: {self.score}/{total}", 
            font=("Arial", 16), 
            bg='#2c3e50', 
            fg='white'
        ).pack()
        
        tk.Label(
            result_window, 
            text=f"Accuracy: {percentage:.1f}%", 
            font=("Arial", 16), 
            bg='#2c3e50', 
            fg='white'
        ).pack(pady=10)
        
        tk.Label(
            result_window, 
            text=msg, 
            font=("Arial", 18, "bold"), 
            bg='#2c3e50', 
            fg=color
        ).pack(pady=20)
        
        tk.Button(
            result_window, 
            text="Close", 
            command=self.root.destroy,
            bg='#e74c3c', 
            fg='white',
            font=("Arial", 12),
            padx=20,
            pady=5
        ).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()