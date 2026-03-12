import tkinter as tk
from tkinter import scrolledtext
import subprocess
import time

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

        run_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Запуск", menu=run_menu)

        run_menu.add_command(label="Выполнить", command=self.run_code)

    def run_code(self):
        code = self.editor.get(1.0, tk.END)

        with open("temp_script.py", "w", encoding="utf-8") as temp_file:
            temp_file.write(code)

        start_time = time.time()

        process = subprocess.run(
            ["python", "temp_script.py"],
            capture_output=True,
            text=True
        )

        output = process.stdout
        error = process.stderr

        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)

        self.console.insert(tk.END, output)

        if error:
            self.console.insert(tk.END, error)

        end_time = time.time()
        execution_time = end_time - start_time

        self.console.insert(
            tk.END,
            f"\n\n--- Конец выполнения ---\nВремя выполнения: {execution_time:.4f} секунд\n"
        )

        self.console.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()