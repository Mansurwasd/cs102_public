import unittest
import sys
from src.lab4.exersize2 import Respondent, AgeGroup, AgeGroupManager, parse_respondent

class TestRespondent(unittest.TestCase):
    """Тесты для класса Respondent."""
    
    def test_creation_and_str(self):
        """Тест создания респондента и строкового представления."""
        r = Respondent("Иванов Иван Иванович", 25)
        self.assertEqual(r.full_name, "Иванов Иван Иванович")
        self.assertEqual(r.age, 25)
        self.assertEqual(str(r), "Иванов Иван Иванович (25)")
    
class TestAgeGroup(unittest.TestCase):
    """Тесты для класса AgeGroup."""
    
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.group = AgeGroup(19, 25)
    
    def test_creation_and_str(self):
        """Тест создания группы и строкового представления."""
        self.assertEqual(self.group.lower, 19)
        self.assertEqual(self.group.upper, 25)
        self.assertFalse(self.group.is_last)
        self.assertEqual(str(self.group), "19-25")
    
    def test_last_group(self):
        """Тест создания последней группы."""
        last_group = AgeGroup(101, None, is_last=True)
        self.assertEqual(str(last_group), "101+")
    
    def test_is_in_group(self):
        """Тест проверки попадания возраста в группу."""
        # Возраст внутри группы
        self.assertTrue(self.group.is_in_group(20))
        self.assertTrue(self.group.is_in_group(19))
        self.assertTrue(self.group.is_in_group(25))
        
        # Возраст вне группы
        self.assertFalse(self.group.is_in_group(18))
        self.assertFalse(self.group.is_in_group(26))
    
    def test_add_and_sort_respondents(self):
        """Тест добавления и сортировки респондентов."""
        # Добавляем респондентов в разном порядке
        self.group.add_respondent(Respondent("Б", 20))
        self.group.add_respondent(Respondent("А", 25))
        self.group.add_respondent(Respondent("В", 20))
        self.group.add_respondent(Respondent("Г", 19))
        
        # Сортируем
        self.group.sort_respondents()
        
        # Проверяем порядок сортировки
        self.assertEqual(len(self.group.respondents), 4)
        
        # Должны быть отсортированы по убыванию возраста, затем по возрастанию ФИО
        self.assertEqual(self.group.respondents[0].age, 25)
        self.assertEqual(self.group.respondents[0].full_name, "А")
        
        self.assertEqual(self.group.respondents[1].age, 20)
        self.assertEqual(self.group.respondents[1].full_name, "Б")
        
        self.assertEqual(self.group.respondents[2].age, 20)
        self.assertEqual(self.group.respondents[2].full_name, "В")
        
        self.assertEqual(self.group.respondents[3].age, 19)
        self.assertEqual(self.group.respondents[3].full_name, "Г")

