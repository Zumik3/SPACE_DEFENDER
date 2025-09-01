import pygame
import os
from .constants import *
import time

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.music_sound = None
        self.shoot_sound = None
        self.explosion_sound = None
        self.load_sounds()

    def load_sounds(self):
        script_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(os.path.dirname(script_dir), 'assets')
        self.music_sound = pygame.mixer.Sound(os.path.join(assets_dir, "music.wav"))
        self.shoot_sound = pygame.mixer.Sound(os.path.join(assets_dir, "shoot.wav"))
        self.explosion_sound = pygame.mixer.Sound(os.path.join(assets_dir, "explosion.wav"))
        
        # Инициализируем громкость
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Устанавливаем громкость по умолчанию, но не включаем музыку
        self.set_music_volume(self.music_volume)
        self.set_sfx_volume(self.sfx_volume)

    def play_music(self, loops=-1):
        # Устанавливаем текущую громкость перед воспроизведением
        if hasattr(self, 'music_volume') and self.music_sound:
            self.music_sound.set_volume(self.music_volume)
        if self.music_sound:
            self.music_sound.play(loops)

    def stop_music(self):
        if self.music_sound:
            self.music_sound.stop()

    def set_music_volume(self, volume):
        if self.music_sound:
            self.music_sound.set_volume(volume)
        # Сохраняем значение громкости
        self.music_volume = volume

    def set_sfx_volume(self, volume):
        if self.shoot_sound:
            self.shoot_sound.set_volume(volume)
        if self.explosion_sound:
            self.explosion_sound.set_volume(volume)
        # Сохраняем значение громкости
        self.sfx_volume = volume

    def get_music_volume(self):
        if self.music_sound:
            return self.music_sound.get_volume()
        return 1.0

    def play_shoot(self):
        # Применяем текущую громкость SFX перед воспроизведением
        if hasattr(self, 'sfx_volume') and self.shoot_sound:
            self.shoot_sound.set_volume(self.sfx_volume)
        if self.shoot_sound:
            self.shoot_sound.play()

    def play_explosion(self):
        # Применяем текущую громкость SFX перед воспроизведением
        if hasattr(self, 'sfx_volume') and self.explosion_sound:
            self.explosion_sound.set_volume(self.sfx_volume)
        if self.explosion_sound:
            self.explosion_sound.play()

    def fade_out_music(self, duration=2000):
        fade_start_time = pygame.time.get_ticks()
        fade_duration = duration
        start_volume = self.music_sound.get_volume()

        while pygame.time.get_ticks() - fade_start_time < fade_duration:
            progress = (pygame.time.get_ticks() - fade_start_time) / fade_duration
            self.music_sound.set_volume(start_volume * (1.0 - progress))
            pygame.time.delay(10)  # Small delay to prevent high CPU usage

        self.stop_music()