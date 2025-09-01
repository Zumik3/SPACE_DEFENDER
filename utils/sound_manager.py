import pygame
import os
from .constants import *
import time

class SoundManager:
    def __init__(self, settings_manager=None):
        pygame.mixer.init()
        self.music_sound = None
        self.menu_sound = None
        self.shoot_sound = None
        self.explosion_sound = None
        self.settings_manager = settings_manager
        self.load_sounds()
        
        # Инициализируем громкость из настроек или значениями по умолчанию
        if self.settings_manager:
            self.music_volume = self.settings_manager.get("music_volume", 0.5)
            self.sfx_volume = self.settings_manager.get("sfx_volume", 0.5)
        else:
            self.music_volume = 0.5
            self.sfx_volume = 0.5
            
        # Устанавливаем начальную громкость
        self.set_music_volume(self.music_volume)
        self.set_sfx_volume(self.sfx_volume)

    def load_sounds(self):
        script_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(os.path.dirname(script_dir), 'assets')
        self.music_sound = pygame.mixer.Sound(os.path.join(assets_dir, "music.wav"))
        self.menu_sound = pygame.mixer.Sound(os.path.join(assets_dir, "menu.wav"))
        self.shoot_sound = pygame.mixer.Sound(os.path.join(assets_dir, "shoot.wav"))
        self.explosion_sound = pygame.mixer.Sound(os.path.join(assets_dir, "explosion.wav"))

    def play_music(self, loops=-1):
        if self.music_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            self.music_sound.set_volume(self.music_volume)
            self.music_sound.play(loops)

    def play_menu_music(self, loops=-1):
        """Воспроизведение музыки меню"""
        if self.menu_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            self.menu_sound.set_volume(self.music_volume)
            self.menu_sound.play(loops)

    def stop_music(self):
        if self.music_sound:
            self.music_sound.stop()

    def stop_menu_music(self):
        """Остановка музыки меню"""
        if self.menu_sound:
            self.menu_sound.stop()

    def stop_all_music(self):
        """Остановка всей музыки"""
        self.stop_music()
        self.stop_menu_music()

    def set_music_volume(self, volume):
        # Ограничиваем значение между 0 и 1
        volume = max(0, min(1, volume))
        # Округляем до 2 знаков после запятой
        self.music_volume = round(volume, 2)
        if self.music_sound:
            self.music_sound.set_volume(self.music_volume)
        if self.menu_sound:
            self.menu_sound.set_volume(self.music_volume)
        # Сохраняем настройку, если есть SettingsManager
        if self.settings_manager:
            self.settings_manager.set("music_volume", self.music_volume)

    def set_sfx_volume(self, volume):
        # Ограничиваем значение между 0 и 1
        volume = max(0, min(1, volume))
        # Округляем до 2 знаков после запятой
        self.sfx_volume = round(volume, 2)
        if self.shoot_sound:
            self.shoot_sound.set_volume(self.sfx_volume)
        if self.explosion_sound:
            self.explosion_sound.set_volume(self.sfx_volume)
        # Сохраняем настройку, если есть SettingsManager
        if self.settings_manager:
            self.settings_manager.set("sfx_volume", self.sfx_volume)

    def get_music_volume(self):
        return self.music_volume

    def play_shoot(self):
        if self.shoot_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            self.shoot_sound.set_volume(self.sfx_volume)
            self.shoot_sound.play()

    def play_explosion(self):
        if self.explosion_sound:
            # Устанавливаем текущую громкость перед воспроизведением
            self.explosion_sound.set_volume(self.sfx_volume)
            self.explosion_sound.play()