import pytest
from books_collector import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

class TestBooksCollector:
    def test_add_new_book_valid_name_adds_book(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.books_genre
        assert collector.books_genre["Гарри Поттер"] == ""

    @pytest.mark.parametrize("book_name", ["", "A"*41])
    def test_add_new_book_invalid_name_doesnt_add(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    def test_set_book_genre_for_existing_book_with_valid_genre(self, collector):
        collector.books_genre = {"Гарри Поттер": ""}
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.books_genre["Гарри Поттер"] == "Фантастика"

    def test_set_book_genre_with_invalid_genre_doesnt_change(self, collector):
        collector.books_genre = {"Гарри Поттер": ""}
        collector.set_book_genre("Гарри Поттер", "Несуществующий жанр")
        assert collector.books_genre["Гарри Поттер"] == ""

    def test_set_book_genre_for_non_existing_book_does_nothing(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.books_genre

    def test_get_book_genre_returns_correct_genre(self, collector):
        collector.books_genre = {"Гарри Поттер": "Фантастика"}
        assert collector.get_book_genre("Гарри Поттер") == "Фантастика"

    def test_get_books_with_specific_genre_returns_correct_books(self, collector):
        collector.books_genre = {
            "Книга 1": "Фантастика",
            "Книга 2": "Ужасы",
            "Книга 3": "Фантастика"
        }
        result = collector.get_books_with_specific_genre("Фантастика")
        assert sorted(result) == ["Книга 1", "Книга 3"]

    def test_get_books_for_children_returns_only_child_friendly(self, collector):
        collector.books_genre = {
            "Книга 1": "Фантастика",
            "Книга 2": "Ужасы",
            "Книга 3": "Мультфильмы"
        }
        result = collector.get_books_for_children()
        assert sorted(result) == ["Книга 1", "Книга 3"]

    def test_add_book_in_favorites_adds_to_favorites(self, collector):
        collector.books_genre = {"Гарри Поттер": "Фантастика"}
        collector.add_book_in_favorites("Гарри Поттер")
        assert "Гарри Поттер" in collector.favorites

    def test_add_book_in_favorites_twice_doesnt_duplicate(self, collector):
        collector.books_genre = {"Гарри Поттер": "Фантастика"}
        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Гарри Поттер")
        assert len(collector.favorites) == 1

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.favorites = ["Гарри Поттер"]
        collector.delete_book_from_favorites("Гарри Поттер")
        assert "Гарри Поттер" not in collector.favorites

    def test_delete_non_existent_book_from_favorites_does_nothing(self, collector):
        initial_favorites = ["Гарри Поттер"]
        collector.favorites = initial_favorites.copy()
        collector.delete_book_from_favorites("Несуществующая книга")
        assert collector.favorites == initial_favorites

    def test_get_list_of_favorites_books_returns_all_favorites(self, collector):
        collector.favorites = ["Книга 1", "Книга 2", "Книга 3"]
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 3
        assert "Книга 1" in favorites
        assert "Книга 2" in favorites 
        assert "Книга 3" in favorites
        assert favorites == ["Книга 1", "Книга 2", "Книга 3"]
