import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from typing import Callable, Optional
import time

class NoteView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cosmic Notes")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        self.root.configure(bg='#0a0e17')
        
        # Шрифты
        self.title_font = ('Arial', 16, 'bold')
        self.text_font = ('Arial', 12)
        self.button_font = ('Arial', 10)
        self.status_font = ('Arial', 9)
        
        # Цветовая схема
        self.bg_color = '#0a0e17'
        self.sidebar_color = '#121a2a'
        self.card_color = '#1a2238'
        self.accent_color = '#6d4aff'
        self.secondary_accent = '#9d7aff'
        self.text_color = '#e0e0e0'
        self.highlight_color = '#2a3655'
        self.danger_color = '#ff4d6d'
        
        self.animation_speed = 0.15
        
        self._setup_styles()
        self._create_widgets()
        
        # Эффект открытия
        self.root.withdraw()
        self.root.after(100, self._animate_open)

    def _animate_open(self):
        self.root.deiconify()
        for i in range(0, 101, 5):
            alpha = i/100
            self.root.attributes('-alpha', alpha)
            self.root.update()
            time.sleep(0.01)
        self.root.attributes('-alpha', 1.0)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.bg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.text_font)
        style.configure('TButton', 
                      background='transparent',
                      foreground=self.text_color,
                      borderwidth=0,
                      font=self.button_font,
                      padding=6)
        style.map('TButton',
                 background=[('active', self.highlight_color)],
                 foreground=[('active', self.text_color)])
        
        style.configure('Treeview', 
                      background=self.card_color,
                      fieldbackground=self.card_color,
                      foreground=self.text_color,
                      rowheight=32,
                      font=self.text_font,
                      borderwidth=0)
        style.map('Treeview', 
                 background=[('selected', self.highlight_color)],
                 foreground=[('selected', self.text_color)])
        
        style.configure('TEntry', 
                      fieldbackground=self.card_color,
                      foreground=self.text_color,
                      insertcolor=self.text_color,
                      borderwidth=0,
                      padding=8,
                      font=self.text_font)
        
        style.configure('Close.TButton', 
                      background='transparent',
                      foreground='#ff5e7d',
                      font=('Arial', 12))

    def _create_widgets(self):
        # Основной контейнер
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Боковая панель
        self.sidebar = ttk.Frame(self.main_container, width=250)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        
        # Заголовок боковой панели
        sidebar_header = ttk.Frame(self.sidebar)
        sidebar_header.pack(fill=tk.X, pady=(10, 20), padx=10)
        
        self.close_btn = ttk.Button(sidebar_header, text="✕", style='Close.TButton')
        self.close_btn.pack(side=tk.LEFT)
        
        ttk.Label(sidebar_header, text="COSMIC NOTES", 
                 font=('Arial', 14, 'bold'), 
                 foreground=self.accent_color).pack(side=tk.LEFT, padx=10)
        
        # Поиск
        search_frame = ttk.Frame(self.sidebar)
        search_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X, expand=True)
        self.search_entry.insert(0, "Поиск заметок...")
        
        # Кнопка поиска
        self.search_btn = ttk.Button(search_frame, text="🔍", width=3)
        self.search_btn.pack(side=tk.RIGHT)
        
        # Список заметок
        notes_container = ttk.Frame(self.sidebar)
        notes_container.pack(fill=tk.BOTH, expand=True, padx=10)
        
        ttk.Label(notes_container, text="Ваши заметки", 
                 font=('Arial', 11, 'bold')).pack(anchor='w')
        
        self.notes_list = ttk.Treeview(notes_container, show='tree', selectmode='browse', height=20)
        self.notes_list.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Область контента
        self.content_area = ttk.Frame(self.main_container)
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Заголовок заметки
        title_frame = ttk.Frame(self.content_area)
        title_frame.pack(fill=tk.X, pady=(20, 10), padx=20)
        
        ttk.Label(title_frame, text="НАЗВАНИЕ", 
                 font=('Arial', 10), 
                 foreground='#6d7cff').pack(anchor='w')
        
        self.title_entry = ttk.Entry(title_frame, font=self.title_font)
        self.title_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Текстовый редактор
        editor_frame = ttk.Frame(self.content_area)
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        ttk.Label(editor_frame, text="СОДЕРЖАНИЕ", 
                 font=('Arial', 10), 
                 foreground='#6d7cff').pack(anchor='w')
        
        self.text_editor = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.WORD, 
            font=self.text_font,
            padx=15,
            pady=15,
            bg=self.card_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            selectbackground=self.accent_color,
            highlightthickness=0,
            bd=0
        )
        self.text_editor.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Панель кнопок
        actions_frame = ttk.Frame(self.content_area)
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.new_btn = ttk.Button(actions_frame, text="Новая")
        self.new_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(actions_frame, text="Сохранить")
        self.save_btn.pack(side=tk.LEFT, padx=10)
        
        self.delete_btn = ttk.Button(actions_frame, text="Удалить")
        self.delete_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Статус бар
        self.status_bar = ttk.Label(self.content_area, 
                                  text="Готово", 
                                  font=self.status_font,
                                  foreground='#6d7cff',
                                  anchor='w')
        self.status_bar.pack(fill=tk.X, padx=20, pady=(0, 15))

    def set_status(self, message: str):
        self.status_bar.config(text=message)

    def show_error(self, message: str):
        messagebox.showerror("Ошибка", message)

    def show_info(self, message: str):
        messagebox.showinfo("Информация", message)

    def clear_editor(self):
        self.title_entry.delete(0, tk.END)
        self.text_editor.delete(1.0, tk.END)

    def get_note_data(self) -> dict:
        return {
            'title': self.title_entry.get(),
            'content': self.text_editor.get(1.0, tk.END).strip()
        }

    def set_note_data(self, title: str, content: str):
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.END, content)

    def update_notes_list(self, notes: list):
        self.notes_list.delete(*self.notes_list.get_children())
        for note in notes:
            self.notes_list.insert('', tk.END, iid=note['id'], text=note['title'])

    def get_selected_note_id(self) -> Optional[int]:
        selection = self.notes_list.selection()
        return int(selection[0]) if selection else None

    def bind_events(self, controller):
        self.new_btn.config(command=controller.create_new_note)
        self.save_btn.config(command=controller.save_current_note)
        self.delete_btn.config(command=controller.delete_current_note)
        self.search_btn.config(command=controller.search_notes)
        self.search_entry.bind('<Return>', lambda e: controller.search_notes())
        self.notes_list.bind('<<TreeviewSelect>>', lambda e: controller.load_selected_note())
        self.close_btn.config(command=controller.safe_exit)