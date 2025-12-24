# ex1_test.py

import unittest
import os
import tempfile
from src.lab4.exersize1 import Movie, UserHistory, RecommendationSystem

class TestMovie(unittest.TestCase):
    """Тесты для класса Movie"""
    
    def test_movie_creation(self):
        """Тест создания объекта фильма"""
        movie = Movie(1, "Тестовый фильм")
        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.title, "Тестовый фильм")

class TestUserHistory(unittest.TestCase):
    """Тесты для класса UserHistory"""
    
    def test_history_creation(self):
        """Тест создания истории просмотров"""
        history = UserHistory(1, [1, 2, 3])
        self.assertEqual(history.user_id, 1)
        self.assertEqual(history.movie_ids, [1, 2, 3])
        self.assertEqual(history.movie_set, {1, 2, 3})
    
    def test_similarity_calculation(self):
        """Тест вычисления сходства"""
        history = UserHistory(1, [1, 2, 3, 4])
    
        self.assertEqual(history.get_similarity({1, 2, 3, 4}), 1.0)
        self.assertEqual(history.get_similarity({1, 2}), 1)
        self.assertEqual(history.get_similarity({5, 6}), 0.0)
        self.assertEqual(history.get_similarity(set()), 0.0)

class TestRecommendationSystem(unittest.TestCase):
    """Тесты для системы рекомендаций"""
    
    def setUp(self):
        """Создание временных файлов для тестов"""
        self.movies_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        movies_data = [
            "1,Мстители: Финал",
            "2,Хатико",
            "3,Дюна",
            "4,Унесенные призраками",
            "5,Интерстеллар",
            "6,Начало",
            "7,Матрица"
        ]
        self.movies_file.write('\n'.join(movies_data))
        self.movies_file.close()
        
        self.history_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        history_data = [
            "2,1,3",
            "1,4,3",
            "2,2,2,2,2,3",
            "1,2,3,4,5",
            "3,5,6",
            "4,5,6,7",
            "5,1,2,3,4,5,6,7"
        ]
        self.history_file.write('\n'.join(history_data))
        self.history_file.close()
        
        self.recommender = RecommendationSystem(self.movies_file.name, self.history_file.name)
    
    def tearDown(self):
        """Удаление временных файлов после тестов"""
        os.unlink(self.movies_file.name)
        os.unlink(self.history_file.name)
    
    def test_load_movies(self):
        """Тест загрузки фильмов"""
        self.assertEqual(len(self.recommender.movies), 7)
        self.assertEqual(self.recommender.movies[1].title, "Мстители: Финал")
        self.assertEqual(self.recommender.movies[3].title, "Дюна")
    
    def test_load_histories(self):
        """Тест загрузки историй просмотров"""
        self.assertEqual(len(self.recommender.histories), 7)
        self.assertEqual(self.recommender.histories[0].movie_ids, [2, 1, 3])
        self.assertEqual(self.recommender.histories[0].movie_set, {1, 2, 3})
        self.assertEqual(self.recommender.histories[2].movie_ids, [2, 2, 2, 2, 2, 3])
    
    def test_recommendation_example(self):
        """Тест примера из условия задачи"""
        recommendation = self.recommender.recommend("2,4")
        self.assertEqual(recommendation, "Дюна")
    
    def test_no_similar_users(self):
        """Тест случая, когда нет похожих пользователей"""
        recommendation = self.recommender.recommend("100,200")
        self.assertEqual(recommendation, "Не найдено подходящих рекомендаций")
    
    def test_all_movies_watched(self):
        """Тест случая, когда пользователь посмотрел все возможные фильмы"""
        recommendation = self.recommender.recommend("1,2,3,4,5,6,7")
        self.assertEqual(recommendation, "Все возможные фильмы уже просмотрены")
    
    def test_invalid_input_format(self):
        """Тест неверного формата ввода"""
        recommendation = self.recommender.recommend("не число,второе не число")
        self.assertIn("Ошибка", recommendation)
    
    def test_weighted_recommendations(self):
        """Тест рекомендаций с учетом весов"""
        test_movies_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        test_movies_file.write("1,Фильм 1\n2,Фильм 2\n3,Фильм 3\n4,Фильм 4")
        test_movies_file.close()
        
        test_history_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        test_history_file.write("1,1,2,3\n2,1,2\n3,1")
        test_history_file.close()
        
        test_recommender = RecommendationSystem(test_movies_file.name, test_history_file.name)

        recommendation = test_recommender.recommend("1,2")
        self.assertEqual(recommendation, "Фильм 3")
        
        os.unlink(test_movies_file.name)
        os.unlink(test_history_file.name)
    
    def test_recommendation_with_duplicates(self):
        """Тест рекомендаций с учетом количества просмотров"""

        test_movies_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        test_movies_file.write("1,Фильм 1\n2,Фильм 2\n3,Фильм 3")
        test_movies_file.close()
        
        test_history_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')

        test_history_file.write("1,1,2,3\n2,1,2,2,2,2")
        test_history_file.close()
        
        test_recommender = RecommendationSystem(test_movies_file.name, test_history_file.name)

        recommendation = test_recommender.recommend("1,2")
        
        self.assertEqual(recommendation, "Фильм 3")
        
        os.unlink(test_movies_file.name)
        os.unlink(test_history_file.name)

def run_tests():
    """Запуск всех тестов"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMovie)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUserHistory))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRecommendationSystem))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

if __name__ == "__main__":
    run_tests()