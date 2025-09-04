import pygame
from utils.constants import enemy_strong_width, enemy_strong_height, enemy_normal_width, enemy_normal_height, enemy_speed, screen_height, white, PIXEL_SIZE, enemy_normal_body, enemy_normal_highlight, enemy_strong_body, enemy_strong_core, enemy_strong_highlight, player_engine
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.type = enemy_type
        
        if self.type == 'strong':
            width, height = enemy_strong_width, enemy_strong_height
            health = 4  # Большие враги имеют 4 жизни
        else:
            width, height = enemy_normal_width, enemy_normal_height
            health = 2  # Маленькие враги имеют 2 жизни
            
        # Создаем изображение для спрайта
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.shoot_counter = random.randint(0, 29)  # for staggering
        # Отрисовываем врага в image
        self._draw_enemy()

    def update(self):
        self.rect.y += enemy_speed
        
        # Автоматическое удаление, если враг вышел за экран
        if self.rect.top > screen_height:
            self.kill()

    def _draw_pixel(self, x, y, color):
        pygame.draw.rect(self.image, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
    def _draw_normal_enemy(self):
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Рисуем обычного врага
        for i in range(5): self._draw_pixel((1+i)*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_body)
        self._draw_pixel(3*PIXEL_SIZE, 1*PIXEL_SIZE, white)
        for i in range(7): self._draw_pixel(i*PIXEL_SIZE, 3*PIXEL_SIZE, enemy_normal_body)
        self._draw_pixel(1*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_highlight)
        self._draw_pixel(5*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_highlight)
        self._draw_pixel(3*PIXEL_SIZE, 4*PIXEL_SIZE, player_engine)

    def _draw_strong_enemy(self):
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
        
    def _draw_enemy(self):
        if self.type == 'strong':
            self._draw_strong_enemy()
        else:
            self._draw_normal_enemy()

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
            
    def reset(self, x=None, y=None, enemy_type=None):
        """Сброс состояния врага для повторного использования"""
        # Если передан тип врага, обновляем его
        if enemy_type is not None and enemy_type != self.type:
            self.type = enemy_type
            # Обновляем размеры и здоровье в соответствии с новым типом
            if self.type == 'strong':
                width, height = enemy_strong_width, enemy_strong_height
                self.health = 4
            else:
                width, height = enemy_normal_width, enemy_normal_height
                self.health = 2
            # Обновляем размеры image и rect
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            
        # Обновляем позицию, если передана
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
            
        # Сбрасываем остальные параметры
        self.shoot_counter = random.randint(0, 29)
        # Перерисовываем врага в image
        self._draw_enemy()
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        # Используем стандартный метод alive() для проверки активности
        return self.alive()