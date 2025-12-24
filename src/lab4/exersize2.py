import sys
from typing import List, Optional, Tuple

class Respondent:
    """Класс для представления респондента."""
    def __init__(self, full_name: str, age: int):
        self.full_name = full_name
        self.age = age

    def __str__(self) -> str:
        """Этот метод вызывается при str(respondent)"""
        return f"{self.full_name} ({self.age})"

class AgeGroup:
    """Класс для представления возрастной группы."""
    
    def __init__(self, lower: int, upper: Optional[int], is_last: bool = False):
        self.lower = lower
        self.upper = upper
        self.is_last = is_last
        self.respondents: List[Respondent] = []

    def __str__(self) -> str:
        """Этот метод вызывается при str(group) или print(group)"""
        if self.is_last:
            return f"{self.lower}+"
        return f"{self.lower}-{self.upper}"
    
    def add_respondent(self, respondent: Respondent) -> None:
        """Добавить респондента в группу."""
        self.respondents.append(respondent)
    
    def sort_respondents(self) -> None:
        """Отсортировать респондентов в группе."""
        self.respondents.sort(key=lambda r: (-r.age, r.full_name))
    
    def is_in_group(self, age: int) -> bool:
        """Проверить, попадает ли возраст в эту группу."""
        if self.is_last:
            return age >= self.lower
        return self.lower <= age <= self.upper


class AgeGroupManager:
    """Менеджер для управления возрастными группами и респондентами."""
    
    MAX_AGE = 123
    
    def __init__(self, boundaries: List[int]):
        self.boundaries = sorted(boundaries)
        self.groups = self._create_groups()
    
    def _create_groups(self) -> List[AgeGroup]:
        """Создать возрастные группы на основе границ."""
        groups = []
        
        if self.boundaries:
            groups.append(AgeGroup(0, self.boundaries[0]))
        
        for i in range(len(self.boundaries) - 1):
            groups.append(AgeGroup(self.boundaries[i] + 1, self.boundaries[i + 1]))
        
        if self.boundaries:
            groups.append(AgeGroup(self.boundaries[-1] + 1, None, is_last=True))
        
        return groups
    
    def add_respondent(self, respondent: Respondent) -> None:
        """Добавить респондента в соответствующую возрастную группу."""
        for group in self.groups:
            if group.is_in_group(respondent.age):
                group.add_respondent(respondent)
                break
    
    def sort_all_groups(self) -> None:
        """Отсортировать респондентов во всех группах."""
        for group in self.groups:
            group.sort_respondents()
    
    def get_non_empty_groups(self) -> List[AgeGroup]:
        """Получить только непустые группы."""
        return [group for group in self.groups if group.respondents]
    
    def format_output(self) -> List[str]:
        """Отформатировать вывод для всех непустых групп (от старшей к младшей)."""
        output_lines = []
        non_empty_groups = self.get_non_empty_groups()
        
        for group in reversed(non_empty_groups):
            if group.respondents:
                respondents_str = ", ".join(str(r) for r in group.respondents)
                output_lines.append(f"{group}: {respondents_str}")
        
        return output_lines

def read_input() -> Tuple[List[str], List[int]]:
    """Чтение входных данных."""
    boundaries = [int(arg) for arg in sys.argv[1:]]
    
    respondents_data = []
    for line in sys.stdin:
        line = line.strip()
        if line == "END":
            break
        if line:
            respondents_data.append(line)
    
    return respondents_data, boundaries

def parse_respondent(line: str) -> Respondent:
    """Парсинг строки с данными респондента."""
    try:
        full_name, age_str = line.rsplit(',', 1)
        age = int(age_str)
        return Respondent(full_name.strip(), age)
    except ValueError as e:
        raise ValueError(f"Неверный формат строки: {line}") from e

def main():
    """Основная функция приложения."""
    respondents_data, boundaries = read_input()
    
    manager = AgeGroupManager(boundaries)
    
    for line in respondents_data:
        respondent = parse_respondent(line)
        manager.add_respondent(respondent)
    
    manager.sort_all_groups()
    
    output_lines = manager.format_output()
    for line in output_lines:
        print(line)

if __name__ == "__main__":
    main()