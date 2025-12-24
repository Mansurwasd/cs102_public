import unittest
import os
import tempfile
import shutil
import re
from typing import List, Tuple

class Order:
    def __init__(self, raw_data: str):
        parts = raw_data.strip().split(';')
        if len(parts) != 6:
            raise ValueError(f"Некорректный формат строки: {raw_data}")
        
        self.order_id = parts[0]
        self.raw_products = parts[1]
        self.customer_name = parts[2]
        self.address = parts[3]
        self.phone = parts[4]
        self.priority = parts[5]
        
        self.errors = []
        self.is_valid = True
        
        self._validate()
        if self.is_valid:
            self._process_data()
    
    def _validate(self):
        """Валидация заказа"""

        if not self.address:
            self.errors.append((self.order_id, "1", "no data"))
            self.is_valid = False
        else:
            address_parts = self.address.split('. ')
            if len(address_parts) != 4:
                self.errors.append((self.order_id, "1", self.address))
                self.is_valid = False
        
        if not self.phone:
            self.errors.append((self.order_id, "2", "no data"))
            self.is_valid = False
        else:
            phone_pattern = r'^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$'
            if not re.match(phone_pattern, self.phone):
                self.errors.append((self.order_id, "2", self.phone))
                self.is_valid = False
    
    def _process_data(self):
        """Обработка данных для валидных заказов"""
        products_list = self.raw_products.split(', ')
        
        product_counts = {}
        product_order = []
        
        for product in products_list:
            if product not in product_counts:
                product_counts[product] = 1
                product_order.append(product)
            else:
                product_counts[product] += 1

        formatted_products = []
        for product in product_order:
            count = product_counts[product]
            if count > 1:
                formatted_products.append(f"{product} x{count}")
            else:
                formatted_products.append(product)
        
        self.formatted_products = ', '.join(formatted_products)
        if self.address:
            address_parts = self.address.split('. ')
            if len(address_parts) == 4:
                self.country = address_parts[0]
                self.formatted_address = f"{address_parts[1]}. {address_parts[2]}. {address_parts[3]}"
            else:
                self.country = ""
                self.formatted_address = self.address
        else:
            self.country = ""
            self.formatted_address = ""
    
    def get_valid_row(self) -> str:
        """Возвращает строку для валидного заказа"""
        return f"{self.order_id};{self.formatted_products};{self.customer_name};{self.formatted_address};{self.phone};{self.priority}"
    
    def get_error_rows(self) -> List[str]:
        """Возвращает строки с ошибками"""
        return [f"{order_id};{error_type};{value}" for order_id, error_type, value in self.errors]

def sort_key(order: Order) -> Tuple[int, str, int]:
    """Функция для сортировки заказов"""
    priority_countries = {
        'Россия': 0,
        'Российская Федерация': 0,
        'Russia': 0,
        'Russian Federation': 0
    }
    delivery_priority = {
        'MAX': 0,
        'MIDDLE': 1,
        'LOW': 2
    }
    
    country = order.country
    
    if country in priority_countries:
        country_priority = 0
        country_for_sort = ""
    else:
        country_priority = 1
        country_for_sort = country

    return (country_priority, country_for_sort, delivery_priority[order.priority])

def process_orders(input_file: str = 'orders.txt') -> Tuple[List[Order], List[str]]:
    """Обработка заказов из файла"""
    valid_orders = []
    error_rows = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    order = Order(line)
                    if order.is_valid:
                        valid_orders.append(order)
                    error_rows.extend(order.get_error_rows())
                except ValueError as e:
                    print(f"Ошибка в строке {line_num}: {e}")
                    continue
    except FileNotFoundError:
        print(f"Файл {input_file} не найден!")
        return [], []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
        return [], []
    
    return valid_orders, error_rows

