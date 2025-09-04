import pygame
from core.bullet import Bullet
from core.enemy import Enemy
from utils.constants import enemy_normal_width, enemy_strong_width, enemy_normal_height, enemy_strong_height
import random

class ObjectPool:
    def __init__(self):
        self.bullet_pool = []
        self.enemy_pool = []
        self.max_pool_size = 100
        
    def get_bullet(self, x, y, vel_y, color, vel_x=0, width=4, height=10):
        if self.bullet_pool:
            bullet = self.bullet_pool.pop()
            bullet.reset(x, y, vel_y, color, vel_x, width, height)
            return bullet
        else:
            return Bullet(x, y, vel_y, color, vel_x, width, height)
            
    def return_bullet(self, bullet):
        if len(self.bullet_pool) < self.max_pool_size:
            self.bullet_pool.append(bullet)
            
    def get_enemy(self, enemy_type, screen_width):
        # Ищем врага нужного типа в пуле
        for i, enemy in enumerate(self.enemy_pool):
            if enemy.type == enemy_type:
                # Устанавливаем правильные координаты для врага
                if enemy_type == 'strong':
                    enemy_x = random.randint(0, screen_width - enemy_strong_width)
                    enemy.rect.x = enemy_x
                    enemy.rect.y = -enemy_strong_height
                else:
                    enemy_x = random.randint(0, screen_width - enemy_normal_width)
                    enemy.rect.x = enemy_x
                    enemy.rect.y = -enemy_normal_height
                return enemy
                
        # Если не нашли, создаем нового
        if enemy_type == 'strong':
            enemy_x = random.randint(0, screen_width - enemy_strong_width)
            return Enemy(enemy_x, -enemy_strong_height, 'strong')
        else:
            enemy_x = random.randint(0, screen_width - enemy_normal_width)
            return Enemy(enemy_x, -enemy_normal_height, 'normal')
            
    def return_enemy(self, enemy):
        if len(self.enemy_pool) < self.max_pool_size:
            enemy.reset()  # Сброс состояния врага
            self.enemy_pool.append(enemy)