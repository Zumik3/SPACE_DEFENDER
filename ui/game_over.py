import pygame
from utils.constants import *
from ui.ui_screen import UIScreen


class GameOverScreen(UIScreen):
    """Класс для экрана окончания игры"""
    
    def __init__(self, screen, event_manager=None):
        super().__init__(screen, event_manager)
        self.selected_option = 0
        self.options = ["Restart Game", "Main Menu"]
        self.final_score = 0
        
    def draw(self, score=None):
        """Отрисовка экрана окончания игры"""
        if score is not None:
            self.final_score = score
            
        self.screen.fill(black)
        
        # Рисуем надпись GAME OVER
        game_over_text = game_over_font.render("GAME OVER", True, white)
        final_score_text = score_font.render(f"Final Score: {self.final_score}", True, white)
        
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(screen_width/2, screen_height/2 - 80)))
        self.screen.blit(final_score_text, final_score_text.get_rect(center=(screen_width/2, screen_height/2 - 20)))
        
        # Рисуем пункты меню
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else white  # Желтый для выбранного пункта
            text = menu_item_font.render(option, True, color)
            text_rect = text.get_rect(center=(screen_width/2, screen_height/2 + 30 + i * 40))
            self.screen.blit(text, text_rect)
            
        pygame.display.update()
        
    def handle_events(self):
        """Обработка событий экрана окончания игры"""
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
                    if self.selected_option == 0:  # Restart Game
                        return "restart"
                    elif self.selected_option == 1:  # Main Menu
                        return "main_menu"
        return None
        
    def on_game_over(self, event_type, data):
        """Обработчик события окончания игры"""
        if data and "score" in data:
            self.final_score = data["score"]