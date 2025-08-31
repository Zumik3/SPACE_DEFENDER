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

    def play_music(self, loops=-1):
        self.music_sound.play(loops)
        self.music_sound.set_volume(1.0)

    def stop_music(self):
        if self.music_sound:
            self.music_sound.stop()

    def set_music_volume(self, volume):
        if self.music_sound:
            self.music_sound.set_volume(volume)

    def get_music_volume(self):
        if self.music_sound:
            return self.music_sound.get_volume()
        return 1.0

    def play_shoot(self):
        self.shoot_sound.play()

    def play_explosion(self):
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