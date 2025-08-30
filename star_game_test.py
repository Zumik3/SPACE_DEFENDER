import pygame
import random
import os

# --- Инициализация Pygame ---
pygame.init()
pygame.mixer.init()

# --- Настройки экрана и стиля ---
PIXEL_SIZE = 4
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Game")

# --- Цвета ---
black = (0, 0, 0); white = (255, 255, 255)
player_body = (200, 200, 200); player_wing = (0, 200, 0); player_cockpit = (100, 200, 255); player_engine = (255, 165, 0)
bullet_color = (255, 255, 0)
enemy_bullet_color = (255, 100, 100)
heart_color = (255, 50, 50)
enemy_normal_body = (200, 40, 40); enemy_normal_highlight = (255, 100, 100)
enemy_strong_body = (150, 50, 180); enemy_strong_highlight = (200, 100, 220); enemy_strong_core = (255, 0, 0)
star_colors = [(100, 100, 100), (180, 180, 180), (255, 255, 255)]

# --- Настройки игры ---
clock = pygame.time.Clock()
player_width = 11 * PIXEL_SIZE; player_height = 7 * PIXEL_SIZE
player_speed = 7
bullet_speed = 10
enemy_bullet_speed = 6
enemy_normal_width = 7 * PIXEL_SIZE; enemy_normal_height = 5 * PIXEL_SIZE
enemy_strong_width = 9 * PIXEL_SIZE; enemy_strong_height = 7 * PIXEL_SIZE
enemy_speed = 4

# --- Глобальные переменные состояния ---
score = 0
player_lives = 3
player_rect = pygame.Rect(0, 0, player_width, player_height)
bullets = []
enemy_bullets = []
enemies = []
player_invincible = False
player_invincible_end_time = 0
starfield = [[], [], []] # Три слоя для параллакса

# --- Таймеры ---
PLAYER_SHOOT_EVENT = pygame.USEREVENT + 1; ENEMY_SPAWN_EVENT = pygame.USEREVENT + 2; ENEMY_SHOOT_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(PLAYER_SHOOT_EVENT, 300)
pygame.time.set_timer(ENEMY_SPAWN_EVENT, 900)
pygame.time.set_timer(ENEMY_SHOOT_EVENT, 2000)

# --- Звуки ---
script_dir = os.path.dirname(os.path.abspath(__file__))
music_sound = pygame.mixer.Sound(os.path.join(script_dir, "music.wav"))
shoot_sound = pygame.mixer.Sound(os.path.join(script_dir, "shoot.wav"))
explosion_sound = pygame.mixer.Sound(os.path.join(script_dir, "explosion.wav"))

# --- Шрифты ---
score_font = pygame.font.SysFont("Verdana", 24)
game_over_font = pygame.font.SysFont("Verdana", 60)
restart_font = pygame.font.SysFont("Verdana", 30)

# --- Функции подготовки и отрисовки ---
def prepare_starfield():
    for i in range(3):
        speed = 0.5 + i * 0.5
        size = 1 + i
        for _ in range(50):
            star = {
                'rect': pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), size, size),
                'speed': speed,
                'color': random.choice(star_colors)
            }
            starfield[i].append(star)

def draw_starfield():
    for layer in starfield:
        for star in layer:
            pygame.draw.rect(screen, star['color'], star['rect'])

def draw_pixel(x, y, color):
    pygame.draw.rect(screen, color, (x, y, PIXEL_SIZE, PIXEL_SIZE))

def draw_player_ship(rect):
    x, y = rect.topleft
    for i in range(5): draw_pixel(x + (3+i)*PIXEL_SIZE, y + 2*PIXEL_SIZE, player_body)
    for i in range(3): draw_pixel(x + (4+i)*PIXEL_SIZE, y + 3*PIXEL_SIZE, player_body)
    for i in range(11): draw_pixel(x + i*PIXEL_SIZE, y + 4*PIXEL_SIZE, player_wing)
    for i in range(7): draw_pixel(x + (2+i)*PIXEL_SIZE, y + 5*PIXEL_SIZE, player_wing)
    draw_pixel(x + 5*PIXEL_SIZE, y + 1*PIXEL_SIZE, player_cockpit)
    draw_pixel(x + 4*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine); draw_pixel(x + 6*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine)

