import random

class TextLoader:
    def __init__(self, file_path="typing_test.txt"):
        self.file_path = file_path

    def load_text(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()
            return random.choice(lines).strip()