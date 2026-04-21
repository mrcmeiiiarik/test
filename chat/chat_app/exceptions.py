class ChatError(Exception):
    """Базовое исключение для чат-приложения"""
    pass

class PermissionDeniedError(ChatError):
    """Исключение при попытке доступа без прав"""
    pass

class ChatNotFoundError(ChatError):
    """Исключение когда чат не найден"""
    pass

class UserNotFoundError(ChatError):
    """Исключение когда пользователь не найден"""
    pass

class MessageNotFoundError(ChatError):
    """Исключение когда сообщение не найдено"""
    pass

class InvalidOperationError(ChatError):
    """Исключение при недопустимой операции"""
    pass