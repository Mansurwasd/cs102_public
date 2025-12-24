#exersize1.py

from typing import Dict, List, Tuple, Set

class Movie:
    """Класс для представления фильма"""
    def __init__(self, movie_id: int, title: str):
        self.id = movie_id
        self.title = title

class UserHistory:
    """Класс для представления истории просмотров пользователя"""
    def __init__(self, user_id: int, movie_ids: List[int]):
        self.user_id = user_id
        self.movie_ids = movie_ids
        self.movie_set = set(movie_ids)
    
    def get_similarity(self, other_movies: Set[int]) -> float:
        """Вычисляет долю совпадения фильмов"""
        common = len(self.movie_set.intersection(other_movies))
        total_other = len(other_movies)
        if total_other == 0:
            return 0
        return common / total_other

class RecommendationSystem:
    """Основная система рекомендаций"""
    
    def __init__(self, movies_file: str, history_file: str):
        """Инициализация системы рекомендаций"""
        self.movies = self._load_movies(movies_file)
        self.histories = self._load_histories(history_file)
    
    def _load_movies(self, file_path: str) -> Dict[int, Movie]:
        """Загружает фильмы из файла"""
        movies = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',', 1)
                    if len(parts) == 2:
                        movie_id = int(parts[0].strip())
                        title = parts[1].strip()
                        movies[movie_id] = Movie(movie_id, title)
        return movies
    
    def _load_histories(self, file_path: str) -> List[UserHistory]:
        """Загружает истории просмотров из файла"""
        histories = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line:
                    movie_ids = [int(x.strip()) for x in line.split(',')]
                    histories.append(UserHistory(i, movie_ids))
        return histories
    
    def _get_rating_for_movie(self, movie_id: int, similar_users: List[Tuple[UserHistory, float]]) -> float:
        """Вычисляет рейтинг для фильма на основе похожих пользователей"""
        total_rating = 0.0
        
        for user_history, weight in similar_users:
            view_count = user_history.movie_ids.count(movie_id)
            total_rating += view_count * weight
        
        return total_rating
    
    def recommend(self, user_movies_input: str) -> str:
        """Формирует рекомендацию для пользователя"""
        try:
            user_movies = {int(x.strip()) for x in user_movies_input.split(',')}
        except ValueError:
            return "Ошибка: неверный формат ввода"
        
        similar_users = []
        for history in self.histories:
            similarity = history.get_similarity(user_movies)
            if similarity >= 0.5:
                similar_users.append((history, similarity))
        
        if not similar_users:
            return "Не найдено подходящих рекомендаций"
        
        candidate_movies = set()
        for user_history, _ in similar_users:
            candidate_movies.update(user_history.movie_ids)
        
        candidate_movies -= user_movies
        
        if not candidate_movies:
            return "Все возможные фильмы уже просмотрены"
        
        movie_ratings = {}
        for movie_id in candidate_movies:
            if movie_id in self.movies:
                rating = self._get_rating_for_movie(movie_id, similar_users)
                movie_ratings[movie_id] = rating
        
        # Выбираем фильм с максимальным рейтингом
        if not movie_ratings:
            return "Не найдено подходящих рекомендаций"
        
        best_movie_id = max(movie_ratings.items(), key=lambda x: x[1])[0]
        return self.movies[best_movie_id].title

def main():

    MOVIES_FILE = "movies.txt"
    HISTORY_FILE = "history.txt"

    recommender = RecommendationSystem(MOVIES_FILE, HISTORY_FILE)
    print("Введите ID просмотренных фильмов через запятую:")
    user_input = input().strip()
    recommendation = recommender.recommend(user_input)
    print(recommendation)
        

if __name__ == "__main__":
    main()