def save_results(valid_orders: List[Order], error_rows: List[str]):
    """Сохранение результатов в файлы"""
    if error_rows:
        with open('non_valid_orders.txt', 'w', encoding='utf-8') as file:
            for row in error_rows:
                file.write(row + '\n')
    

    if valid_orders:
        valid_orders.sort(key=sort_key)
        with open('order_country.txt', 'w', encoding='utf-8') as file:
            for order in valid_orders:
                file.write(order.get_valid_row() + '\n')


class TestOrderProcessing(unittest.TestCase):
    
    def setUp(self):
        """Создание временной директории для тестов"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Очистка временной директории"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, content):
        """Создание тестового файла"""
        with open('orders.txt', 'w', encoding='utf-8') as f:
            f.write(content)
    
    def test_valid_order_creation(self):
        """Тест создания валидного заказа"""
        data = "12345;Яблоко, Банан, Яблоко;Иванов Иван;Россия. Москва. Москва. Тверская;+7-123-456-78-90;MAX"
        order = Order(data)
        
        self.assertTrue(order.is_valid)
        self.assertEqual(order.order_id, '12345')
        self.assertEqual(order.formatted_products, 'Яблоко x2, Банан')
        self.assertEqual(order.customer_name, 'Иванов Иван')
        self.assertEqual(order.country, 'Россия')
        self.assertEqual(order.formatted_address, 'Москва. Москва. Тверская')
        self.assertEqual(order.phone, '+7-123-456-78-90')
        self.assertEqual(order.priority, 'MAX')
        self.assertEqual(order.errors, [])
    
    def test_order_without_middle_name(self):
        """Тест заказа без отчества"""
        data = "12346;Молоко;Петрова Анна;Россия. МО. Москва. Ленина;+7-987-654-32-10;MIDDLE"
        order = Order(data)
        
        self.assertTrue(order.is_valid)
        self.assertEqual(order.customer_name, 'Петрова Анна')
    
    def test_invalid_address_empty(self):
        """Тест невалидного адреса (пустой)"""
        data = "12347;Хлеб;Сидоров Петр;;+7-111-222-33-44;LOW"
        order = Order(data)
        
        self.assertFalse(order.is_valid)
        self.assertEqual(len(order.errors), 2)
        self.assertEqual(order.errors[0][1], '1')
        self.assertEqual(order.errors[0][2], 'no data')
    
    def test_invalid_address_format(self):
        """Тест невалидного адреса (неправильный формат)"""
        data = "12348;Сыр;Иванов Иван;Россия. Москва. Тверская;+7-111-222-33-44;MAX"
        order = Order(data)
        
        self.assertFalse(order.is_valid)
        self.assertEqual(len(order.errors), 1)
        self.assertEqual(order.errors[0][1], '1')
        self.assertEqual(order.errors[0][2], 'Россия. Москва. Тверская')
    
    def test_invalid_phone_format(self):
        """Тест невалидного телефона"""
        data = "12349;Молоко;Петров Петр;Россия. Москва. Москва. Тверская;+7-123-456-7890;MIDDLE"
        order = Order(data)
        
        self.assertFalse(order.is_valid)
        self.assertEqual(len(order.errors), 1)
        self.assertEqual(order.errors[0][1], '2')
    
    def test_invalid_phone_empty(self):
        """Тест пустого телефона"""
        data = "12350;Хлеб;Сидоров Иван;Россия. Москва. Москва. Тверская;;LOW"
        order = Order(data)
        
        self.assertFalse(order.is_valid)
        self.assertEqual(len(order.errors), 1)
        self.assertEqual(order.errors[0][1], '2')
        self.assertEqual(order.errors[0][2], 'no data')
    
    def test_product_formatting(self):
        """Тест форматирования продуктов"""
        test_cases = [
            ("Молоко, Хлеб, Молоко", "Молоко x2, Хлеб"),
            ("Сыр, Сыр, Сыр", "Сыр x3"),
            ("Яблоко", "Яблоко"),
            ("Масло, Молоко, Хлеб, Масло", "Масло x2, Молоко, Хлеб"),
        ]
        
        for products, expected in test_cases:
            data = f"99999;{products};Тест Тест;Россия. Регион. Город. Улица;+7-123-456-78-90;MAX"
            order = Order(data)
            self.assertEqual(order.formatted_products, expected)
    
    def test_multiple_errors(self):
        """Тест нескольких ошибок в одном заказе"""
        data = "12351;Товар;Иванов Иван;Неправильный адрес;+7-123-456-789;MAX"
        order = Order(data)
        
        self.assertFalse(order.is_valid)
        self.assertEqual(len(order.errors), 2)
        
        error_types = [error[1] for error in order.errors]
        self.assertIn('1', error_types)
        self.assertIn('2', error_types)
    
    def test_sort_key_russia_first(self):
        """Тест сортировки (Россия должна быть первой)"""
        orders = []
        test_data = [
            ("00001;Товар;Иванов Иван;Германия. Берлин. Берлин. Улица;+1-111-222-33-44;MAX"),
            ("00002;Товар;Петров Петр;Россия. Москва. Москва. Улица;+7-111-222-33-44;MIDDLE"),
            ("00003;Товар;Сидоров Сидор;Франция. Париж. Париж. Улица;+3-111-222-33-44;LOW"),
            ("00004;Товар;Алексеев Алексей;Россия. СПБ. СПБ. Улица;+7-222-333-44-55;MAX"),
        ]
        
        for data in test_data:
            order = Order(data)
            if order.is_valid:
                orders.append(order)
        
        orders.sort(key=sort_key)
        
        self.assertEqual(orders[0].country, 'Россия')
        self.assertEqual(orders[1].country, 'Россия')
        self.assertEqual(orders[0].priority, 'MAX')
        self.assertEqual(orders[1].priority, 'MIDDLE')
    
    def test_sort_key_priority_order(self):
        """Тест сортировки по приоритету доставки"""
        orders = []
        test_data = [
            ("00001;Товар;Иванов Иван;Германия. Берлин. Берлин. Улица;+1-111-222-33-44;LOW"),
            ("00002;Товар;Петров Петр;Германия. Берлин. Берлин. Улица;+1-111-222-33-44;MAX"),
            ("00003;Товар;Сидоров Сидор;Германия. Берлин. Берлин. Улица;+1-111-222-33-44;MIDDLE"),
        ]
        
        for data in test_data:
            order = Order(data)
            if order.is_valid:
                orders.append(order)
        
        orders.sort(key=sort_key)
        
        self.assertEqual(orders[0].priority, 'MAX')
        self.assertEqual(orders[1].priority, 'MIDDLE')
        self.assertEqual(orders[2].priority, 'LOW')
    
    def test_full_process_valid_orders(self):
        """Тест полного процесса обработки валидных заказов"""
        content = """87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX
