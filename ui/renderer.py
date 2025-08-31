import pygame
import random
from utils.constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.starfield = [[], [], []]
        self.prepare_starfield()

    def prepare_starfield(self):
        for i in range(3):
            speed = 0.5 + i * 0.5
            size = 1 + i
            for _ in range(50):
                star = {
                    'rect': pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), size, size),
                    'speed': speed,
                    'color': random.choice(star_colors)
                }
                self.starfield[i].append(star)

    def update_starfield(self):
        for layer in self.starfield:
            for star in layer:
                star['rect'].y += star['speed']
                if star['rect'].top > screen_height:
                    star['rect'].y = -star['rect'].height
                    star['rect'].x = random.randint(0, screen_width)

    def draw_starfield(self):
        for layer in self.starfield:
            for star in layer:
                pygame.draw.rect(self.screen, star['color'], star['rect'])

    def draw_pixel(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

    def draw_player_ship(self, rect):
        x, y = rect.topleft
        for i in range(5): self.draw_pixel(x + (3+i)*PIXEL_SIZE, y + 2*PIXEL_SIZE, player_body)
        for i in range(3): self.draw_pixel(x + (4+i)*PIXEL_SIZE, y + 3*PIXEL_SIZE, player_body)
        for i in range(11): self.draw_pixel(x + i*PIXEL_SIZE, y + 4*PIXEL_SIZE, player_wing)
        for i in range(7): self.draw_pixel(x + (2+i)*PIXEL_SIZE, y + 5*PIXEL_SIZE, player_wing)
        self.draw_pixel(x + 5*PIXEL_SIZE, y + 1*PIXEL_SIZE, player_cockpit)
        self.draw_pixel(x + 4*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine)
        self.draw_pixel(x + 6*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine)

    def draw_normal_enemy(self, rect):
        x, y = rect.topleft
        for i in range(5): self.draw_pixel(x + (1+i)*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_normal_body)
        self.draw_pixel(x + 3*PIXEL_SIZE, y + 1*PIXEL_SIZE, white)
        for i in range(7): self.draw_pixel(x + i*PIXEL_SIZE, y + 3*PIXEL_SIZE, enemy_normal_body)
        self.draw_pixel(x + 1*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_normal_highlight)
        self.draw_pixel(x + 5*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_normal_highlight)
        self.draw_pixel(x + 3*PIXEL_SIZE, y + 4*PIXEL_SIZE, player_engine)

    def draw_strong_enemy(self, rect):
        x, y = rect.topleft
        for i in range(7): self.draw_pixel(x + (1+i)*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_strong_body)
        for i in range(5): self.draw_pixel(x + (2+i)*PIXEL_SIZE, y + 3*PIXEL_SIZE, enemy_strong_body)
        self.draw_pixel(x + 4*PIXEL_SIZE, y + 1*PIXEL_SIZE, enemy_strong_core)
        for i in range(9): self.draw_pixel(x + i*PIXEL_SIZE, y + 4*PIXEL_SIZE, enemy_strong_body)
        for i in range(7): self.draw_pixel(x + (1+i)*PIXEL_SIZE, y + 5*PIXEL_SIZE, enemy_strong_body)
        self.draw_pixel(x + 2*PIXEL_SIZE, y + 4*PIXEL_SIZE, enemy_strong_highlight)
        self.draw_pixel(x + 6*PIXEL_SIZE, y + 4*PIXEL_SIZE, enemy_strong_highlight)
        self.draw_pixel(x + 3*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine)
        self.draw_pixel(x + 5*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            if enemy.type == 'strong':
                self.draw_strong_enemy(enemy.rect)
            else:
                self.draw_normal_enemy(enemy.rect)

    def draw_bullets(self, bullets, color):
        for bullet in bullets:
            pygame.draw.rect(self.screen, color, bullet['rect'])

    def draw_heart(self, x, y):
        self.draw_pixel(x + 1*PIXEL_SIZE, y, heart_color)
        self.draw_pixel(x + 3*PIXEL_SIZE, y, heart_color)
        for j in range(5): self.draw_pixel(x + j*PIXEL_SIZE, y + 1*PIXEL_SIZE, heart_color)
        for j in range(3): self.draw_pixel(x + (1+j)*PIXEL_SIZE, y + 2*PIXEL_SIZE, heart_color)
        self.draw_pixel(x + 2*PIXEL_SIZE, y + 3*PIXEL_SIZE, heart_color)

    def draw_lives(self, lives):
        heart_width = 5 * PIXEL_SIZE
        for i in range(lives):
            x = screen_width - (i + 1) * (heart_width + 10)
            y = 10
            self.draw_heart(x, y)

    def draw_score(self, score):
        score_text = score_font.render(f"Score: {score}", True, white)
        self.screen.blit(score_text, (10, 10))

    def fade_out_display(self, duration=2000):
        fade_start_time = pygame.time.get_ticks()
        fade_duration = duration
        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill((0, 0, 0))
        while pygame.time.get_ticks() - fade_start_time < fade_duration:
            progress = (pygame.time.get_ticks() - fade_start_time) / fade_duration
            alpha = int(progress * 255)
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(10)