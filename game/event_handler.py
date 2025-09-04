import random
import pygame
from utils.constants import (
    PLAYER_SHOOT_EVENT, ENEMY_SPAWN_EVENT, ENEMY_SHOOT_EVENT,
    bullet_speed, bullet_color, enemy_bullet_speed, enemy_bullet_color,
    player_speed
)


class GameEventHandler:
    """Класс для централизованной обработки событий игры"""
    
    def __init__(self, game_logic, object_pool_manager, enemy_factory, sound_manager):
        self.game_logic = game_logic
        self.object_pool_manager = object_pool_manager
        self.enemy_factory = enemy_factory
        self.sound_manager = sound_manager
        
    def handle_events(self, events, player, bullets, enemy_bullets, enemies, powerups, screen_width, screen_height):
        """Обработка событий pygame"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == PLAYER_SHOOT_EVENT:
                # Создание пуль игрока через пул объектов
                bullet = self.object_pool_manager.get_object(
                    'bullet',
                    player.rect.centerx - 2, 
                    player.rect.top, 
                    -bullet_speed, 
                    bullet_color, 
                    0, 
                    4, 
                    10
                )
                bullets.add(bullet)
                self.sound_manager.play_shoot()
            elif event.type == ENEMY_SPAWN_EVENT:
                enemy = self.enemy_factory.create_random_enemy(screen_width)
                enemies.add(enemy)
            elif event.type == ENEMY_SHOOT_EVENT:
                # Проверяем всех врагов на возможность стрельбы
                for enemy in enemies:
                    if hasattr(enemy, 'shoot'):
                        start_pos, direction = enemy.shoot(player.rect)
                        if start_pos is not None and direction is not None:
                            from utils.constants import enemy_bullet_speed, enemy_bullet_color
                            vel = direction * enemy_bullet_speed
                            # Создание пуль врагов через пул объектов
                            bullet = self.object_pool_manager.get_object(
                                'bullet',
                                start_pos.x, 
                                start_pos.y, 
                                vel.y, 
                                enemy_bullet_color, 
                                vel.x, 
                                6, 
                                6
                            )
                            enemy_bullets.add(bullet)
                        
    def handle_keys(self, keys, player):
        """Обработка нажатий клавиш"""
        if keys[pygame.K_LEFT]:
            player.move(-player_speed)
        if keys[pygame.K_RIGHT]:
            player.move(player_speed)