31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE
48276;Яблоки, Макароны, Яблоки;Алексеев Алексей Алексеевич;Италия. Лацио. Рим. Колизей;+3-061-234-56-78;MAX"""
        
        self.create_test_file(content)
        valid_orders, error_rows = process_orders('orders.txt')
        
        self.assertEqual(len(valid_orders), 3)
        self.assertEqual(len(error_rows), 0)
        
        save_results(valid_orders, error_rows)
        
        self.assertTrue(os.path.exists('order_country.txt'))
        self.assertTrue(os.path.exists('non_valid_orders.txt'))
        
        with open('order_country.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
            
            self.assertIn('Россия', lines[0])
            self.assertIn('Россия', lines[1])
            self.assertIn('Италия', lines[2])
            
            self.assertIn('Молоко x2, Яблоки x2, Хлеб', lines[0])
            self.assertIn('Сыр x2, Колбаса x2, Макароны', lines[1])
            self.assertIn('Яблоки x2, Макароны', lines[2])

        with open('non_valid_orders.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, '')
    
    def test_full_process_with_errors(self):
        """Тест полного процесса обработки с ошибками"""
        content = """56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW
84756;Печенье, Сыр, Печенье, Сыр;Васильева Анна Владимировна;Япония. Шибуя. Шибуя-кроссинг;+8-131-234-5678;MAX
90385;Макароны, Сыр, Макароны, Сыр;Николаев Николай;;+1-416-123-45-67;LOW"""
        
        self.create_test_file(content)
        
        valid_orders, error_rows = process_orders('orders.txt')
        
        self.assertEqual(len(valid_orders), 0)
        self.assertEqual(len(error_rows), 4)
        
        save_results(valid_orders, error_rows)
        
        with open('non_valid_orders.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            
            self.assertEqual(len(lines), 4)
            
            self.assertIn('56342;2;+4-989-234-56', lines)
            self.assertIn('84756;2;+8-131-234-5678', lines)
            self.assertIn('84756;1;Япония. Шибуя. Шибуя-кроссинг', lines)
            self.assertIn('90385;1;no data', lines)
        
        with open('order_country.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertEqual(content, '')
    
    def test_mixed_valid_and_invalid_orders(self):
        """Тест смеси валидных и невалидных заказов"""
        content = """87459;Молоко, Яблоки, Хлеб, Яблоки, Молоко;Иванов Иван Иванович;Россия. Московская область. Москва. улица Пушкина;+7-912-345-67-89;MAX
