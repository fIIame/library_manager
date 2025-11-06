from typing import List, Optional
import sqlite3 as sql

from database.manager import DatabaseManager
from database.models import Book
from core.enums import BookStatus


class LibraryRepository:
    """
    Репозиторий для работы с таблицей Library в базе данных.

    Предоставляет CRUD-операции:
      - добавление книги,
      - получение одной или всех книг,
      - обновление статуса книги,
      - удаление книги.
    """

    def __init__(self, manager: DatabaseManager):
        """
        Инициализация репозитория.

        Args:
            manager (DatabaseManager): менеджер базы данных, управляющий соединением.
        """
        self.manager = manager

    def _execute(self, query: str, params=(), commit: bool = False) -> sql.Cursor:
        """
        Выполняет SQL-запрос с параметрами.

        Args:
            query (str): SQL-запрос.
            params (tuple): параметры для подстановки в запрос.
            commit (bool): если True — фиксирует изменения (для INSERT/UPDATE/DELETE).

        Returns:
            sqlite3.Cursor: объект курсора после выполнения запроса.

        Raises:
            ConnectionError: если соединение с базой данных отсутствует.
        """
        if self.manager.connection is None:
            raise ConnectionError("База данных не подключена")

        conn = self.manager.connection
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
        return cursor

    def add(self, title: str, author: str, year: int) -> bool:
        """
        Добавляет новую книгу в базу данных.

        Args:
            title (str): название книги.
            author (str): автор книги.
            year (int): год издания.

        Returns:
            bool: True, если добавление прошло успешно, иначе False.
        """
        try:
            self._execute(
                "INSERT INTO Library (title, author, year) VALUES (?, ?, ?)",
                (title, author, year),
                commit=True
            )
            return True
        except sql.IntegrityError:
            return False

    def get(self, title: str) -> Optional[Book]:
        """
        Получает книгу по названию.

        Args:
            title (str): название книги.

        Returns:
            Optional[Book]: объект книги, если найдена, иначе None.
        """
        cursor = self._execute(
            "SELECT * FROM Library WHERE title = ?",
            (title,)
        )
        row = cursor.fetchone()
        return Book(*row) if row else None

    def getall(self) -> List[Book]:
        """
        Возвращает все книги из базы данных.

        Returns:
            List[Book]: список всех книг.
        """
        cursor = self._execute("SELECT * FROM Library")
        rows = cursor.fetchall()
        return [Book(*row) for row in rows]

    def update_status(self, status: str, title: str) -> bool:
        """
        Обновляет статус книги по названию.

        Args:
            status (BookStatus): новый статус книги.
            title (str): название книги.

        Returns:
            bool: True, если обновление выполнено успешно, иначе False.
        """
        cursor = self._execute(
            "UPDATE Library SET status = ? WHERE title = ?",
            (status, title),
            commit=True
        )
        return cursor.rowcount > 0

    def delete(self, title: str) -> bool:
        """
        Удаляет книгу из базы по названию.

        Args:
            title (str): название книги.

        Returns:
            bool: True, если книга удалена, иначе False.
        """
        cursor = self._execute(
            "DELETE FROM Library WHERE title = ?",
            (title,),
            commit=True
        )
        return cursor.rowcount > 0
