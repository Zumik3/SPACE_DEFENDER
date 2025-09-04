import pygame
from utils.constants import (
    screen_width, screen_height, bullet_color, bullet_speed, enemy_bullet_color
)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_y, color, vel_x=0, width=4, height=10):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Автоматическое удаление, если пуля вышла за экран
        if (self.rect.bottom < 0 or 
            self.rect.right < 0 or 
            self.rect.left > screen_width or 
            self.rect.top > screen_height):
            self.kill()

    def draw(self, renderer):
        # Для пуль используется стандартная отрисовка через Group.draw()
        # Этот метод добавлен для совместимости с интерфейсом GameObject
        pass
        
    def get_rect(self):
        # Возвращаем rect для совместимости с интерфейсом GameObject
        return self.rect
        
    def is_active(self):
        # Используем стандартный метод alive() для проверки активности
        return self.alive()

    @classmethod
    def player_bullet(cls, player_rect):
        from utils.constants import bullet_color, bullet_speed
        return cls(player_rect.centerx - 2, player_rect.top, -bullet_speed, bullet_color, 0, 4, 10)

    @classmethod
    def enemy_bullet(cls, start_pos, vel, size=6):
        from utils.constants import enemy_bullet_color
        return cls(start_pos.x, start_pos.y, vel.y, enemy_bullet_color, vel.x, size, size)
        
    def reset(self, x=None, y=None, vel_y=None, color=None, vel_x=None, width=None, height=None):
        """Сброс состояния пули для повторного использования"""
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
        if vel_x is not None:
            self.vel_x = vel_x
        if vel_y is not None:
            self.vel_y = vel_y
        if color is not None:
            # Обновляем цвет, если он изменился
            if width is not None and height is not None and self.image.get_size() != (width, height):
                self.image = pygame.Surface((width, height))
            self.image.fill(color)