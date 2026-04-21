from datetime import datetime, timedelta
from typing import List, Optional, Dict


class Book:
    def __init__(self, book_id: int, title: str, author: str, isbn: str, year: int):
        self.id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_available = True
        self.current_reader_id: Optional[int] = None
        self.due_date: Optional[datetime] = None
    
    def check_out(self, reader_id: int, days: int = 14):
        self.is_available = False
        self.current_reader_id = reader_id
        self.due_date = datetime.now() + timedelta(days=days)
    
    def return_book(self):
        self.is_available = True
        self.current_reader_id = None
        self.due_date = None


class Reader:
    def __init__(self, reader_id: int, name: str, email: str, phone: str):
        self.id = reader_id
        self.name = name
        self.email = email
        self.phone = phone
        self.registered_at = datetime.now()
        self.borrowed_books: List[int] = []  # список ID книг
    
    def borrow_book(self, book_id: int):
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
    
    def return_book(self, book_id: int) -> bool:
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False


class Library:
    def __init__(self, name: str):
        self.name = name
        self.books: Dict[int, Book] = {}
        self.readers: Dict[int, Reader] = {}
        self._next_book_id = 1
        self._next_reader_id = 1
        self.borrow_history: List[Dict] = []
    
    def add_book(self, title: str, author: str, isbn: str, year: int) -> Book:
        if not title or not title.strip():
            raise ValueError("Название книги не может быть пустым")
        if not author or not author.strip():
            raise ValueError("Автор не может быть пустым")
        if not isbn or not isbn.strip():
            raise ValueError("ISBN не может быть пустым")
        if year <= 0 or year > datetime.now().year + 1:
            raise ValueError("Некорректный год издания")
        
        # Проверка уникальности ISBN
        for book in self.books.values():
            if book.isbn == isbn:
                raise ValueError(f"Книга с ISBN {isbn} уже существует")
        
        book = Book(self._next_book_id, title.strip(), author.strip(), isbn.strip(), year)
        self.books[book.id] = book
        self._next_book_id += 1
        return book
    
    def remove_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if book:
            if not book.is_available:
                raise ValueError("Нельзя удалить книгу, которая выдана читателю")
            del self.books[book_id]
            return True
        return False
    
    def get_book(self, book_id: int) -> Optional[Book]:
        return self.books.get(book_id)
    
    def get_all_books(self) -> List[Book]:
        return list(self.books.values())
    
    def find_books_by_title(self, title: str) -> List[Book]:
        return [book for book in self.books.values() if title.lower() in book.title.lower()]
    
    def find_books_by_author(self, author: str) -> List[Book]:
        return [book for book in self.books.values() if author.lower() in book.author.lower()]
    
    def get_available_books(self) -> List[Book]:
        return [book for book in self.books.values() if book.is_available]
    
    def get_borrowed_books(self) -> List[Book]:
        return [book for book in self.books.values() if not book.is_available]
    
    def register_reader(self, name: str, email: str, phone: str) -> Reader:
        if not name or not name.strip():
            raise ValueError("Имя читателя не может быть пустым")
        if not email or not email.strip():
            raise ValueError("Email не может быть пустым")
        if not phone or not phone.strip():
            raise ValueError("Телефон не может быть пустым")
        
        # Проверка уникальности email
        for reader in self.readers.values():
            if reader.email == email:
                raise ValueError(f"Читатель с email {email} уже зарегистрирован")
        
        reader = Reader(self._next_reader_id, name.strip(), email.strip(), phone.strip())
        self.readers[reader.id] = reader
        self._next_reader_id += 1
        return reader
    
    def remove_reader(self, reader_id: int) -> bool:
        reader = self.get_reader(reader_id)
        if reader:
            if len(reader.borrowed_books) > 0:
                raise ValueError("Нельзя удалить читателя с книгами на руках")
            del self.readers[reader_id]
            return True
        return False
    
    def get_reader(self, reader_id: int) -> Optional[Reader]:
        return self.readers.get(reader_id)
    
    def get_all_readers(self) -> List[Reader]:
        return list(self.readers.values())
    
    def find_readers_by_name(self, name: str) -> List[Reader]:
        return [reader for reader in self.readers.values() if name.lower() in reader.name.lower()]
    
    def checkout_book(self, book_id: int, reader_id: int, days: int = 14) -> bool:
        book = self.get_book(book_id)
        reader = self.get_reader(reader_id)
        
        if not book:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        if not reader:
            raise ValueError(f"Читатель с ID {reader_id} не найден")
        if not book.is_available:
            raise ValueError(f"Книга '{book.title}' уже выдана")
        if len(reader.borrowed_books) >= 5:
            raise ValueError("Читатель не может взять больше 5 книг")
        
        book.check_out(reader_id, days)
        reader.borrow_book(book_id)
        
        self.borrow_history.append({
            'book_id': book_id,
            'reader_id': reader_id,
            'checkout_date': datetime.now(),
            'due_date': book.due_date,
            'return_date': None
        })
        
        return True
    
    def return_book(self, book_id: int, reader_id: int) -> bool:
        book = self.get_book(book_id)
        reader = self.get_reader(reader_id)
        
        if not book:
            raise ValueError(f"Книга с ID {book_id} не найдена")
        if not reader:
            raise ValueError(f"Читатель с ID {reader_id} не найден")
        if book.is_available:
            raise ValueError(f"Книга '{book.title}' не была выдана")
        if book.current_reader_id != reader_id:
            raise ValueError(f"Книга выдана другому читателю")
        
        book.return_book()
        reader.return_book(book_id)
        
        # Обновляем историю
        for record in self.borrow_history:
            if record['book_id'] == book_id and record['reader_id'] == reader_id and record['return_date'] is None:
                record['return_date'] = datetime.now()
                break
        
        return True
    
    def get_reader_books(self, reader_id: int) -> List[Book]:
        reader = self.get_reader(reader_id)
        if not reader:
            return []
        
        return [self.books[book_id] for book_id in reader.borrowed_books if book_id in self.books]
    
    def get_overdue_books(self) -> List[Book]:
        now = datetime.now()
        overdue = []
        for book in self.books.values():
            if not book.is_available and book.due_date and book.due_date < now:
                overdue.append(book)
        return overdue
    
    def get_reader_history(self, reader_id: int) -> List[Dict]:
        return [record for record in self.borrow_history if record['reader_id'] == reader_id]