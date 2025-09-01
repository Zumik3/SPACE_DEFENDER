import pygame
from utils.constants import player_width, player_height, screen_width, screen_height
from core.game_object import GameObject

class Player(pygame.sprite.Sprite, GameObject):
    def __init__(self, x, y):
        super().__init__()
        # Создаем изображение для спрайта (временно пустая поверхность)
        self.image = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.invincible = False
        self.invincible_end_time = 0

    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    def make_invincible(self, duration=2000):
        self.invincible = True
        self.invincible_end_time = pygame.time.get_ticks() + duration

    def update(self):
        if self.invincible and pygame.time.get_ticks() > self.invincible_end_time:
            self.invincible = False

    def draw(self, renderer):
        renderer.draw_player_ship(self.rect)
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        return True