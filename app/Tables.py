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

    def get_sql_type(self, type_name: str) -> str:
        """Преобразовать тип в SQL тип"""
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