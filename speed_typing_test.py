# Final Project:

# Hanap kayo ng any existing python project na interesting para sa inyo. Gawin nyo yung project tapos pag gumagana na gawan nyo ng demo video.

# Explain each of the 4 pillars of OOP, find sample code implementation in the project. If any of the pillar is  not used in the project you may just explain the concept.

# - Send the link of your demo to my messenger before June 28.
# - Upload the source code to your github account using gitbash.
# - Add to the README the source of the project to give credit to the original creator.

import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Welcome to the Speed Typing Test!")
	stdscr.addstr("\nPress any key to begin!")
	stdscr.refresh()
	stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)
	stdscr.addstr(1, 0, f"WPM: {wpm}")

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)

def load_text():
	with open("typing_text.txt", "r") as f:
		lines = f.readlines()
		return random.choice(lines).strip()

def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if ord(key) == 27:
			break

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(2, 0, "You completed the text! Press any key to continue onto the next test.")
		stdscr.addstr(3, 0, "Press ESC to exit.")
		key = stdscr.getkey()
		
		if ord(key) == 27:
			break

wrapper(main)