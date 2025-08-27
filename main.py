import psycopg2
from tkinter import ttk, messagebox, simpledialog
import tkinter as tk



db_name = ""
db_user = ""
db_password = ""
db_host = "localhost"
db_port = "5432"
def connect():
    try:
        return psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except psycopg2.Error as e:
        messagebox.showerror("Error", "Connection error:", e)

def create_table(cursor, table_name: str, ):
        cursor.execute(f"""CREATE TABLE {table_name}""")

def main_function():
    conn = connect()
    cursor = conn.cursor()