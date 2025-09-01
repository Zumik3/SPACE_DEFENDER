import pygame
from utils.constants import *
import os

class Settings:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        
        # Определяем путь к шрифту
        font_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'PressStart2P-Regular.ttf')
        
        # Проверяем, существует ли файл шрифта
        if os.path.exists(font_path):
            # Используем шрифт Press Start 2P
            self.font_large = pygame.font.Font(font_path, 36)
            self.font_medium = pygame.font.Font(font_path, 24)
        else:
            # Если шрифт не найден, используем системный шрифт
            self.font_large = pygame.font.SysFont("Verdana", 36)
            self.font_medium = pygame.font.SysFont("Verdana", 24)
        
        # Значения по умолчанию
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Выбранный пункт настроек
        self.selected_option = 0
        self.options = ["Music Volume", "SFX Volume", "Back to Menu"]
        
    def draw(self):
        self.screen.fill(black)
        
        # Рисуем заголовок
        title_text = self.font_large.render("SETTINGS", True, white)
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Рисуем пункты настроек
        for i, option in enumerate(self.options):
            if i == 2:  # Back to Menu
                # Выделение выбранного пункта
                color = (255, 255, 0) if i == self.selected_option else white
                text = self.font_medium.render(option, True, color)
                text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i * 50))
                self.screen.blit(text, text_rect)
            else:  # Volume settings
                # Выделение выбранного пункта
                color = (255, 255, 0) if i == self.selected_option else white
                # Формат: "Option Name: Value%"
                value = self.music_volume if i == 0 else self.sfx_volume
                text = self.font_medium.render(f"{option}: {int(value * 100)}%", True, color)
                text_rect = text.get_rect(center=(screen_width/2, screen_height/2 - 50 + i * 50))
                self.screen.blit(text, text_rect)
        
        pygame.display.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key == pygame.K_UP:
                    # Перемещение вверх по пунктам настроек
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    # Перемещение вниз по пунктам настроек
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_LEFT:
                    # Уменьшение значения выбранной настройки
                    if self.selected_option < 2:  # Только для настроек громкости
                        self.adjust_selected_option(-0.05)
                elif event.key == pygame.K_RIGHT:
                    # Увеличение значения выбранной настройки
                    if self.selected_option < 2:  # Только для настроек громкости
                        self.adjust_selected_option(0.05)
                elif event.key == pygame.K_RETURN:
                    # Выбор пункта меню
                    if self.selected_option == 2:  # Back to Menu
                        return "back"
                        
        return None
        
    def adjust_selected_option(self, delta):
        # Ограничиваем значение между 0 и 1
        if self.selected_option == 0:  # Music Volume
            self.music_volume = max(0, min(1, self.music_volume + delta))
            self.sound_manager.set_music_volume(self.music_volume)
        elif self.selected_option == 1:  # SFX Volume
            self.sfx_volume = max(0, min(1, self.sfx_volume + delta))
            self.sound_manager.set_sfx_volume(self.sfx_volume)
        
    def apply_settings(self):
        # Применяем настройки громкости
        self.sound_manager.set_music_volume(self.music_volume)
        self.sound_manager.set_sfx_volume(self.sfx_volume)