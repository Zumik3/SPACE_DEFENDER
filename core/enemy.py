import random

import pygame

from utils.constants import (
    enemy_strong_width, enemy_strong_height, enemy_normal_width, enemy_normal_height,
    enemy_speed, screen_height, white, PIXEL_SIZE, enemy_normal_body, enemy_normal_highlight,
    enemy_strong_body, enemy_strong_core, enemy_strong_highlight, player_engine
)

class Enemy(pygame.sprite.Sprite):
    """Базовый класс для всех врагов"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((self.get_width(), self.get_height()), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = self.get_initial_health()  # Устанавливаем начальное здоровье
        self.shoot_counter = random.randint(0, 29)  # for staggering
        self._draw_enemy()
        
    def update(self):
        self.rect.y += enemy_speed
        
        # Автоматическое удаление, если враг вышел за экран
        if self.rect.top > screen_height:
            self.kill()
            
    def _draw_pixel(self, x, y, color):
        pygame.draw.rect(self.image, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
    def hit(self, damage=1):
        self.health -= damage
        return self.health <= 0
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        # Используем стандартный метод alive() для проверки активности
        return self.alive()
        
    # Методы, которые должны быть реализованы в подклассах
    def get_width(self):
        raise NotImplementedError
        
    def get_height(self):
        raise NotImplementedError
        
    def get_initial_health(self):
        raise NotImplementedError
        
    def get_score(self):
        raise NotImplementedError
        
    def _draw_enemy(self):
        raise NotImplementedError


class NormalEnemy(Enemy):
    """Класс для обычного врага"""
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def get_width(self):
        return enemy_normal_width
        
    def get_height(self):
        return enemy_normal_height
        
    def get_initial_health(self):
        return 2  # Маленькие враги имеют 2 жизни
        
    def get_score(self):
        # За обычного врага (2 жизни) - 2 очка (1 за жизнь)
        return 2
        
    def _draw_enemy(self):
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Рисуем обычного врага
        for i in range(5): self._draw_pixel((1+i)*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_body)
        self._draw_pixel(3*PIXEL_SIZE, 1*PIXEL_SIZE, white)
        for i in range(7): self._draw_pixel(i*PIXEL_SIZE, 3*PIXEL_SIZE, enemy_normal_body)
        self._draw_pixel(1*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_highlight)
        self._draw_pixel(5*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_highlight)
        self._draw_pixel(3*PIXEL_SIZE, 4*PIXEL_SIZE, player_engine)
        
    def reset(self, x=None, y=None):
        """Сброс состояния врага для повторного использования"""
        # Обновляем позицию, если передана
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
            
        # Сбрасываем остальные параметры
        self.health = self.get_initial_health()
        self.shoot_counter = random.randint(0, 29)
        # Перерисовываем врага в image
        self._draw_enemy()


class StrongEnemy(Enemy):
    """Класс для сильного врага"""
    def __init__(self, x, y):
        super().__init__(x, y)
        
    def get_width(self):
        return enemy_strong_width
        
    def get_height(self):
        return enemy_strong_height
        
    def get_initial_health(self):
        return 4  # Большие враги имеют 4 жизни
        
    def get_score(self):
        # За сильного врага (4 жизни) - 12 очков (3 за жизнь)
        return 12
        
    def _draw_enemy(self):
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Рисуем сильного врага
        for i in range(7): self._draw_pixel((1+i)*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_strong_body)
        for i in range(5): self._draw_pixel((2+i)*PIXEL_SIZE, 3*PIXEL_SIZE, enemy_strong_body)
        self._draw_pixel(4*PIXEL_SIZE, 1*PIXEL_SIZE, enemy_strong_core)
        for i in range(9): self._draw_pixel(i*PIXEL_SIZE, 4*PIXEL_SIZE, enemy_strong_body)
        for i in range(7): self._draw_pixel((1+i)*PIXEL_SIZE, 5*PIXEL_SIZE, enemy_strong_body)
        self._draw_pixel(2*PIXEL_SIZE, 4*PIXEL_SIZE, enemy_strong_highlight)
        self._draw_pixel(6*PIXEL_SIZE, 4*PIXEL_SIZE, enemy_strong_highlight)
        self._draw_pixel(3*PIXEL_SIZE, 6*PIXEL_SIZE, player_engine)
        self._draw_pixel(5*PIXEL_SIZE, 6*PIXEL_SIZE, player_engine)
        
    def reset(self, x=None, y=None):
        """Сброс состояния врага для повторного использования"""
        # Обновляем позицию, если передана
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
            
        # Сбрасываем остальные параметры
        self.health = self.get_initial_health()
        self.shoot_counter = random.randint(0, 29)
        # Перерисовываем врага в image
        self._draw_enemy()


def create_random_enemy(screen_width):
    if random.randint(1, 5) == 1:
        enemy_x = random.randint(0, screen_width - enemy_strong_width)
        return StrongEnemy(enemy_x, -enemy_strong_height)
    else:
        enemy_x = random.randint(0, screen_width - enemy_normal_width)
        return NormalEnemy(enemy_x, -enemy_normal_height)