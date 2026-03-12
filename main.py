import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import time
import re
import tempfile
import os

class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.line_numbers = tk.Text(
            frame,
            width=4,
            padx=5,
            takefocus=0,
            borderwidth=0,
            background="lightgray",
            state="disabled",
            wrap=tk.NONE
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.editor = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            font=("Courier New", 12),
            height=20,
            undo=True
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

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

        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        run_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Запуск", menu=run_menu)
        run_menu.add_command(label="Выполнить", command=self.run_code)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        self.editor.tag_configure("keyword", foreground="blue")
        self.editor.tag_configure("string", foreground="green")
        self.editor.tag_configure("comment", foreground="gray")
        self.editor.tag_configure("number", foreground="darkorange")

        self.keywords = r"\b(False|None|True|and|as|assert|async|await|break|class|" \
                        r"continue|def|del|elif|else|except|finally|for|from|global|" \
                        r"if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|" \
                        r"try|while|with|yield)\b"

        self.string_re = r"(\".*?\"|\'.*?\')"
        self.comment_re = r"#[^\n]*"
        self.number_re = r"\b[0-9]+\b"

        self.editor.bind("<Tab>", self.insert_tab)
        self.editor.bind("<KeyRelease>", self.on_key_release)
        self.editor.bind("<Configure>", self.update_line_numbers)

        self.update_line_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )

        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            self.editor.delete(1.0, tk.END)
            self.editor.insert(tk.END, content)
            self.highlight_syntax()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.editor.get(1.0, tk.END))

    def insert_tab(self, event):
        self.editor.insert(tk.INSERT, "    ")
        return "break"

    def run_code(self):
        code = self.editor.get(1.0, tk.END)

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as temp_file:
                temp_file.write(code)
                temp_file_path = temp_file.name

            start_time = time.time()

            process = subprocess.run(
                ["python", temp_file_path],
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

            os.remove(temp_file_path)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить код:\n{e}")

    def show_about(self):
        messagebox.showinfo(
            "О программе",
            "Простая IDE для Python с подсветкой синтаксиса."
        )

    def update_line_numbers(self, event=None):
        line_count = self.editor.index('end-1c').split('.')[0]

        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)

        for i in range(1, int(line_count) + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

        self.line_numbers.config(state=tk.DISABLED)

    def on_key_release(self, event=None):
        self.update_line_numbers()
        self.highlight_syntax()

    def highlight_syntax(self):
        code = self.editor.get(1.0, tk.END)

        self.editor.tag_remove("keyword", "1.0", tk.END)
        self.editor.tag_remove("string", "1.0", tk.END)
        self.editor.tag_remove("comment", "1.0", tk.END)
        self.editor.tag_remove("number", "1.0", tk.END)

        for match in re.finditer(self.keywords, code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.editor.tag_add("keyword", start, end)

        for match in re.finditer(self.string_re, code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.editor.tag_add("string", start, end)

        for match in re.finditer(self.comment_re, code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.editor.tag_add("comment", start, end)

        for match in re.finditer(self.number_re, code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.editor.tag_add("number", start, end)

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()