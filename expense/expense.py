from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category:
    def __init__(self, category_id: int, name: str, transaction_type: TransactionType):
        self.id = category_id
        self.name = name
        self.type = transaction_type


class Transaction:
    def __init__(self, transaction_id: int, amount: float, category_id: int, description: str = ""):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        self.id = transaction_id
        self.amount = amount
        self.category_id = category_id
        self.description = description
        self.date = datetime.now()
    
    def edit(self, amount: float, category_id: int, description: str):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        self.amount = amount
        self.category_id = category_id
        self.description = description


class ExpenseTracker:
    def __init__(self):
        self.transactions: Dict[int, Transaction] = {}
        self.categories: Dict[int, Category] = {}
        self._next_transaction_id = 1
        self._next_category_id = 1
        
        # Добавляем стандартные категории
        self.add_category("Зарплата", TransactionType.INCOME)
        self.add_category("Фриланс", TransactionType.INCOME)
        self.add_category("Продукты", TransactionType.EXPENSE)
        self.add_category("Транспорт", TransactionType.EXPENSE)
        self.add_category("Развлечения", TransactionType.EXPENSE)
        self.add_category("Коммунальные услуги", TransactionType.EXPENSE)
    
    def add_category(self, name: str, transaction_type: TransactionType) -> Category:
        if not name or not name.strip():
            raise ValueError("Название категории не может быть пустым")
        
        # Проверка на уникальность имени
        for category in self.categories.values():
            if category.name.lower() == name.strip().lower():
                raise ValueError(f"Категория с названием '{name}' уже существует")
        
        category = Category(self._next_category_id, name.strip(), transaction_type)
        self.categories[category.id] = category
        self._next_category_id += 1
        return category
    
    def get_category(self, category_id: int) -> Optional[Category]:
        return self.categories.get(category_id)
    
    def get_all_categories(self) -> List[Category]:
        return list(self.categories.values())
    
    def get_categories_by_type(self, transaction_type: TransactionType) -> List[Category]:
        return [cat for cat in self.categories.values() if cat.type == transaction_type]
    
    def add_transaction(self, amount: float, category_id: int, description: str = "") -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        category = self.get_category(category_id)
        if not category:
            raise ValueError(f"Категория с ID {category_id} не найдена")
        
        transaction = Transaction(self._next_transaction_id, amount, category_id, description.strip())
        self.transactions[transaction.id] = transaction
        self._next_transaction_id += 1
        return transaction
    
    def get_transaction(self, transaction_id: int) -> Optional[Transaction]:
        return self.transactions.get(transaction_id)
    
    def get_all_transactions(self) -> List[Transaction]:
        return list(self.transactions.values())
    
    def update_transaction(self, transaction_id: int, amount: float, category_id: int, description: str) -> bool:
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            return False
        
        category = self.get_category(category_id)
        if not category:
            raise ValueError(f"Категория с ID {category_id} не найдена")
        
        transaction.edit(amount, category_id, description)
        return True
    
    def delete_transaction(self, transaction_id: int) -> bool:
        if transaction_id in self.transactions:
            del self.transactions[transaction_id]
            return True
        return False
    
    def get_transactions_by_category(self, category_id: int) -> List[Transaction]:
        return [t for t in self.transactions.values() if t.category_id == category_id]
    
    def get_transactions_by_type(self, transaction_type: TransactionType) -> List[Transaction]:
        result = []
        for transaction in self.transactions.values():
            category = self.get_category(transaction.category_id)
            if category and category.type == transaction_type:
                result.append(transaction)
        return result
    
    def get_total_income(self) -> float:
        total = 0
        for transaction in self.transactions.values():
            category = self.get_category(transaction.category_id)
            if category and category.type == TransactionType.INCOME:
                total += transaction.amount
        return total
    
    def get_total_expense(self) -> float:
        total = 0
        for transaction in self.transactions.values():
            category = self.get_category(transaction.category_id)
            if category and category.type == TransactionType.EXPENSE:
                total += transaction.amount
        return total
    
    def get_balance(self) -> float:
        return self.get_total_income() - self.get_total_expense()
    
    def get_transactions_by_period(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        return [t for t in self.transactions.values() if start_date <= t.date <= end_date]
    
    def get_statistics_by_category(self) -> Dict[str, float]:
        stats = {}
        for transaction in self.transactions.values():
            category = self.get_category(transaction.category_id)
            if category:
                if category.name not in stats:
                    stats[category.name] = 0
                stats[category.name] += transaction.amount
        return stats
    
    def get_monthly_summary(self, month: int, year: int) -> Dict[str, float]:
        income = 0
        expense = 0
        
        for transaction in self.transactions.values():
            if transaction.date.month == month and transaction.date.year == year:
                category = self.get_category(transaction.category_id)
                if category:
                    if category.type == TransactionType.INCOME:
                        income += transaction.amount
                    else:
                        expense += transaction.amount
        
        return {
            'income': income,
            'expense': expense,
            'balance': income - expense
        }
    
    def clear_all_transactions(self):
        self.transactions.clear()
        self._next_transaction_id = 1