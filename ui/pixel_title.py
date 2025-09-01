import pygame
from utils.constants import *

class PixelTitle:
    def __init__(self):
        # Определяем пиксельное изображение для каждой буквы названия "STAR GATE"
        # Каждая буква представлена как матрица 5x5 пикселей (1 = цветной пиксель, 0 = пусто)
        self.letters = {
            'S': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 1, 1, 1, 0]
            ],
            'T': [
                [1, 1, 1, 1, 1],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0]
            ],
            'A': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1]
            ],
            'R': [
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1]
            ],
            'G': [
                [0, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 0, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 1, 0]
            ],
            'E': [
                [1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1]
            ],
            ' ': [  # Пробел
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]
        }
        
        # Цвета для пикселей в космическом стиле
        self.colors = [
            (100, 100, 255),   # Синий
            (100, 255, 255),   # Голубой
            (255, 100, 255),   # Пурпурный
            (255, 255, 100),   # Желтый
            (100, 255, 100),   # Зеленый
        ]
        
        # Размер пикселя и отступы
        self.pixel_size = 6
        self.letter_spacing = 10
        self.word_spacing = 20
        
    def draw(self, screen, x, y):
        # Рисуем название "STAR GATE"
        title = "STAR GATE"
        current_x = x
        
        for i, char in enumerate(title):
            if char in self.letters:
                self._draw_letter(screen, char, current_x, y)
                # Перемещаем позицию для следующей буквы
                current_x += len(self.letters[char][0]) * self.pixel_size + self.letter_spacing
                
                # Добавляем дополнительный отступ между словами
                if char == 'R':
                    current_x += self.word_spacing - self.letter_spacing
        
    def _draw_letter(self, screen, letter, x, y):
        # Получаем матрицу пикселей для буквы
        pixel_matrix = self.letters[letter]
        
        # Рисуем каждый пиксель буквы
        for row in range(len(pixel_matrix)):
            for col in range(len(pixel_matrix[row])):
                if pixel_matrix[row][col] == 1:
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