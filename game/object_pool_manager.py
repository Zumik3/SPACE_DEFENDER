import pygame
from core.bullet import Bullet
from core.enemy import Enemy
from core.powerup import Powerup
from core.player import Player
from utils.constants import enemy_normal_width, enemy_strong_width, enemy_normal_height, enemy_strong_height


class ObjectPoolManager:
    """Универсальный менеджер пула объектов для всех типов игровых объектов"""
    
    def __init__(self):
        # Словарь для хранения пулов разных типов объектов
        self.pools = {}
        # Словарь для хранения максимальных размеров пулов
        self.max_pool_sizes = {}
        
        # Инициализация пулов по умолчанию
        self._initialize_default_pools()
        
    def _initialize_default_pools(self):
        """Инициализация пулов по умолчанию"""
        # Пул для пуль
        self.pools['bullet'] = []
        self.max_pool_sizes['bullet'] = 100
        
        # Пул для врагов
        self.pools['enemy'] = []
        self.max_pool_sizes['enemy'] = 50
        
        # Пул для бонусов
        self.pools['powerup'] = []
        self.max_pool_sizes['powerup'] = 20
        
        # Пул для игроков
        self.pools['player'] = []
        self.max_pool_sizes['player'] = 5
        
    def set_max_pool_size(self, object_type, max_size):
        """Установка максимального размера пула для определенного типа объектов"""
        self.max_pool_sizes[object_type] = max_size
        
    def get_object(self, object_type, *args, **kwargs):
        """Получение объекта из пула или создание нового"""
        pool = self.pools.get(object_type, [])
        
        if pool:
            obj = pool.pop()
            # Сброс состояния объекта
            if hasattr(obj, 'reset'):
                obj.reset(*args, **kwargs)
            return obj
        else:
            # Создание нового объекта
            return self._create_object(object_type, *args, **kwargs)
            
    def return_object(self, object_type, obj):
        """Возврат объекта в пул"""
        pool = self.pools.get(object_type, [])
        max_size = self.max_pool_sizes.get(object_type, 100)
        
        if len(pool) < max_size and hasattr(obj, 'active') and obj.active:
            # Сброс состояния объекта перед возвратом в пул
            if hasattr(obj, 'reset'):
                # Для некоторых объектов reset может не требовать аргументов
                try:
                    # Пытаемся вызвать reset без аргументов
                    obj.reset()
                except TypeError:
                    # Если reset требует аргументов, пропускаем сброс
                    # Вместо этого просто очищаем объект перед возвратом в пул
                    if hasattr(obj, '__init__') and hasattr(obj, 'rect'):
                        # Для объектов с rect (pygame.sprite.Sprite) просто сбрасываем флаг active
                        pass
            pool.append(obj)
            
    def _create_object(self, object_type, *args, **kwargs):
        """Создание нового объекта заданного типа"""
        if object_type == 'bullet':
            return self._create_bullet(*args, **kwargs)
        elif object_type == 'enemy':
            return self._create_enemy(*args, **kwargs)
        elif object_type == 'powerup':
            return self._create_powerup(*args, **kwargs)
        elif object_type == 'player':
            return self._create_player(*args, **kwargs)
        else:
            raise ValueError(f"Неизвестный тип объекта: {object_type}")
            
    def _create_bullet(self, x, y, vel_y, color, vel_x=0, width=4, height=10):
        """Создание пули"""
        return Bullet(x, y, vel_y, color, vel_x, width, height)
        
    def _create_enemy(self, enemy_type, x=0, y=0):
        """Создание врага"""
        if enemy_type == 'strong':
            if y == 0:
                y = -enemy_strong_height
            return Enemy(x, y, 'strong')
        else:
            if y == 0:
                y = -enemy_normal_height
            return Enemy(x, y, 'normal')
            
    def _create_powerup(self, powerup_type, x, y):
        """Создание бонуса"""
        if powerup_type == 'health':
            from core.powerup import HealthPowerup
            return HealthPowerup(x, y)
        elif powerup_type == 'fire_rate':
            from core.powerup import FireRatePowerup
            return FireRatePowerup(x, y)
        else:
            raise ValueError(f"Неизвестный тип бонуса: {powerup_type}")
            
    def _create_player(self, x, y):
        """Создание игрока"""
        return Player(x, y)
        
    def clear_pool(self, object_type):
        """Очистка пула определенного типа объектов"""
        if object_type in self.pools:
            self.pools[object_type].clear()
            
    def get_pool_stats(self):
        """Получение статистики по пулам"""
        stats = {}
        for obj_type, pool in self.pools.items():
            stats[obj_type] = {
                'current_size': len(pool),
                'max_size': self.max_pool_sizes.get(obj_type, 0)
            }
        return stats