def draw_normal_enemy(rect):
    x, y = rect.topleft
    for i in range(5): draw_pixel(x + (1+i)*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_normal_body)
    draw_pixel(x + 3*PIXEL_SIZE, y + 1*PIXEL_SIZE, white)
    for i in range(7): draw_pixel(x + i*PIXEL_SIZE, y + 3*PIXEL_SIZE, enemy_normal_body)
    draw_pixel(x + 1*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_normal_highlight); draw_pixel(x + 5*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_normal_highlight)
    draw_pixel(x + 3*PIXEL_SIZE, y + 4*PIXEL_SIZE, player_engine)

def draw_strong_enemy(rect):
    x, y = rect.topleft
    for i in range(7): draw_pixel(x + (1+i)*PIXEL_SIZE, y + 2*PIXEL_SIZE, enemy_strong_body)
    for i in range(5): draw_pixel(x + (2+i)*PIXEL_SIZE, y + 3*PIXEL_SIZE, enemy_strong_body)
    draw_pixel(x + 4*PIXEL_SIZE, y + 1*PIXEL_SIZE, enemy_strong_core)
    for i in range(9): draw_pixel(x + i*PIXEL_SIZE, y + 4*PIXEL_SIZE, enemy_strong_body)
    for i in range(7): draw_pixel(x + (1+i)*PIXEL_SIZE, y + 5*PIXEL_SIZE, enemy_strong_body)
    draw_pixel(x + 2*PIXEL_SIZE, y + 4*PIXEL_SIZE, enemy_strong_highlight); draw_pixel(x + 6*PIXEL_SIZE, y + 4*PIXEL_SIZE, enemy_strong_highlight)
    draw_pixel(x + 3*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine); draw_pixel(x + 5*PIXEL_SIZE, y + 6*PIXEL_SIZE, player_engine)

def draw_enemies(enemy_list):
    for enemy in enemy_list:
        if enemy['type'] == 'strong': draw_strong_enemy(enemy['rect'])
        else: draw_normal_enemy(enemy['rect'])

def draw_bullets(bullet_list, color):
    for bullet in bullet_list:
        pygame.draw.rect(screen, color, bullet['rect'])

def draw_score(current_score):
    score_text = score_font.render(f"Score: {current_score}", True, white)
    screen.blit(score_text, (10, 10))

def draw_lives(lives):
    heart_width = 5 * PIXEL_SIZE
    for i in range(lives):
        x = screen_width - (i + 1) * (heart_width + 10)
        y = 10
        draw_pixel(x + 1*PIXEL_SIZE, y, heart_color); draw_pixel(x + 3*PIXEL_SIZE, y, heart_color)
        for j in range(5): draw_pixel(x + j*PIXEL_SIZE, y + 1*PIXEL_SIZE, heart_color)
        for j in range(3): draw_pixel(x + (1+j)*PIXEL_SIZE, y + 2*PIXEL_SIZE, heart_color)
        draw_pixel(x + 2*PIXEL_SIZE, y + 3*PIXEL_SIZE, heart_color)

