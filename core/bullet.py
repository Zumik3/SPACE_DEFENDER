import pygame
from utils.constants import screen_width, screen_height

class Bullet:
    def __init__(self, x, y, vel_y, color, vel_x=0, width=4, height=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def is_off_screen(self):
        return (self.rect.bottom < 0 or
                self.rect.right < 0 or
                self.rect.left > screen_width or
                self.rect.top > screen_height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collides_with(self, other_rect):
        return self.rect.colliderect(other_rect)

    @classmethod
    def player_bullet(cls, player_rect):
        from utils.constants import bullet_color, bullet_speed
        return cls(player_rect.centerx - 2, player_rect.top, -bullet_speed, bullet_color, 0, 4, 10)

    @classmethod
    def enemy_bullet(cls, start_pos, vel, size=6):
        from utils.constants import enemy_bullet_color
        return cls(start_pos.x, start_pos.y, vel.y, enemy_bullet_color, vel.x, size, size)