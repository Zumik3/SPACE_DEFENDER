import random
from core.enemy import Enemy
from utils.constants import enemy_strong_width, enemy_normal_width, enemy_strong_height, enemy_normal_height

class EnemyFactory:
    """Фабрика для создания врагов разных типов"""
    
    @staticmethod
    def create_enemy(enemy_type, screen_width):
        """Создание врага заданного типа"""
        if enemy_type == 'strong':
            enemy_x = random.randint(0, screen_width - enemy_strong_width)
            return Enemy(enemy_x, -enemy_strong_height, 'strong')
        else:
            enemy_x = random.randint(0, screen_width - enemy_normal_width)
            return Enemy(enemy_x, -enemy_normal_height, 'normal')
            
    @staticmethod
    def create_random_enemy(screen_width):
        """Создание случайного врага"""
        if random.randint(1, 5) == 1:
            return EnemyFactory.create_enemy('strong', screen_width)
        else:
            return EnemyFactory.create_enemy('normal', screen_width)