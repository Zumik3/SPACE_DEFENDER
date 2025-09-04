import pygame
import os

# Настройки экрана и стиля
PIXEL_SIZE = 4
screen_width = 600
screen_height = 800

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)
player_body = (200, 200, 200)
player_wing = (0, 200, 0)
player_cockpit = (100, 200, 255)
player_engine = (255, 165, 0)
bullet_color = (255, 255, 0)
enemy_bullet_color = (255, 100, 100)
heart_color = (255, 50, 50)
enemy_normal_body = (200, 40, 40)
enemy_normal_highlight = (255, 100, 100)
enemy_strong_body = (150, 50, 180)
enemy_strong_highlight = (200, 100, 220)
enemy_strong_core = (255, 0, 0)
star_colors = [(100, 100, 100), (180, 180, 180), (255, 255, 255)]

# Настройки игры
player_width = 11 * PIXEL_SIZE
player_height = 7 * PIXEL_SIZE
player_speed = 7
bullet_speed = 10
enemy_bullet_speed = 6
enemy_normal_width = 7 * PIXEL_SIZE
enemy_normal_height = 5 * PIXEL_SIZE
enemy_strong_width = 9 * PIXEL_SIZE
enemy_strong_height = 7 * PIXEL_SIZE
enemy_speed = 4

# Таймеры
PLAYER_SHOOT_EVENT = pygame.USEREVENT + 1
ENEMY_SPAWN_EVENT = pygame.USEREVENT + 2
ENEMY_SHOOT_EVENT = pygame.USEREVENT + 3
PLAYER_SHOOT_DELAY = 300
ENEMY_SPAWN_DELAY = 900
ENEMY_SHOOT_DELAY = 800
ENEMY_NORMAL_SPEED = 8  # for small bullets

# Настройки бонусов
POWERUP_HEALTH_CHANCE_STRONG = 0.15
POWERUP_HEALTH_CHANCE_NORMAL = 0.1
POWERUP_FIRE_CHANCE_STRONG = 0.1
POWERUP_FIRE_CHANCE_NORMAL = 0.05
POWERUP_SPEED = 3
POWERUP_HEALTH_COLOR = (0, 255, 0)
POWERUP_FIRE_COLOR = (255, 255, 0)
POWERUP_SIZE = 30
FIRE_RATE_BOOST = 100

# Размеры шрифтов
SCORE_FONT_SIZE = 24
GAME_OVER_FONT_SIZE = 48
MENU_TITLE_FONT_SIZE = 36
MENU_ITEM_FONT_SIZE = 24
SETTINGS_TITLE_FONT_SIZE = 36
SETTINGS_ITEM_FONT_SIZE = 24

# Шрифты
score_font = None
game_over_font = None
menu_title_font = None
menu_item_font = None
settings_title_font = None
settings_item_font = None

def init_fonts():
    global score_font, game_over_font, menu_title_font, menu_item_font, settings_title_font, settings_item_font
    if score_font is None:
        # Определяем путь к шрифту
        font_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts', 'PressStart2P-Regular.ttf')
        
        # Проверяем, существует ли файл шрифта
        if os.path.exists(font_path):
            # Используем шрифт Press Start 2P
            try:
                score_font = pygame.font.Font(font_path, SCORE_FONT_SIZE)
                game_over_font = pygame.font.Font(font_path, GAME_OVER_FONT_SIZE)
                menu_title_font = pygame.font.Font(font_path, MENU_TITLE_FONT_SIZE)
                menu_item_font = pygame.font.Font(font_path, MENU_ITEM_FONT_SIZE)
                settings_title_font = pygame.font.Font(font_path, SETTINGS_TITLE_FONT_SIZE)
                settings_item_font = pygame.font.Font(font_path, SETTINGS_ITEM_FONT_SIZE)
            except Exception as e:
                # Если шрифт не найден, используем системный шрифт
                score_font = pygame.font.SysFont("Verdana", SCORE_FONT_SIZE)
                game_over_font = pygame.font.SysFont("Verdana", GAME_OVER_FONT_SIZE)
                menu_title_font = pygame.font.SysFont("Verdana", MENU_TITLE_FONT_SIZE)
                menu_item_font = pygame.font.SysFont("Verdana", MENU_ITEM_FONT_SIZE)
                settings_title_font = pygame.font.SysFont("Verdana", SETTINGS_TITLE_FONT_SIZE)
                settings_item_font = pygame.font.SysFont("Verdana", SETTINGS_ITEM_FONT_SIZE)
        else:
            # Если шрифт не найден, используем системный шрифт
            score_font = pygame.font.SysFont("Verdana", SCORE_FONT_SIZE)
            game_over_font = pygame.font.SysFont("Verdana", GAME_OVER_FONT_SIZE)
            menu_title_font = pygame.font.SysFont("Verdana", MENU_TITLE_FONT_SIZE)
            menu_item_font = pygame.font.SysFont("Verdana", MENU_ITEM_FONT_SIZE)
            settings_title_font = pygame.font.SysFont("Verdana", SETTINGS_TITLE_FONT_SIZE)
            settings_item_font = pygame.font.SysFont("Verdana", SETTINGS_ITEM_FONT_SIZE)