class TestAgeGroupManager(unittest.TestCase):
    """Тесты для класса AgeGroupManager."""
    
    def test_creation_with_boundaries(self):
        """Тест создания менеджера с границами."""
        boundaries = [18, 25, 35]
        manager = AgeGroupManager(boundaries)
        
        # Проверяем созданные группы
        self.assertEqual(len(manager.groups), 4)
        self.assertEqual(str(manager.groups[0]), "0-18")
        self.assertEqual(str(manager.groups[1]), "19-25")
        self.assertEqual(str(manager.groups[2]), "26-35")
        self.assertEqual(str(manager.groups[3]), "36+")
    
    def test_add_respondent_to_correct_group(self):
        """Тест добавления респондента в правильную группу."""
        boundaries = [18, 25, 35]
        manager = AgeGroupManager(boundaries)
        
        # Добавляем респондентов разных возрастов
        manager.add_respondent(Respondent("Ребенок", 10))
        manager.add_respondent(Respondent("Молодой", 20))
        manager.add_respondent(Respondent("Взрослый", 30))
        manager.add_respondent(Respondent("Пожилой", 40))
        
        # Проверяем распределение
        self.assertEqual(len(manager.groups[0].respondents), 1)  # 0-18
        self.assertEqual(manager.groups[0].respondents[0].full_name, "Ребенок")
        
        self.assertEqual(len(manager.groups[1].respondents), 1)  # 19-25
        self.assertEqual(manager.groups[1].respondents[0].full_name, "Молодой")
        
        self.assertEqual(len(manager.groups[2].respondents), 1)  # 26-35
        self.assertEqual(manager.groups[2].respondents[0].full_name, "Взрослый")
        
        self.assertEqual(len(manager.groups[3].respondents), 1)  # 36+
        self.assertEqual(manager.groups[3].respondents[0].full_name, "Пожилой")
    
    def test_sort_all_groups(self):
        """Тест сортировки всех групп."""
        boundaries = [25]
        manager = AgeGroupManager(boundaries)
        
        # Добавляем респондентов
        manager.add_respondent(Respondent("Б", 30))
        manager.add_respondent(Respondent("А", 35))
        manager.add_respondent(Respondent("В", 30))
        
        # Сортируем
        manager.sort_all_groups()
        
        # Проверяем сортировку в группе 26+
        respondents = manager.groups[1].respondents  # Группа 26+
        self.assertEqual(len(respondents), 3)
        
        # Должны быть отсортированы по убыванию возраста, затем по возрастанию ФИО
        self.assertEqual(respondents[0].full_name, "А")  # 35 лет
        self.assertEqual(respondents[1].full_name, "Б")  # 30 лет, Б < В
        self.assertEqual(respondents[2].full_name, "В")  # 30 лет
    
    def test_get_non_empty_groups(self):
        """Тест получения непустых групп."""
        boundaries = [18, 25]
        manager = AgeGroupManager(boundaries)
        
        # Добавляем только в некоторые группы
        manager.add_respondent(Respondent("Ребенок", 10))
        manager.add_respondent(Respondent("Взрослый", 30))
        
        # Получаем непустые группы
        non_empty = manager.get_non_empty_groups()
        
        # Должны быть только 2 непустые группы
        self.assertEqual(len(non_empty), 2)
        
        # Проверяем, что пустая группа (19-25) не включена
        group_strs = [str(g) for g in non_empty]
        self.assertIn("0-18", group_strs)
        self.assertIn("26+", group_strs)
        self.assertNotIn("19-25", group_strs)
    
    def test_format_output(self):
        """Тест форматирования вывода."""
        boundaries = [18, 25]
        manager = AgeGroupManager(boundaries)
        
        # Добавляем респондентов
        manager.add_respondent(Respondent("Младший", 10))
        manager.add_respondent(Respondent("Старший", 30))
        manager.add_respondent(Respondent("Средний", 20))
        
        # Сортируем
        manager.sort_all_groups()
        
        # Получаем отформатированный вывод
        output = manager.format_output()
        
        # Проверяем вывод
        self.assertEqual(len(output), 3)
        
        # Группы должны быть в порядке от старшей к младшей
        self.assertTrue(output[0].startswith("26+:"))
        self.assertIn("Старший (30)", output[0])
        
        self.assertTrue(output[1].startswith("19-25:"))
        self.assertIn("Средний (20)", output[1])
        
        self.assertTrue(output[2].startswith("0-18:"))
        self.assertIn("Младший (10)", output[2])

class TestHelperFunctions(unittest.TestCase):
    """Тесты вспомогательных функций."""
    
    def test_parse_respondent_valid(self):
        """Тест парсинга корректной строки респондента."""
        
        
        respondent = parse_respondent("Иванов Иван Иванович,25")
        self.assertEqual(respondent.full_name, "Иванов Иван Иванович")
        self.assertEqual(respondent.age, 25)
    
    def test_parse_respondent_invalid_format(self):
        """Тест парсинга некорректной строки."""
        
        
        with self.assertRaises(ValueError):
            parse_respondent("Иванов Иван Иванович")
        
        with self.assertRaises(ValueError):
            parse_respondent("Иванов Иван Иванович,abc")
    
    def test_parse_respondent_with_spaces(self):
        """Тест парсинга строки с пробелами."""
        
        respondent = parse_respondent("  Иванов Иван Иванович  ,  25  ")
        self.assertEqual(respondent.full_name, "Иванов Иван Иванович")
        self.assertEqual(respondent.age, 25)

def run_tests():
    """Запуск всех тестов."""
    # Создаем тестовый набор
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавляем все тесты
    suite.addTests(loader.loadTestsFromTestCase(TestRespondent))
    suite.addTests(loader.loadTestsFromTestCase(TestAgeGroup))
    suite.addTests(loader.loadTestsFromTestCase(TestAgeGroupManager))
    suite.addTests(loader.loadTestsFromTestCase(TestHelperFunctions))
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)