import unittest
from datetime import datetime, timedelta
from expense import ExpenseTracker, TransactionType


class TestExpenseTracker(unittest.TestCase):
    
    def setUp(self):
        self.tracker = ExpenseTracker()
    
    def test_1_add_category(self):
        category = self.tracker.add_category("Кафе", TransactionType.EXPENSE)
        
        self.assertEqual(len(self.tracker.categories), 7)  # 6 стандартных + 1 новая
        self.assertEqual(category.id, 7)
        self.assertEqual(category.name, "Кафе")
        self.assertEqual(category.type, TransactionType.EXPENSE)
        
        category2 = self.tracker.add_category("Подарки", TransactionType.EXPENSE)
        self.assertEqual(category2.id, 8)
        self.assertEqual(len(self.tracker.categories), 8)
    
    def test_2_add_category_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.tracker.add_category("", TransactionType.EXPENSE)
        self.assertEqual(str(context.exception), "Название категории не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.tracker.add_category("   ", TransactionType.INCOME)
        self.assertEqual(str(context.exception), "Название категории не может быть пустым")
    
    def test_3_add_category_duplicate(self):
        with self.assertRaises(ValueError) as context:
            self.tracker.add_category("Зарплата", TransactionType.INCOME)
        self.assertEqual(str(context.exception), "Категория с названием 'Зарплата' уже существует")
    
    def test_4_get_category(self):
        category = self.tracker.get_category(1)  # Зарплата
        self.assertIsNotNone(category)
        self.assertEqual(category.name, "Зарплата")
        self.assertEqual(category.type, TransactionType.INCOME)
        
        category = self.tracker.get_category(999)
        self.assertIsNone(category)
    
    def test_5_get_categories_by_type(self):
        income_categories = self.tracker.get_categories_by_type(TransactionType.INCOME)
        expense_categories = self.tracker.get_categories_by_type(TransactionType.EXPENSE)
        
        self.assertEqual(len(income_categories), 2)  # Зарплата, Фриланс
        self.assertEqual(len(expense_categories), 4)  # Продукты, Транспорт, Развлечения, Коммунальные
        
        self.assertEqual(income_categories[0].name, "Зарплата")
        self.assertEqual(income_categories[1].name, "Фриланс")
    
    def test_6_add_transaction(self):
        transaction = self.tracker.add_transaction(5000, 1, "Зарплата за январь")
        
        self.assertEqual(len(self.tracker.transactions), 1)
        self.assertEqual(transaction.id, 1)
        self.assertEqual(transaction.amount, 5000)
        self.assertEqual(transaction.category_id, 1)
        self.assertEqual(transaction.description, "Зарплата за январь")
        self.assertIsNotNone(transaction.date)
        
        transaction2 = self.tracker.add_transaction(300, 3, "Продукты в Пятерочке")
        self.assertEqual(transaction2.id, 2)
        self.assertEqual(len(self.tracker.transactions), 2)
    
    def test_7_add_transaction_invalid_amount(self):
        with self.assertRaises(ValueError) as context:
            self.tracker.add_transaction(0, 1)
        self.assertEqual(str(context.exception), "Сумма должна быть положительной")
        
        with self.assertRaises(ValueError) as context:
            self.tracker.add_transaction(-100, 1)
        self.assertEqual(str(context.exception), "Сумма должна быть положительной")
        
        self.assertEqual(len(self.tracker.transactions), 0)
    
    def test_8_add_transaction_invalid_category(self):
        with self.assertRaises(ValueError) as context:
            self.tracker.add_transaction(1000, 999)
        self.assertEqual(str(context.exception), "Категория с ID 999 не найдена")
        
        self.assertEqual(len(self.tracker.transactions), 0)
    
    def test_9_get_transaction(self):
        self.tracker.add_transaction(5000, 1)
        self.tracker.add_transaction(300, 3)
        
        transaction = self.tracker.get_transaction(1)
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, 5000)
        
        transaction = self.tracker.get_transaction(999)
        self.assertIsNone(transaction)
    
    def test_10_update_transaction(self):
        transaction = self.tracker.add_transaction(5000, 1, "Старая зарплата")
        
        result = self.tracker.update_transaction(1, 5500, 2, "Новая зарплата с фрилансом")
        
        self.assertTrue(result)
        self.assertEqual(transaction.amount, 5500)
        self.assertEqual(transaction.category_id, 2)
        self.assertEqual(transaction.description, "Новая зарплата с фрилансом")
        
        result = self.tracker.update_transaction(999, 1000, 1, "Тест")
        self.assertFalse(result)
    
    def test_11_update_transaction_invalid_category(self):
        self.tracker.add_transaction(5000, 1)
        
        with self.assertRaises(ValueError) as context:
            self.tracker.update_transaction(1, 1000, 999, "Тест")
        self.assertEqual(str(context.exception), "Категория с ID 999 не найдена")
    
    def test_12_delete_transaction(self):
        self.tracker.add_transaction(5000, 1)
        self.tracker.add_transaction(300, 3)
        self.tracker.add_transaction(200, 4)
        
        result = self.tracker.delete_transaction(2)
        
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.transactions), 2)
        self.assertIsNone(self.tracker.get_transaction(2))
        self.assertIsNotNone(self.tracker.get_transaction(1))
        self.assertIsNotNone(self.tracker.get_transaction(3))
        
        result = self.tracker.delete_transaction(999)
        self.assertFalse(result)
        self.assertEqual(len(self.tracker.transactions), 2)
    
    def test_13_get_transactions_by_category(self):
        self.tracker.add_transaction(5000, 1)
        self.tracker.add_transaction(300, 3)
        self.tracker.add_transaction(200, 3)
        self.tracker.add_transaction(100, 4)
        
        transactions = self.tracker.get_transactions_by_category(3)
        
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].amount, 300)
        self.assertEqual(transactions[1].amount, 200)
        
        transactions = self.tracker.get_transactions_by_category(999)
        self.assertEqual(len(transactions), 0)
    
    def test_14_get_transactions_by_type(self):
        self.tracker.add_transaction(5000, 1)  # income
        self.tracker.add_transaction(3000, 2)  # income
        self.tracker.add_transaction(300, 3)   # expense
        self.tracker.add_transaction(200, 4)   # expense
        self.tracker.add_transaction(150, 5)   # expense
        
        income = self.tracker.get_transactions_by_type(TransactionType.INCOME)
        expense = self.tracker.get_transactions_by_type(TransactionType.EXPENSE)
        
        self.assertEqual(len(income), 2)
        self.assertEqual(len(expense), 3)
        
        self.assertEqual(income[0].amount, 5000)
        self.assertEqual(income[1].amount, 3000)
        
        total_income = sum(t.amount for t in income)
        total_expense = sum(t.amount for t in expense)
        
        self.assertEqual(total_income, 8000)
        self.assertEqual(total_expense, 650)
    
    def test_15_get_total_income_and_expense(self):
        self.tracker.add_transaction(10000, 1)  # income
        self.tracker.add_transaction(5000, 2)   # income
        self.tracker.add_transaction(500, 3)    # expense
        self.tracker.add_transaction(300, 4)    # expense
        self.tracker.add_transaction(200, 5)    # expense
        self.tracker.add_transaction(100, 6)    # expense
        
        total_income = self.tracker.get_total_income()
        total_expense = self.tracker.get_total_expense()
        balance = self.tracker.get_balance()
        
        self.assertEqual(total_income, 15000)
        self.assertEqual(total_expense, 1100)
        self.assertEqual(balance, 13900)
    
    def test_16_get_statistics_by_category(self):
        self.tracker.add_transaction(10000, 1)  # Зарплата
        self.tracker.add_transaction(5000, 2)   # Фриланс
        self.tracker.add_transaction(500, 3)    # Продукты
        self.tracker.add_transaction(300, 3)    # Продукты
        self.tracker.add_transaction(200, 4)    # Транспорт
        self.tracker.add_transaction(1000, 5)   # Развлечения
        
        stats = self.tracker.get_statistics_by_category()
        
        self.assertEqual(stats['Зарплата'], 10000)
        self.assertEqual(stats['Фриланс'], 5000)
        self.assertEqual(stats['Продукты'], 800)
        self.assertEqual(stats['Транспорт'], 200)
        self.assertEqual(stats['Развлечения'], 1000)
        self.assertEqual(len(stats), 5)
    
    def test_17_get_transactions_by_period(self):
        # Создаем транзакции с разными датами
        transaction1 = self.tracker.add_transaction(1000, 1)
        transaction1.date = datetime.now() - timedelta(days=5)
        
        transaction2 = self.tracker.add_transaction(2000, 1)
        transaction2.date = datetime.now() - timedelta(days=3)
        
        transaction3 = self.tracker.add_transaction(300, 3)
        transaction3.date = datetime.now() - timedelta(days=1)
        
        start_date = datetime.now() - timedelta(days=4)
        end_date = datetime.now()
        
        transactions = self.tracker.get_transactions_by_period(start_date, end_date)
        
        self.assertEqual(len(transactions), 2)  # только транзакции 2 и 3
        self.assertIn(transaction2, transactions)
        self.assertIn(transaction3, transactions)
        self.assertNotIn(transaction1, transactions)
    
    def test_18_get_monthly_summary(self):
        now = datetime.now()
        
        transaction1 = self.tracker.add_transaction(10000, 1)  # income
        transaction1.date = datetime(now.year, now.month, 5)
        
        transaction2 = self.tracker.add_transaction(5000, 2)   # income
        transaction2.date = datetime(now.year, now.month, 10)
        
        transaction3 = self.tracker.add_transaction(500, 3)    # expense
        transaction3.date = datetime(now.year, now.month, 15)
        
        transaction4 = self.tracker.add_transaction(300, 4)    # expense
        transaction4.date = datetime(now.year, now.month, 20)
        
        # Транзакция в другом месяце
        transaction5 = self.tracker.add_transaction(1000, 1)
        prev_month = now.month - 1 if now.month > 1 else 12
        prev_year = now.year if now.month > 1 else now.year - 1
        transaction5.date = datetime(prev_year, prev_month, 10)
        
        summary = self.tracker.get_monthly_summary(now.month, now.year)
        
        self.assertEqual(summary['income'], 15000)
        self.assertEqual(summary['expense'], 800)
        self.assertEqual(summary['balance'], 14200)
    
    def test_19_clear_all_transactions(self):
        self.tracker.add_transaction(1000, 1)
        self.tracker.add_transaction(2000, 1)
        self.tracker.add_transaction(300, 3)
        
        self.assertEqual(len(self.tracker.transactions), 3)
        
        self.tracker.clear_all_transactions()
        
        self.assertEqual(len(self.tracker.transactions), 0)
        self.assertIsNone(self.tracker.get_transaction(1))
    
    def test_20_complex_scenario(self):
        # Добавляем доходы
        self.tracker.add_transaction(50000, 1, "Зарплата за январь")
        self.tracker.add_transaction(10000, 2, "Фриланс проект")
        
        # Добавляем расходы
        self.tracker.add_transaction(3000, 3, "Продукты")
        self.tracker.add_transaction(1000, 4, "Такси")
        self.tracker.add_transaction(2000, 5, "Кино и ресторан")
        self.tracker.add_transaction(4000, 6, "Квартплата")
        
        self.assertEqual(len(self.tracker.transactions), 6)
        
        # Проверяем баланс
        self.assertEqual(self.tracker.get_total_income(), 60000)
        self.assertEqual(self.tracker.get_total_expense(), 10000)
        self.assertEqual(self.tracker.get_balance(), 50000)
        
        # Добавляем новую категорию
        self.tracker.add_category("Здоровье", TransactionType.EXPENSE)
        
        # Добавляем транзакцию в новую категорию
        self.tracker.add_transaction(1500, 7, "Аптека")
        
        self.assertEqual(self.tracker.get_total_expense(), 11500)
        self.assertEqual(self.tracker.get_balance(), 48500)
        
        # Обновляем транзакцию
        self.tracker.update_transaction(3, 3500, 3, "Продукты и бытовая химия")
        
        self.assertEqual(self.tracker.get_total_expense(), 12000)
        self.assertEqual(self.tracker.get_balance(), 48000)
        
        # Удаляем транзакцию
        self.tracker.delete_transaction(5)  # удаляем развлечения
        
        self.assertEqual(len(self.tracker.transactions), 6)
        self.assertEqual(self.tracker.get_total_expense(), 10000)
        self.assertEqual(self.tracker.get_balance(), 50000)
        
        # Проверяем статистику по категориям
        stats = self.tracker.get_statistics_by_category()
        self.assertEqual(stats['Зарплата'], 50000)
        self.assertEqual(stats['Фриланс'], 10000)
        self.assertEqual(stats['Продукты'], 3500)
        self.assertEqual(stats['Транспорт'], 1000)
        self.assertEqual(stats['Коммунальные услуги'], 4000)
        self.assertEqual(stats['Здоровье'], 1500)


if __name__ == '__main__':
    unittest.main()