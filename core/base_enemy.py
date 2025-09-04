import random
import pygame
from utils.constants import enemy_speed, screen_height

class Enemy(pygame.sprite.Sprite):
    """Базовый класс для всех врагов"""
    
    def __init__(self, x, y, health, width, height):
        super().__init__()
        self.health = health
        self.max_health = health
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shoot_counter = random.randint(0, 29)  # for staggering
        
    def update(self):
        """Общая логика обновления для всех врагов"""
        self.rect.y += enemy_speed
        
        # Автоматическое удаление, если враг вышел за экран
        if self.rect.top > screen_height:
            self.kill()
            
    def hit(self, damage=1):
        """Урон врагу"""
        self.health -= damage
        return self.health <= 0
        
    def reset(self, x=None, y=None, health=None):
        """Сброс состояния врага для повторного использования"""
        if x is not None:
            self.rect.x = x
        if y is not None:
            self.rect.y = y
        if health is not None:
            self.health = health
        else:
            self.health = self.max_health
        self.shoot_counter = random.randint(0, 29)
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        return self.alive()
        
    def get_score(self):
        """Возвращает очки за убитого врага по умолчанию"""
        return self.max_health  # 1 очко за каждую единицу здоровья