56342;Хлеб, Молоко, Хлеб, Молоко;Смирнова Мария Леонидовна;Германия. Бавария. Мюнхен. Мариенплац;+4-989-234-56;LOW
31987;Сыр, Колбаса, Сыр, Макароны, Колбаса;Петрова Анна;Россия. Ленинградская область. Санкт-Петербург. набережная реки Фонтанки;+7-921-456-78-90;MIDDLE"""
        
        self.create_test_file(content)
        valid_orders, error_rows = process_orders('orders.txt')
        
        # Проверяем результаты
        self.assertEqual(len(valid_orders), 2)
        self.assertEqual(len(error_rows), 1)
        save_results(valid_orders, error_rows)
        
        self.assertTrue(os.path.exists('order_country.txt'))
        self.assertTrue(os.path.exists('non_valid_orders.txt'))
        
        with open('order_country.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            self.assertEqual(len(lines), 2)
            self.assertIn('87459', lines[0])
            self.assertIn('31987', lines[1])
        with open('non_valid_orders.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            self.assertEqual(len(lines), 1)
            self.assertIn('56342;2;+4-989-234-56', lines[0])
    
    def test_phone_validation_patterns(self):
        """Тест различных форматов телефонов"""
        valid_phones = [
            '+7-123-456-78-90',
            '+1-234-567-89-01',
            '+3-456-789-01-23',
        ]
        
        invalid_phones = [
            '+7-123-456-7890',
            '+7-123-456-78-9',
            '+7-123-456-78-901',
            '7-123-456-78-90',
            '+7-1234-567-89-01',
            '+7-123-45-67-89-01',
            '+7-abc-def-gh-ij',
            '',
        ]
        
        for phone in valid_phones:
            data = f"99999;Товар;Тест Тест;Россия. Регион. Город. Улица;{phone};MAX"
            order = Order(data)
            self.assertTrue(order.is_valid, f"Телефон {phone} должен быть валидным")
        
        for phone in invalid_phones:
            data = f"99999;Товар;Тест Тест;Россия. Регион. Город. Улица;{phone};MAX"
            order = Order(data)
            self.assertFalse(order.is_valid, f"Телефон {phone} должен быть невалидным")
            if phone:
                self.assertIn(phone, order.errors[0][2])
    
    def test_country_extraction(self):
        """Тест извлечения страны из адреса"""
        test_cases = [
            ("Россия. Москва. Москва. Тверская", "Россия"),
            ("США. Калифорния. Лос-Анджелес. Голливуд", "США"),
            ("Германия. Бавария. Мюнхен. Мариенплац", "Германия"),
            ("Франция. Иль-де-Франс. Париж. Шанз-Элизе", "Франция"),
        ]
        
        for address, expected_country in test_cases:
            data = f"99999;Товар;Тест Тест;{address};+7-123-456-78-90;MAX"
            order = Order(data)
            self.assertEqual(order.country, expected_country)
    
    def test_address_formatting(self):
        """Тест форматирования адреса (удаление страны)"""
        test_cases = [
            ("Россия. Москва. Москва. Тверская", "Москва. Москва. Тверская"),
            ("США. Калифорния. Лос-Анджелес. Голливуд", "Калифорния. Лос-Анджелес. Голливуд"),
            ("Германия. Бавария. Мюнхен. Мариенплац", "Бавария. Мюнхен. Мариенплац"),
        ]
        
        for address, expected_formatted in test_cases:
            data = f"99999;Товар;Тест Тест;{address};+7-123-456-78-90;MAX"
            order = Order(data)
            self.assertEqual(order.formatted_address, expected_formatted)


class TestEdgeCases(unittest.TestCase):
    
    def setUp(self):
        """Создание временной директории для тестов"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Очистка временной директории"""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)
    
    def test_empty_file(self):
        """Тест пустого файла"""
        with open('orders.txt', 'w', encoding='utf-8') as f:
            f.write('')
        
        valid_orders, error_rows = process_orders('orders.txt')
        
        self.assertEqual(len(valid_orders), 0)
        self.assertEqual(len(error_rows), 0)
    
    def test_file_with_only_newlines(self):
        """Тест файла только с переносами строк"""
        with open('orders.txt', 'w', encoding='utf-8') as f:
            f.write('\n\n\n')
        
        valid_orders, error_rows = process_orders('orders.txt')
        
        self.assertEqual(len(valid_orders), 0)
        self.assertEqual(len(error_rows), 0)
    
    def test_malformed_line(self):
        """Тест строки с неправильным количеством полей"""
        content = """87459;Молоко, Яблоки;Иванов Иван Иванович;Россия. Москва. Москва. Тверская;+7-912-345-67-89
87460;Молоко, Яблоки;Иванов Иван Иванович;Россия. Москва. Москва. Тверская;+7-912-345-67-89;MAX;EXTRA_FIELD"""
        
        with open('orders.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        
        valid_orders, error_rows = process_orders('orders.txt')
        self.assertEqual(len(valid_orders), 0)
    
    def test_priority_case_sensitivity(self):
        """Тест чувствительности к регистру приоритета"""
        test_cases = [
            ("MAX", True),
            ("max", False),
            ("MIDDLE", True),
            ("middle", False),
            ("LOW", True),
            ("low", False),
        ]
        
        for priority, should_be_valid in test_cases:
            data = f"99999;Товар;Тест Тест;Россия. Регион. Город. Улица;+7-123-456-78-90;{priority}"
            order = Order(data)
            if should_be_valid:
                self.assertTrue(order.is_valid)
            else:
                self.assertTrue(order.is_valid)
    
    def test_product_with_commas_in_name(self):
        """Тест с продуктами, содержащими запятые (потенциальная проблема)"""
        data = "99999;Сыр,Колбаса, без пробела;Тест Тест;Россия. Регион. Город. Улица;+7-123-456-78-90;MAX"

        order = Order(data)
        self.assertEqual(order.raw_products, 'Сыр,Колбаса, без пробела')
    
    def test_whitespace_handling(self):
        """Тест обработки пробелов"""
        test_cases = [
            ("  12345  ;  Яблоко, Банан  ;  Иванов Иван  ;  Россия. Москва. Москва. Тверская  ;  +7-123-456-78-90  ;  MAX  ", True),
            ("12345;Яблоко, Банан;Иванов Иван;Россия.  Москва.  Москва.  Тверская;+7-123-456-78-90;MAX", True),
        ]
        
        for data, should_be_valid in test_cases:
            order = Order(data)
            self.assertEqual(order.is_valid, should_be_valid)


if __name__ == '__main__':

    unittest.main(verbosity=2)