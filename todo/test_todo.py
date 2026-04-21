import unittest
from todo import TaskManager


class TestTodoApp(unittest.TestCase):
    
    def setUp(self):
        self.manager = TaskManager()
    
    def test_1_add_task(self):
        task = self.manager.add_task("Купить продукты", "Молоко, хлеб")
        
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Купить продукты")
        self.assertEqual(task.description, "Молоко, хлеб")
        self.assertFalse(task.completed)
        
        task2 = self.manager.add_task("Сделать ДЗ")
        self.assertEqual(len(self.manager.tasks), 2)
        self.assertEqual(task2.id, 2)
    
    def test_2_get_task(self):
        self.manager.add_task("Задача 1")
        self.manager.add_task("Задача 2")
        
        task = self.manager.get_task(1)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Задача 1")
        
        task = self.manager.get_task(999)
        self.assertIsNone(task)
    
    def test_3_update_task(self):
        task = self.manager.add_task("Старое название", "Старое описание")
        
        result = self.manager.update_task(1, "Новое название", "Новое описание")
        
        self.assertTrue(result)
        self.assertEqual(task.title, "Новое название")
        self.assertEqual(task.description, "Новое описание")
        
        result = self.manager.update_task(999, "Тест", "Тест")
        self.assertFalse(result)
    
    def test_4_delete_task(self):
        self.manager.add_task("Задача 1")
        self.manager.add_task("Задача 2")
        self.manager.add_task("Задача 3")
        
        result = self.manager.delete_task(2)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 2)
        self.assertIsNone(self.manager.get_task(2))
        
        result = self.manager.delete_task(999)
        self.assertFalse(result)
        self.assertEqual(len(self.manager.tasks), 2)
    
    def test_5_mark_completed(self):
        task1 = self.manager.add_task("Задача 1")
        task2 = self.manager.add_task("Задача 2")
        
        result = self.manager.mark_completed(1)
        
        self.assertTrue(result)
        self.assertTrue(task1.completed)
        self.assertFalse(task2.completed)
        
        completed = self.manager.get_completed_tasks()
        active = self.manager.get_active_tasks()
        
        self.assertEqual(len(completed), 1)
        self.assertEqual(len(active), 1)
        self.assertIn(task1, completed)
        self.assertIn(task2, active)
    
    def test_6_mark_uncompleted(self):
        task = self.manager.add_task("Задача")
        self.manager.mark_completed(1)
        self.assertTrue(task.completed)
        
        result = self.manager.mark_uncompleted(1)
        
        self.assertTrue(result)
        self.assertFalse(task.completed)
        
        self.assertEqual(len(self.manager.get_completed_tasks()), 0)
        self.assertEqual(len(self.manager.get_active_tasks()), 1)


if __name__ == '__main__':
    unittest.main()