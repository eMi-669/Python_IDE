import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import time
import re

class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()
