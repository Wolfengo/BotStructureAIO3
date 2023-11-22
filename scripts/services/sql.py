import sys

import psycopg2


class Changer:
    """Класс используется для проверки наличия базы данных, при её отсутствии,
    класс создаст новую базу данных, либо завершит работу"""
    def __init__(self, dbname, password_postgres, host, port):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(
                dbname='postgres', user='postgres', password=password_postgres, host=host, port=port
            )
            self.conn.set_isolation_level(0)

            self.cursor = self.conn.cursor()
            print('Подключение к серверу прошло успешно. Проверяю наличие нужной базы данных...')
            try:
                self.cursor.execute("SELECT datname FROM pg_database;")
                databases = self.cursor.fetchall()
                database_names = [db[0] for db in databases]
                result = True if dbname in database_names else False
                if result is False:
                    print('База данных не найдена. Создаю базу данных...')
                    try:
                        self.cursor.execute(f"CREATE DATABASE {dbname};")
                        print('База данных успешно создана')
                    except Exception as e:
                        print(f'Возникла ошибка при создании базы данных: {e}')
                        sys.exit()
                else:
                    print('База данных обнаружена! Проверка выполнена успешно')
            except Exception as e:
                print(f'Возникла ошибка при проверке наличия базы данных: {e}')
                sys.exit()
        except Exception as e:
            print(f'Возникла ошибка при подключении к серверу: {e}')
            sys.exit()
        finally:
            if self.conn is not None and self.cursor is not None:
                print("Закрываю подключение к серверу")
                self.cursor.close()
                self.conn.close()


class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            self.cursor = self.conn.cursor()
            print('Подключение к базе данных бота прошло успешно')
        except Exception as e:
            print(f'Не удалось подключиться к базе данных бота, работа будет завершена. - {e}')

    def execute_query(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def create_user_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL
        )
        """
        self.execute_query(query)
        self.close_connection()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

