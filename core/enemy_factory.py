import random
from core.normal_enemy import NormalEnemy
from core.strong_enemy import StrongEnemy
from utils.constants import (
    enemy_strong_width, enemy_normal_width, enemy_strong_height, enemy_normal_height
)

class EnemyFactory:
    """Фабрика для создания врагов разных типов"""
    
    @staticmethod
    def create_enemy(enemy_type, screen_width):
        """Создание врага заданного типа"""
        if enemy_type == 'strong':
            enemy_x = random.randint(0, screen_width - enemy_strong_width)
            return StrongEnemy(enemy_x, -enemy_strong_height)
        else:
            enemy_x = random.randint(0, screen_width - enemy_normal_width)
            return NormalEnemy(enemy_x, -enemy_normal_height)
            
    @staticmethod
    def create_random_enemy(screen_width):
        """Создание случайного врага"""
        if random.randint(1, 5) == 1:
            return EnemyFactory.create_enemy('strong', screen_width)
        else:
            return EnemyFactory.create_enemy('normal', screen_width)