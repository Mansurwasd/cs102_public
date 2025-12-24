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

def sort_key(order: Order) -> Tuple[int, int]:
    """Функция для сортировки заказов"""
    priority_order = {
        'Россия': 0,
        'Российская Федерация': 0,
        'Russia': 0
    }
    
    delivery_priority = {
        'MAX': 0,
        'MIDDLE': 1,
        'LOW': 2
    }
    
    country = order.country
    country_priority = priority_order.get(country, 1)
    
    if country_priority == 1:
        return (country_priority, country, delivery_priority[order.priority])
    else:
        return (country_priority, 0, delivery_priority[order.priority])

def process_orders(input_file: str = 'orders.txt') -> Tuple[List[Order], List[str]]:
    """Обработка заказов из файла"""
    valid_orders = []
    error_rows = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    order = Order(line)
                    if order.is_valid:
                        valid_orders.append(order)
                    error_rows.extend(order.get_error_rows())
                except ValueError as e:
                    print(f"Ошибка обработки строки: {e}")
                    continue
    except FileNotFoundError:
        print(f"Файл {input_file} не найден!")
        return [], []
    
    return valid_orders, error_rows

def save_results(valid_orders: List[Order], error_rows: List[str]):
    """Сохранение результатов в файлы"""
    with open('non_valid_orders.txt', 'w', encoding='utf-8') as file:
        for row in error_rows:
            file.write(row + '\n')
    
    valid_orders.sort(key=sort_key)
    
    with open('order_country.txt', 'w', encoding='utf-8') as file:
        for order in valid_orders:
            file.write(order.get_valid_row() + '\n')

def main():
    print("Обработка заказов...")
    
    valid_orders, error_rows = process_orders()
    
    if not valid_orders and not error_rows:
        print("Нет данных для обработки.")
        return
    
    save_results(valid_orders, error_rows)
    
    print(f"Обработано валидных заказов: {len(valid_orders)}")
    print(f"Найдено ошибок: {len(error_rows)}")
    print("Результаты сохранены в файлы:")
    print("  - order_country.txt (валидные заказы)")
    print("  - non_valid_orders.txt (ошибки)")

if __name__ == "__main__":
    main()