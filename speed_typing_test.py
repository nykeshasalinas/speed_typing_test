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

        self.text_display = tk.Text(self.root, height=5, font=("Courier", 14), wrap="word")
        self.text_display.pack(pady=10)
        self.text_display.config(state="disabled")
        self.text_display.tag_config("correct", foreground="green")
        self.text_display.tag_config("incorrect", foreground="red")

        self.input_entry = tk.Text(self.root, height=5, font=("Courier", 14), wrap="word")
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<KeyRelease>", self.on_key_release)

        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Arial", 16))
        self.wpm_label.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="Try Again", command=self.reset)
        self.restart_button.pack(pady=10)

    def load_new_text(self):
        self.text_to_type = self.text_loader.load_text()
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", self.text_to_type)
        self.text_display.config(state="disabled")

    def on_key_release(self, event=None):
        typed = self.input_entry.get("1.0", tk.END).strip()
        self.highlight_text(typed)

        if not self.timer_running and typed:
            self.start_time = time.time()
            self.timer_running = True
            self.update_wpm()

        if typed == self.text_to_type:
            self.timer_running = False
            wpm = self.calculator.calculate(typed, max(time.time() - self.start_time, 1))
            self.wpm_label.config(text=f"WPM: {wpm}")
            messagebox.showinfo("Done!", f"Great job! Your WPM is {wpm}.")

    def highlight_text(self, typed):
        self.text_display.config(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", self.text_to_type)

        for i, char in enumerate(typed):
            if i >= len(self.text_to_type):
                break
            tag = "correct" if char == self.text_to_type[i] else "incorrect"
            self.text_display.tag_add(tag, f"1.{i}", f"1.{i+1}")

        self.text_display.config(state="disabled")

    def update_wpm(self):
        if not self.timer_running:
            return
        time_elapsed = max(time.time() - self.start_time, 1)
        typed = self.input_entry.get("1.0", tk.END).strip()
        wpm = self.calculator.calculate(typed, time_elapsed)
        self.wpm_label.config(text=f"WPM: {wpm}")
        self.root.after(500, self.update_wpm)

    def reset(self):
        self.timer_running = False
        self.input_entry.delete("1.0", tk.END)
        self.wpm_label.config(text="WPM: 0")
        self.load_new_text()