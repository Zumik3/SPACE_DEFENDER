import pygame
import random
from ui.renderer import Renderer
from utils.sound_manager import SoundManager
from core.player import Player
from core.enemy import Enemy
from core.bullet import Bullet
from utils.constants import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Star Game")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self.sound_manager = SoundManager()
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.player_lives = 3
        x = (screen_width - player_width) // 2
        y = screen_height - player_height - 10
        self.player = Player(x, y)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.renderer.prepare_starfield()
        self.sound_manager.play_music()

    def fade_out(self, duration=2000):
        fade_start_time = pygame.time.get_ticks()
        fade_duration = duration
        # Создаем поверхность для затухания
        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill((0, 0, 0))

        while pygame.time.get_ticks() - fade_start_time < fade_duration:
            # Вычисляем прогресс затухания (от 0 до 1)
            progress = (pygame.time.get_ticks() - fade_start_time) / fade_duration
            alpha = int(progress * 255)  # От 0 до 255

            # Уменьшаем громкость музыки пропорционально прогрессу
            self.sound_manager.set_music_volume(1.0 - progress)

            # Рисуем затемнение
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        # Полностью останавливаем музыку
        self.sound_manager.stop_music()

    def update(self):
        self.player.update()
        self.renderer.update_starfield()

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
            if not self.player.invincible and self.player.collides_with(enemy.rect):
                self.player_lives -= 1
                self.enemies.remove(enemy)
                self.player.make_invincible()
                self.sound_manager.play_explosion()
                if self.player_lives <= 0:
                    self.game_over = True

        # Player hit by enemy bullets
        if not self.player.invincible:
            for bullet in self.enemy_bullets[:]:
                if bullet.collides_with(self.player.rect):
                    self.player_lives -= 1
                    self.enemy_bullets.remove(bullet)
                    self.player.make_invincible()
                    if self.player_lives <= 0:
                        self.game_over = True
                    break

        # Player bullets hit enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.collides_with(enemy.rect):
                    self.bullets.remove(bullet)
                    if enemy.hit():
                        self.enemies.remove(enemy)
                        self.score += enemy.get_score()
                        self.sound_manager.play_explosion()
                    break

    def draw(self):
        self.screen.fill(black)
        self.renderer.draw_starfield()
        if not self.player.invincible or (pygame.time.get_ticks() // 200) % 2 == 0:
            self.renderer.draw_player_ship(self.player.rect)
        self.renderer.draw_enemies(self.enemies)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        self.renderer.draw_score(self.score)
        self.renderer.draw_lives(self.player_lives)
        pygame.display.update()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == PLAYER_SHOOT_EVENT:
                bullet = Bullet.player_bullet(self.player.rect)
                self.bullets.append(bullet)
                self.sound_manager.play_shoot()
            elif event.type == ENEMY_SPAWN_EVENT:
                enemy = Enemy.create_random(screen_width)
                self.enemies.append(enemy)
            elif event.type == ENEMY_SHOOT_EVENT:
                strong_enemies_on_screen = [e for e in self.enemies if e.type == 'strong' and e.rect.y < screen_height * (2/3)]
                if strong_enemies_on_screen:
                    shooter = random.choice(strong_enemies_on_screen)
                    start_pos = pygame.math.Vector2(shooter.rect.center)
                    target_pos = pygame.math.Vector2(self.player.rect.center)
                    if (target_pos - start_pos).length() > 0:
                        direction = (target_pos - start_pos).normalize()
                        vel = direction * enemy_bullet_speed
                        bullet = Bullet.enemy_bullet(start_pos, vel)
                        self.enemy_bullets.append(bullet)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-player_speed)
        if keys[pygame.K_RIGHT]:
            self.player.move(player_speed)

    def run(self):
        pygame.time.set_timer(PLAYER_SHOOT_EVENT, PLAYER_SHOOT_DELAY)
        pygame.time.set_timer(ENEMY_SPAWN_EVENT, ENEMY_SPAWN_DELAY)
        pygame.time.set_timer(ENEMY_SHOOT_EVENT, ENEMY_SHOOT_DELAY)

        while True:
            self.reset_game()
            self.game_over = False

            while not self.game_over:
                events = pygame.event.get()
                self.handle_events(events)
                self.handle_keys()
                self.update()
                self.draw()
                self.clock.tick(60)

            # Game Over Screen
            self.fade_out()
            # self.screen.fill(black)
            game_over_text = score_font.render("Game Over", True, white)
            final_score_text = score_font.render(f"Final Score: {self.score}", True, white)
            restart_text = restart_font.render("Press ENTER to restart", True, white)
            self.screen.blit(game_over_text, game_over_text.get_rect(center=(screen_width/2, screen_height/2 - 60)))
            self.screen.blit(final_score_text, final_score_text.get_rect(center=(screen_width/2, screen_height/2 + 10)))
            self.screen.blit(restart_text, restart_text.get_rect(center=(screen_width/2, screen_height/2 + 60)))
            pygame.display.update()

            # Wait for restart
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting_for_restart = False