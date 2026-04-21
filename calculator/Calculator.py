
class Calculator: 
    def get_number(self, prompt):
        while True:
            try:
                number = float(input(prompt))
                if number.is_integer():
                    return int(number)
                return number
            except ValueError:
                print("Это не число! Пожалуйста, введите число.") 

    def get_operation(self):
        message = '''
    Выберете математическую операцию:

    + : Сложение
    - : Вычитание
    / : Деление
    * : Умножение
    Ваш выбор:
    '''

        correct_operations = '+-/*'
    
        operation = input(message)

        while operation not in correct_operations:
            print('Такая операция недоступна. Повторите попытку.')
            operation = input(message)
        return operation

    
    def calculate(self, num1, num2, operation):
        result = None
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '/':
            try:
                result = num1 / num2
            except ZeroDivisionError:
                result = "Деление на ноль запрещено"
        elif operation == '*':
            result = num1 * num2
        return result

    def main(self):
        num1 = self.get_number("Введите первое число: ") # ввод первого числа
        num2 = self.get_number("Введите второе число: ") # ввод второго числа
        operation = self.get_operation() 
        result = self.calculate(num1, num2, operation)
        print("Результат:", result)



if __name__ == "__main__":
    calc = Calculator()
    calc.main()

    while True:
        decision = (input('Продолжить? (да/нет) ')).lower()
   
        if decision == 'да':
            calc.main()
        elif decision == 'нет':
            break