import pygame
import random
from utils.constants import *

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.vel_y = POWERUP_SPEED
        
        # Создаем изображение для спрайта
        self.image = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Рисуем бонус на изображении спрайта
        self.draw_powerup()

    def update(self):
        self.rect.y += self.vel_y
        
        # Автоматическое удаление, если бонус вышел за экран
        if self.rect.top > screen_height:
            self.kill()

    def draw_powerup(self):
        # Этот метод должен быть переопределен в подклассах
        pass

    def apply_effect(self, game):
        # Этот метод должен быть переопределен в подклассах
        pass

    def reset(self):
        """Сброс состояния бонуса для повторного использования (обычно не используется)"""
        # Для бонусов сброс обычно не требуется, так как они создаются заново
        # Но метод добавлен для совместимости с интерфейсом пула
        pass

    @staticmethod
    def drop_powerup(enemy, game):
        """Метод для определения, какой бонус должен выпасть при убийстве врага"""
        from core.enemy import StrongEnemy, NormalEnemy  # Import here to avoid circular imports
        
        r = random.random()
        # Use isinstance to check enemy type
        is_strong = isinstance(enemy, StrongEnemy)
        health_chance = POWERUP_HEALTH_CHANCE_STRONG if is_strong else POWERUP_HEALTH_CHANCE_NORMAL
        fire_chance = POWERUP_FIRE_CHANCE_STRONG if is_strong else POWERUP_FIRE_CHANCE_NORMAL
        
        if r < health_chance:
            x_spawn = enemy.rect.centerx - POWERUP_SIZE // 2
            # Создаем бонус через ObjectPoolManager
            if game.object_pool_manager:
                return game.object_pool_manager.get_object('powerup', 'health', x_spawn, enemy.rect.centery - 10)
            else:
                return HealthPowerup(x_spawn, enemy.rect.centery - 10)
        elif r < health_chance + fire_chance:
            x_spawn = enemy.rect.centerx - POWERUP_SIZE // 2
            # Создаем бонус через ObjectPoolManager
            if game.object_pool_manager:
                return game.object_pool_manager.get_object('powerup', 'fire_rate', x_spawn, enemy.rect.centery - 10)
            else:
                return FireRatePowerup(x_spawn, enemy.rect.centery - 10)
        
        return None
        
    def get_rect(self):
        return self.rect
        
    def is_active(self):
        # Используем стандартный метод alive() для проверки активности
        return self.alive()


class HealthPowerup(Powerup):
    def __init__(self, x, y):
        self.color = POWERUP_HEALTH_COLOR
        super().__init__(x, y)

    def draw_powerup(self):
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Draw heart (размер 5x4 пикселя, масштабированных в PIXEL_SIZE раз)
        self.draw_pixel(2*PIXEL_SIZE, 1*PIXEL_SIZE)
        self.draw_pixel(4*PIXEL_SIZE, 1*PIXEL_SIZE)
        self.draw_pixel(1*PIXEL_SIZE, 2*PIXEL_SIZE)
        self.draw_pixel(2*PIXEL_SIZE, 2*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 2*PIXEL_SIZE)
        self.draw_pixel(4*PIXEL_SIZE, 2*PIXEL_SIZE)
        self.draw_pixel(5*PIXEL_SIZE, 2*PIXEL_SIZE)
        self.draw_pixel(2*PIXEL_SIZE, 3*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 3*PIXEL_SIZE)
        self.draw_pixel(4*PIXEL_SIZE, 3*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 4*PIXEL_SIZE)

    def draw_pixel(self, x, y):
        pygame.draw.rect(self.image, self.color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

    def apply_effect(self, game):
        if game.state_manager:
            # Увеличиваем количество жизней через GameStateManager
            current_lives = game.state_manager.get_lives()
            game.state_manager.player_lives = current_lives + 1


class FireRatePowerup(Powerup):
    def __init__(self, x, y):
        self.color = POWERUP_FIRE_COLOR
        super().__init__(x, y)

    def draw_powerup(self):
        # Очищаем поверхность
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        
        # Draw speed arrow (вертикальная линия с наконечником)
        self.draw_pixel(3*PIXEL_SIZE, 1*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 2*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 3*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 4*PIXEL_SIZE)
        self.draw_pixel(2*PIXEL_SIZE, 5*PIXEL_SIZE)
        self.draw_pixel(3*PIXEL_SIZE, 5*PIXEL_SIZE)
        self.draw_pixel(4*PIXEL_SIZE, 5*PIXEL_SIZE)

    def draw_pixel(self, x, y):
        pygame.draw.rect(self.image, self.color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

    def apply_effect(self, game):
        if game.state_manager:
            game.shoot_delay = max(100, game.shoot_delay - FIRE_RATE_BOOST)
            pygame.time.set_timer(PLAYER_SHOOT_EVENT, game.shoot_delay)