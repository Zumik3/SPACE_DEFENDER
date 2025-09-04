import pygame
from utils.constants import black

class GameRenderer:
    """Класс для отрисовки игровых объектов"""
    
    def __init__(self, screen, renderer):
        self.screen = screen
        self.renderer = renderer
        
    def draw_game(self, player, bullets, enemy_bullets, enemies, powerups, score, invincible=False):
        """Отрисовка игрового экрана"""
        self.screen.fill(black)
        self.renderer.draw_starfield()
        
        # Рисуем пули игрока
        bullets.draw(self.screen)
        # Рисуем пули врагов
        enemy_bullets.draw(self.screen)
        # Рисуем врагов
        enemies.draw(self.screen)
        # Рисуем бонусы
        powerups.draw(self.screen)
        # Рисуем игрока с миганием, если он неуязвим
        if not invincible or (pygame.time.get_ticks() // 200) % 2 == 0:
            self.screen.blit(player.image, player.rect)
            
        self.renderer.draw_score(score)
        self.renderer.draw_lives(player.health)  # Отображаем здоровье игрока
        pygame.display.update()