# --- Функция сброса игры ---
def reset_game():
    global score, enemies, bullets, player_lives, player_invincible, enemy_bullets, starfield
    score = 0
    player_lives = 3
    player_invincible = False
    player_rect.topleft = ((screen_width - player_width) // 2, screen_height - player_height - 10)
    enemies.clear()
    bullets.clear()
    enemy_bullets.clear()
    starfield = [[], [], []]
    prepare_starfield()
    # Запуск фоновой музыки
    music_sound.set_volume(1.0)
    music_sound.play(-1)  # -1 означает бесконечное воспроизведение

# --- Функция плавного затухания ---
def fade_out(duration=2000):
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
        music_sound.set_volume(1.0 - progress)
        
        # Рисуем затемнение
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        clock.tick(60)
    
    # Полностью останавливаем музыку
    music_sound.stop()

# --- Основной цикл приложения ---
while True:
    reset_game()
    game_over = False

    # --- Игровой цикл ---
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); quit()
            if event.type == PLAYER_SHOOT_EVENT: 
                bullets.append({'rect': pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10)})
                # Воспроизвести звук выстрела
                shoot_sound.play()
            if event.type == ENEMY_SPAWN_EVENT:
                if random.randint(1, 5) == 1:
                    enemy_x = random.randint(0, screen_width - enemy_strong_width)
                    enemies.append({'rect': pygame.Rect(enemy_x, -enemy_strong_height, enemy_strong_width, enemy_strong_height), 'health': 2, 'type': 'strong'})
                else:
                    enemy_x = random.randint(0, screen_width - enemy_normal_width)
                    enemies.append({'rect': pygame.Rect(enemy_x, -enemy_normal_height, enemy_normal_width, enemy_normal_height), 'health': 1, 'type': 'normal'})
            if event.type == ENEMY_SHOOT_EVENT:
                strong_enemies_on_screen = [e for e in enemies if e['type'] == 'strong' and e['rect'].y < screen_height * (2/3)]
                if strong_enemies_on_screen:
                    shooter = random.choice(strong_enemies_on_screen)
                    start_pos = pygame.math.Vector2(shooter['rect'].center)
                    target_pos = pygame.math.Vector2(player_rect.center)
                    if (target_pos - start_pos).length() > 0:
                        direction = (target_pos - start_pos).normalize()
                        vel = direction * enemy_bullet_speed
                        enemy_bullets.append({'rect': pygame.Rect(start_pos.x, start_pos.y, 6, 6), 'vel': vel})

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < screen_width: player_rect.x += player_speed

        # --- Логика игры ---
        if player_invincible and pygame.time.get_ticks() > player_invincible_end_time: player_invincible = False
        for layer in starfield:
            for star in layer:
                star['rect'].y += star['speed']
                if star['rect'].top > screen_height:
                    star['rect'].y = -star['rect'].height
                    star['rect'].x = random.randint(0, screen_width)

        for bullet in bullets[:]:
            bullet['rect'].y -= bullet_speed
            if bullet['rect'].bottom < 0: bullets.remove(bullet)
        for bullet in enemy_bullets[:]:
            bullet['rect'].x += bullet['vel'].x
            bullet['rect'].y += bullet['vel'].y
            if not screen.get_rect().colliderect(bullet['rect']): enemy_bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy['rect'].y += enemy_speed
            if enemy['rect'].top > screen_height: enemies.remove(enemy)
            if not player_invincible and player_rect.colliderect(enemy['rect']):
                player_lives -= 1; enemies.remove(enemy); player_invincible = True; player_invincible_end_time = pygame.time.get_ticks() + 2000
                if player_lives <= 0: game_over = True
        
        if not player_invincible:
            for bullet in enemy_bullets[:]:
                if player_rect.colliderect(bullet['rect']):
                    player_lives -= 1; enemy_bullets.remove(bullet); player_invincible = True; player_invincible_end_time = pygame.time.get_ticks() + 2000
                    if player_lives <= 0: game_over = True
                    break

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet['rect'].colliderect(enemy['rect']):
                    if bullet in bullets: bullets.remove(bullet)
                    enemy['health'] -= 1
                    if enemy['health'] <= 0:
                        enemies.remove(enemy)
                        score += 3 if enemy['type'] == 'strong' else 1
                        # Воспроизвести звук взрыва
                        explosion_sound.play()
                    break

        # --- Отрисовка ---
        screen.fill(black)
        draw_starfield()
        if not player_invincible or (pygame.time.get_ticks() // 200) % 2 == 0: draw_player_ship(player_rect)
        draw_enemies(enemies)
        draw_bullets(bullets, bullet_color)
        draw_bullets(enemy_bullets, enemy_bullet_color)
        draw_score(score)
        draw_lives(player_lives)
        pygame.display.update()
        clock.tick(60)

    # --- Экран Game Over ---
    # Плавное затухание перед показом Game Over
    fade_out()
    
    screen.fill(black)
    game_over_text = game_over_font.render("Game Over", True, white)
    final_score_text = score_font.render(f"Final Score: {score}", True, white)
    restart_text = restart_font.render("Press ENTER to restart", True, white)
    screen.blit(game_over_text, game_over_text.get_rect(center=(screen_width/2, screen_height/2 - 60)))
    screen.blit(final_score_text, final_score_text.get_rect(center=(screen_width/2, screen_height/2 + 10)))
    screen.blit(restart_text, restart_text.get_rect(center=(screen_width/2, screen_height/2 + 60)))
    pygame.display.update()

    # --- Цикл ожидания рестарта ---
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_restart = False
