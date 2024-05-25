import psycopg2
from config import *


class Human:

    def __init__(self, name: str, last_name: str, age: int, job: str) -> None:
        self.name = name
        self.last_name = last_name
        self.age = age
        self.job = job

    @staticmethod
    def __connect_to_database(func):
        def wrapper(*args, **kwargs):
            try:
                connection = psycopg2.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                connection.autocommit = True

                print(f'[INFO] Успешное подключение к БД {db_name}.')

                result = func(*args, **kwargs, connect=connection)

            except Exception as e:
                print(f'[ERROR] Ошибка. {e}')
                return

            else:
                if connection:
                    connection.close()
                    print('[INFO] Успешное закрытие БД.')
                return result

        return wrapper

    @staticmethod
    @__connect_to_database
    def create_table(connect=None):
        cursor = connect.cursor()
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS human (
                human_id SERIAL PRIMARY KEY,
                name VARCHAR(35),
                last_name VARCHAR(35),
                age INT,
                job VARCHAR(50)
            )
            '''
        )

    @__connect_to_database
    def add_person_in_database(self, connect=None):
        cursor = connect.cursor()
        cursor.execute(
            f'''
            INSERT INTO human (name, last_name, age, job)
            VALUES
            ('{self.name}', '{self.last_name}', '{self.age}', '{self.job}')
            '''
        )

    @staticmethod
    @__connect_to_database
    def get_info_from_database(name=None, last_name=None, connect=None):
        cursor = connect.cursor()
        request = \
            f'''
            SELECT * FROM human
            '''
        if name:
            request += f'WHERE name = \'{name}\' '
        if last_name:
            value = 'WHERE' if 'WHERE' not in request else 'AND'
            request += f'{value} last_name = \'{last_name}\''

        cursor.execute(request)

        last = cursor.fetchone()
        while last:
            print(last)
            last = cursor.fetchone()
