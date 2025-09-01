import pygame
from utils.constants import *

class PixelTitle:
    def __init__(self):
        # Определяем пиксельное изображение для каждой буквы названия "SPACE DEFENDER"
        # Каждая буква представлена как матрица пикселей (1 = цветной пиксель, 0 = пусто)
        self.letters = {
            'S': [
                [0, 1, 1, 1, 1],
                [1, 1, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 1, 1],
                [1, 1, 1, 1, 0]
            ],
            'P': [
                [1, 1, 1, 1, 0],
                [1, 1, 0, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0]
            ],
            'A': [
                [0, 1, 1, 1, 0],
                [1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 0, 0, 1],
                [1, 1, 0, 0, 1]
            ],
            'C': [
                [0, 1, 1, 1, 1],
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 1, 1, 1, 1]
            ],
            'E': [
                [1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1]
            ],
            'D': [
                [1, 1, 1, 1, 0],
                [1, 1, 0, 0, 1],
                [1, 1, 0, 0, 1],
                [1, 1, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ],
            'F': [
                [1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0]
            ],
            'N': [
                [1, 1, 0, 0, 1],
                [1, 1, 1, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 1, 0, 0, 1],
                [1, 1, 0, 0, 1]
            ],
            'R': [
                [1, 1, 1, 1, 0],
                [1, 1, 0, 0, 1],
                [1, 1, 1, 1, 0],
                [1, 1, 0, 1, 0],
                [1, 1, 0, 0, 1]
            ],
            ' ': [  # Пробел
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]
            ]
        }
        
        # Цвета для пикселей
        self.primary_color = (100, 200, 255)  # Голубой
        self.secondary_color = (200, 100, 255)  # Пурпурный
        self.glow_color = (100, 255, 255, 100)  # Светло-голубой с прозрачностью
        
        # Размер пикселя и отступы
        self.pixel_size = 5
        self.letter_spacing = 8
        self.word_spacing = 20
        
    def draw(self, screen, x, y):
        # Рисуем название "SPACE DEFENDER"
        title = "SPACE DEFENDER"
        current_x = x
        
        for i, char in enumerate(title):
            if char in self.letters:
                self._draw_letter(screen, char, current_x, y)
                # Перемещаем позицию для следующей буквы
                current_x += len(self.letters[char][0]) * self.pixel_size + self.letter_spacing
                
                # Добавляем дополнительный отступ между словами
                if char == 'E' and i == 4:  # После "SPACE"
                    current_x += self.word_spacing - self.letter_spacing
        
    def _draw_letter(self, screen, letter, x, y):
        # Получаем матрицу пикселей для буквы
        pixel_matrix = self.letters[letter]
        
        # Рисуем каждый пиксель буквы
        for row in range(len(pixel_matrix)):
            for col in range(len(pixel_matrix[row])):
                if pixel_matrix[row][col] == 1:
                    # Чередуем цвета для создания эффекта
                    if (row + col) % 2 == 0:
                        color = self.primary_color
                    else:
                        color = self.secondary_color
                    
                    # Рисуем пиксель
                    pixel_rect = pygame.Rect(
                        x + col * self.pixel_size,
                        y + row * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size
                    )
                    pygame.draw.rect(screen, color, pixel_rect)
                    
                    # Добавляем свечение
                    glow_rect = pygame.Rect(
                        x + col * self.pixel_size - 1,
                        y + row * self.pixel_size - 1,
                        self.pixel_size + 2,
                        self.pixel_size + 2
                    )
                    glow_surface = pygame.Surface((self.pixel_size + 2, self.pixel_size + 2), pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, self.glow_color, (1, 1, self.pixel_size, self.pixel_size))
                    screen.blit(glow_surface, glow_rect)