import pygame
from core.base_enemy import Enemy
from utils.constants import (
    enemy_normal_width, enemy_normal_height, PIXEL_SIZE, enemy_normal_body, 
    enemy_normal_highlight, white, player_engine
)

class NormalEnemy(Enemy):
    """Класс для обычного врага"""
    
    def __init__(self, x, y):
        super().__init__(x, y, health=2, width=enemy_normal_width, height=enemy_normal_height)
        self._draw_enemy()
        
    def _draw_pixel(self, x, y, color):
        pygame.draw.rect(self.image, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
    def _draw_enemy(self):
        """Отрисовка обычного врага"""
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Рисуем обычного врага
        for i in range(5): self._draw_pixel((1+i)*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_body)
        self._draw_pixel(3*PIXEL_SIZE, 1*PIXEL_SIZE, white)
        for i in range(7): self._draw_pixel(i*PIXEL_SIZE, 3*PIXEL_SIZE, enemy_normal_body)
        self._draw_pixel(1*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_highlight)
        self._draw_pixel(5*PIXEL_SIZE, 2*PIXEL_SIZE, enemy_normal_highlight)
        self._draw_pixel(3*PIXEL_SIZE, 4*PIXEL_SIZE, player_engine)
        
    def reset(self, x=None, y=None, health=None):
        """Сброс состояния обычного врага"""
        super().reset(x, y, health if health is not None else 2)
        self._draw_enemy()