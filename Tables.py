import psycopg2
from tkinter import ttk, messagebox, simpledialog
import tkinter as tk


class Tables():
    def __init__(self, name, host, database, user, password):
        self.connection = None
        self.name = name
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                name=self.name,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return True
        except Exception as e:
            raise Exception("Error:", e)

    def create_table(self, cursor, table_name: str, columns: list):
            cursor.execute(f"""CREATE TABLE {table_name}""")