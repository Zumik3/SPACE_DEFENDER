import pygame
from utils.constants import *

class PixelTitle:
    def __init__(self):
        # Создаем более впечатляющее пиксельное изображение для космической тематики
        # Большой логотип размером 15x15 пикселей
        self.logo = [
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        ]
        
        # Цвета для пикселей в космическом стиле
        self.colors = [
            (100, 100, 255),   # Синий
            (100, 255, 255),   # Голубой
            (255, 100, 255),   # Пурпурный
            (255, 255, 100),   # Желтый
            (100, 255, 100),   # Зеленый
            (255, 100, 100),   # Красный
        ]
        
        # Размер пикселя
        self.pixel_size = 8
        
    def draw(self, screen, x, y):
        # Рисуем космический логотип
        for row in range(len(self.logo)):
            for col in range(len(self.logo[row])):
                if self.logo[row][col] == 1:
                    # Выбираем цвет в зависимости от позиции
                    color_index = (row + col) % len(self.colors)
                    color = self.colors[color_index]
                    
                    # Рисуем пиксель
                    pixel_rect = pygame.Rect(
                        x + col * self.pixel_size,
                        y + row * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size
                    )
                    pygame.draw.rect(screen, color, pixel_rect)
                    
                    # Добавляем свечение вокруг пикселей
                    glow_rect = pygame.Rect(
                        x + col * self.pixel_size - 1,
                        y + row * self.pixel_size - 1,
                        self.pixel_size + 2,
                        self.pixel_size + 2
                    )
                    # Создаем поверхность для свечения
                    glow_surface = pygame.Surface((self.pixel_size + 2, self.pixel_size + 2), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (*color[:3], 50), (1, 1, self.pixel_size, self.pixel_size))
                    screen.blit(glow_surface, glow_rect)