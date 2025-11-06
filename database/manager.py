from typing import Optional
import sqlite3 as sql


class DatabaseManager:
    """
    Класс для управления подключением к базе данных SQLite.

    Отвечает за установку, инициализацию и закрытие соединения с базой.
    При первом подключении создаёт таблицу `Library`, если её нет.
    """

    def __init__(self, path: str = "database.db"):
        """
        Инициализация менеджера базы данных.

        Args:
            path (str): Путь к файлу базы данных. По умолчанию — "database.db".
        """
        self.path = path
        self.connection: Optional[sql.Connection] = None

    def connect_to_database(self) -> None:
        """
        Подключается к базе данных SQLite и создаёт таблицу Library, если она отсутствует.

        Таблица содержит поля:
            - book_id (INTEGER, PRIMARY KEY)
            - title (TEXT, NOT NULL)
            - author (TEXT, NOT NULL)
            - year (INTEGER, NOT NULL)
            - status (TEXT, DEFAULT 'в наличии')

        Raises:
            sqlite3.Error: В случае ошибки при подключении или создании таблицы.
        """
        if self.connection is None:
            try:
                self.connection = sql.connect(self.path, check_same_thread=False)
                cursor = self.connection.cursor()

                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS Library(
                        book_id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        year INTEGER NOT NULL,
                        status TEXT DEFAULT 'в наличии'
                    )
                    '''
                )
                self.connection.commit()

            except sql.Error as e:
                print(f"Ошибка подключения к базе данных: {e}")
                self.connection = None

    def close_connection(self) -> None:
        """
        Закрывает текущее соединение с базой данных, если оно существует.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
