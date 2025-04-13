import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Callable

class NoteView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Мини-заметки")
        self.root.configure(bg='#f0f0f0')
        
        # Состояния
        self.editor_visible = False
        
        # Шрифты
        self.title_font = ('Arial', 12, 'bold')
        self.text_font = ('Arial', 11)
        
        # Цвета
        self.bg_color = '#f0f0f0'
        self.card_color = '#ffffff'
        self.accent_color = '#4a6baf'
        self.text_color = '#333333'
        
        self._create_widgets()

    def _create_widgets(self):
        # Основной контейнер
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Список заметок
        self.notes_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.notes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.notes_list = tk.Listbox(
            self.notes_frame,
            bg=self.card_color,
            fg=self.text_color,
            selectbackground=self.accent_color,
            borderwidth=0,
            highlightthickness=0,
            font=self.text_font
        )
        self.notes_list.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка добавления
        self.add_btn_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.add_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.add_btn = tk.Button(
            self.add_btn_frame,
            text="+",
            bg=self.accent_color,
            fg='white',
            font=('Arial', 14, 'bold'),
            borderwidth=0,
            relief='flat',
            width=3
        )
        self.add_btn.pack(side=tk.RIGHT)
        
        # Редактор (изначально скрыт)
        self.editor_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        
        self.text_editor = scrolledtext.ScrolledText(
            self.editor_frame,
            wrap=tk.WORD,
            font=self.text_font,
            bg=self.card_color,
            fg=self.text_color,
            padx=10,
            pady=10,
            borderwidth=0,
            highlightthickness=0
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка назад
        self.back_btn = tk.Button(
            self.editor_frame,
            text="← Назад",
            bg=self.bg_color,
            fg=self.accent_color,
            font=self.text_font,
            borderwidth=0,
            relief='flat'
        )
        self.back_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

    def show_editor(self):
        if not self.editor_visible:
            self.notes_frame.pack_forget()
            self.add_btn_frame.pack_forget()
            self.editor_frame.pack(fill=tk.BOTH, expand=True)
            self.root.geometry("400x600")
            self.editor_visible = True

    def hide_editor(self):
        if self.editor_visible:
            self.editor_frame.pack_forget()
            self.notes_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.add_btn_frame.pack(fill=tk.X, padx=5, pady=5)
            self.root.geometry("200x600")
            self.editor_visible = False

    def clear_editor(self):
        self.text_editor.delete(1.0, tk.END)

    def get_note_data(self) -> dict:
        content = self.text_editor.get(1.0, tk.END).strip()
        title = content.split('\n')[0] if content else "Новая заметка"
        return {'title': title, 'content': content}

    def set_note_data(self, content: str):
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.END, content)

    def update_notes_list(self, notes: list):
        self.notes_list.delete(0, tk.END)
        for note in notes:
            title = note['content'].split('\n')[0] if note['content'] else "Новая заметка"
            self.notes_list.insert(tk.END, title)

    def get_selected_note_index(self) -> int:
        return self.notes_list.curselection()[0] if self.notes_list.curselection() else -1

    def bind_events(self, controller):
        self.add_btn.config(command=controller.create_new_note)
        self.back_btn.config(command=self.hide_editor)
        self.notes_list.bind('<<ListboxSelect>>', lambda e: controller.load_selected_note())
        self.text_editor.bind('<KeyRelease>', lambda e: controller.auto_save_note())
        self.root.bind('<Escape>', lambda e: self.hide_editor())