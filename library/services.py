from typing import List, Optional
import logging

from database import LibraryRepository
from database.models import Book
from core.utils import validate_year, validate_status
from core.enums import BookStatus


logger = logging.getLogger(__name__)


class LibraryService:
    """Сервис для работы с библиотекой книг."""

    def __init__(self, repository: LibraryRepository):
        """
        Инициализация сервиса.

        Args:
            repository (LibraryRepository): Репозиторий для взаимодействия с базой данных.
        """
        self.repository = repository

    def add_book(self, title: str, author: str, year: str) -> None:
        """
        Добавляет книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (str): Год издания (строка, приводится к int внутри функции).

        Raises:
            IncorrectYearError: Если год не удалось преобразовать в число.
        """
        year = validate_year(year)
        self.repository.add(title, author, year)
        logger.info(f"Книга '{title}' автора {author} ({year}) успешно добавлена")

    def get_book(self, title: str) -> Optional[Book]:
        """
        Возвращает книгу по названию, если она есть в наличии.

        Args:
            title (str): Название книги.

        Returns:
            Optional[Book]: Объект книги, если найдена и находится в библиотеке, иначе None.
        """
        book = self.repository.get(title)
        if book and book.status == BookStatus.IN_STOCK.value:
            logger.info(f"Книга '{title}' найдена и доступна")
            return book

        logger.warning(f"Книга с названием '{title}' не найдена или недоступна")
        return None

    def get_all_books(self) -> List[Book]:
        """
        Возвращает список всех доступных книг в библиотеке.

        Returns:
            List[Book]: Список книг, у которых статус `IN_STOCK`.
        """
        books = self.repository.getall()
        available_books = [book for book in books if book.status == BookStatus.IN_STOCK.value]
        logger.info(f"Получен список из {len(available_books)} доступных книг")
        return available_books

    def update_status(self, status: BookStatus, title: str) -> bool:
        """
        Обновляет статус книги.

        Args:
            status (BookStatus | str): Новый статус книги.
            title (str): Название книги.

        Returns:
            bool: True, если обновление прошло успешно, иначе False.

        Raises:
            UpdateStatusError: Если статус некорректный.
        """
        status = validate_status(status)
        success = self.repository.update_status(status.value, title)
        if success:
            logger.info(f"Статус книги '{title}' изменён на {status}")
        else:
            logger.warning(f"Не удалось обновить статус: книга '{title}' не найдена")
        return success

    def delete_book(self, title: str) -> bool:
        """
        Удаляет книгу из библиотеки.

        Args:
            title (str): Название книги.

        Returns:
            bool: True, если книга была удалена, иначе False.
        """
        success = self.repository.delete(title)
        if success:
            logger.info(f"Книга '{title}' удалена из библиотеки")
        else:
            logger.warning(f"Попытка удалить несуществующую книгу '{title}'")
        return success