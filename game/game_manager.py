import pygame
from game.game_logic import Game
from ui.renderer import Renderer
from utils.sound_manager import SoundManager
from game.object_pool_manager import ObjectPoolManager
from core.enemy_factory import EnemyFactory
from utils.settings_manager import SettingsManager
from game.state_manager import GameStateManager
from game.event_handler import GameEventHandler
from game.renderer import GameRenderer
from utils.event_manager import EventManager


class GameManager:
    """Централизованный класс управления игрой, координирующий работу всех компонентов"""
    
    def __init__(self, screen, settings_manager=None):
        self.screen = screen
        self.settings_manager = settings_manager or SettingsManager()
        
        # Инициализация всех компонентов
        self.sound_manager = self._create_sound_manager()
        self.renderer = self._create_renderer()
        self.object_pool_manager = self._create_object_pool_manager()
        self.enemy_factory = self._create_enemy_factory()
        self.state_manager = self._create_state_manager()
        self.event_handler = self._create_event_handler()
        self.game_renderer = self._create_game_renderer()
        self.event_manager = self._create_event_manager()
        
        # Инициализация игровой логики с передачей зависимостей
        self.game = self._create_game()
        
    def _create_sound_manager(self):
        """Создание менеджера звука"""
        return SoundManager(self.settings_manager)
        
    def _create_renderer(self):
        """Создание рендерера"""
        return Renderer(self.screen)
        
    def _create_object_pool_manager(self):
        """Создание менеджера пула объектов"""
        pool_manager = ObjectPoolManager()
        
        # Настраиваем размеры пулов для разных типов объектов
        pool_manager.set_max_pool_size('bullet', 150)  # Пули - самый многочисленный тип объектов
        pool_manager.set_max_pool_size('enemy', 30)    # Враги - среднее количество
        pool_manager.set_max_pool_size('powerup', 10)  # Бонусы - редкие объекты
        pool_manager.set_max_pool_size('player', 3)    # Игрок - единственный объект
        
        return pool_manager
        
    def _create_enemy_factory(self):
        """Создание фабрики врагов"""
        return EnemyFactory()
        
    def _create_state_manager(self):
        """Создание менеджера состояния игры"""
        return GameStateManager()
        
    def _create_event_handler(self):
        """Создание обработчика событий"""
        # Этот компонент будет инициализирован позже, когда будет создан Game
        return None
        
    def _create_game_renderer(self):
        """Создание рендерера игры"""
        return GameRenderer(self.screen, self.renderer)
        
    def _create_event_manager(self):
        """Создание менеджера событий"""
        return EventManager()
        
    def _create_game(self):
        """Создание игровой логики с передачей всех зависимостей"""
        game = Game(self.sound_manager)
        # Передаем зависимости напрямую в конструктор Game
        game.renderer = self.renderer
        game.object_pool_manager = self.object_pool_manager
        game.enemy_factory = self.enemy_factory
        game.state_manager = self.state_manager
        game.game_renderer = self.game_renderer
        game.event_manager = self.event_manager
        # Инициализируем PyGame в Game
        game.init_pygame(self.screen)
        return game
        
    def start_game(self):
        """Запуск игры"""
        # Создаем обработчик событий с передачей всех необходимых зависимостей
        self.event_handler = GameEventHandler(
            self.game, 
            self.object_pool_manager, 
            self.enemy_factory, 
            self.sound_manager
        )
        # Передаем event_handler в Game
        self.game.event_handler = self.event_handler
        return self.game.run(self.screen)
        
    def get_sound_manager(self):
        """Получение менеджера звука"""
        return self.sound_manager
        
    def get_renderer(self):
        """Получение рендерера"""
        return self.renderer
        
    def get_object_pool_manager(self):
        """Получение менеджера пула объектов"""
        return self.object_pool_manager
        
    def get_enemy_factory(self):
        """Получение фабрики врагов"""
        return self.enemy_factory
        
    def get_state_manager(self):
        """Получение менеджера состояния игры"""
        return self.state_manager
        
    def get_event_manager(self):
        """Получение менеджера событий"""
        return self.event_manager