import unittest
import sys
import os
from datetime import datetime


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chat_app import ChatService, User, Chat, Message
from chat_app.exceptions import PermissionDeniedError, ChatNotFoundError, UserNotFoundError

class TestChatApplication(unittest.TestCase):
    """Простой тест для проверки основного функционала чат-приложения"""
    
    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.service = ChatService()
        
   
        self.alice = self.service.register_user("Alice")
        self.bob = self.service.register_user("Bob")
        self.charlie = self.service.register_user("Charlie")
        
  
        self.chat = self.service.create_chat([self.alice, self.bob])
    
    def test_1_user_registration(self):
        """Тест регистрации пользователей"""
        self.assertIsNotNone(self.alice.id)
        self.assertEqual(self.alice.name, "Alice")
        self.assertEqual(self.bob.name, "Bob")
        found_user = self.service.get_user(self.alice.id)
        self.assertEqual(found_user, self.alice)
    
    def test_2_chat_creation(self):
        """Тест создания чата"""
        self.assertIsNotNone(self.chat.id)
        self.assertEqual(len(self.chat.participants), 2)
        self.assertIn(self.alice, self.chat.participants)
        self.assertIn(self.bob, self.chat.participants)
        self.assertTrue(self.chat.is_active)
        self.assertEqual(len(self.chat.messages), 0)
        found_chat = self.service.get_chat(self.chat.id)
        self.assertEqual(found_chat.id, self.chat.id)
    
    def test_3_send_message(self):
        """Тест отправки сообщения"""
        message_text = "Привет, Боб!"
        message = self.service.send_message(self.chat.id, self.alice.id, message_text)
        self.assertIsNotNone(message.id)
        self.assertEqual(message.chat_id, self.chat.id)
        self.assertEqual(message.sender_id, self.alice.id)
        self.assertEqual(message.text, message_text)
        self.assertIsInstance(message.timestamp, datetime)
        chat = self.service.get_chat(self.chat.id)
        self.assertEqual(len(chat.messages), 1)
        self.assertEqual(chat.messages[0].text, message_text)
    
    def test_4_get_messages(self):
        """Тест получения сообщений"""
        self.service.send_message(self.chat.id, self.alice.id, "Сообщение 1")
        self.service.send_message(self.chat.id, self.bob.id, "Сообщение 2")
        self.service.send_message(self.chat.id, self.alice.id, "Сообщение 3")
        messages = self.service.get_messages(self.chat.id, self.bob.id)
        self.assertEqual(len(messages), 3)
        self.assertEqual(messages[0].text, "Сообщение 1")
        self.assertEqual(messages[1].text, "Сообщение 2")
        self.assertEqual(messages[2].text, "Сообщение 3")
    
    def test_5_access_security(self):
        """Тест безопасности доступа"""
        self.service.send_message(self.chat.id, self.alice.id, "Секретное сообщение")
        with self.assertRaises(PermissionDeniedError):
            self.service.get_messages(self.chat.id, self.charlie.id)
        with self.assertRaises(PermissionDeniedError):
            self.service.send_message(self.chat.id, self.charlie.id, "Привет")
    
    def test_6_soft_delete_chat(self):
        """Тест мягкого удаления чата (скрытие)"""
        self.service.send_message(self.chat.id, self.alice.id, "Важное сообщение")
        result = self.service.delete_chat_for_user(self.chat.id, self.alice.id)
        self.assertTrue(result)
        alice_chats = self.service.get_user_chats(self.alice.id)
        bob_chats = self.service.get_user_chats(self.bob.id)
        self.assertNotIn(self.chat, alice_chats)
        self.assertIn(self.chat, bob_chats)
        chat = self.service.get_chat(self.chat.id)
        self.assertEqual(len(chat.messages), 1)
        alice_messages = self.service.get_messages(self.chat.id, self.alice.id)
        self.assertEqual(len(alice_messages), 0)
    
    def test_7_hard_delete_chat(self):
        """Тест полного удаления чата"""
        chat_id = self.chat.id
        result = self.service.delete_chat_permanently(chat_id)
        self.assertTrue(result)
        with self.assertRaises(ChatNotFoundError):
            self.service.get_chat(chat_id)
        alice_chats = self.service.get_user_chats(self.alice.id)
        bob_chats = self.service.get_user_chats(self.bob.id)
        
        self.assertNotIn(self.chat, alice_chats)
        self.assertNotIn(self.chat, bob_chats)
    
    def test_8_delete_message(self):
        """Тест удаления сообщения"""
        msg1 = self.service.send_message(self.chat.id, self.alice.id, "Сообщение 1")
        msg2 = self.service.send_message(self.chat.id, self.alice.id, "Сообщение 2")
        result = self.service.delete_message(self.chat.id, msg1.id, self.alice.id)
        self.assertTrue(result)
        chat = self.service.get_chat(self.chat.id)
        deleted_msg = None
        for msg in chat.messages:
            if msg.id == msg1.id:
                deleted_msg = msg
                break
        
        self.assertIsNotNone(deleted_msg)
        self.assertTrue(deleted_msg.is_deleted)
        messages = self.service.get_messages(self.chat.id, self.bob.id)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].text, "Сообщение 2")
        with self.assertRaises(PermissionDeniedError):
            self.service.delete_message(self.chat.id, msg2.id, self.bob.id)
    
    def test_9_edit_message(self):
        """Тест редактирования сообщения"""
        message = self.service.send_message(self.chat.id, self.alice.id, "Старый текст")
        edited = self.service.edit_message(self.chat.id, message.id, self.alice.id, "Новый текст")
        self.assertEqual(edited.text, "Новый текст")
        self.assertTrue(edited.edited)
        self.assertEqual(len(edited.edit_history), 1)
        self.assertEqual(edited.edit_history[0], "Старый текст")
        with self.assertRaises(PermissionDeniedError):
            self.service.edit_message(self.chat.id, message.id, self.bob.id, "Попытка взлома")
    
    def test_10_chat_statistics(self):
        """Тест статистики чата"""
        self.service.send_message(self.chat.id, self.alice.id, "Сообщение от Алисы 1")
        self.service.send_message(self.chat.id, self.alice.id, "Сообщение от Алисы 2")
        self.service.send_message(self.chat.id, self.bob.id, "Сообщение от Боба")
        
        messages = self.service.get_messages(self.chat.id, self.alice.id)
        self.service.delete_message(self.chat.id, messages[0].id, self.alice.id)
        

        stats = self.service.get_chat_statistics(self.chat.id)
        
    
        self.assertEqual(stats['total_messages'], 3)
        self.assertEqual(stats['active_messages'], 2)
        self.assertEqual(stats['deleted_messages'], 1)
        self.assertEqual(stats['participants_count'], 2)
        self.assertTrue(stats['is_active'])
        

        self.assertEqual(stats['user_statistics']['Alice']['total'], 2)
        self.assertEqual(stats['user_statistics']['Alice']['deleted'], 1)
        self.assertEqual(stats['user_statistics']['Bob']['total'], 1)
        self.assertEqual(stats['user_statistics']['Bob']['deleted'], 0)

if __name__ == '__main__':
 
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChatApplication)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n{'='*50}")
    print(f"Запущено тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Ошибки: {len(result.errors)}")
    print(f"Падения: {len(result.failures)}")