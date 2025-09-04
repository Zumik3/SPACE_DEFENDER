import pygame
from utils.constants import *
from ui.ui_screen import UIScreen


class HubScreen(UIScreen):
    """Класс для экрана хаба"""
    
    def __init__(self, screen, event_manager=None):
        super().__init__(screen, event_manager)
        self.selected_option = 0
        self.options = ["Battle", "Rearm", "Main Menu"]
        
    def draw(self):
        """Отрисовка экрана хаба"""
        self.screen.fill(black)
        
        # Рисуем заголовок хаба
        hub_title_text = game_over_font.render("HUB", True, white)
        self.screen.blit(hub_title_text, hub_title_text.get_rect(center=(screen_width/2, screen_height/2 - 80)))
        
        # Рисуем пункты меню
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else white  # Желтый для выбранного пункта
            text = menu_item_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + 30 + i * 40))
            self.screen.blit(text, text_rect)
            
        pygame.display.update()
        
    def handle_events(self):
        """Обработка событий экрана хаба"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                    return "redraw"
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                    return "redraw"
                elif event.key == pygame.K_RETURN:
                    if self.selected_option == 0:  # Battle
                        return "battle"
                    elif self.selected_option == 1:  # Rearm
                        return "rearm"
                    elif self.selected_option == 2:  # Main Menu
                        return "main_menu"
        return None
        
    def on_game_over(self, event_type, data):
        """Обработчик события окончания игры"""
        # В хабе мы не обрабатываем событие окончания игры
        pass