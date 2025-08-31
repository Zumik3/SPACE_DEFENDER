import pygame
from utils.constants import enemy_strong_width, enemy_strong_height, enemy_normal_width, enemy_normal_height, enemy_speed, screen_height, white
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type):
        if enemy_type == 'strong':
            width, height = enemy_strong_width, enemy_strong_height
            health = 1
        else:
            width, height = enemy_normal_width, enemy_normal_height
            health = 1
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.type = enemy_type
        self.shoot_counter = random.randint(0, 29)  # for staggering

    def update(self):
        self.rect.y += enemy_speed

    def draw(self, renderer):
        if self.type == 'strong':
            renderer.draw_strong_enemy(self.rect)
        else:
            renderer.draw_normal_enemy(self.rect)

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def get_score(self):
        return 3 if self.type == 'strong' else 1

    def is_off_screen(self):
        return self.rect.top > screen_height

    def shoot(self, player_rect):
        if self.type == 'strong':
            start_pos = pygame.math.Vector2(self.rect.center)
            target_pos = pygame.math.Vector2(player_rect.center)
            if (target_pos - start_pos).length() > 0:
                direction = (target_pos - start_pos).normalize()
                vel = direction * 6  # enemy_bullet_speed
                return {'rect': pygame.Rect(start_pos.x, start_pos.y, 6, 6), 'vel': vel}
        return None

    @classmethod
    def create_random(cls, screen_width):
        if random.randint(1, 5) == 1:
            enemy_x = random.randint(0, screen_width - enemy_strong_width)
            return cls(enemy_x, -enemy_strong_height, 'strong')
        else:
            enemy_x = random.randint(0, screen_width - enemy_normal_width)
            return cls(enemy_x, -enemy_normal_height, 'normal')