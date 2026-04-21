import unittest
from marketplace import Marketplace, ProductStatus


class TestMarketplace(unittest.TestCase):
    
    def setUp(self):
        self.market = Marketplace()
        
        # Регистрируем пользователей
        self.seller1 = self.market.register_user("Продавец1", "seller1@mail.com")
        self.seller2 = self.market.register_user("Продавец2", "seller2@mail.com")
        self.buyer1 = self.market.register_user("Покупатель1", "buyer1@mail.com")
        self.buyer2 = self.market.register_user("Покупатель2", "buyer2@mail.com")
    
    def test_1_register_user(self):
        user = self.market.register_user("Новый пользователь", "new@mail.com")
        
        self.assertEqual(len(self.market.users), 5)
        self.assertEqual(user.id, 5)
        self.assertEqual(user.username, "Новый пользователь")
        self.assertEqual(user.email, "new@mail.com")
        self.assertEqual(user.rating, 0.0)
        self.assertEqual(user.reviews_count, 0)
    
    def test_2_register_user_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.market.register_user("", "email@mail.com")
        self.assertEqual(str(context.exception), "Имя пользователя не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.market.register_user("Имя", "")
        self.assertEqual(str(context.exception), "Email не может быть пустым")
    
    def test_3_register_user_duplicate_email(self):
        with self.assertRaises(ValueError) as context:
            self.market.register_user("Другой", "seller1@mail.com")
        self.assertEqual(str(context.exception), "Пользователь с email seller1@mail.com уже существует")
    
    def test_4_get_user(self):
        user = self.market.get_user(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "Продавец1")
        
        user = self.market.get_user(999)
        self.assertIsNone(user)
    
    def test_5_create_product(self):
        product = self.market.create_product(
            "iPhone 13", 
            "Отличный телефон", 
            50000, 
            self.seller1.id
        )
        
        self.assertEqual(len(self.market.products), 1)
        self.assertEqual(product.id, 1)
        self.assertEqual(product.title, "iPhone 13")
        self.assertEqual(product.description, "Отличный телефон")
        self.assertEqual(product.price, 50000)
        self.assertEqual(product.seller_id, self.seller1.id)
        self.assertEqual(product.status, ProductStatus.ACTIVE)
        self.assertEqual(product.views, 0)
        self.assertEqual(len(product.reviews), 0)
        
        product2 = self.market.create_product(
            "Samsung Galaxy", 
            "Хороший телефон", 
            40000, 
            self.seller1.id
        )
        self.assertEqual(product2.id, 2)
        self.assertEqual(len(self.market.products), 2)
    
    def test_6_create_product_invalid_data(self):
        with self.assertRaises(ValueError) as context:
            self.market.create_product("", "Описание", 1000, self.seller1.id)
        self.assertEqual(str(context.exception), "Название товара не может быть пустым")
        
        with self.assertRaises(ValueError) as context:
            self.market.create_product("Товар", "Описание", 0, self.seller1.id)
        self.assertEqual(str(context.exception), "Цена должна быть положительной")
        
        with self.assertRaises(ValueError) as context:
            self.market.create_product("Товар", "Описание", -100, self.seller1.id)
        self.assertEqual(str(context.exception), "Цена должна быть положительной")
    
    def test_7_create_product_invalid_seller(self):
        with self.assertRaises(ValueError) as context:
            self.market.create_product("Товар", "Описание", 1000, 999)
        self.assertEqual(str(context.exception), "Продавец с ID 999 не найден")
    
    def test_8_get_product(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        # Первый просмотр
        retrieved = self.market.get_product(1)
        self.assertEqual(retrieved.views, 1)
        
        # Второй просмотр
        retrieved = self.market.get_product(1)
        self.assertEqual(retrieved.views, 2)
        
        retrieved = self.market.get_product(999)
        self.assertIsNone(retrieved)
    
    def test_9_get_products_by_seller(self):
        self.market.create_product("Товар 1", "Описание 1", 1000, self.seller1.id)
        self.market.create_product("Товар 2", "Описание 2", 2000, self.seller1.id)
        self.market.create_product("Товар 3", "Описание 3", 3000, self.seller2.id)
        
        seller1_products = self.market.get_products_by_seller(self.seller1.id)
        seller2_products = self.market.get_products_by_seller(self.seller2.id)
        
        self.assertEqual(len(seller1_products), 2)
        self.assertEqual(len(seller2_products), 1)
        
        self.assertEqual(seller1_products[0].title, "Товар 1")
        self.assertEqual(seller1_products[1].title, "Товар 2")
        self.assertEqual(seller2_products[0].title, "Товар 3")
    
    def test_10_update_product(self):
        product = self.market.create_product("Старый товар", "Старое описание", 1000, self.seller1.id)
        
        result = self.market.update_product(1, "Новый товар", "Новое описание", 2000)
        
        self.assertTrue(result)
        self.assertEqual(product.title, "Новый товар")
        self.assertEqual(product.description, "Новое описание")
        self.assertEqual(product.price, 2000)
        
        result = self.market.update_product(999, "Тест", "Тест", 1000)
        self.assertFalse(result)
    
    def test_11_change_product_status(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        self.assertEqual(product.status, ProductStatus.ACTIVE)
        
        result = self.market.change_product_status(1, ProductStatus.SOLD)
        
        self.assertTrue(result)
        self.assertEqual(product.status, ProductStatus.SOLD)
        
        result = self.market.change_product_status(999, ProductStatus.ARCHIVED)
        self.assertFalse(result)
    
    def test_12_delete_product(self):
        self.market.create_product("Товар 1", "Описание", 1000, self.seller1.id)
        self.market.create_product("Товар 2", "Описание", 2000, self.seller1.id)
        
        result = self.market.delete_product(1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.market.products), 1)
        self.assertIsNone(self.market.get_product(1))
        self.assertIsNotNone(self.market.get_product(2))
        
        result = self.market.delete_product(999)
        self.assertFalse(result)
        self.assertEqual(len(self.market.products), 1)
    
    def test_13_add_review(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        review = self.market.add_review(1, self.buyer1.id, 5, "Отличный товар!")
        
        self.assertIsNotNone(review)
        self.assertEqual(review.id, 1)
        self.assertEqual(review.product_id, 1)
        self.assertEqual(review.author_id, self.buyer1.id)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Отличный товар!")
        
        self.assertEqual(len(product.reviews), 1)
        self.assertIn(review, product.reviews)
        
        # Проверяем обновление рейтинга продавца
        seller = self.market.get_user(self.seller1.id)
        self.assertEqual(seller.rating, 5.0)
        self.assertEqual(seller.reviews_count, 1)
    
    def test_14_add_review_invalid_rating(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        with self.assertRaises(ValueError) as context:
            self.market.add_review(1, self.buyer1.id, 0, "Комментарий")
        self.assertEqual(str(context.exception), "Рейтинг должен быть от 1 до 5")
        
        with self.assertRaises(ValueError) as context:
            self.market.add_review(1, self.buyer1.id, 6, "Комментарий")
        self.assertEqual(str(context.exception), "Рейтинг должен быть от 1 до 5")
        
        self.assertEqual(len(product.reviews), 0)
    
    def test_15_add_review_seller_cannot_review_own_product(self):
        self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        with self.assertRaises(ValueError) as context:
            self.market.add_review(1, self.seller1.id, 5, "Комментарий")
        self.assertEqual(str(context.exception), "Продавец не может оставлять отзыв на свой товар")
    
    def test_16_add_review_duplicate(self):
        self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        self.market.add_review(1, self.buyer1.id, 5, "Первый отзыв")
        
        with self.assertRaises(ValueError) as context:
            self.market.add_review(1, self.buyer1.id, 4, "Второй отзыв")
        self.assertEqual(str(context.exception), "Вы уже оставили отзыв на этот товар")
    
    def test_17_add_review_invalid_product(self):
        with self.assertRaises(ValueError) as context:
            self.market.add_review(999, self.buyer1.id, 5, "Комментарий")
        self.assertEqual(str(context.exception), "Товар с ID 999 не найден")
    
    def test_18_add_review_invalid_author(self):
        self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        with self.assertRaises(ValueError) as context:
            self.market.add_review(1, 999, 5, "Комментарий")
        self.assertEqual(str(context.exception), "Пользователь с ID 999 не найден")
    
    def test_19_get_reviews(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        self.market.add_review(1, self.buyer1.id, 5, "Отлично")
        self.market.add_review(1, self.buyer2.id, 4, "Хорошо")
        
        reviews = self.market.get_reviews(1)
        
        self.assertEqual(len(reviews), 2)
        self.assertEqual(reviews[0].rating, 5)
        self.assertEqual(reviews[1].rating, 4)
        
        reviews = self.market.get_reviews(999)
        self.assertEqual(len(reviews), 0)
    
    def test_20_update_review(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        review = self.market.add_review(1, self.buyer1.id, 5, "Отличный товар!")
        
        result = self.market.update_review(1, 1, 4, "Хороший, но есть недостатки")
        
        self.assertTrue(result)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Хороший, но есть недостатки")
        
        # Проверяем обновление рейтинга продавца
        seller = self.market.get_user(self.seller1.id)
        self.assertEqual(seller.rating, 4.0)
        
        result = self.market.update_review(1, 999, 5, "Тест")
        self.assertFalse(result)
    
    def test_21_delete_review(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        self.market.add_review(1, self.buyer1.id, 5, "Отлично")
        self.market.add_review(1, self.buyer2.id, 4, "Хорошо")
        
        result = self.market.delete_review(1, 1)
        
        self.assertTrue(result)
        self.assertEqual(len(product.reviews), 1)
        self.assertEqual(product.reviews[0].author_id, self.buyer2.id)
        
        # Проверяем обновление рейтинга продавца
        seller = self.market.get_user(self.seller1.id)
        self.assertEqual(seller.rating, 4.0)
        self.assertEqual(seller.reviews_count, 1)
        
        result = self.market.delete_review(1, 999)
        self.assertFalse(result)
        
        result = self.market.delete_review(999, 1)
        self.assertFalse(result)
    
    def test_22_product_average_rating(self):
        product = self.market.create_product("Товар", "Описание", 1000, self.seller1.id)
        
        self.assertEqual(product.get_average_rating(), 0.0)
        
        self.market.add_review(1, self.buyer1.id, 5, "Отлично")
        self.assertEqual(product.get_average_rating(), 5.0)
        
        self.market.add_review(1, self.buyer2.id, 3, "Нормально")
        self.assertEqual(product.get_average_rating(), 4.0)
    
    def test_23_search_products(self):
        self.market.create_product("iPhone 13", "Новый телефон Apple", 50000, self.seller1.id)
        self.market.create_product("Samsung Galaxy", "Флагман Samsung", 40000, self.seller1.id)
        self.market.create_product("MacBook Pro", "Ноутбук Apple", 100000, self.seller2.id)
        
        # Поиск по слову "Apple"
        results = self.market.search_products("Apple")
        self.assertEqual(len(results), 2)
        
        # Поиск по слову "iPhone"
        results = self.market.search_products("iPhone")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "iPhone 13")
        
        # Поиск по несуществующему слову
        results = self.market.search_products("Xiaomi")
        self.assertEqual(len(results), 0)
    
    def test_24_get_products_by_price_range(self):
        self.market.create_product("Товар 1", "Описание", 1000, self.seller1.id)
        self.market.create_product("Товар 2", "Описание", 2000, self.seller1.id)
        self.market.create_product("Товар 3", "Описание", 3000, self.seller1.id)
        self.market.create_product("Товар 4", "Описание", 4000, self.seller1.id)
        
        results = self.market.get_products_by_price_range(1500, 3500)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].price, 2000)
        self.assertEqual(results[1].price, 3000)
    
    def test_25_get_top_rated_products(self):
        product1 = self.market.create_product("Товар 1", "Описание", 1000, self.seller1.id)
        product2 = self.market.create_product("Товар 2", "Описание", 2000, self.seller1.id)
        product3 = self.market.create_product("Товар 3", "Описание", 3000, self.seller1.id)
        
        self.market.add_review(1, self.buyer1.id, 5, "Отлично")
        self.market.add_review(2, self.buyer1.id, 3, "Нормально")
        self.market.add_review(3, self.buyer1.id, 4, "Хорошо")
        
        top_rated = self.market.get_top_rated_products()
        
        self.assertEqual(len(top_rated), 3)
        self.assertEqual(top_rated[0].id, 1)  # Рейтинг 5
        self.assertEqual(top_rated[1].id, 3)  # Рейтинг 4
        self.assertEqual(top_rated[2].id, 2)  # Рейтинг 3
    
    def test_26_get_most_viewed_products(self):
        product1 = self.market.create_product("Товар 1", "Описание", 1000, self.seller1.id)
        product2 = self.market.create_product("Товар 2", "Описание", 2000, self.seller1.id)
        product3 = self.market.create_product("Товар 3", "Описание", 3000, self.seller1.id)
        
        # Накручиваем просмотры
        for _ in range(5):
            self.market.get_product(1)
        for _ in range(3):
            self.market.get_product(2)
        for _ in range(1):
            self.market.get_product(3)
        
        most_viewed = self.market.get_most_viewed_products()
        
        self.assertEqual(len(most_viewed), 3)
        self.assertEqual(most_viewed[0].id, 1)  # 5 просмотров
        self.assertEqual(most_viewed[1].id, 2)  # 3 просмотра
        self.assertEqual(most_viewed[2].id, 3)  # 1 просмотр
    
    def test_27_get_products_by_status(self):
        product1 = self.market.create_product("Товар 1", "Описание", 1000, self.seller1.id)
        product2 = self.market.create_product("Товар 2", "Описание", 2000, self.seller1.id)
        product3 = self.market.create_product("Товар 3", "Описание", 3000, self.seller1.id)
        
        self.market.change_product_status(2, ProductStatus.SOLD)
        self.market.change_product_status(3, ProductStatus.ARCHIVED)
        
        active = self.market.get_products_by_status(ProductStatus.ACTIVE)
        sold = self.market.get_products_by_status(ProductStatus.SOLD)
        archived = self.market.get_products_by_status(ProductStatus.ARCHIVED)
        
        self.assertEqual(len(active), 1)
        self.assertEqual(len(sold), 1)
        self.assertEqual(len(archived), 1)
        
        self.assertEqual(active[0].id, 1)
        self.assertEqual(sold[0].id, 2)
        self.assertEqual(archived[0].id, 3)
    
    def test_28_complex_scenario(self):
        # Регистрируем нового продавца
        seller = self.market.register_user("TechSeller", "tech@mail.com")
        
        # Создаем товары
        phone = self.market.create_product("iPhone 14", "Новый iPhone", 60000, seller.id)
        laptop = self.market.create_product("MacBook Air", "Ноутбук Apple", 80000, seller.id)
        tablet = self.market.create_product("iPad Pro", "Планшет Apple", 40000, seller.id)
        
        self.assertEqual(len(self.market.get_products_by_seller(seller.id)), 3)
        
        # Покупатели просматривают товары
        for _ in range(10):
            self.market.get_product(phone.id)
        for _ in range(5):
            self.market.get_product(laptop.id)
        
        self.assertEqual(phone.views, 10)
        self.assertEqual(laptop.views, 5)
        
        # Покупатели оставляют отзывы
        self.market.add_review(phone.id, self.buyer1.id, 5, "Отличный телефон!")
        self.market.add_review(phone.id, self.buyer2.id, 4, "Хороший, но дорогой")
        self.market.add_review(laptop.id, self.buyer1.id, 5, "Лучший ноутбук")
        
        # Проверяем рейтинг товаров
        self.assertEqual(phone.get_average_rating(), 4.5)
        self.assertEqual(laptop.get_average_rating(), 5.0)
        self.assertEqual(tablet.get_average_rating(), 0.0)
        
        # Проверяем рейтинг продавца (используем assertAlmostEqual для float)
        updated_seller = self.market.get_user(seller.id)
        self.assertAlmostEqual(updated_seller.rating, 4.666666666666667, places=2)
        self.assertEqual(updated_seller.reviews_count, 3)
        
        # Обновляем товар
        self.market.update_product(phone.id, "iPhone 14 Pro", "Новый iPhone с камерой", 65000)
        self.assertEqual(phone.title, "iPhone 14 Pro")
        self.assertEqual(phone.price, 65000)
        
        # Продаем товар
        self.market.change_product_status(phone.id, ProductStatus.SOLD)
        self.assertEqual(phone.status, ProductStatus.SOLD)
        
        # Удаляем отзыв
        self.market.delete_review(phone.id, 2)  # удаляем отзыв от buyer2
        
        # Проверяем обновление рейтинга
        self.assertEqual(phone.get_average_rating(), 5.0)  # остался только отзыв на 5
        updated_seller = self.market.get_user(seller.id)
        self.assertEqual(updated_seller.rating, 5.0)  # (5+5)/2
        self.assertEqual(updated_seller.reviews_count, 2)
        
        # Поиск товаров
        search_results = self.market.search_products("iPhone")
        self.assertEqual(len(search_results), 0)  # товар продан
        
        search_results = self.market.search_products("MacBook")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].id, laptop.id)


if __name__ == '__main__':
    unittest.main()