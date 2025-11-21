from typing import Optional
import sqlite3 as sql


class DatabaseManager:
    _instance = None

    def __new__(cls, path: str = "database.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.path = path
            cls._instance.connection = None
        return cls._instance

    def connect_to_database(self) -> None:
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
        if self.connection:
            self.connection.close()
            self.connection = None