import unittest
from blog import BlogAPI


class TestBlogAPI(unittest.TestCase):
    
    def setUp(self):
        self.api = BlogAPI()
    
    def test_1_create_post(self):
        post = self.api.create_post("Мой первый пост", "Содержание поста", "testuser")
        
        self.assertEqual(len(self.api.posts), 1)
        self.assertEqual(post.id, 1)
        self.assertEqual(post.title, "Мой первый пост")
        self.assertEqual(post.content, "Содержание поста")
        self.assertEqual(post.author, "testuser")
        self.assertEqual(len(post.comments), 0)
    
    def test_2_get_post(self):
        self.api.create_post("Пост 1", "Содержание 1", "testuser")
        self.api.create_post("Пост 2", "Содержание 2", "testuser")
        
        post = self.api.get_post(1)
        self.assertIsNotNone(post)
        self.assertEqual(post.title, "Пост 1")
        
        post = self.api.get_post(999)
        self.assertIsNone(post)
    
    def test_3_update_post(self):
        post = self.api.create_post("Старый заголовок", "Старое содержание", "testuser")
        
        result = self.api.update_post(1, "Новый заголовок", "Новое содержание")
        
        self.assertTrue(result)
        self.assertEqual(post.title, "Новый заголовок")
        self.assertEqual(post.content, "Новое содержание")
        
        result = self.api.update_post(999, "Заголовок", "Содержание")
        self.assertFalse(result)
    
    def test_4_delete_post(self):
        self.api.create_post("Пост 1", "Содержание 1", "testuser")
        self.api.create_post("Пост 2", "Содержание 2", "testuser")
        self.api.create_post("Пост 3", "Содержание 3", "testuser")
        
        result = self.api.delete_post(2)
        
        self.assertTrue(result)
        self.assertEqual(len(self.api.posts), 2)
        self.assertIsNone(self.api.get_post(2))
        self.assertIsNotNone(self.api.get_post(1))
        self.assertIsNotNone(self.api.get_post(3))
        
        result = self.api.delete_post(999)
        self.assertFalse(result)
        self.assertEqual(len(self.api.posts), 2)
    
    def test_5_add_comment(self):
        post = self.api.create_post("Пост", "Содержание", "testuser")
        
        comment = self.api.add_comment(1, "reader", "Отличный пост!")
        
        self.assertIsNotNone(comment)
        self.assertEqual(comment.id, 1)
        self.assertEqual(comment.author, "reader")
        self.assertEqual(comment.content, "Отличный пост!")
        self.assertEqual(comment.post_id, 1)
        
        self.assertEqual(len(post.comments), 1)
        self.assertIn(comment, post.comments)
        
        comment2 = self.api.add_comment(1, "another_reader", "Согласен")
        self.assertEqual(comment2.id, 2)
        self.assertEqual(len(post.comments), 2)
    
    def test_6_get_comments(self):
        post = self.api.create_post("Пост", "Содержание", "testuser")
        
        self.api.add_comment(1, "user1", "Коммент 1")
        self.api.add_comment(1, "user2", "Коммент 2")
        
        comments = self.api.get_comments(1)
        
        self.assertEqual(len(comments), 2)
        self.assertEqual(comments[0].author, "user1")
        self.assertEqual(comments[1].author, "user2")
        
        comments = self.api.get_comments(999)
        self.assertEqual(len(comments), 0)
    
    def test_7_delete_comment(self):
        post = self.api.create_post("Пост", "Содержание", "testuser")
        
        self.api.add_comment(1, "user1", "Коммент 1")
        self.api.add_comment(1, "user2", "Коммент 2")
        
        result = self.api.delete_comment(1, 1)
        
        self.assertTrue(result)
        self.assertEqual(len(post.comments), 1)
        self.assertEqual(post.comments[0].author, "user2")
        
        result = self.api.delete_comment(1, 999)
        self.assertFalse(result)
        self.assertEqual(len(post.comments), 1)
        
        result = self.api.delete_comment(999, 1)
        self.assertFalse(result)
    
    def test_8_update_comment(self):
        post = self.api.create_post("Пост", "Содержание", "testuser")
        
        comment = self.api.add_comment(1, "user1", "Старый комментарий")
        
        result = self.api.update_comment(1, 1, "Обновленный комментарий")
        
        self.assertTrue(result)
        self.assertEqual(comment.content, "Обновленный комментарий")
        
        result = self.api.update_comment(1, 999, "Тест")
        self.assertFalse(result)
        
        result = self.api.update_comment(999, 1, "Тест")
        self.assertFalse(result)
    
    def test_9_create_post_empty_title(self):
        with self.assertRaises(ValueError) as context:
            self.api.create_post("   ", "Содержание", "testuser")
        self.assertEqual(str(context.exception), "Заголовок не может быть пустым")
        self.assertEqual(len(self.api.posts), 0)
    
    def test_10_create_post_empty_content(self):
        with self.assertRaises(ValueError) as context:
            self.api.create_post("Заголовок", "   ", "testuser")
        self.assertEqual(str(context.exception), "Содержание не может быть пустым")
        self.assertEqual(len(self.api.posts), 0)
    
    def test_11_add_comment_empty_content(self):
        self.api.create_post("Пост", "Содержание", "testuser")
        
        with self.assertRaises(ValueError) as context:
            self.api.add_comment(1, "user", "   ")
        self.assertEqual(str(context.exception), "Комментарий не может быть пустым")
        
        post = self.api.get_post(1)
        self.assertEqual(len(post.comments), 0)
    
    def test_12_add_comment_to_nonexistent_post(self):
        comment = self.api.add_comment(999, "user", "Комментарий")
        self.assertIsNone(comment)
    
    def test_13_complex_scenario(self):
        post1 = self.api.create_post("Первый пост", "Содержание первого поста", "testuser")
        post2 = self.api.create_post("Второй пост", "Содержание второго поста", "testuser")
        
        self.assertEqual(len(self.api.get_all_posts()), 2)
        
        self.api.add_comment(1, "user1", "Комментарий к первому посту")
        self.api.add_comment(1, "user2", "Еще комментарий")
        self.api.add_comment(2, "user1", "Комментарий ко второму посту")
        
        self.assertEqual(len(post1.comments), 2)
        self.assertEqual(len(post2.comments), 1)
        
        self.api.update_comment(1, 1, "Обновленный комментарий")
        self.assertEqual(post1.comments[0].content, "Обновленный комментарий")
        
        self.api.delete_comment(2, 3)
        self.assertEqual(len(post2.comments), 0)
        
        self.api.update_post(1, "Обновленный заголовок", "Обновленное содержание")
        self.assertEqual(post1.title, "Обновленный заголовок")
        self.assertEqual(post1.content, "Обновленное содержание")
        
        self.api.delete_post(2)
        self.assertEqual(len(self.api.get_all_posts()), 1)
        self.assertIsNone(self.api.get_post(2))
        self.assertIsNotNone(self.api.get_post(1))


if __name__ == '__main__':
    unittest.main()