import pygame
from utils.constants import *


class GameRenderer:
    """Класс для отрисовки игровых объектов"""
    
    def __init__(self, screen, renderer):
        self.screen = screen
        self.renderer = renderer
        
    def draw_game(self, player, bullets, enemy_bullets, enemies, powerups, score, player_lives, invincible=False):
        """Отрисовка игрового экрана"""
        self.screen.fill(black)
        self.renderer.draw_starfield()
        
        if not invincible or (pygame.time.get_ticks() // 200) % 2 == 0:
            self.renderer.draw_player_ship(player.rect)
        # Рисуем врагов через рендерер
        for enemy in enemies:
            enemy.draw(self.renderer)
        # Рисуем бонусы
        powerups.draw(self.screen)
        # Рисуем пули игрока
        bullets.draw(self.screen)
        # Рисуем пули врагов
        enemy_bullets.draw(self.screen)
        self.renderer.draw_score(score)
        self.renderer.draw_lives(player_lives)
        pygame.display.update()