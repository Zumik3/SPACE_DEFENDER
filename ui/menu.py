import pygame
from ui.pixel_title import PixelTitle
from ui.ui_screen import UIScreen
from utils import constants
from utils.constants import black, white, screen_width, screen_height


class Menu(UIScreen):
    def __init__(self, screen, event_manager=None):
        super().__init__(screen, event_manager)
        self.selected_option = 0
        self.options = ["New Game", "Settings", "Exit"]
        self.pixel_title = PixelTitle()
        
    def draw(self):
        self.screen.fill(black)
        
        # Рисуем пиксельное название игры (по центру горизонтали, на фиксированной высоте)
        title_x = 0  # Будет центрировано внутри PixelTitle
        title_y = 50  # Фиксированная позиция сверху
        self.pixel_title.draw(self.screen, title_x, title_y)
        
        # Рисуем пункты меню
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else white  # Выделенный пункт желтого цвета
            text = constants.menu_item_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + i * 50))
            self.screen.blit(text, text_rect)
            
        pygame.display.update()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    self.draw()  # Перерисовываем меню с новым выделенным пунктом
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    self.draw()  # Перерисовываем меню с новым выделенным пунктом
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # New Game
                        return "new_game"
                    elif self.selected_option == 1:  # Settings
                        return "settings"
                    elif self.selected_option == 2:  # Exit
                        return "exit"
        return None