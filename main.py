import pygame
pygame.font.init()

from utils.constants import init_fonts, screen_width, screen_height
init_fonts()

from game import Game
from ui.menu import Menu

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Star Game")
    
    menu = Menu(screen)
    game = Game()
    
    # Показываем меню
    in_menu = True
    while in_menu:
        menu.draw()
        action = menu.handle_events()
        
        if action == "new_game":
            in_menu = False
            # Запускаем игру
            game.run(screen)
        elif action == "settings":
            # Пока не реализовано
            pass
        elif action == "exit":
            pygame.quit()
            quit()
        
        pygame.time.Clock().tick(60)