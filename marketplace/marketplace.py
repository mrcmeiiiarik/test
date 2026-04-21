from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class ProductStatus(Enum):
    ACTIVE = "active"
    SOLD = "sold"
    ARCHIVED = "archived"


class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.id = user_id
        self.username = username
        self.email = email
        self.registered_at = datetime.now()
        self.rating = 0.0
        self.reviews_count = 0


class Review:
    def __init__(self, review_id: int, product_id: int, author_id: int, rating: int, comment: str):
        if rating < 1 or rating > 5:
            raise ValueError("Рейтинг должен быть от 1 до 5")
        
        self.id = review_id
        self.product_id = product_id
        self.author_id = author_id
        self.rating = rating
        self.comment = comment
        self.created_at = datetime.now()
    
    def edit(self, rating: int, comment: str):
        if rating < 1 or rating > 5:
            raise ValueError("Рейтинг должен быть от 1 до 5")
        
        self.rating = rating
        self.comment = comment
        self.updated_at = datetime.now()


class Product:
    def __init__(self, product_id: int, title: str, description: str, price: float, seller_id: int):
        if not title or not title.strip():
            raise ValueError("Название товара не может быть пустым")
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        
        self.id = product_id
        self.title = title.strip()
        self.description = description.strip()
        self.price = price
        self.seller_id = seller_id
        self.status = ProductStatus.ACTIVE
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.reviews: List[Review] = []
        self.views = 0
    
    def update(self, title: str, description: str, price: float):
        if not title or not title.strip():
            raise ValueError("Название товара не может быть пустым")
        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        
        self.title = title.strip()
        self.description = description.strip()
        self.price = price
        self.updated_at = datetime.now()
    
    def change_status(self, status: ProductStatus):
        self.status = status
        self.updated_at = datetime.now()
    
    def add_review(self, review: Review):
        self.reviews.append(review)
    
    def remove_review(self, review_id: int) -> bool:
        for review in self.reviews:
            if review.id == review_id:
                self.reviews.remove(review)
                return True
        return False
    
    def get_average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
    
    def increment_views(self):
        self.views += 1


class Marketplace:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.products: Dict[int, Product] = {}
        self._next_user_id = 1
        self._next_product_id = 1
        self._next_review_id = 1
    
    def register_user(self, username: str, email: str) -> User:
        if not username or not username.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        if not email or not email.strip():
            raise ValueError("Email не может быть пустым")
        
        # Проверка уникальности email
        for user in self.users.values():
            if user.email == email:
                raise ValueError(f"Пользователь с email {email} уже существует")
        
        user = User(self._next_user_id, username.strip(), email.strip())
        self.users[user.id] = user
        self._next_user_id += 1
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[User]:
        return list(self.users.values())
    
    def create_product(self, title: str, description: str, price: float, seller_id: int) -> Product:
        seller = self.get_user(seller_id)
        if not seller:
            raise ValueError(f"Продавец с ID {seller_id} не найден")
        
        product = Product(self._next_product_id, title, description, price, seller_id)
        self.products[product.id] = product
        self._next_product_id += 1
        return product
    
    def get_product(self, product_id: int) -> Optional[Product]:
        product = self.products.get(product_id)
        if product:
            product.increment_views()
        return product
    
    def get_all_products(self) -> List[Product]:
        return list(self.products.values())
    
    def get_products_by_seller(self, seller_id: int) -> List[Product]:
        return [p for p in self.products.values() if p.seller_id == seller_id]
    
    def get_products_by_status(self, status: ProductStatus) -> List[Product]:
        return [p for p in self.products.values() if p.status == status]
    
    def update_product(self, product_id: int, title: str, description: str, price: float) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        
        product.update(title, description, price)
        return True
    
    def delete_product(self, product_id: int) -> bool:
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False
    
    def change_product_status(self, product_id: int, status: ProductStatus) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        
        product.change_status(status)
        return True
    
    def add_review(self, product_id: int, author_id: int, rating: int, comment: str) -> Optional[Review]:
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Товар с ID {product_id} не найден")
        
        author = self.get_user(author_id)
        if not author:
            raise ValueError(f"Пользователь с ID {author_id} не найден")
        
        # Проверка, что автор не является продавцом
        if product.seller_id == author_id:
            raise ValueError("Продавец не может оставлять отзыв на свой товар")
        
        # Проверка, что пользователь уже не оставлял отзыв
        for review in product.reviews:
            if review.author_id == author_id:
                raise ValueError("Вы уже оставили отзыв на этот товар")
        
        review = Review(self._next_review_id, product_id, author_id, rating, comment.strip())
        product.add_review(review)
        self._next_review_id += 1
        
        # Обновляем рейтинг продавца
        self._update_seller_rating(product.seller_id)
        
        return review
    
    def get_reviews(self, product_id: int) -> List[Review]:
        product = self.get_product(product_id)
        if product:
            return product.reviews.copy()
        return []
    
    def update_review(self, product_id: int, review_id: int, rating: int, comment: str) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        
        for review in product.reviews:
            if review.id == review_id:
                review.edit(rating, comment)
                self._update_seller_rating(product.seller_id)
                return True
        return False
    
    def delete_review(self, product_id: int, review_id: int) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        
        result = product.remove_review(review_id)
        if result:
            self._update_seller_rating(product.seller_id)
        return result
    
    def _update_seller_rating(self, seller_id: int):
        seller = self.get_user(seller_id)
        if not seller:
            return
        
        all_reviews = []
        for product in self.get_products_by_seller(seller_id):
            all_reviews.extend(product.reviews)
        
        if all_reviews:
            seller.rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            seller.reviews_count = len(all_reviews)
        else:
            seller.rating = 0.0
            seller.reviews_count = 0
    
    def search_products(self, query: str) -> List[Product]:
        query = query.lower()
        result = []
        
        for product in self.products.values():
            if product.status != ProductStatus.ACTIVE:
                continue
            
            if (query in product.title.lower() or 
                query in product.description.lower()):
                result.append(product)
        
        return result
    
    def get_products_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        return [p for p in self.products.values() 
                if p.status == ProductStatus.ACTIVE and min_price <= p.price <= max_price]
    
    def get_top_rated_products(self, limit: int = 10) -> List[Product]:
        active_products = [p for p in self.products.values() if p.status == ProductStatus.ACTIVE]
        return sorted(active_products, 
                     key=lambda p: p.get_average_rating(), 
                     reverse=True)[:limit]
    
    def get_most_viewed_products(self, limit: int = 10) -> List[Product]:
        active_products = [p for p in self.products.values() if p.status == ProductStatus.ACTIVE]
        return sorted(active_products, 
                     key=lambda p: p.views, 
                     reverse=True)[:limit]