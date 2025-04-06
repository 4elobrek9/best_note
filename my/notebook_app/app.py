import tkinter as tk
from model import NoteModel
from view import NoteView
from controller import NoteController

def main():
    root = tk.Tk()
    
    # Настройки окна
    root.geometry("900x650")
    root.minsize(800, 600)
    
    # Инициализация MVC
    model = NoteModel()
    view = NoteView(root)
    controller = NoteController(model, view)
    
    # Центрирование окна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()