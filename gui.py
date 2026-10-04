"""Графический интерфейс приложения ROT13 Cipher (Tkinter + ttk)."""

import tkinter as tk
import os
import sys
from tkinter import ttk

import cipher

BACKGROUND = "#f4f6fb"
ACCENT = "#3b5bdb"

LANGUAGE_HINTS = {
    cipher.LANGUAGE_ENGLISH: (
        "Классический ROT13: сдвиг на 13 из 26 букв. "
        "Шифрование и расшифровка — одна и та же операция."
    ),
    cipher.LANGUAGE_RUSSIAN: (
        "Это НЕ классический ROT13, а его аналог: сдвиг на 13 в алфавите из 33 букв "
        "(Ё в конце). Расшифровка — сдвиг назад."
    ),
}


def resource_path(file_name):
    """Путь к файлу и в PyCharm, и внутри собранного .exe."""
    base_folder = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_folder, file_name)

class RotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Altair Cipher")
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except tk.TclError:
            pass
        self.geometry("720x500")
        self.minsize(560, 600)
        self.configure(bg=BACKGROUND)

        self.language_var = tk.StringVar(value=cipher.LANGUAGE_ENGLISH)
        self.status_var = tk.StringVar(value="Готово")
        self.hint_var = tk.StringVar(value=LANGUAGE_HINTS[cipher.LANGUAGE_ENGLISH])

        self.setup_styles()
        self.build_widgets()
        self.setup_shortcuts()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=BACKGROUND)
        style.configure("TLabel", background=BACKGROUND, font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground=ACCENT)
        style.configure("Hint.TLabel", foreground="#555555", wraplength=640)
        style.configure("Status.TLabel", foreground="#555555")
        style.configure("TButton", font=("Segoe UI", 10), padding=8)
        style.configure(
            "Accent.TButton", font=("Segoe UI", 10, "bold"),
            background=ACCENT, foreground="white",
        )
        style.map("Accent.TButton", background=[("active", "#2f4ac0")])

    def build_widgets(self):
        main = ttk.Frame(self, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Altair Cipher", style="Title.TLabel").pack(anchor="w")

        ttk.Label(main, text="Алфавит:").pack(anchor="w", pady=(12, 2))
        language_box = ttk.Combobox(
            main, textvariable=self.language_var, state="readonly",
            values=[cipher.LANGUAGE_ENGLISH, cipher.LANGUAGE_RUSSIAN],
            font=("Segoe UI", 11),
        )
        language_box.pack(fill="x")
        language_box.bind("<<ComboboxSelected>>", self.on_language_change)

        ttk.Label(main, textvariable=self.hint_var, style="Hint.TLabel").pack(
            anchor="w", pady=(6, 0)
        )

        ttk.Label(main, text="Введите текст:").pack(anchor="w", pady=(12, 2))
        self.input_text = self.make_text_area(main, read_only=False)

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=10)
        ttk.Button(
            buttons, text="Зашифровать", style="Accent.TButton",
            command=self.on_encrypt,
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ttk.Button(
            buttons, text="Расшифровать", style="Accent.TButton",
            command=self.on_decrypt,
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        ttk.Label(main, text="Результат:").pack(anchor="w", pady=(0, 2))
        self.output_text = self.make_text_area(main, read_only=True)

        buttons2 = ttk.Frame(main)
        buttons2.pack(fill="x", pady=10)
        ttk.Button(buttons2, text="Копировать", command=self.on_copy).pack(
            side="left", expand=True, fill="x", padx=(0, 5)
        )
        ttk.Button(buttons2, text="Очистить", command=self.on_clear).pack(
            side="left", expand=True, fill="x", padx=(5, 0)
        )

        ttk.Label(main, textvariable=self.status_var, style="Status.TLabel").pack(
            anchor="w"
        )

    def make_text_area(self, parent, read_only):
        """Создаёт текстовое поле с полосой прокрутки."""
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        text = tk.Text(
            frame, height=8, wrap="word", font=("Segoe UI", 12),
            relief="solid", borderwidth=1, padx=8, pady=8,
        )
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)

        text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if read_only:
            text.configure(state="disabled", bg="#eef1f8")
        return text

    # ---------- Горячие клавиши (работают и в русской раскладке) ----------

    def setup_shortcuts(self):
        """Ctrl+C/V/X/A работают в любой раскладке."""
        self.bind_all("<Control-KeyPress>", self.on_ctrl_key)
        # Клик по полю результата даёт ему фокус, чтобы можно было выделять и копировать
        self.output_text.bind("<Button-1>", lambda event: self.output_text.focus_set())

    def on_ctrl_key(self, event):
        widget = self.focus_get()
        if not isinstance(widget, tk.Text):
            return
        # В английской раскладке Tkinter сам всё обрабатывает, чтобы не вставить дважды
        if event.keysym.lower() in ("c", "v", "x"):
            return

        if event.keycode == 67:      # клавиша C
            widget.event_generate("<<Copy>>")
        elif event.keycode == 86:    # клавиша V
            widget.event_generate("<<Paste>>")
        elif event.keycode == 88:    # клавиша X
            widget.event_generate("<<Cut>>")
        elif event.keycode == 65:    # клавиша A (выделить всё)
            widget.tag_add("sel", "1.0", "end-1c")
            return "break"

    # ---------- Работа с полями ----------

    def get_input(self):
        return self.input_text.get("1.0", "end-1c")

    def set_output(self, value):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", value)
        self.output_text.configure(state="disabled")

    # ---------- Обработчики кнопок ----------

    def on_language_change(self, event=None):
        self.hint_var.set(LANGUAGE_HINTS[self.language_var.get()])
        self.status_var.set("Алфавит изменён")

    def on_encrypt(self):
        text = self.get_input()
        if not text.strip():
            self.status_var.set("Введите текст для шифрования")
            return
        self.set_output(cipher.encrypt(text, self.language_var.get()))
        self.status_var.set("Текст зашифрован")

    def on_decrypt(self):
        text = self.get_input()
        if not text.strip():
            self.status_var.set("Введите текст для расшифровки")
            return
        self.set_output(cipher.decrypt(text, self.language_var.get()))
        self.status_var.set("Текст расшифрован")

    def on_copy(self):
        result = self.output_text.get("1.0", "end-1c")
        if not result:
            self.status_var.set("Нечего копировать")
            return
        self.clipboard_clear()
        self.clipboard_append(result)
        self.status_var.set("Результат скопирован в буфер обмена")

    def on_clear(self):
        self.input_text.delete("1.0", "end")
        self.set_output("")
        self.status_var.set("Поля очищены")