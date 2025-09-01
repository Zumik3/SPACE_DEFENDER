import pygame
import os
from utils.constants import *

class PixelTitle:
    def __init__(self):
        # Загружаем изображение названия игры
        assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
        self.title_image = pygame.image.load(os.path.join(assets_dir, 'title.png')).convert_alpha()
        
        # Получаем оригинальные размеры изображения
        self.original_width = self.title_image.get_width()
        self.original_height = self.title_image.get_height()
        
        # Масштабируем изображение, если оно шире экрана
        if self.original_width > screen_width:
            scale_factor = screen_width / self.original_width
            new_width = int(self.original_width * scale_factor)
            new_height = int(self.original_height * scale_factor)
            self.title_image = pygame.transform.scale(self.title_image, (new_width, new_height))
        
        # Получаем финальные размеры изображения
        self.width = self.title_image.get_width()
        self.height = self.title_image.get_height()
        
    def draw(self, screen, x, y):
        # Рисуем изображение названия игры
        # Центрируем по экрану, если координаты (0, 0)
        if x == 0 and y == 0:
            x = (screen_width - self.width) // 2
            y = screen_height // 2 - 200  # Подняли еще выше
            
        screen.blit(self.title_image, (x, y))