import pygame
from utils.constants import *

class Powerup:
    def __init__(self, x, y, powerup_type):
        self.rect = pygame.Rect(x, y, POWERUP_SIZE, POWERUP_SIZE)
        self.type = powerup_type
        self.vel_y = POWERUP_SPEED
        if self.type == 'health':
            self.color = POWERUP_HEALTH_COLOR
        elif self.type == 'fire_rate':
            self.color = POWERUP_FIRE_COLOR

    def update(self):
        self.rect.y += self.vel_y

    def draw(self, screen):
        x, y = self.rect.x, self.rect.y
        if self.type == 'health':
            # Draw heart
            self.draw_pixel(x + 3*PIXEL_SIZE, y + 8*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 5*PIXEL_SIZE, y + 8*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 2*PIXEL_SIZE, y + 9*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 9*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 6*PIXEL_SIZE, y + 9*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 3*PIXEL_SIZE, y + 10*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 5*PIXEL_SIZE, y + 10*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 11*PIXEL_SIZE, self.color, screen)
        elif self.type == 'fire_rate':
            # Draw speed arrow (vertical line with arrow head)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 4*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 5*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 6*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 7*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 3*PIXEL_SIZE, y + 8*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 4*PIXEL_SIZE, y + 8*PIXEL_SIZE, self.color, screen)
            self.draw_pixel(x + 5*PIXEL_SIZE, y + 8*PIXEL_SIZE, self.color, screen)

    def draw_pixel(self, x, y, color, screen):
        pygame.draw.rect(screen, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

    def is_off_screen(self):
        return self.rect.top > screen_height