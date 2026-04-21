from typing import List, Dict, Optional, Tuple
from datetime import datetime

from .models import User, Message, Chat
from .exceptions import (
    PermissionDeniedError, 
    ChatNotFoundError, 
    UserNotFoundError,
    MessageNotFoundError,
    InvalidOperationError
)

class ChatService:
    """Сервис для управления чатами и сообщениями"""
    
    def __init__(self):
        self.chats: Dict[str, Chat] = {}
        self.users: Dict[str, User] = {}
    
    def register_user(self, name: str) -> User:
        """Регистрация нового пользователя"""
        if not name or not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        
        user = User(name.strip())
        self.users[user.id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Получение пользователя по ID"""
        return self.users.get(user_id)
    
    def get_all_users(self) -> List[User]:
        """Получение всех пользователей"""
        return list(self.users.values())
    
    def find_user_by_name(self, name: str) -> Optional[User]:
        """Поиск пользователя по имени"""
        name = name.strip().lower()
        for user in self.users.values():
            if user.name.lower() == name:
                return user
        return None
    
    def create_chat(self, participants: List[User], chat_name: Optional[str] = None) -> Chat:
        """Создание нового чата"""
        if len(participants) < 2:
            raise InvalidOperationError("Чат должен содержать минимум 2 участников")
        

        for user in participants:
            if user.id not in self.users:
                raise UserNotFoundError(f"Пользователь {user.name} не зарегистрирован")
        
        unique_users = {}
        for user in participants:
            unique_users[user.id] = user
        
        if len(unique_users) < len(participants):
            raise InvalidOperationError("Чат не может содержать дубликаты пользователей")
        
        chat = Chat(list(unique_users.values()))
        self.chats[chat.id] = chat
        return chat
    
    def get_chat(self, chat_id: str) -> Chat:
        """Получение чата по ID"""
        chat = self.chats.get(chat_id)
        if not chat:
            raise ChatNotFoundError(f"Чат с ID {chat_id} не найден")
        return chat
    
    def get_user_chats(self, user_id: str) -> List[Chat]:
        user = self.get_user(user_id)
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
        
        visible_chats = []
        for chat in self.chats.values():
            if user in chat.participants and chat.is_visible_for_user(user_id):
                visible_chats.append(chat)
        
        return visible_chats
    

    def send_message(self, chat_id: str, sender_id: str, text: str) -> Message:
        """Отправка сообщения в чат"""
        if not text or not text.strip():
            raise ValueError("Сообщение не может быть пустым")
        
        chat = self.get_chat(chat_id)
        sender = self.get_user(sender_id)
        
        if not sender:
            raise UserNotFoundError(f"Отправитель с ID {sender_id} не найден")
        
  
        if sender not in chat.participants:
            raise PermissionDeniedError("Пользователь не является участником чата")
        

        if not chat.is_active:
            raise InvalidOperationError("Чат неактивен")
        
        message = Message(chat_id, sender_id, text.strip())
        chat.add_message(message)
        return message
    
    def get_messages(self, chat_id: str, user_id: str, include_deleted: bool = False) -> List[Message]:
        """Получение сообщений чата"""
        chat = self.get_chat(chat_id)
        user = self.get_user(user_id)
        
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
 
        if user not in chat.participants:
            raise PermissionDeniedError("Доступ запрещен: пользователь не является участником чата")
        

        if not chat.is_visible_for_user(user_id):
            return []
        
        messages = chat.messages.copy()
        if not include_deleted:
            messages = [msg for msg in messages if not msg.is_deleted]
        
        return messages
    
    def get_messages_since(self, chat_id: str, user_id: str, since: datetime) -> List[Message]:
        """Получение новых сообщений после указанной даты"""
        all_messages = self.get_messages(chat_id, user_id)
        return [msg for msg in all_messages if msg.timestamp > since]
    
    def edit_message(self, chat_id: str, message_id: str, user_id: str, new_text: str) -> Message:
        """Редактирование сообщения"""
        chat = self.get_chat(chat_id)
        user = self.get_user(user_id)
        
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
        
        if user not in chat.participants:
            raise PermissionDeniedError("Доступ запрещен")
        
       
        message = None
        for msg in chat.messages:
            if msg.id == message_id:
                message = msg
                break
        
        if not message:
            raise MessageNotFoundError(f"Сообщение с ID {message_id} не найдено")
        
       
        if message.sender_id != user_id:
            raise PermissionDeniedError("Только автор может редактировать сообщение")
        
        if message.is_deleted:
            raise InvalidOperationError("Нельзя редактировать удаленное сообщение")
        
        message.edit(new_text.strip())
        return message
    
    def delete_message(self, chat_id: str, message_id: str, user_id: str) -> bool:
        """Мягкое удаление сообщения"""
        chat = self.get_chat(chat_id)
        user = self.get_user(user_id)
        
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
        
        if user not in chat.participants:
            raise PermissionDeniedError("Доступ запрещен")
        
        # Поиск сообщения
        message = None
        for msg in chat.messages:
            if msg.id == message_id:
                message = msg
                break
        
        if not message:
            raise MessageNotFoundError(f"Сообщение с ID {message_id} не найдено")
        
        # Только автор может удалить
        if message.sender_id != user_id:
            raise PermissionDeniedError("Только автор может удалить сообщение")
        
        message.delete()
        return True
    
    # --- Управление удалением чатов ---
    def delete_chat_for_user(self, chat_id: str, user_id: str) -> bool:
        """Soft delete - скрытие чата для пользователя"""
        chat = self.get_chat(chat_id)
        user = self.get_user(user_id)
        
        if not user:
            raise UserNotFoundError(f"Пользователь с ID {user_id} не найден")
        
        if user not in chat.participants:
            raise PermissionDeniedError("Пользователь не является участником чата")
        
        chat.hide_for_user(user_id)
        return True
    
    def delete_chat_permanently(self, chat_id: str) -> bool:
        """Hard delete - полное удаление чата"""
        if chat_id not in self.chats:
            raise ChatNotFoundError(f"Чат с ID {chat_id} не найден")
        
        del self.chats[chat_id]
        return True
    
    def deactivate_chat(self, chat_id: str) -> bool:
        """Деактивация чата (без удаления)"""
        chat = self.get_chat(chat_id)
        chat.is_active = False
        return True
    
    def restore_chat(self, chat_id: str) -> bool:
        """Восстановление чата"""
        chat = self.get_chat(chat_id)
        chat.is_active = True
        # Очищаем скрытых пользователей при восстановлении
        chat.hidden_for_users.clear()
        return True
    
    # --- Статистика и утилиты ---
    def get_chat_statistics(self, chat_id: str) -> Dict:
        """Получение статистики чата"""
        chat = self.get_chat(chat_id)
        
        stats = {
            'total_messages': len(chat.messages),
            'active_messages': len([m for m in chat.messages if not m.is_deleted]),
            'deleted_messages': len([m for m in chat.messages if m.is_deleted]),
            'participants_count': len(chat.participants),
            'created_at': chat.created_at,
            'last_activity': chat.last_activity,
            'is_active': chat.is_active
        }
        
        # Статистика по участникам
        user_stats = {}
        for user in chat.participants:
            user_msgs = [m for m in chat.messages if m.sender_id == user.id]
            user_stats[user.name] = {
                'total': len(user_msgs),
                'deleted': len([m for m in user_msgs if m.is_deleted])
            }
        
        stats['user_statistics'] = user_stats
        return stats