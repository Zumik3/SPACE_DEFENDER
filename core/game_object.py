from abc import ABC, abstractmethod

class GameObject(ABC):
    """Базовый интерфейс для игровых объектов"""
    
    @abstractmethod
    def update(self):
        """Обновление состояния объекта"""
        pass
        
    @abstractmethod
    def draw(self, renderer):
        """Отрисовка объекта"""
        pass
        
    @abstractmethod
    def get_rect(self):
        """Получение прямоугольника объекта для коллизий"""
        pass
        
    @abstractmethod
    def is_active(self):
        """Проверка, активен ли объект"""
        pass