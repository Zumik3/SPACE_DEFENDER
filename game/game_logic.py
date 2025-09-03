import pygame
import random
from ui.renderer import Renderer
from utils.sound_manager import SoundManager
from core.player import Player
from core.enemy import Enemy
from core.bullet import Bullet
from core.powerup import Powerup
from utils.constants import *
from game.object_pool import ObjectPool
from core.enemy_factory import EnemyFactory

class Game:
    def __init__(self, sound_manager=None):
        self.sound_manager = sound_manager
        # Объекты пула и фабрика теперь передаются извне
        self.object_pool_manager = None
        self.enemy_factory = None
        self.renderer = None
        # Добавляем новые компоненты
        self.state_manager = None
        self.event_handler = None
        self.game_renderer = None
        self.event_manager = None
        self.reset_game()
        self.game_over = False

    def init_pygame(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        # Renderer теперь передается из GameManager
        # self.renderer = Renderer(self.screen)
        # SoundManager теперь всегда передается из GameManager
        # if self.sound_manager is None:
        #     self.sound_manager = SoundManager()

    def reset_game(self):
        if self.state_manager:
            self.state_manager.reset()
        x = (screen_width - player_width) // 2
        y = screen_height - player_height - 10
        # Создаем игрока через ObjectPoolManager
        if self.object_pool_manager:
            self.player = self.object_pool_manager.get_object('player', x, y)
        else:
            self.player = Player(x, y)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.shoot_delay = PLAYER_SHOOT_DELAY
        # Подготовка звездного поля теперь происходит в start_level
        # if hasattr(self, 'renderer'):
        #     self.renderer.prepare_starfield()
        # Не включаем музыку здесь, она включается в методе run

    def add_powerup(self, type, x, y):
        # Этот метод больше не нужен, так как мы используем новый подход к бонусам
        pass

    def fade_out(self, duration=2000):
        """Одновременное затухание музыки и экрана"""
        if not self.sound_manager or not hasattr(self, 'renderer') or not hasattr(self, 'clock') or not self.renderer:
            return
            
        fade_start_time = pygame.time.get_ticks()
        fade_duration = duration
        
        # Получаем начальную громкость музыки
        start_volume = self.sound_manager.get_music_volume()
        
        # Создаем поверхность для затухания
        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill((0, 0, 0))

        while pygame.time.get_ticks() - fade_start_time < fade_duration:
            # Вычисляем прогресс затухания (от 0 до 1)
            progress = (pygame.time.get_ticks() - fade_start_time) / fade_duration
            
            # Уменьшаем громкость музыки пропорционально прогрессу
            current_music_volume = start_volume * (1.0 - progress)
            self.sound_manager.set_music_volume(current_music_volume)
            
            # Рисуем затемнение экрана
            alpha = int(progress * 255)
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        # Полностью останавливаем музыку
        self.sound_manager.stop_music()
        # Восстанавливаем исходную громкость для следующего запуска
        self.sound_manager.set_music_volume(start_volume)

    def update(self):
        self.player.update()
        self.renderer.update_starfield()

        # Update all sprite groups
        self.bullets.update()
        self.enemy_bullets.update()
        self.enemies.update()
        self.powerups.update()

        # Normal enemy independent shoot
        for enemy in self.enemies:
            if enemy.type == 'normal' and enemy.rect.y < screen_height * (2/3) and random.random() < 0.001:
                start_pos = pygame.math.Vector2(enemy.rect.centerx, enemy.rect.bottom)
                vel = (0, ENEMY_NORMAL_SPEED)
                # Используем пул объектов для создания пуль
                bullet = self.object_pool_manager.get_object(
                    'bullet',
                    start_pos.x, 
                    start_pos.y, 
                    vel[1], 
                    enemy_bullet_color, 
                    vel[0], 
                    4, 
                    4
                )
                self.enemy_bullets.add(bullet)

        # Check collisions between player and enemies
        if not self.player.invincible:
            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
            for enemy in enemy_hits:
                if self.state_manager:
                    game_over = self.state_manager.lose_life()
                    self.player.make_invincible()
                    self.sound_manager.play_explosion()
                    # Возвращаем врага в пул
                    if enemy.active and self.object_pool_manager:
                        self.object_pool_manager.return_object('enemy', enemy)
                    if game_over:
                        self.game_over = True
                        # Уведомляем подписчиков об окончании игры
                        if self.event_manager:
                            self.event_manager.notify("game_over", {"score": self.state_manager.get_score()})

        # Check collisions between player and enemy bullets
        if not self.player.invincible:
            bullet_hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
            for bullet in bullet_hits:
                if self.state_manager:
                    game_over = self.state_manager.lose_life()
                    self.player.make_invincible()
                    # Возвращаем пулю в пул
                    if bullet.active and self.object_pool_manager:
                        self.object_pool_manager.return_object('bullet', bullet)
                    if game_over:
                        self.game_over = True
                        # Уведомляем подписчиков об окончании игры
                        if self.event_manager:
                            self.event_manager.notify("game_over", {"score": self.state_manager.get_score()})

        # Check collisions between player and powerups
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hits:
            self.sound_manager.play_explosion()
            powerup.apply_effect(self)
            # Уведомляем подписчиков о получении бонуса
            if self.event_manager:
                self.event_manager.notify("powerup_collected", {"type": type(powerup).__name__})

        # Check collisions between player bullets and enemies
        bullet_hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet, hit_enemies in bullet_hits.items():
            for enemy in hit_enemies:
                # Враг теряет одну единицу здоровья
                if enemy.hit():
                    # Враг умирает
                    enemy.kill()
                    # Drop powerups only when enemy dies
                    powerup = Powerup.drop_powerup(enemy, self)
                    if powerup:
                        self.powerups.add(powerup)
                    if self.state_manager:
                        self.state_manager.update_score(enemy.get_score())
                        # Уведомляем подписчиков об изменении счета
                        if self.event_manager:
                            self.event_manager.notify("score_updated", {"score": self.state_manager.get_score()})
                    self.sound_manager.play_explosion()
                    # Возвращаем врага в пул
                    if enemy.active and self.object_pool_manager:
                        self.object_pool_manager.return_object('enemy', enemy)
                # Возвращаем пулю в пул
                if bullet.active and self.object_pool_manager:
                    self.object_pool_manager.return_object('bullet', bullet)

    def draw(self):
        if self.game_renderer and self.state_manager:
            self.game_renderer.draw_game(
                self.player,
                self.bullets,
                self.enemy_bullets,
                self.enemies,
                self.powerups,
                self.state_manager.get_score(),
                self.state_manager.get_lives(),
                self.player.invincible
            )

    def handle_events(self, events):
        if self.event_handler:
            self.event_handler.handle_events(
                events,
                self.player,
                self.bullets,
                self.enemy_bullets,
                self.enemies,
                self.powerups,
                screen_width,
                screen_height
            )

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if self.event_handler:
            self.event_handler.handle_keys(keys, self.player)

    def start_level(self):
        """Единая точка запуска уровня"""
        # Подготовка звездного поля теперь происходит здесь
        if hasattr(self, 'renderer') and self.renderer:
            self.renderer.prepare_starfield()
        # Восстанавливаем громкость музыки из настроек перед запуском
        # Убеждаемся, что громкость установлена правильно
        if self.sound_manager:
            # Устанавливаем громкость из настроек
            if hasattr(self.sound_manager, 'music_volume'):
                self.sound_manager.set_music_volume(self.sound_manager.music_volume)
            self.sound_manager.play_music()
        pygame.time.set_timer(PLAYER_SHOOT_EVENT, self.shoot_delay)
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_DELAY)
        pygame.time.set_timer(ENEMY_SHOOT_EVENT, ENEMY_SHOOT_DELAY)

        self.game_over = False
        while not self.game_over:
            events = pygame.event.get()
            self.handle_events(events)
            self.handle_keys()
            self.update()
            self.draw()
            self.clock.tick(60)
            
    def run(self, screen):
        """Основной метод запуска игры"""
        self.init_pygame(screen)
        
        # Игровой цикл с возможностью перезапуска
        while True:
            # Запускаем уровень
            self.start_level()
            
            # Game Over Screen
            self.fade_out()
            
            # Показываем меню Game Over и ждем выбора
            restart = self.show_game_over_menu()
            if not restart:
                break  # Выход в главное меню
                
        return True  # Возвращаемся в главное меню
        
    def show_game_over_menu(self):
        """Показывает меню Game Over и возвращает True для перезапуска или False для выхода"""
        if self.game_renderer and self.state_manager:
            # Создаем экран окончания игры
            from ui.game_over import GameOverScreen
            game_over_screen = GameOverScreen(self.screen, self.event_manager)
            
            # Отображаем начальное меню
            game_over_screen.draw(self.state_manager.get_score())

            # Wait for menu selection
            waiting_for_selection = True
            while waiting_for_selection:
                action = game_over_screen.handle_events()
                if action == "restart":
                    self.reset_game()
                    return True
                elif action == "main_menu":
                    return False
                elif action == "exit":
                    pygame.quit()
                    quit()
                elif action == "redraw":
                    game_over_screen.draw()