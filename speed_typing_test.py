import tkinter as tk
from tkinter import messagebox
import time
from load_typing_test import TextLoader
from calculate_wpm import WPMCalculator

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.text_loader = TextLoader()
        self.calculator = WPMCalculator()

        self.text_to_type = ""
        self.start_time = None
        self.timer_running = False

        self.setup_widgets()
        self.load_new_text()

    def setup_widgets(self):
        self.root.title("Typing Speed Test")
        self.root.geometry("700x400")
        self.root.resizable(False, False)

        self.title_label = tk.Label(self.root, text="Typing Speed Test", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.text_display = tk.Label(self.root, text="", wraplength=650, font=("Courier", 14), justify="left")
        self.text_display.pack(pady=10)

        self.input_entry = tk.Text(self.root, height=5, font=("Courier", 14), wrap="word")
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<KeyPress>", self.start_timer)

        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Arial", 16))
        self.wpm_label.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="Try Again", command=self.reset)
        self.restart_button.pack(pady=10)

    def load_new_text(self):
        self.text_to_type = self.text_loader.load_text()
        self.text_display.config(text=self.text_to_type)

    def start_timer(self, event):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_wpm()

    def update_wpm(self):
        if not self.timer_running:
            return

        time_elapsed = max(time.time() - self.start_time, 1)
        typed_text = self.input_entry.get("1.0", tk.END).strip()
        wpm = self.calculator.calculate(typed_text, time_elapsed)
        self.wpm_label.config(text=f"WPM: {wpm}")

        if typed_text == self.text_to_type:
            self.timer_running = False
            messagebox.showinfo("Done!", f"Great job! Your WPM is {wpm}.")
        else:
            self.root.after(500, self.update_wpm)

    def reset(self):
        self.timer_running = False
        self.input_entry.delete("1.0", tk.END)
        self.wpm_label.config(text="WPM: 0")
        self.load_new_text()