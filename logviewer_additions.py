# Name:
# Student Number:

# This file is provided to you as a starting point for the "logviewer.py" program of Project
# of CSI6208 in Semester 2, 2024.  It aims to give you just enough code to help ensure
# that your program is well structured.  Please use this file as the basis for your assignment work.
# You are not required to reference it.

# The "pass" command tells Python to do nothing.  It is simply a placeholder to ensure that the starter file runs smoothly.
# They are not needed in your completed program.  Replace them with your own code as you complete the assignment.

# Import the necessary modules.
import json

import tkinter as tk
from datetime import date
from tkinter import messagebox, simpledialog, ttk

import urllib.request

# Please delete the following comments after implementation and add your own comments.


class ProgramGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WordChain Log Viewer")
        self.root.minsize(500, 400)

        try:
            with open("logs.txt", "r") as f:
                self.logs = json.load(f)
        except Exception:
            messagebox.showerror("Error ! Missing or Invalid file")
            self.root.destroy()
            return

        self.current_log = 0

        self.create_widgets()
        self.check_log_count()
        self.show_log()
        self.root.mainloop()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        log_frame = ttk.LabelFrame(main_frame, text="Log Details", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.players_label = ttk.Label(log_frame, text="Players: ", font=("Arial", 12))
        self.players_label.pack(anchor=tk.W)

        self.names_label = ttk.Label(log_frame, text="Names: ", font=("Arial", 12))
        self.names_label.pack(anchor=tk.W)

        self.chain_label = ttk.Label(
            log_frame, text="Chain: ", font=("Arial", 12, "bold")
        )
        self.chain_label.pack(anchor=tk.W)

        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(pady=10)

        self.first_button = ttk.Button(
            nav_frame, text="First Log", command=lambda: self.navigate_log("first")
        )
        self.first_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = ttk.Button(
            nav_frame, text="Previous Log", command=lambda: self.navigate_log("prev")
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(
            nav_frame, text="Next Log", command=lambda: self.navigate_log("next")
        )
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.last_button = ttk.Button(
            nav_frame, text="Last Log", command=lambda: self.navigate_log("last")
        )
        self.last_button.pack(side=tk.LEFT, padx=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        self.stats_button = ttk.Button(
            button_frame, text="Show Stats", command=self.show_stats
        )
        self.stats_button.pack(side=tk.LEFT, padx=5)

        self.word_of_day_button = ttk.Button(
            button_frame, text="Word of the Day", command=self.show_word_of_day
        )
        self.word_of_day_button.pack(side=tk.LEFT, padx=5)

        entry_frame = ttk.Frame(main_frame)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame, text="Go to Log:").pack(side=tk.LEFT, padx=5)
        self.log_entry = ttk.Entry(entry_frame, width=10)
        self.log_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(entry_frame, text="Go", command=self.go_to_log).pack(
            side=tk.LEFT, padx=5
        )

    def check_log_count(self):
        if len(self.logs) == 1:
            self.disable_navigation()
            messagebox.showinfo(
                "Limited Logs", "Only 1 log found - Navigation and statistics disabled."
            )

    def disable_navigation(self):
        for button in [
            self.first_button,
            self.prev_button,
            self.next_button,
            self.last_button,
            self.stats_button,
        ]:
            button.config(state=tk.DISABLED)
        self.log_entry.config(state=tk.DISABLED)

    def navigate_log(self, direction):
        if direction == "first":
            self.current_log = 0
        elif direction == "prev":
            self.current_log = (self.current_log - 1) % len(self.logs)
        elif direction == "next":
            self.current_log = (self.current_log + 1) % len(self.logs)
        elif direction == "last":
            self.current_log = len(self.logs) - 1
        self.show_log()

    def show_log(self):
        log = self.logs[self.current_log]
        self.players_label.config(text=f"Players: {log['players']}")
        self.names_label.config(text=f"Names: {', '.join(log['names'])}")
        self.chain_label.config(text=f"Chain: {log['chain']}")

    def go_to_log(self):
        try:
            log_num = int(self.log_entry.get()) - 1
            if 0 <= log_num < len(self.logs):
                self.current_log = log_num
                self.show_log()
            else:
                messagebox.showerror(
                    "Invalid Log Number",
                    f"Please enter a number between 1 and {len(self.logs)}",
                )
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")

    def show_stats(self):
        total_games = len(self.logs)
        total_players = sum(log["players"] for log in self.logs)
        avg_players = round(total_players / total_games, 1)
        max_chain = max(log["chain"] for log in self.logs)

        total_nouns = sum(log.get("nouns", 0) for log in self.logs)
        total_verbs = sum(log.get("verbs", 0) for log in self.logs)
        total_adjectives = sum(log.get("adjectives", 0) for log in self.logs)

        stats = {
            "Number of Games": total_games,
            "Average Players": avg_players,
            "Max Chain": max_chain,
            "Total Nouns": total_nouns,
            "Total Verbs": total_verbs,
            "Total Adjectives": total_adjectives,
        }

        stats_window = tk.Toplevel(self.root)
        stats_window.title("WordChain Statistics")
        stats_window.geometry("300x320")
        stats_window.resizable(False, False)

        main_frame = ttk.Frame(stats_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame, text="WordChain Statistics", font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))

        for key, value in stats.items():
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=key, font=("Arial", 10)).pack(side=tk.LEFT)
            ttk.Label(frame, text=str(value), font=("Arial", 10, "bold")).pack(
                side=tk.RIGHT
            )

        ttk.Button(main_frame, text="OK", command=stats_window.destroy).pack(
            pady=(20, 0)
        )

    def show_word_of_day(self):
        api_key = "b7dghzb5k4j5ewthefzc6qjkp4gnwklxjf3ume4krcnfj28ul"
        today = date.today().strftime("%Y-%m-%d")
        url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?date={today}&api_key={api_key}"

        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

                word = data["word"]
                definition = data["definitions"][0]["text"]
                note = data["note"]

                message = f"Word of the Day: {word}\n\nDefinition: {definition}\n\nNote: {note}"
                messagebox.showinfo("Word of the Day", message)
        except Exception as e:
            messagebox.showerror(f"Error ! Failed to fetch Word of the Day: {str(e)}")


# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
