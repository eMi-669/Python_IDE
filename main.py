import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import time
import re

class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.editor = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=("Courier New", 12),
            height=20,
            undo=True
        )

        self.editor.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()