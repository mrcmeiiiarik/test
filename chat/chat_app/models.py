from datetime import datetime
from typing import List, Optional
from uuid import uuid4

class User:
    """Модель пользователя чата"""
    def __init__(self, name: str):
        self.id = str(uuid4())
        self.name = name
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id
    
    def __repr__(self):
        return f"User(id='{self.id}', name='{self.name}')"


class Message:
    """Модель сообщения"""
    def __init__(self, chat_id: str, sender_id: str, text: str):
        self.id = str(uuid4())
        self.chat_id = chat_id
        self.sender_id = sender_id
        self.text = text
        self.timestamp = datetime.now()
        self.is_deleted = False
        self.edited = False
        self.edit_history: List[str] = []
    
    def edit(self, new_text: str):
        """Редактирование сообщения"""
        self.edit_history.append(self.text)
        self.text = new_text
        self.edited = True
    
    def delete(self):
        """Мягкое удаление сообщения"""
        self.is_deleted = True
    
    def __repr__(self):
        return f"Message(id='{self.id}', chat='{self.chat_id}', text='{self.text[:20]}...')"


class Chat:
    """Модель чата"""
    def __init__(self, participants: List[User]):
        self.id = str(uuid4())
        self.participants = participants.copy()
        self.messages: List[Message] = []
        self.is_active = True
        self.hidden_for_users: List[str] = []  # ID пользователей, скрывших чат
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def add_message(self, message: Message):
        """Добавление сообщения в чат"""
        self.messages.append(message)
        self.last_activity = datetime.now()
    
    def hide_for_user(self, user_id: str):
        """Скрыть чат для пользователя"""
        if user_id not in self.hidden_for_users:
            self.hidden_for_users.append(user_id)
    
    def is_visible_for_user(self, user_id: str) -> bool:
        """Проверка, виден ли чат пользователю"""
        return user_id not in self.hidden_for_users and self.is_active
    
    def get_messages_since(self, timestamp: datetime) -> List[Message]:
        """Получить сообщения после указанной даты"""
        return [msg for msg in self.messages if msg.timestamp > timestamp]
    
    def get_participant_names(self) -> List[str]:
        """Получить имена участников"""
        return [user.name for user in self.participants]
    
    def __repr__(self):
        return f"Chat(id='{self.id}', participants={self.get_participant_names()})"