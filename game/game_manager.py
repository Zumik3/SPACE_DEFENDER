import pygame
from game.game_logic import Game
from ui.renderer import Renderer
from utils.sound_manager import SoundManager
from game.object_pool import ObjectPool
from core.enemy_factory import EnemyFactory
from utils.settings_manager import SettingsManager


class GameManager:
    """Централизованный класс управления игрой, координирующий работу всех компонентов"""
    
    def __init__(self, screen, settings_manager=None):
        self.screen = screen
        self.settings_manager = settings_manager or SettingsManager()
        
        # Инициализация всех компонентов
        self.sound_manager = self._create_sound_manager()
        self.renderer = self._create_renderer()
        self.object_pool = self._create_object_pool()
        self.enemy_factory = self._create_enemy_factory()
        
        # Инициализация игровой логики с передачей зависимостей
        self.game = self._create_game()
        
    def _create_sound_manager(self):
        """Создание менеджера звука"""
        return SoundManager(self.settings_manager)
        
    def _create_renderer(self):
        """Создание рендерера"""
        return Renderer(self.screen)
        
    def _create_object_pool(self):
        """Создание пула объектов"""
        return ObjectPool()
        
    def _create_enemy_factory(self):
        """Создание фабрики врагов"""
        return EnemyFactory()
        
    def _create_game(self):
        """Создание игровой логики с передачей всех зависимостей"""
        game = Game(self.sound_manager)
        # Передаем зависимости напрямую в конструктор Game
        game.renderer = self.renderer
        game.object_pool = self.object_pool
        game.enemy_factory = self.enemy_factory
        # Инициализируем PyGame в Game
        game.init_pygame(self.screen)
        return game
        
    def start_game(self):
        """Запуск игры"""
        return self.game.run(self.screen)
        
    def get_sound_manager(self):
        """Получение менеджера звука"""
        return self.sound_manager
        
    def get_renderer(self):
        """Получение рендерера"""
        return self.renderer
        
    def get_object_pool(self):
        """Получение пула объектов"""
        return self.object_pool
        
    def get_enemy_factory(self):
        """Получение фабрики врагов"""
        return self.enemy_factory