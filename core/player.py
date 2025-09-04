import pygame
from utils.constants import player_width, player_height, screen_width, screen_height, PIXEL_SIZE, player_body, player_wing, player_cockpit, player_engine

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Создаем изображение для спрайта
        self.image = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.invincible = False
        self.invincible_end_time = 0
        # Отрисовываем корабль в image
        self._draw_player_ship()

    def move(self, dx):
        self.rect.x += dx
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

    def make_invincible(self, duration=2000):
        self.invincible = True
        self.invincible_end_time = pygame.time.get_ticks() + duration

    def update(self):
        if self.invincible and pygame.time.get_ticks() > self.invincible_end_time:
            self.invincible = False

    def reset(self, x=None, y=None):
        """Сброс состояния игрока для повторного использования"""
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
        self.invincible = False
        self.invincible_end_time = 0
        # Перерисовываем корабль
        self._draw_player_ship()
        
    def _draw_pixel(self, x, y, color):
        pygame.draw.rect(self.image, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))
        
    def _draw_player_ship(self):
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Рисуем корабль
        for i in range(5): self._draw_pixel((3+i)*PIXEL_SIZE, 2*PIXEL_SIZE, player_body)
        for i in range(3): self._draw_pixel((4+i)*PIXEL_SIZE, 3*PIXEL_SIZE, player_body)
        for i in range(11): self._draw_pixel(i*PIXEL_SIZE, 4*PIXEL_SIZE, player_wing)
        for i in range(7): self._draw_pixel((2+i)*PIXEL_SIZE, 5*PIXEL_SIZE, player_wing)
        self._draw_pixel(5*PIXEL_SIZE, 1*PIXEL_SIZE, player_cockpit)
        self._draw_pixel(4*PIXEL_SIZE, 6*PIXEL_SIZE, player_engine)
        self._draw_pixel(6*PIXEL_SIZE, 6*PIXEL_SIZE, player_engine)
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        return True