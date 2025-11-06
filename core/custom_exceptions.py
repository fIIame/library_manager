class LibraryError(Exception):
    """Базовый класс для ошибок библиотеки."""
    pass

class UpdateStatusError(LibraryError):
    pass

class IncorrectYearError(LibraryError):
    pass
