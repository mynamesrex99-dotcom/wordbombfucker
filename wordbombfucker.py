str = ''' _       _                  _                                     
( )  _  ( )                ( )   /'\_/`\                          
| | ( ) | |   _    _ __   _| |   |     |   _ _    ___  _ __   _   
| | | | | | /'_`\ ( '__)/'_` |   | (_) | /'_` ) /'___)( '__)/'_`\ 
| (_/ \_) |( (_) )| |  ( (_| |   | | | |( (_| |( (___ | |  ( (_) )
`\___x___/'`\___/'(_)  `\__,_)   (_) (_)`\__,_)`\____)(_)  `\___/'
                                                                  
                                                                  '''
                                                                                  
print(str)
print("\nMade by @mynamesrex99")
print("https://github.com/mynamesrex99-dotcom")

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import time
from pynput.keyboard import Controller as KeyboardController
import keyboard

# --- COLORS ---
BG = "#0e0e0e"
PANEL = "#151515"
ACCENT = "#4cffb0"
TEXT = "#eaeaea"
MUTED = "#8a8a8a"

def sort_words(input_text):
    with open('word_list.txt', 'r') as file:
        words = [word.strip() for word in file.readlines()]

    filtered_words = [word for word in words if input_text.lower() in word.lower()]
    return sorted(filtered_words, key=lambda x: (len(x), x), reverse=True)

class ResultWindow:
    def __init__(self, master):
        self.master = master

        container = tk.Frame(master, bg=BG)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        title = tk.Label(
            container,
            text="Word Macro",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=BG
        )
        title.pack(pady=(0, 12))

        self.new_word_entry = tk.Entry(
            container,
            font=("Segoe UI", 14),
            width=30,
            bg=PANEL,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat"
        )
        self.new_word_entry.pack(pady=6, ipady=6)
        self.new_word_entry.bind('<Return>', lambda event: self.sort_new_words())

        self.result_text = scrolledtext.ScrolledText(
            container,
            font=("Consolas", 13),
            wrap=tk.WORD,
            width=70,
            height=20,
            bg=PANEL,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#222",
            highlightcolor=ACCENT
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=12)

        self.update_content(sort_words(""))

    def update_content(self, sorted_words):
        self.result_text.delete(1.0, tk.END)
        for word in sorted_words:
            self.result_text.insert(tk.END, f"{word} ({len(word)} letters)\n")

    def sort_new_words(self, event=None):
        new_word = self.new_word_entry.get().strip()
        if not new_word:
            messagebox.showinfo("Error", "Please enter a letter combination")
            return

        existing_sorted_words = self.result_text.get(1.0, tk.END).strip().split('\n')
        existing_sorted_words = [word.split(' ')[0] for word in existing_sorted_words]
        all_words = existing_sorted_words + [new_word]
        updated_sorted_words = sorted(all_words, key=lambda x: (len(x), x), reverse=True)
        self.update_content(updated_sorted_words)

    def autotype_word(self, key):
        sorted_words = self.result_text.get(1.0, tk.END).strip().split('\n')
        for word in sorted_words:
            if key == 'F1' and len(word.split(' ')[0]) == len(sorted_words[0].split(' ')[0]):
                autotype_word = word.split(' ')[0]
                break
        else:
            return

        keyboard_controller = KeyboardController()
        words_per_minute = 120
        seconds_per_word = 60 / words_per_minute

        for char in autotype_word:
            keyboard_controller.press(char)
            keyboard_controller.release(char)
            time.sleep(seconds_per_word / len(autotype_word))

def show_word_list(event=None):
    result_window.update_content(sort_words(result_window.new_word_entry.get()))

window = tk.Tk()
window.title("Word Macro")
window.geometry("720x760")
window.configure(bg=BG)

top_bar = tk.Frame(window, bg=BG)
top_bar.pack(pady=10)

button = tk.Button(
    top_bar,
    text="Find Words",
    font=("Segoe UI", 12, "bold"),
    bg=ACCENT,
    fg="#000000",
    activebackground="#3de39c",
    activeforeground="#000000",
    relief="flat",
    padx=28,
    pady=8,
    command=show_word_list
)
button.pack()

result_window = ResultWindow(window)

footer = tk.Frame(window, bg=BG)
footer.pack(pady=10)

tk.Label(
    footer,
    text="https://github.com/mynamesrex99-dotcom",
    font=("Segoe UI", 11),
    fg=MUTED,
    bg=BG
).pack()


window.bind('<Return>', lambda event: show_word_list())
keyboard.add_hotkey('F1', lambda: result_window.autotype_word('F1'))

window.mainloop()
