import pygame
from core.bullet import Bullet
from core.enemy import Enemy
from utils.constants import enemy_normal_width, enemy_strong_width, enemy_normal_height, enemy_strong_height, screen_width

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
            
    def get_enemy(self, enemy_type):
        # Ищем врага нужного типа в пуле
        for i, enemy in enumerate(self.enemy_pool):
            if enemy.type == enemy_type:
                return self.enemy_pool.pop(i)
                
        # Если не нашли, создаем нового
        if enemy_type == 'strong':
            enemy_x = 0  # Будет установлен позже
            return Enemy(enemy_x, -enemy_strong_height, 'strong')
        else:
            enemy_x = 0  # Будет установлен позже
            return Enemy(enemy_x, -enemy_normal_height, 'normal')
            
    def return_enemy(self, enemy):
        if len(self.enemy_pool) < self.max_pool_size:
            enemy.reset()  # Сброс состояния врага
            self.enemy_pool.append(enemy)