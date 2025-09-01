from tkinter import ttk, messagebox, simpledialog
import tkinter as tk
from Tables import Tables
import os

class TableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление таблицами БД")
        self.root.geometry("1000x600")

        self.db_manager = None
        self.current_table = None

        #ui
        self.auto_connect()

    def auto_connect(self):
        """Automatic connection to DB"""
        host = os.getenv('DB_HOST', 'localhost')
        database = os.getenv('DB_NAME', 'postgres')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASS', 'postgres')
        port = 5432

        self.show_loading_message("DB connection...")

        try:
            if self.connect_to_db(host, database, user, password, port):
                self.hide_loading_message()
                return

        except Exception:
            self.hide_loading_message()
            messagebox.showerror("Error",
                                 "Failed to connect to database. "
                                 "Try to check postgres connection settings")

            return



    def show_loading_message(self, message):
        """Show loading message"""
        self.loading_label = ttk.Label(self.root, text=message, font=('Arial', 12))
        self.loading_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.root.update()

    def hide_loading_message(self):
        """Hide loading message"""
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()

    def connect_to_db(self, host, database, user, password, port):
        """DB connection"""
        try:
            self.db_manager = Tables(host, database, user, password, port)
            if self.db_manager.connect():
                return True
        except Exception:
            pass
        return False