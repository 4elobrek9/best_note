from typing import Optional
from model import NoteModel
from view import NoteView
import time

class NoteController:
    def __init__(self, model: NoteModel, view: NoteView):
        self.model = model
        self.view = view
        self.current_note_id: Optional[int] = None
        self.last_save_time = 0
        self._setup_view()
        self.load_notes()

    def _setup_view(self):
        self.view.bind_events(self)

    def load_notes(self):
        notes = self.model.get_all_notes()
        self.view.update_notes_list(notes)

    def load_selected_note(self):
        notes = self.model.get_all_notes()
        index = self.view.get_selected_note_index()
        if 0 <= index < len(notes):
            self.current_note_id = notes[index]['id']
            self.view.show_editor()
            self.view.set_note_data(notes[index]['content'])

    def create_new_note(self):
        self.current_note_id = self.model.create_note("", "")
        self.view.show_editor()
        self.view.clear_editor()
        self.load_notes()
        self.view.text_editor.focus()

    def auto_save_note(self):
        current_time = time.time()
        if current_time - self.last_save_time > 1 and self.current_note_id:
            self.save_current_note()
            self.last_save_time = current_time

    def save_current_note(self):
        if self.current_note_id is None:
            return
            
        note_data = self.view.get_note_data()
        self.model.update_note(self.current_note_id, note_data['title'], note_data['content'])
        self.load_notes()