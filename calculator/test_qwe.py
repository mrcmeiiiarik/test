
import unittest
from Calculator import Calculator

class TestCalc(unittest.TestCase):
    
    def setUp(self):
        self.calc = Calculator()
    
    def test_1_add(self):
        self.assertEqual(self.calc.calculate(2, 2, '+'), 4)
    
    def test_2_sub(self):
        self.assertEqual(self.calc.calculate(5, 3, '-'), 2)
    
    def test_3_mul(self):
        self.assertEqual(self.calc.calculate(3, 3, '*'), 9)
    
    def test_4_div(self):
        self.assertEqual(self.calc.calculate(10, 2, '/'), 5)
    
    def test_5_div_zero(self):
        self.assertEqual(self.calc.calculate(5, 0, '/'), "Деление на ноль запрещено")

if __name__ == '__main__':
    unittest.main()