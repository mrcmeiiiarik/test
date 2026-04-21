import unittest
from datetime import datetime, timedelta
from library import Library


class TestLibrary(unittest.TestCase):
    
    def setUp(self):
        self.library = Library("Городская библиотека")
    
    def test_1_add_book(self):
        book = self.library.add_book("Война и мир", "Лев Толстой", "978-5-17-123456-7", 1869)
        
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Война и мир")
        self.assertEqual(book.author, "Лев Толстой")
        self.assertEqual(book.isbn, "978-5-17-123456-7")
        self.assertEqual(book.year, 1869)
        self.assertTrue(book.is_available)
        self.assertIsNone(book.current_reader_id)
        
        book2 = self.library.add_book("Преступление и наказание", "Ф. Достоевский", "978-5-17-765432-1", 1866)
        self.assertEqual(book2.id, 2)
        self.assertEqual(len(self.library.books), 2)
    
    def test_2_add_book_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.library.add_book("", "Автор", "123", 2000)
        self.assertEqual(str(context.exception), "Название книги не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Книга", "", "123", 2000)
        self.assertEqual(str(context.exception), "Автор не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Книга", "Автор", "", 2000)
        self.assertEqual(str(context.exception), "ISBN не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Книга", "Автор", "123", -5)
        self.assertEqual(str(context.exception), "Некорректный год издания")
        
        self.assertEqual(len(self.library.books), 0)
    
    def test_3_add_book_duplicate_isbn(self):
        self.library.add_book("Книга 1", "Автор 1", "978-5-17-123456-7", 2000)
        
        with self.assertRaises(ValueError) as context:
            self.library.add_book("Книга 2", "Автор 2", "978-5-17-123456-7", 2001)
        self.assertEqual(str(context.exception), "Книга с ISBN 978-5-17-123456-7 уже существует")
        
        self.assertEqual(len(self.library.books), 1)
    
    def test_4_get_book(self):
        self.library.add_book("Книга 1", "Автор 1", "111", 2000)
        self.library.add_book("Книга 2", "Автор 2", "222", 2001)
        
        book = self.library.get_book(1)
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Книга 1")
        
        book = self.library.get_book(999)
        self.assertIsNone(book)
    
    def test_5_find_books_by_title(self):
        self.library.add_book("Война и мир", "Толстой", "111", 1869)
        self.library.add_book("Война миров", "Уэллс", "222", 1898)
        self.library.add_book("Преступление и наказание", "Достоевский", "333", 1866)
        
        # Поиск по слову "Война"
        books = self.library.find_books_by_title("Война")
        self.assertEqual(len(books), 2)
        
        # Поиск по слову "мир"
        books = self.library.find_books_by_title("мир")
        self.assertEqual(len(books), 2)  # Изменил с 1 на 2, потому что "мир" есть и в "Война и мир" и в "Война миров"
        
        # Поиск по точному названию
        books = self.library.find_books_by_title("Война и мир")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].author, "Толстой")
        
        books = self.library.find_books_by_title("несуществующее")
        self.assertEqual(len(books), 0)
    
    def test_6_find_books_by_author(self):
        self.library.add_book("Война и мир", "Лев Толстой", "111", 1869)
        self.library.add_book("Анна Каренина", "Лев Толстой", "222", 1877)
        self.library.add_book("Идиот", "Федор Достоевский", "333", 1869)
        
        books = self.library.find_books_by_author("толстой")
        self.assertEqual(len(books), 2)
        
        books = self.library.find_books_by_author("достоевский")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Идиот")
        
        books = self.library.find_books_by_author("пушкин")
        self.assertEqual(len(books), 0)
    
    def test_7_remove_book(self):
        self.library.add_book("Книга 1", "Автор 1", "111", 2000)
        self.library.add_book("Книга 2", "Автор 2", "222", 2001)
        
        result = self.library.remove_book(1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.library.books), 1)
        self.assertIsNone(self.library.get_book(1))
        self.assertIsNotNone(self.library.get_book(2))
        
        result = self.library.remove_book(999)
        self.assertFalse(result)
        self.assertEqual(len(self.library.books), 1)
    
    def test_8_remove_book_borrowed(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        reader = self.library.register_reader("Иван", "ivan@mail.com", "+123456789")
        
        self.library.checkout_book(1, 1)
        
        with self.assertRaises(ValueError) as context:
            self.library.remove_book(1)
        self.assertEqual(str(context.exception), "Нельзя удалить книгу, которая выдана читателю")
        
        self.assertEqual(len(self.library.books), 1)
    
    def test_9_register_reader(self):
        reader = self.library.register_reader("Иван Петров", "ivan@mail.com", "+7-123-456-78-90")
        
        self.assertEqual(len(self.library.readers), 1)
        self.assertEqual(reader.id, 1)
        self.assertEqual(reader.name, "Иван Петров")
        self.assertEqual(reader.email, "ivan@mail.com")
        self.assertEqual(reader.phone, "+7-123-456-78-90")
        self.assertEqual(len(reader.borrowed_books), 0)
        
        reader2 = self.library.register_reader("Мария Сидорова", "maria@mail.com", "+7-987-654-32-10")
        self.assertEqual(reader2.id, 2)
        self.assertEqual(len(self.library.readers), 2)
    
    def test_10_register_reader_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.library.register_reader("", "email@mail.com", "123")
        self.assertEqual(str(context.exception), "Имя читателя не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.library.register_reader("Иван", "", "123")
        self.assertEqual(str(context.exception), "Email не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.library.register_reader("Иван", "email@mail.com", "")
        self.assertEqual(str(context.exception), "Телефон не может быть пустым")
        
        self.assertEqual(len(self.library.readers), 0)
    
    def test_11_register_reader_duplicate_email(self):
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        with self.assertRaises(ValueError) as context:
            self.library.register_reader("Петр", "ivan@mail.com", "456")
        self.assertEqual(str(context.exception), "Читатель с email ivan@mail.com уже зарегистрирован")
        
        self.assertEqual(len(self.library.readers), 1)
    
    def test_12_get_reader(self):
        self.library.register_reader("Иван", "ivan@mail.com", "111")
        self.library.register_reader("Мария", "maria@mail.com", "222")
        
        reader = self.library.get_reader(1)
        self.assertIsNotNone(reader)
        self.assertEqual(reader.name, "Иван")
        
        reader = self.library.get_reader(999)
        self.assertIsNone(reader)
    
    def test_13_find_readers_by_name(self):
        self.library.register_reader("Иван Петров", "ivan@mail.com", "111")
        self.library.register_reader("Иван Сидоров", "ivan2@mail.com", "222")
        self.library.register_reader("Мария Иванова", "maria@mail.com", "333")
        
        # Поиск по имени "Иван" - должно найти 2 читателей (Иван Петров и Иван Сидоров)
        readers = self.library.find_readers_by_name("Иван")
        self.assertEqual(len(readers), 2)
        
        # Поиск по фамилии "Петров"
        readers = self.library.find_readers_by_name("Петров")
        self.assertEqual(len(readers), 1)
        self.assertEqual(readers[0].email, "ivan@mail.com")
        
        # Поиск по фамилии "Иванова" - должно найти 1 читателя (Мария Иванова)
        readers = self.library.find_readers_by_name("Иванова")
        self.assertEqual(len(readers), 1)
        self.assertEqual(readers[0].name, "Мария Иванова")
        
        readers = self.library.find_readers_by_name("кузнецов")
        self.assertEqual(len(readers), 0)
    
    def test_14_remove_reader(self):
        self.library.register_reader("Иван", "ivan@mail.com", "111")
        self.library.register_reader("Мария", "maria@mail.com", "222")
        
        result = self.library.remove_reader(1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.library.readers), 1)
        self.assertIsNone(self.library.get_reader(1))
        self.assertIsNotNone(self.library.get_reader(2))
        
        result = self.library.remove_reader(999)
        self.assertFalse(result)
        self.assertEqual(len(self.library.readers), 1)
    
    def test_15_remove_reader_with_books(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        self.library.checkout_book(1, 1)
        
        with self.assertRaises(ValueError) as context:
            self.library.remove_reader(1)
        self.assertEqual(str(context.exception), "Нельзя удалить читателя с книгами на руках")
        
        self.assertEqual(len(self.library.readers), 1)
    
    def test_16_checkout_book(self):
        self.library.add_book("Война и мир", "Толстой", "111", 1869)
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        result = self.library.checkout_book(1, 1)
        
        self.assertTrue(result)
        
        book = self.library.get_book(1)
        reader = self.library.get_reader(1)
        
        self.assertFalse(book.is_available)
        self.assertEqual(book.current_reader_id, 1)
        self.assertIsNotNone(book.due_date)
        self.assertIn(1, reader.borrowed_books)
        
        self.assertEqual(len(self.library.borrow_history), 1)
    
    def test_17_checkout_book_not_found(self):
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        with self.assertRaises(ValueError) as context:
            self.library.checkout_book(999, 1)
        self.assertEqual(str(context.exception), "Книга с ID 999 не найдена")
    
    def test_18_checkout_reader_not_found(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        
        with self.assertRaises(ValueError) as context:
            self.library.checkout_book(1, 999)
        self.assertEqual(str(context.exception), "Читатель с ID 999 не найден")
    
    def test_19_checkout_already_borrowed(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        self.library.checkout_book(1, 1)
        
        self.library.register_reader("Петр", "petr@mail.com", "456")
        
        with self.assertRaises(ValueError) as context:
            self.library.checkout_book(1, 2)
        self.assertEqual(str(context.exception), "Книга 'Книга' уже выдана")
    
    def test_20_checkout_max_books_limit(self):
        self.library.add_book("Книга 1", "Автор", "111", 2000)
        self.library.add_book("Книга 2", "Автор", "222", 2001)
        self.library.add_book("Книга 3", "Автор", "333", 2002)
        self.library.add_book("Книга 4", "Автор", "444", 2003)
        self.library.add_book("Книга 5", "Автор", "555", 2004)
        self.library.add_book("Книга 6", "Автор", "666", 2005)
        
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        for i in range(1, 6):
            self.library.checkout_book(i, 1)
        
        with self.assertRaises(ValueError) as context:
            self.library.checkout_book(6, 1)
        self.assertEqual(str(context.exception), "Читатель не может взять больше 5 книг")
    
    def test_21_return_book(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        self.library.checkout_book(1, 1)
        
        result = self.library.return_book(1, 1)
        
        self.assertTrue(result)
        
        book = self.library.get_book(1)
        reader = self.library.get_reader(1)
        
        self.assertTrue(book.is_available)
        self.assertIsNone(book.current_reader_id)
        self.assertIsNone(book.due_date)
        self.assertNotIn(1, reader.borrowed_books)
        
        for record in self.library.borrow_history:
            if record['book_id'] == 1:
                self.assertIsNotNone(record['return_date'])
    
    def test_22_return_book_not_found(self):
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        with self.assertRaises(ValueError) as context:
            self.library.return_book(999, 1)
        self.assertEqual(str(context.exception), "Книга с ID 999 не найдена")
    
    def test_23_return_book_reader_not_found(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        
        with self.assertRaises(ValueError) as context:
            self.library.return_book(1, 999)
        self.assertEqual(str(context.exception), "Читатель с ID 999 не найден")
    
    def test_24_return_book_not_borrowed(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        with self.assertRaises(ValueError) as context:
            self.library.return_book(1, 1)
        self.assertEqual(str(context.exception), "Книга 'Книга' не была выдана")
    
    def test_25_return_book_wrong_reader(self):
        self.library.add_book("Книга", "Автор", "111", 2000)
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        self.library.register_reader("Петр", "petr@mail.com", "456")
        
        self.library.checkout_book(1, 1)
        
        with self.assertRaises(ValueError) as context:
            self.library.return_book(1, 2)
        self.assertEqual(str(context.exception), "Книга выдана другому читателю")
    
    def test_26_get_reader_books(self):
        self.library.add_book("Книга 1", "Автор", "111", 2000)
        self.library.add_book("Книга 2", "Автор", "222", 2001)
        self.library.add_book("Книга 3", "Автор", "333", 2002)
        
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        self.library.checkout_book(1, 1)
        self.library.checkout_book(2, 1)
        
        books = self.library.get_reader_books(1)
        
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].title, "Книга 1")
        self.assertEqual(books[1].title, "Книга 2")
        
        books = self.library.get_reader_books(999)
        self.assertEqual(len(books), 0)
    
    def test_27_get_available_books(self):
        self.library.add_book("Книга 1", "Автор", "111", 2000)
        self.library.add_book("Книга 2", "Автор", "222", 2001)
        self.library.add_book("Книга 3", "Автор", "333", 2002)
        
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        self.library.checkout_book(1, 1)
        
        available = self.library.get_available_books()
        borrowed = self.library.get_borrowed_books()
        
        self.assertEqual(len(available), 2)
        self.assertEqual(len(borrowed), 1)
        self.assertEqual(borrowed[0].title, "Книга 1")
    
    def test_28_get_overdue_books(self):
        self.library.add_book("Книга 1", "Автор", "111", 2000)
        self.library.add_book("Книга 2", "Автор", "222", 2001)
        
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        
        self.library.checkout_book(1, 1, days=-1)
        
        overdue = self.library.get_overdue_books()
        
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0].title, "Книга 1")
    
    def test_29_get_reader_history(self):
        self.library.add_book("Книга 1", "Автор", "111", 2000)
        self.library.add_book("Книга 2", "Автор", "222", 2001)
        
        self.library.register_reader("Иван", "ivan@mail.com", "123")
        self.library.register_reader("Мария", "maria@mail.com", "456")
        
        self.library.checkout_book(1, 1)
        self.library.checkout_book(2, 2)
        self.library.return_book(1, 1)
        
        history = self.library.get_reader_history(1)
        
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['book_id'], 1)
        self.assertIsNotNone(history[0]['return_date'])
        
        history = self.library.get_reader_history(2)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['book_id'], 2)
        self.assertIsNone(history[0]['return_date'])
        
        history = self.library.get_reader_history(999)
        self.assertEqual(len(history), 0)
    
    def test_30_complex_scenario(self):
        self.library.add_book("Мастер и Маргарита", "Булгаков", "978-5-17-111111-1", 1967)
        self.library.add_book("Собачье сердце", "Булгаков", "978-5-17-222222-2", 1925)
        self.library.add_book("Идиот", "Достоевский", "978-5-17-333333-3", 1869)
        
        self.assertEqual(len(self.library.get_all_books()), 3)
        
        reader1 = self.library.register_reader("Алексей Иванов", "aleksey@mail.com", "+7-111-111-11-11")
        reader2 = self.library.register_reader("Елена Петрова", "elena@mail.com", "+7-222-222-22-22")
        
        self.assertEqual(len(self.library.get_all_readers()), 2)
        
        self.library.checkout_book(1, 1)
        self.library.checkout_book(2, 1)
        self.library.checkout_book(3, 2)
        
        self.assertEqual(len(self.library.get_reader_books(1)), 2)
        self.assertEqual(len(self.library.get_reader_books(2)), 1)
        
        self.assertEqual(len(self.library.get_available_books()), 0)
        self.assertEqual(len(self.library.get_borrowed_books()), 3)
        
        self.library.return_book(1, 1)
        
        self.assertEqual(len(self.library.get_reader_books(1)), 1)
        self.assertEqual(len(self.library.get_available_books()), 1)
        self.assertEqual(len(self.library.get_borrowed_books()), 2)
        
        available_books = self.library.get_available_books()
        self.assertEqual(available_books[0].title, "Мастер и Маргарита")
        
        self.library.checkout_book(1, 2)
        
        self.assertEqual(len(self.library.get_reader_books(2)), 2)
        self.assertEqual(len(self.library.get_borrowed_books()), 3)
        
        history1 = self.library.get_reader_history(1)
        history2 = self.library.get_reader_history(2)
        
        self.assertEqual(len(history1), 2)
        self.assertEqual(len(history2), 2)
        
        self.library.return_book(2, 1)
        self.library.return_book(3, 2)
        self.library.return_book(1, 2)
        
        self.assertEqual(len(self.library.get_available_books()), 3)
        self.assertEqual(len(self.library.get_borrowed_books()), 0)


if __name__ == '__main__':
    unittest.main()