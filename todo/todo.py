from datetime import datetime
from typing import List, Optional


class Task:
    """Класс задачи"""
    
    def __init__(self, task_id: int, title: str, description: str = ""):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now()
    
    def mark_completed(self):
        self.completed = True
    
    def mark_uncompleted(self):
        self.completed = False
    
    def edit(self, title: str, description: str):
        self.title = title
        self.description = description


class TaskManager:
    """Класс для управления задачами"""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1
    
    def add_task(self, title: str, description: str = "") -> Task:
        if not title or not title.strip():
            raise ValueError("Название задачи не может быть пустым")
        
        task = Task(self._next_id, title.strip(), description.strip())
        self.tasks.append(task)
        self._next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        return self.tasks.copy()
    
    def update_task(self, task_id: int, title: str, description: str) -> bool:
        task = self.get_task(task_id)
        if task:
            if not title or not title.strip():
                raise ValueError("Название задачи не может быть пустым")
            task.edit(title.strip(), description.strip())
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
    
    def mark_completed(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            return True
        return False
    
    def mark_uncompleted(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if task:
            task.mark_uncompleted()
            return True
        return False
    
    def get_completed_tasks(self) -> List[Task]:
        return [task for task in self.tasks if task.completed]
    
    def get_active_tasks(self) -> List[Task]:
        return [task for task in self.tasks if not task.completed]