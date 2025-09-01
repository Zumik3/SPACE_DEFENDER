import pygame
from utils.constants import *

class PixelTitle:
    def __init__(self):
        # Определяем пиксельное изображение для каждой буквы названия
        # Каждая буква представлена как матрица пикселей (1 = цветной пиксель, 0 = пусто)
        # Увеличенный размер букв 7x9 пикселей для лучшей видимости
        self.letters = {
            'S': [
                [0, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 1, 1, 0],
                [0, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 0, 0, 0]
            ],
            'P': [
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0]
            ],
            'A': [
                [0, 0, 0, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 0, 0, 1, 1],
                [0, 1, 1, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1]
            ],
            'C': [
                [0, 0, 1, 1, 1, 1, 0],
                [0, 1, 1, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 0, 1, 1],
                [0, 0, 1, 1, 1, 1, 0]
            ],
            'E': [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1]
            ],
            'D': [
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 0, 0]
            ],
            'F': [
                [1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0]
            ],
            'N': [
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 1, 0, 0, 1, 1],
                [1, 1, 1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1, 1, 1],
                [1, 1, 0, 0, 1, 1, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 1]
            ],
            'R': [
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 0, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 0, 0],
                [1, 1, 0, 1, 0, 0, 0],
                [1, 1, 0, 0, 1, 0, 0],
                [1, 1, 0, 0, 0, 1, 0],
                [1, 1, 0, 0, 0, 0, 1]
            ],
            ' ': [  # Пробел
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
        }
        
        # Улучшенные космические цвета
        self.primary_color = (100, 200, 255)    # Ярко-голубой
        self.secondary_color = (255, 100, 255)  # Ярко-пурпурный
        self.accent_color = (100, 255, 100)     # Ярко-зеленый
        
        # Размер пикселя и отступы
        self.pixel_size = 6
        self.letter_spacing = 10
        self.word_spacing = 30
        
    def draw(self, screen, x, y):
        # Рисуем название "SPACE DEFENDER" по центру
        # Разделяем на два слова по центру экрана
        space_word = "SPACE"
        defender_word = "DEFENDER"
        
        # Вычисляем ширину каждого слова
        space_width = len(space_word) * 7 * self.pixel_size + (len(space_word) - 1) * self.letter_spacing
        defender_width = len(defender_word) * 7 * self.pixel_size + (len(defender_word) - 1) * self.letter_spacing
        
        # Центрируем каждое слово отдельно
        space_x = (screen_width - space_width) // 2
        defender_x = (screen_width - defender_width) // 2
        
        # Рисуем первое слово
        current_x = space_x
        for i, char in enumerate(space_word):
            if char in self.letters:
                self._draw_letter(screen, char, current_x, y, i)
                current_x += len(self.letters[char][0]) * self.pixel_size + self.letter_spacing
        
        # Рисуем второе слово ниже
        current_x = defender_x
        for i, char in enumerate(defender_word):
            if char in self.letters:
                self._draw_letter(screen, char, current_x, y + 80, i + len(space_word))
                current_x += len(self.letters[char][0]) * self.pixel_size + self.letter_spacing
        
    def _draw_letter(self, screen, letter, x, y, index):
        # Получаем матрицу пикселей для буквы
        pixel_matrix = self.letters[letter]
        
        # Выбираем цвет в зависимости от позиции буквы в названии
        color_options = [self.primary_color, self.secondary_color, self.accent_color]
        color = color_options[index % len(color_options)]
        
        # Рисуем каждый пиксель буквы
        for row in range(len(pixel_matrix)):
            for col in range(len(pixel_matrix[row])):
                if pixel_matrix[row][col] == 1:
                    # Рисуем пиксель
                    pixel_rect = pygame.Rect(
                        x + col * self.pixel_size,
                        y + row * self.pixel_size,
                        self.pixel_size,
                        self.pixel_size
                    )
                    pygame.draw.rect(screen, color, pixel_rect)
                    
                    # Добавляем более мягкое свечение
                    if self.pixel_size > 4:  # Только для достаточно больших пикселей
                        glow_surface = pygame.Surface((self.pixel_size + 4, self.pixel_size + 4), pygame.SRCALPHA)
                        glow_rect = pygame.Rect(2, 2, self.pixel_size, self.pixel_size)
                        pygame.draw.rect(glow_surface, (*color[:3], 80), glow_rect)
                        screen.blit(glow_surface, (x + col * self.pixel_size - 2, y + row * self.pixel_size - 2))