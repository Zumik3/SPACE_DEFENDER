import pygame
from utils.constants import *
import os

class Menu:
    def __init__(self, screen):
        self.screen = screen
        
        # Определяем путь к шрифту
        font_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'PressStart2P-Regular.ttf')
        
        # Проверяем, существует ли файл шрифта
        if os.path.exists(font_path):
            # Используем шрифт Press Start 2P
            self.font_large = pygame.font.Font(font_path, 48)
            self.font_medium = pygame.font.Font(font_path, 36)
        else:
            # Если шрифт не найден, используем системный шрифт
            self.font_large = pygame.font.SysFont("Verdana", 48)
            self.font_medium = pygame.font.SysFont("Verdana", 36)
            
        self.selected_option = 0
        self.options = ["New Game", "Settings", "Exit"]
        
    def draw(self):
        self.screen.fill(black)
        
        # Рисуем название игры
        title_text = self.font_large.render("STAR GATE", True, white)
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 100))
        self.screen.blit(title_text, title_rect)
        
        # Рисуем пункты меню
        for i, option in enumerate(self.options):
            color = white if i != self.selected_option else (255, 255, 0)  # Выделенный пункт желтого цвета
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i * 50))
            self.screen.blit(text, text_rect)
            
        pygame.display.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # New Game
                        return "new_game"
                    elif self.selected_option == 1:  # Settings
                        return "settings"
                    elif self.selected_option == 2:  # Exit
                        return "exit"
        return None