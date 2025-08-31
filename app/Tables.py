from psycopg2 import sql
import psycopg2



class Tables():
    def __init__(self, name, host, database, user, password, port = 5432):
        self.connection = None
        self.host = host
        self.database = database
        self.user = user
        self.name = name
        self.port = port
        self.password = password

    def connect(self):
        """BD connection"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                name=self.name,
                database=self.database,
                user=self.user,
                password=self.password,
                port = self.port
            )
            return True
        except Exception as e:
            raise Exception("Connection error:", e)

    def disconnect(self):
        """BD disconnect"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_sql_type(self, type_name: str) -> str:
        """Type to SQL type transformation"""
        type_mapping = {
            'integer': 'INTEGER',
            'real': 'REAL',
            'text': 'TEXT',
            'datetime': 'TIMESTAMP',
            'date': 'DATE'
        }
        return type_mapping.get(type_name.lower(), 'TEXT')

    def create_table(self, table_name: str, columns: list, primary_key: str):
        """Create new table"""
        if not self.connection:
            return False
        try:
            with self.connection.cursor() as cursor:
                column_definitions = []
                for column in columns:
                    col_name = column['name']
                    col_type = self.get_sql_type(column['type'])
                    col_def = f"{col_name} {col_type}"

                    if primary_key and col_name == primary_key:
                        col_def += " PRIMARY KEY"

                    column_definitions.append(col_def)

                query = sql.SQL("CREATE TABLE {} ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(', ').join(map(sql.SQL, column_definitions))
                )

                cursor.execute(query)
                self.connection.commit()
                return True

        except Exception as e:
            raise Exception("Create table error:", e)

    def get_tables(self):
        """Get all tables"""
        if not self.connection:
            return []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                return [row[0] for row in cursor.fetchall()]
        except Exception:
            return []

    def remove_table(self, table_name: str):
        """Remove table"""
        if not self.connection:
            return False

        try:
            with self.connection.cursor() as cursor:
                query = sql.SQL("DROP TABLE IF EXISTS {}").format(
                    sql.Identifier(table_name)
                )
                cursor.execute(query)
                self.connection.commit()
                return True

        except Exception as e:
            raise Exception("REmove table error:", e)

    def get_info(self, table_name: str):
        """Get info about the table"""
        if not self.connection:
            return []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        column_name, 
                        data_type,
                        is_nullable,
                        column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position
                """, (table_name,))

                columns = []
                for row in cursor.fetchall():
                    columns.append({
                        'name': row[0],
                        'type': row[1],
                        'nullable': row[2] == 'YES',
                        'default': row[3]
                    })
                return columns

        except Exception:
            return []


