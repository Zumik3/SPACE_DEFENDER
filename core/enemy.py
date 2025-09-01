import pygame
from utils.constants import enemy_strong_width, enemy_strong_height, enemy_normal_width, enemy_normal_height, enemy_speed, screen_height, white
import random
import math
from core.game_object import GameObject

class Enemy(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.type = enemy_type
        
        if self.type == 'strong':
            width, height = enemy_strong_width, enemy_strong_height
            health = 4  # Большие враги имеют 4 жизни
        else:
            width, height = enemy_normal_width, enemy_normal_height
            health = 2  # Маленькие враги имеют 2 жизни
            
        # Создаем изображение для спрайта (временно пустая поверхность)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.shoot_counter = random.randint(0, 29)  # for staggering
        self.active = True

    def update(self):
        self.rect.y += enemy_speed
        
        # Автоматическое удаление, если враг вышел за экран
        if self.rect.top > screen_height:
            self.kill()
            self.active = False

    def draw(self, renderer):
        # Переопределяем отрисовку, чтобы использовать методы рендерера
        if self.type == 'strong':
            renderer.draw_strong_enemy(self.rect)
        else:
            renderer.draw_normal_enemy(self.rect)

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def get_score(self):
        # Возвращаем очки за убитого врага
        # За сильного врага (4 жизни) - 12 очков (3 за жизнь)
        # За обычного врага (2 жизни) - 2 очка (1 за жизнь)
        return 12 if self.type == 'strong' else 2

    @classmethod
    def create_random(cls, screen_width):
        if random.randint(1, 5) == 1:
            enemy_x = random.randint(0, screen_width - enemy_strong_width)
            return cls(enemy_x, -enemy_strong_height, 'strong')
        else:
            enemy_x = random.randint(0, screen_width - enemy_normal_width)
            return cls(enemy_x, -enemy_normal_height, 'normal')
            
    def reset(self):
        """Сброс состояния врага для повторного использования"""
        self.health = 4 if self.type == 'strong' else 2
        self.shoot_counter = random.randint(0, 29)
        self.active = True
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        return self.active