import pygame
from ui.render_component import RenderComponent

class PlayerRenderComponent(RenderComponent):
    """Компонент отрисовки игрока"""
    def draw(self, player):
        if not player.invincible or (pygame.time.get_ticks() // 200) % 2 == 0:
            self.renderer.draw_player_ship(player.rect)

class EnemyRenderComponent(RenderComponent):
    """Компонент отрисовки врагов"""
    def draw(self, enemy):
        from core.enemy import StrongEnemy, NormalEnemy  # Import here to avoid circular imports
        if isinstance(enemy, StrongEnemy):
            self.renderer.draw_strong_enemy(enemy.rect)
        elif isinstance(enemy, NormalEnemy):
            self.renderer.draw_normal_enemy(enemy.rect)

class BulletRenderComponent(RenderComponent):
    """Компонент отрисовки пуль"""
    def draw(self, bullet):
        # Пули рисуются через pygame.sprite.Group, поэтому здесь может быть пусто
        pass

class PowerupRenderComponent(RenderComponent):
    """Компонент отрисовки бонусов"""
    def draw(self, powerup):
        # Бонусы рисуются через их собственный метод draw
        pass