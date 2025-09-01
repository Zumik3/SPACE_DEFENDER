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
        
        # Позиции ползунков
        self.slider_width = 200
        self.slider_height = 20
        self.slider_y_offset = 50
        
        # Позиции ползунков
        self.music_slider_pos = (screen_width // 2 - self.slider_width // 2, screen_height // 2 - 20)
        self.sfx_slider_pos = (screen_width // 2 - self.slider_width // 2, screen_height // 2 + self.slider_y_offset - 20)
        
        # Состояние перетаскивания ползунков
        self.dragging_music = False
        self.dragging_sfx = False
        
    def draw(self):
        self.screen.fill(black)
        
        # Рисуем заголовок
        title_text = self.font_large.render("SETTINGS", True, white)
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Рисуем надписи
        music_text = self.font_medium.render("Music Volume", True, white)
        music_rect = music_text.get_rect(midright=(self.music_slider_pos[0] - 20, self.music_slider_pos[1] + self.slider_height // 2))
        self.screen.blit(music_text, music_rect)
        
        sfx_text = self.font_medium.render("SFX Volume", True, white)
        sfx_rect = sfx_text.get_rect(midright=(self.sfx_slider_pos[0] - 20, self.sfx_slider_pos[1] + self.slider_height // 2))
        self.screen.blit(sfx_text, sfx_rect)
        
        # Рисуем ползунки
        self.draw_slider(self.music_slider_pos, self.music_volume, self.dragging_music)
        self.draw_slider(self.sfx_slider_pos, self.sfx_volume, self.dragging_sfx)
        
        # Рисуем значения
        music_value = self.font_medium.render(f"{int(self.music_volume * 100)}%", True, white)
        music_value_rect = music_value.get_rect(midleft=(self.music_slider_pos[0] + self.slider_width + 20, self.music_slider_pos[1] + self.slider_height // 2))
        self.screen.blit(music_value, music_value_rect)
        
        sfx_value = self.font_medium.render(f"{int(self.sfx_volume * 100)}%", True, white)
        sfx_value_rect = sfx_value.get_rect(midleft=(self.sfx_slider_pos[0] + self.slider_width + 20, self.sfx_slider_pos[1] + self.slider_height // 2))
        self.screen.blit(sfx_value, sfx_value_rect)
        
        # Рисуем кнопку возврата
        back_text = self.font_medium.render("Press ESC to return", True, white)
        back_rect = back_text.get_rect(center=(screen_width/2, screen_height/2 + 150))
        self.screen.blit(back_text, back_rect)
        
        pygame.display.update()
        
    def draw_slider(self, pos, value, dragging):
        # Рисуем фон ползунка
        pygame.draw.rect(self.screen, (100, 100, 100), (pos[0], pos[1], self.slider_width, self.slider_height))
        
        # Рисуем заполненную часть ползунка
        fill_width = int(self.slider_width * value)
        fill_color = (255, 255, 0) if dragging else (200, 200, 200)
        pygame.draw.rect(self.screen, fill_color, (pos[0], pos[1], fill_width, self.slider_height))
        
        # Рисуем ползунок
        knob_x = pos[0] + int(self.slider_width * value) - 5
        knob_color = (255, 255, 0) if dragging else (255, 255, 255)
        pygame.draw.circle(self.screen, knob_color, (knob_x, pos[1] + self.slider_height // 2), 10)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    # Проверяем, нажат ли ползунок музыки
                    if self.is_mouse_over_slider(mouse_pos, self.music_slider_pos):
                        self.dragging_music = True
                    # Проверяем, нажат ли ползунок звуковых эффектов
                    elif self.is_mouse_over_slider(mouse_pos, self.sfx_slider_pos):
                        self.dragging_sfx = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Левая кнопка мыши
                    self.dragging_music = False
                    self.dragging_sfx = False
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_music or self.dragging_sfx:
                    mouse_pos = pygame.mouse.get_pos()
                    # Обновляем значение ползунка музыки
                    if self.dragging_music:
                        self.music_volume = self.get_slider_value(mouse_pos, self.music_slider_pos)
                        self.sound_manager.set_music_volume(self.music_volume)
                    # Обновляем значение ползунка звуковых эффектов
                    elif self.dragging_sfx:
                        self.sfx_volume = self.get_slider_value(mouse_pos, self.sfx_slider_pos)
                        self.sound_manager.set_sfx_volume(self.sfx_volume)
                        
        return None
        
    def is_mouse_over_slider(self, mouse_pos, slider_pos):
        knob_x = slider_pos[0] + int(self.slider_width * (self.music_volume if slider_pos == self.music_slider_pos else self.sfx_volume))
        knob_rect = pygame.Rect(knob_x - 10, slider_pos[1], 20, self.slider_height)
        return knob_rect.collidepoint(mouse_pos)
        
    def get_slider_value(self, mouse_pos, slider_pos):
        # Вычисляем значение ползунка на основе позиции мыши
        relative_x = mouse_pos[0] - slider_pos[0]
        value = max(0, min(1, relative_x / self.slider_width))
        return value
        
    def apply_settings(self):
        # Применяем настройки громкости
        self.sound_manager.set_music_volume(self.music_volume)
        self.sound_manager.set_sfx_volume(self.sfx_volume)