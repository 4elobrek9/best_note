from typing import Optional
from model import NoteModel
from view import NoteView
import time
from tkinter import messagebox

class NoteController:
    def __init__(self, model: NoteModel, view: NoteView):
        self.model = model
        self.view = view
        self.current_note_id: Optional[int] = None
        self._setup_view()
        self.load_notes()

    def _setup_view(self):
        """Инициализация представления и привязка событий"""
        self.view.bind_events(self)
        self.view.set_status("Готово")
        
        # Привязка горячих клавиш
        self.view.root.bind('<Control-n>', lambda e: self.create_new_note())
        self.view.root.bind('<Control-s>', lambda e: self.save_current_note())
        self.view.root.bind('<Control-f>', lambda e: self.view.search_entry.focus())
        self.view.root.bind('<Escape>', lambda e: self.safe_exit())

    def safe_exit(self):
        """Элегантный выход"""
        self.view.root.destroy()

    def load_notes(self):
        """Загрузка заметок"""
        notes = self.model.get_all_notes()
        self.view.update_notes_list(notes)
        self.view.set_status(f"Загружено заметок: {len(notes)}")

    def load_selected_note(self):
        """Загрузка выбранной заметки"""
        note_id = self.view.get_selected_note_id()
        if note_id:
            note = self.model.get_note(note_id)
            if note:
                self.current_note_id = note_id
                self.view.set_note_data(note['title'], note['content'])
                self.view.set_status(f"Заметка '{note['title']}' загружена")

    def create_new_note(self):
        """Создание новой заметки"""
        self.current_note_id = None
        self.view.clear_editor()
        self.view.title_entry.focus()
        self.view.set_status("Готова новая заметка")

    def save_current_note(self):
        """Сохранение заметки"""
        note_data = self.view.get_note_data()
        
        if not note_data['title']:
            self.view.show_error("Заголовок не может быть пустым")
            return
            
        try:
            if self.current_note_id:
                self.model.update_note(self.current_note_id, note_data['title'], note_data['content'])
                message = "Заметка обновлена"
            else:
                self.current_note_id = self.model.create_note(note_data['title'], note_data['content'])
                message = "Заметка создана"
            
            self.load_notes()
            self.view.set_status(message)
        except Exception as e:
            self.view.show_error(f"Ошибка при сохранении: {str(e)}")

    def delete_current_note(self):
        """Удаление заметки"""
        if not self.current_note_id:
            self.view.show_error("Не выбрана заметка для удаления")
            return
            
        if messagebox.askyesno("Подтверждение", "Удалить выбранную заметку?"):
            try:
                self.model.delete_note(self.current_note_id)
                self.current_note_id = None
                self.view.clear_editor()
                self.load_notes()
                self.view.set_status("Заметка удалена")
            except Exception as e:
                self.view.show_error(f"Ошибка при удалении: {str(e)}")

    def search_notes(self):
        """Поиск заметок"""
        search_term = self.view.search_entry.get()
        if search_term and search_term != "Поиск заметок...":
            notes = self.model.search_notes(search_term)
            self.view.update_notes_list(notes)
            self.view.set_status(f"Найдено заметок: {len(notes)}")
        else:
            self.load_notes()