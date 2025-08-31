import pygame
from utils.constants import player_width, player_height, screen_width, screen_height

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, player_width, player_height)
        self.invincible = False
        self.invincible_end_time = 0

    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    def shoot(self):
        return {'rect': pygame.Rect(self.rect.centerx - 2, self.rect.top, 4, 10)}

    def make_invincible(self, duration=2000):
        self.invincible = True
        self.invincible_end_time = pygame.time.get_ticks() + duration

    def update(self):
        if self.invincible and pygame.time.get_ticks() > self.invincible_end_time:
            self.invincible = False

    def draw(self, renderer):
        renderer.draw_player_ship(self.rect)

    def collides_with(self, other_rect):
        return self.rect.colliderect(other_rect)