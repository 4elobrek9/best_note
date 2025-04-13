import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class NoteModel:
    def __init__(self, db_name: str = 'notes.db'):
        self.conn = sqlite3.connect(db_name)
        self._create_table()
        self._add_default_note()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def _add_default_note(self):
        """Добавляет заметку по умолчанию, если таблица пуста"""
        if not self.get_all_notes():
            self.create_note("Моя первая заметка", "Начните писать здесь...")

    def create_note(self, title: str, content: str) -> int:
        query = "INSERT INTO notes (title, content) VALUES (?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(query, (title, content))
        self.conn.commit()
        return cursor.lastrowid

    def update_note(self, note_id: int, title: str, content: str):
        query = """
        UPDATE notes 
        SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        self.conn.execute(query, (title, content, note_id))
        self.conn.commit()

    def delete_note(self, note_id: int):
        query = "DELETE FROM notes WHERE id = ?"
        self.conn.execute(query, (note_id,))
        self.conn.commit()

    def get_note(self, note_id: int) -> Optional[Dict]:
        query = "SELECT id, title, content, created_at, updated_at FROM notes WHERE id = ?"
        cursor = self.conn.execute(query, (note_id,))
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            }
        return None

    def get_all_notes(self) -> List[Dict]:
        query = "SELECT id, title, content, created_at, updated_at FROM notes ORDER BY updated_at DESC"
        cursor = self.conn.execute(query)
        return [
            {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            }
            for row in cursor.fetchall()
        ]

    def search_notes(self, search_term: str) -> List[Dict]:
        query = """
        SELECT id, title, content, created_at, updated_at 
        FROM notes 
        WHERE title LIKE ? OR content LIKE ?
        ORDER BY updated_at DESC
        """
        search_term = f"%{search_term}%"
        cursor = self.conn.execute(query, (search_term, search_term))
        return [
            {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'created_at': row[3],
                'updated_at': row[4]
            }
            for row in cursor.fetchall()
        ]

    def __del__(self):
        self.conn.close()