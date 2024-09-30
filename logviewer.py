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
import tkinter.messagebox as messagebox

# Please delete the following comments after implementation and add your own comments.


class ProgramGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WordChain Log Viewer")
        self.root.minsize(400, 300)

        try:
            with open("logs.txt", "r") as f:
                self.logs = json.load(f)
        except Exception:
            messagebox.showerror("Error ! Missing or Invalid file")
            self.root.destroy()
            return

        self.nextLog = 0

        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        self.players_label = tk.Label(frame, text="Players: ")
        self.players_label.pack(anchor=tk.W)

        self.names_label = tk.Label(frame, text="Names: ")
        self.names_label.pack(anchor=tk.W)

        self.chain_label = tk.Label(frame, text="Chain: ")
        self.chain_label.pack(anchor=tk.W)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        next_button = tk.Button(button_frame, text="Next Log", command=self.showLog)
        next_button.pack(side=tk.LEFT, padx=5)

        stats_button = tk.Button(
            button_frame, text="Show Stats", command=self.showStats
        )
        stats_button.pack(side=tk.LEFT, padx=5)

        self.showLog()
        self.root.mainloop()

    def showLog(self):
        if self.nextLog < len(self.logs):
            log = self.logs[self.nextLog]
            self.players_label.config(text=f"Players: {log['players']}")
            self.names_label.config(text=f"Names: {', '.join(log['names'])}")
            self.chain_label.config(text=f"Chain: {log['chain']}")
            self.nextLog += 1
        else:
            messagebox.showinfo("No More Logs", "There are no more logs to display.")

    def showStats(self):
        total_games = len(self.logs)
        total_players = sum(log["players"] for log in self.logs)
        avg_players = round(total_players / total_games)
        max_chain = max(log["chain"] for log in self.logs)

        stats_message = f"Total games: {total_games}\n"
        stats_message += f"Average players per game: {avg_players}\n"
        stats_message += f"Maximum chain length: {max_chain}"

        messagebox.showinfo("Game Statistics", stats_message)


# Create an object of the ProgramGUI class to begin the program.
gui = ProgramGUI()
