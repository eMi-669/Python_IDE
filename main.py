import tkinter as tk
from tkinter import scrolledtext

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


        self.console = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Courier New", 12),
            height=10,
            state=tk.DISABLED,
            bg="black",
            fg="white"
        )

        self.console.pack(fill=tk.BOTH, expand=True)


        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)

        file_menu.add_command(label="Открыть")
        file_menu.add_command(label="Сохранить")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()