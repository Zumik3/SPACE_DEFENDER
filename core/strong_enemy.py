import random
import pygame
from core.base_enemy import Enemy
from utils.constants import (
    enemy_strong_width, enemy_strong_height, PIXEL_SIZE, enemy_strong_body, 
    enemy_strong_core, enemy_strong_highlight, player_engine, screen_height
)

class StrongEnemy(Enemy):
    """Класс для сильного врага"""
    
    def __init__(self, x, y):
        super().__init__(x, y, health=4, width=enemy_strong_width, height=enemy_strong_height)
        self._draw_enemy()
        
    def _draw_pixel(self, x, y, color):
        pygame.draw.rect(self.image, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
    def _draw_enemy(self):
        """Отрисовка сильного врага"""
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
        
    def shoot(self, player_rect):
        """Стрельба сильного врага"""
        # Сильный враг стреляет только если он находится в верхней 2/3 экрана
        if self.rect.y < screen_height * (2/3):
            self.shoot_counter = (self.shoot_counter + 1) % 30
            if self.shoot_counter == 0:
                # Вычисляем направление к игроку
                start_pos = pygame.math.Vector2(self.rect.centerx, self.rect.bottom)
                target_pos = pygame.math.Vector2(player_rect.centerx, player_rect.centery)
                if (target_pos - start_pos).length() > 0:
                    direction = (target_pos - start_pos).normalize()
                    return start_pos, direction
        return None, None
        
    def reset(self, x=None, y=None, health=None):
        """Сброс состояния сильного врага"""
        super().reset(x, y, health if health is not None else 4)
        self.shoot_counter = random.randint(0, 29)
        self._draw_enemy()
        
    def get_score(self):
        """Возвращает очки за убитого сильного врага"""
        return 12  # 3 очка за каждую единицу здоровья (4 жизни * 3 = 12)