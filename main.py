import pygame
pygame.font.init()

from utils.constants import init_fonts, screen_width, screen_height
init_fonts()

from game import Game
from ui.menu import Menu
from ui.settings import Settings
from utils.sound_manager import SoundManager
from utils.settings_manager import SettingsManager

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Star Game")
    
    settings_manager = SettingsManager()
    sound_manager = SoundManager(settings_manager)
    menu = Menu(screen)
    settings = Settings(screen, sound_manager, settings_manager)
    
    # Показываем меню
    in_menu = True
    in_settings = False
    
    # Запускаем музыку меню
    sound_manager.play_menu_music(-1)
    
    while True:
        if in_menu:
            menu.draw()
            action = menu.handle_events()
            
            if action == "new_game":
                # Останавливаем музыку меню и запускаем игру
                sound_manager.stop_menu_music()
                in_menu = False
                # Создаем новую игровую сессию при каждом запуске
                game = Game(sound_manager)
                # Запускаем игру
                game.run(screen)
                # После завершения игры возвращаемся в меню и снова включаем музыку меню
                sound_manager.play_menu_music(-1)
                in_menu = True
            elif action == "settings":
                in_menu = False
                in_settings = True
            elif action == "exit":
                sound_manager.stop_all_music()
                pygame.quit()
                quit()
                
        elif in_settings:
            settings.draw()
            action = settings.handle_events()
            
            if action == "back" or action == "exit":
                in_settings = False
                in_menu = True
                
        pygame.time.Clock().tick(60)