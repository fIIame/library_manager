import sys
import logging

from database.manager import DatabaseManager
from database.repositories import LibraryRepository
from library.services import LibraryService
from core.utils import normalize_file_path


def setup_logger(_format: str) -> None:
    """Настраивает формат и вывод логов."""
    logging.basicConfig(
        level=logging.INFO,
        format=_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def main(repository: LibraryRepository) -> None:
    """Простой CLI-интерфейс для управления библиотекой."""
    library_service = LibraryService(repository)
    logger = logging.getLogger(__name__)

    print("Добро пожаловать в библиотеку!")
    print("Введите 'help' для списка команд.\n")

    while True:
        try:
            command = input(">>> ").strip().lower()

            if command == "add":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                year = input("Year: ").strip()
                library_service.add_book(title, author, year)
                print("Книга успешно добавлена!\n")

            elif command == "get":
                title = input("Title: ").strip()
                book = library_service.get_book(title)
                if book:
                    print(book, "\n")
                else:
                    print("Книга не найдена или недоступна.\n")

            elif command == "getall":
                books = library_service.get_all_books()
                if books:
                    print(*books, sep="\n")
                else:
                    print("Библиотека пуста.")
                print()

            elif command == "update":
                title = input("Title: ").strip()
                new_status = input("New status: ").strip()
                success = library_service.update_status(new_status, title)
                msg = "Статус обновлён.\n" if success else "Книга не найдена.\n"
                print(msg)

            elif command == "delete":
                title = input("Title: ").strip()
                success = library_service.delete_book(title)
                msg = "Книга удалена.\n" if success else "Книга не найдена.\n"
                print(msg)

            elif command in ("help", "?"):
                print("""Доступные команды:
    1. add — добавить книгу
    2. get — получить книгу по названию
    3. getall — вывести все книги
    4. update — изменить статус книги
    5. delete — удалить книгу
    6. exit — выход
""")

            elif command == "exit":
                print("Выход из программы.")
                break

            elif command == "":
                continue  # просто Enter

            else:
                print("Неизвестная команда. Введите 'help' для справки.\n")

        except Exception as e:
            logger.exception(f"Ошибка во время выполнения команды: {e}")
            print("Произошла ошибка, проверьте ввод.\n")


if __name__ == "__main__":
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s — %(message)s"
    setup_logger(LOG_FORMAT)
    logger = logging.getLogger(__name__)

    path = input("Path to database: ").strip()
    path = normalize_file_path(path)

    manager = DatabaseManager(path)
    manager.connect_to_database()
    repository = LibraryRepository(manager)

    try:
        main(repository)
    except KeyboardInterrupt:
        logger.info("Приложение завершило работу.")
    finally:
        manager.close_connection()
        logger.info("Соединение с базой данных закрыто.")
