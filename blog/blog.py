from datetime import datetime
from typing import List, Optional, Dict


class User:
    def __init__(self, user_id: int, username: str, email: str):
        self.id = user_id
        self.username = username
        self.email = email


class Comment:
    def __init__(self, comment_id: int, post_id: int, author: str, content: str):
        self.id = comment_id
        self.post_id = post_id
        self.author = author
        self.content = content
        self.created_at = datetime.now()


class Post:
    def __init__(self, post_id: int, title: str, content: str, author: str):
        self.id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.comments: List[Comment] = []
    
    def add_comment(self, comment: Comment):
        self.comments.append(comment)
    
    def remove_comment(self, comment_id: int) -> bool:
        for comment in self.comments:
            if comment.id == comment_id:
                self.comments.remove(comment)
                return True
        return False
    
    def update(self, title: str, content: str):
        self.title = title
        self.content = content
        self.updated_at = datetime.now()


class BlogAPI:
    def __init__(self):
        self.posts: Dict[int, Post] = {}
        self.users: Dict[int, User] = {}
        self._next_post_id = 1
        self._next_comment_id = 1
        self._next_user_id = 1
        
        # Добавляем тестового пользователя
        self.add_user("testuser", "test@example.com")
    
    def add_user(self, username: str, email: str) -> User:
        user = User(self._next_user_id, username, email)
        self.users[user.id] = user
        self._next_user_id += 1
        return user
    
    def create_post(self, title: str, content: str, author: str) -> Post:
        if not title or not title.strip():
            raise ValueError("Заголовок не может быть пустым")
        if not content or not content.strip():
            raise ValueError("Содержание не может быть пустым")
        
        post = Post(self._next_post_id, title.strip(), content.strip(), author)
        self.posts[post.id] = post
        self._next_post_id += 1
        return post
    
    def get_post(self, post_id: int) -> Optional[Post]:
        return self.posts.get(post_id)
    
    def get_all_posts(self) -> List[Post]:
        return list(self.posts.values())
    
    def update_post(self, post_id: int, title: str, content: str) -> bool:
        post = self.get_post(post_id)
        if post:
            if not title or not title.strip():
                raise ValueError("Заголовок не может быть пустым")
            if not content or not content.strip():
                raise ValueError("Содержание не может быть пустым")
            post.update(title.strip(), content.strip())
            return True
        return False
    
    def delete_post(self, post_id: int) -> bool:
        if post_id in self.posts:
            del self.posts[post_id]
            return True
        return False
    
    def add_comment(self, post_id: int, author: str, content: str) -> Optional[Comment]:
        post = self.get_post(post_id)
        if not post:
            return None
        
        if not content or not content.strip():
            raise ValueError("Комментарий не может быть пустым")
        
        comment = Comment(self._next_comment_id, post_id, author, content.strip())
        post.add_comment(comment)
        self._next_comment_id += 1
        return comment
    
    def get_comments(self, post_id: int) -> List[Comment]:
        post = self.get_post(post_id)
        if post:
            return post.comments.copy()
        return []
    
    def delete_comment(self, post_id: int, comment_id: int) -> bool:
        post = self.get_post(post_id)
        if post:
            return post.remove_comment(comment_id)
        return False
    
    def update_comment(self, post_id: int, comment_id: int, content: str) -> bool:
        post = self.get_post(post_id)
        if not post:
            return False
        
        for comment in post.comments:
            if comment.id == comment_id:
                if not content or not content.strip():
                    raise ValueError("Комментарий не может быть пустым")
                comment.content = content.strip()
                return True
        return False