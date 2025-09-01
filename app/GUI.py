from tkinter import ttk, messagebox
import tkinter as tk

from Tables import Tables
import os

class TableApp():
    def __init__(self, root):
        self.root = root
        self.root.title("DB tables editor")
        self.root.geometry("600x600")

        self.Tables = None
        self.current_table = None

        self.gui_settings()
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
            self.hide_loading_message()
            messagebox.showerror("Error",
                                 "Failed to connect to database. "
                                 "Try to check postgres connection settings")
            self.show_connection_message()
            return

        self.show_connection_message()

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
            self.Tables = Tables(host, database, user, password, port)
            if self.Tables.connect():
                return True
        except Exception:
            pass
        return False

    def reconnect(self):
        """Reconnect to DB"""
        self.show_connection_message()

    def gui_settings(self):
        """GUI settings"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        tables_frame = ttk.LabelFrame(main_frame, text="Tables", padding="5")
        tables_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))

        ttk.Button(tables_frame, text="Refresh", command=self.refresh_tables).pack(pady=5)
        ttk.Button(tables_frame, text="Create table", command=self.create_table_message).pack(pady=5)
        ttk.Button(tables_frame, text="Reconnect to the DB", command=self.reconnect).pack(pady=5)

        self.tables_listbox = tk.Listbox(tables_frame, width=20, height=15)
        self.tables_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        self.tables_listbox.bind('<<ListboxSelect>>', self.table_select)

        self.table_frame = ttk.LabelFrame(main_frame, text="Table settings", padding="5")
        self.table_frame.grid(row=1, column=1, sticky="nsew")
        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(1, weight=1)

        button_frame = ttk.Frame(self.table_frame)
        button_frame.grid(row=0, column=0, sticky='we', pady=5)

        ttk.Button(button_frame, text="Edit", command=self.edit_table_message).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Remove", command=self.delete_table_message).pack(side=tk.LEFT, padx=2)

        columns_frame = ttk.Frame(self.table_frame)
        columns_frame.grid(row=1, column=0, sticky="nsew", pady=5)
        columns_frame.columnconfigure(0, weight=1)
        columns_frame.rowconfigure(0, weight=1)

        self.columns_tree = ttk.Treeview(columns_frame, columns=('type', 'nullable', 'default'), show='headings')
        self.columns_tree.heading('#0', text='Name')
        self.columns_tree.heading('type', text='Type')
        self.columns_tree.heading('nullable', text='Null')
        self.columns_tree.heading('default', text='Default')
        self.columns_tree.column('#0', width=120)
        self.columns_tree.column('type', width=100)
        self.columns_tree.column('nullable', width=50)
        self.columns_tree.column('default', width=100)

        scrollbar = ttk.Scrollbar(columns_frame, orient=tk.VERTICAL, command=self.columns_tree.yview)
        self.columns_tree.configure(yscrollcommand=scrollbar.set)



    def table_select(self, event = None):
        """Select table to do smth"""
        selection = self.tables_listbox.curselection()
        if not selection:
            return

        table_name = self.tables_listbox.get(selection[0])
        self.current_table = table_name
        self.show_table_info(table_name)

    def show_table_info(self, table_name):
        """Get info about the table"""
        self.columns_tree.delete(*self.columns_tree.get_children())
        columns = self.Tables.get_info(table_name)
        for col in columns:
            self.columns_tree.insert('', 'end', text=col['name'], values=(
                col['type'],
                'YES' if col['nullable'] else 'NO',
                col['default'] if col['default'] else ''
            ))

    def show_connection_message(self):
        """DB connection message"""
        message = ConnectionMessage(self.root, self)
        self.root.wait_window(message)
        self.hide_loading_message()

    def refresh_tables(self):
        """Refresh tables after some moves"""
        if not self.Tables:
            return

        self.tables_listbox.delete(0, tk.END)
        tables = self.Tables.get_tables()
        for table in tables:
            self.tables_listbox.insert(tk.END, table)

    def create_table_message(self):
        """DB creation message"""
        if not self.Tables:
            messagebox.showerror("Error", "Need to connect to DB")
            return

        message = TableEditorMessage(self.root, "Create table", self.Tables)
        self.root.wait_window(message)
        self.refresh_tables()

    def edit_table_message(self):
        """Db edition message"""
        if not self.current_table:
            messagebox.showinfo("Info", "Choose table to edit")
            return

        current_columns = self.Tables.get_info(self.current_table)

        message = TableEditorMessage(self.root, f"Edit table: {self.current_table}", self.Tables, self.current_table,
                                     current_columns)
        self.root.wait_window(message)
        self.refresh_tables()

    def delete_table_message(self):
        """Delete table message"""
        if not self.current_table:
            messagebox.showinfo("Info", "Choose table to delete")
            return

        result = messagebox.askyesno("Confirm",
                                     f"Are you sure you want to delete: '{self.current_table}'?")
        if result:
            if self.Tables.remove_table(self.current_table):
                messagebox.showinfo("Info", "Table delete")
                self.current_table = None
                self.refresh_tables()
                self.columns_tree.delete(*self.columns_tree.get_children())
            else:
                messagebox.showerror("Error", "Can't delete the table")

class TableEditorMessage(tk.Toplevel):
    def __init__(self, parent, title, db_manager, table_name=None, existing_columns=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.table_name = table_name
        self.title(title)
        self.geometry("600x500")
        self.resizable(False, False)

        self.columns = existing_columns if existing_columns else []
        self.existing_pk = self.get_current_pk()
        self.gui_settings()
        self.grab_set()

        if table_name:
            self.name_entry.insert(0, table_name)
            self.name_entry.config(state='disabled')
            self.update_columns()

    def get_current_pk(self):
        """get current primary key"""
        if not self.table_name or not self.db_manager.connection:
            return ""
        try:
            with self.db_manager.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT a.attname
                    FROM   pg_index i
                    JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                         AND a.attnum = ANY(i.indkey)
                    WHERE  i.indrelid = %s::regclass
                    AND    i.indisprimary;
                """, (self.table_name,))
                row = cursor.fetchone()
                return row[0] if row else ""
        except Exception as e:
            print("Error getting PK:", e)
            return ""

    def gui_settings(self):
        """GUI settings"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Table name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="Primary key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pk_entry = ttk.Entry(main_frame, width=30)
        self.pk_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        if self.existing_pk:
            self.pk_entry.insert(0, self.existing_pk)

        columns_frame = ttk.LabelFrame(main_frame, text="Columns", padding="10")
        columns_frame.grid(row=2, column=0, columnspan=2, sticky="we", pady=10)
        columns_frame.columnconfigure(1, weight=1)

        self.columns_tree = ttk.Treeview(columns_frame, columns=('type',), show='tree headings', height=8)
        self.columns_tree.heading('#0', text='Name')
        self.columns_tree.heading('type', text='Type')

        scrollbar = ttk.Scrollbar(columns_frame, orient=tk.VERTICAL, command=self.columns_tree.yview)
        self.columns_tree.configure(yscrollcommand=scrollbar.set)

        self.columns_tree.grid(row=0, column=0, columnspan=3, sticky="news", pady=5)
        scrollbar.grid(row=0, column=3, sticky="ns")

        ttk.Button(columns_frame, text="Add", command=self.add_column).grid(row=1, column=0, pady=5, padx=2)
        ttk.Button(columns_frame, text="Delete", command=self.remove_column).grid(row=1, column=1, pady=5, padx=2)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Save", command=self.create_table).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=10)

        self.update_columns()

    def add_column(self):
        """Add column to the table"""
        message = ColumnMessage(self)
        self.wait_window(message)

        if message.column_data:
            self.columns.append(message.column_data)
            self.update_columns()

    def remove_column(self):
        """Delete column from the table"""
        selection = self.columns_tree.selection()
        if not selection:
            return

        index = self.columns_tree.index(selection[0])
        if 0 <= index < len(self.columns):
            self.columns.pop(index)
            self.update_columns()

    def update_columns(self):
        """Update columns"""
        self.columns_tree.delete(*self.columns_tree.get_children())
        for column in self.columns:
            self.columns_tree.insert('', 'end', text=column['name'], values=(column['type'],))

    def create_table(self):
        """Create or update table"""
        table_name = self.name_entry.get().strip()
        primary_key = self.pk_entry.get().strip()

        if not table_name:
            messagebox.showerror("Error", "Put the table name first")
            return

        if not self.columns:
            messagebox.showerror("Error", "Put at least one column")
            return

        if primary_key and not any(col['name'] == primary_key for col in self.columns):
            messagebox.showerror("Error", "Primary key is not unique")
            return

        if self.table_name:
            try:
                if not self.db_manager.remove_table(self.table_name):
                    messagebox.showerror("Error", "Can't delete old table")
                    return

                if self.db_manager.create_table(table_name, self.columns, primary_key):
                    messagebox.showinfo("Info", "Table updated successfully")
                    self.destroy()
                else:
                    messagebox.showerror("Error", "Can't create new table")

            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {str(e)}")

        else:
            if self.db_manager.create_table(table_name, self.columns, primary_key):
                messagebox.showinfo("Info", "Table created successfully")
                self.destroy()
            else:
                messagebox.showerror("Error", "Can't create table")


class ConnectionMessage(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("DB connection")
        self.geometry("400x250")
        self.resizable(False, False)

        self.setup_ui()
        self.grab_set()

    def setup_ui(self):
        """GUI settings"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Host:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.host_entry = ttk.Entry(main_frame, width=30)
        self.host_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        self.host_entry.insert(0, "localhost")

        ttk.Label(main_frame, text="Data base:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.db_entry = ttk.Entry(main_frame, width=30)
        self.db_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.db_entry.insert(0, "postgres")

        ttk.Label(main_frame, text="User:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_entry = ttk.Entry(main_frame, width=30)
        self.user_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.user_entry.insert(0, "postgres")

        ttk.Label(main_frame, text="Password:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(main_frame, width=30, show="")
        self.password_entry.grid(row=3, column=1, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="Port:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.port_entry = ttk.Entry(main_frame, width=30)
        self.port_entry.grid(row=4, column=1, pady=5, padx=(10, 0))
        self.port_entry.insert(0, "5432")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Connect", command=self.connect).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def connect(self):
        """Connect to DB"""
        host = self.host_entry.get()
        database = self.db_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        try:
            port = int(self.port_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Port should be integer")
            return

        if self.app.connect_to_db(host, database, user, password, port):
            self.destroy()
        else:
            messagebox.showerror("Error", "Can't connect to the DB")

class ColumnMessage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add column")
        self.geometry("300x200")
        self.resizable(False, False)

        self.column_data = None
        self.gui_settings()
        self.grab_set()

    def gui_settings(self):
        """GUI settings"""
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Column name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=20)
        self.name_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(main_frame, textvariable=self.type_var, width=18, state='readonly')
        type_combo['values'] = ('integer', 'real', 'text', 'datetime')
        type_combo.grid(row=1, column=1, pady=5, padx=(10, 0))
        type_combo.current(0)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Add", command=self.add_column).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=10)

    def add_column(self):
        """Add column"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Put column name")
            return

        self.column_data = {
            'name': name,
            'type': self.type_var.get()
        }
        self.destroy()
