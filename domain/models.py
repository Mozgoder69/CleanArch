# models.py
import psycopg2, pyramid
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from pyramid.decorator import reify
from pyramid.request import Request

class Database:
    def __init__(self, request):
        self._request = request
        self._connection = None

    @reify
    def connection(self):
        if self._connection is None:
            # Замените параметры подключения на свои
            self._connection = psycopg2.connect(
                user='your_username',
                password='your_password',
                host='your_host',
                database='your_database'
            )
        return self._connection

    def close_connection(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

db = Database(Request)

class TableInfo:
    def __init__(self, table_name):
        self.table_name = table_name

    def create_table(self):
        # Создание таблицы
        with db.connection, db.connection.cursor() as cursor:
            create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} (id SERIAL PRIMARY KEY);").format(sql.Identifier(self.table_name))
            cursor.execute(create_table_query)

    def fetch_data(self):
        # Получение данных из таблицы
        with db.connection, db.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            select_data_query = sql.SQL("SELECT * FROM {};").format(sql.Identifier(self.table_name))
            cursor.execute(select_data_query)
            return cursor.fetchall()

class DynamicModel:
    def __init__(self, table_name):
        self.table_name = table_name

    def insert_data(self, data):
        # Вставка данных в таблицу
        with db.connection, db.connection.cursor() as cursor:
            columns = data.keys()
            values = [data[col] for col in columns]
            insert_data_query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *;").format(
                sql.Identifier(self.table_name),
                sql.SQL(', ').join(map(sql.Identifier, columns)),
                sql.SQL(', ').join([sql.Placeholder()] * len(columns))
            )
            cursor.execute(insert_data_query, values)
            return cursor.fetchone()

def generate_models():
    with db.connection, db.connection.cursor() as cursor:
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        table_names = [record[0] for record in cursor.fetchall()]

        for table_name in table_names:
            class_name = ''.join(word.capitalize() for word in table_name.split('_'))
            setattr(DynamicModel, class_name, type(class_name, (object,), {'table_info': TableInfo(table_name)}))

generate_models()