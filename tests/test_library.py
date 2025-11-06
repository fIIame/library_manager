import pytest
from database.manager import DatabaseManager
from database.repositories import LibraryRepository
from library.services import LibraryService
from core.enums import BookStatus
from core.custom_exceptions import IncorrectYearError, UpdateStatusError

# Фикстура для чистой базы данных в памяти
@pytest.fixture
def repository():
    manager = DatabaseManager(":memory:")
    manager.connect_to_database()
    repo = LibraryRepository(manager)
    yield repo
    manager.close_connection()

@pytest.fixture
def service(repository):
    return LibraryService(repository)

def test_add_and_get_book(repository):
    assert repository.add("Test Book", "Author", 2000) is True
    book = repository.get("Test Book")
    assert book.title == "Test Book"
    assert book.author == "Author"
    assert book.year == 2000
    assert book.status == BookStatus.IN_STOCK.value

def test_get_all_books(repository):
    repository.add("Book1", "Author1", 2000)
    repository.add("Book2", "Author2", 2010)
    books = repository.getall()
    assert len(books) == 2

def test_update_status(repository):
    repository.add("Book1", "Author1", 2000)
    assert repository.update_status(BookStatus.OUT_OF_STOCK.value, "Book1") is True
    book = repository.get("Book1")
    assert book.status == BookStatus.OUT_OF_STOCK.value

def test_delete_book(repository):
    repository.add("Book1", "Author1", 2000)
    assert repository.delete("Book1") is True
    assert repository.get("Book1") is None

def test_service_add_book(service):
    service.add_book("Service Book", "Author", "2005")
    book = service.get_book("Service Book")
    assert book.title == "Service Book"

def test_service_invalid_year(service):
    with pytest.raises(IncorrectYearError):
        service.add_book("Invalid Year Book", "Author", "abcd")

def test_service_update_status_invalid(service):
    service.add_book("Book", "Author", "2000")
    with pytest.raises(UpdateStatusError):
        service.update_status("invalid_status", "Book")
