import datetime

from core.custom_exceptions import IncorrectYearError, UpdateStatusError
from core.enums import BookStatus


def normalize_file_path(path: str) -> str:
    """
    Нормализует путь к файлу базы данных.

    - Удаляет лишний символ `/` в конце, если он есть.
    - Добавляет расширение `.db`, если отсутствует.

    Args:
        path (str): Исходный путь, введённый пользователем.

    Returns:
        str: Корректный путь к базе данных.
    """
    if path.endswith('/'):
        path = path[:-1]
    if not path.endswith('.db'):
        path = path + '.db'

    return path


def _is_year_correct(year: int) -> bool:
    """
    Проверяет корректность указанного года издания книги.

    Условие корректности:
    - Год не больше текущего.
    - Год не меньше 1000 (исключаем некорректные даты).

    Args:
        year (int): Год издания книги.

    Returns:
        bool: True, если год корректен, иначе False.
    """
    current_year = datetime.datetime.now().year
    return 1000 <= year <= current_year


def validate_year(year: str) -> int:
    """
    Валидирует и преобразует введённое значение года в целое число.

    Args:
        year (str): Год в строковом виде, введённый пользователем.

    Raises:
        IncorrectYearError: Если год не является числом или выходит за допустимые границы.

    Returns:
        int: Преобразованный и проверенный год.
    """
    try:
        year = int(year)
    except ValueError:
        raise IncorrectYearError("Введен некорректный год")

    if not _is_year_correct(year):
        raise IncorrectYearError("Введен некорректный год")

    return year


def validate_status(status: BookStatus) -> BookStatus:
    """
    Проверяет, что переданный статус является элементом перечисления BookStatus.

    Args:
        status (BookStatus): Проверяемое значение статуса.

    Raises:
        UpdateStatusError: Если передано невалидное значение статуса.

    Returns:
        BookStatus: Валидный объект статуса.
    """
    if not isinstance(status, BookStatus):
        raise UpdateStatusError(f"Недопустимый статус: {status}")
    return status
