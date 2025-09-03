import pygame
from utils.constants import *
from ui.ui_screen import UIScreen


class Settings(UIScreen):
    def __init__(self, screen, sound_manager, settings_manager=None, event_manager=None):
        super().__init__(screen, event_manager)
        self.sound_manager = sound_manager
        self.settings_manager = settings_manager
        
        # Значения из настроек или по умолчанию
        if self.settings_manager:
            self.music_volume = self.settings_manager.get("music_volume", 0.5)
            self.sfx_volume = self.settings_manager.get("sfx_volume", 0.5)
        else:
            self.music_volume = 0.5
            self.sfx_volume = 0.5
        
        # Округляем значения до 2 знаков после запятой
        self.music_volume = round(self.music_volume, 2)
        self.sfx_volume = round(self.sfx_volume, 2)
        
        # Выбранный пункт настроек
        self.selected_option = 0
        self.options = ["Music Volume", "SFX Volume", "Back to Menu"]
        
    def draw(self):
        self.screen.fill(black)
        
        # Рисуем заголовок
        title_text = settings_title_font.render("SETTINGS", True, white)
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 150))
        self.screen.blit(title_text, title_rect)
        
        # Рисуем пункты настроек
        for i, option in enumerate(self.options):
            if i == 2:  # Back to Menu
                # Выделение выбранного пункта
                color = (255, 255, 0) if i == self.selected_option else white
                text = settings_item_font.render(option, True, color)
                text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i * 50))
                self.screen.blit(text, text_rect)
            else:  # Volume settings
                # Выделение выбранного пункта
                color = (255, 255, 0) if i == self.selected_option else white
                # Формат: "Option Name: Value%"
                value = self.music_volume if i == 0 else self.sfx_volume
                text = settings_item_font.render(f"{option}: {int(value * 100)}%", True, color)
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
                    self.draw()  # Перерисовываем меню с новым выделенным пунктом
                elif event.key == pygame.K_DOWN:
                    # Перемещение вниз по пунктам настроек
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    self.draw()  # Перерисовываем меню с новым выделенным пунктом
                elif event.key == pygame.K_LEFT:
                    # Уменьшение значения выбранной настройки
                    if self.selected_option < 2:  # Только для настроек громкости
                        self.adjust_selected_option(-0.05)
                        self.draw()  # Перерисовываем меню с новыми значениями
                elif event.key == pygame.K_RIGHT:
                    # Увеличение значения выбранной настройки
                    if self.selected_option < 2:  # Только для настроек громкости
                        self.adjust_selected_option(0.05)
                        self.draw()  # Перерисовываем меню с новыми значениями
                elif event.key == pygame.K_RETURN:
                    # Выбор пункта меню
                    if self.selected_option == 2:  # Back to Menu
                        return "back"
                        
        return None
        
    def adjust_selected_option(self, delta):
        # Ограничиваем значение между 0 и 1
        if self.selected_option == 0:  # Music Volume
            self.music_volume = max(0, min(1, self.music_volume + delta))
            # Округляем до 2 знаков после запятой
            self.music_volume = round(self.music_volume, 2)
            self.sound_manager.set_music_volume(self.music_volume)
        elif self.selected_option == 1:  # SFX Volume
            self.sfx_volume = max(0, min(1, self.sfx_volume + delta))
            # Округляем до 2 знаков после запятой
            self.sfx_volume = round(self.sfx_volume, 2)
            self.sound_manager.set_sfx_volume(self.sfx_volume)
        
    def apply_settings(self):
        # Применяем настройки громкости
        self.sound_manager.set_music_volume(self.music_volume)
        self.sound_manager.set_sfx_volume(self.sfx_volume)
        
        # Сохраняем настройки, если есть SettingsManager
        if self.settings_manager:
            self.settings_manager.set("music_volume", self.music_volume)
            self.settings_manager.set("sfx_volume", self.sfx_volume)