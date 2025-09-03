import pygame


class UIScreen:
    """Базовый класс для экранов UI"""
    
    def __init__(self, screen, event_manager=None):
        self.screen = screen
        self.event_manager = event_manager
        # Подписываемся на события, если есть менеджер событий
        if self.event_manager:
            self.event_manager.subscribe("score_updated", self.on_score_updated)
            self.event_manager.subscribe("powerup_collected", self.on_powerup_collected)
            self.event_manager.subscribe("game_over", self.on_game_over)
        
    def draw(self):
        """Отрисовка экрана"""
        pass
        
    def handle_events(self):
        """Обработка событий экрана"""
        pass
        
    def on_score_updated(self, event_type, data):
        """Обработчик события обновления счета"""
        pass
        
    def on_powerup_collected(self, event_type, data):
        """Обработчик события получения бонуса"""
        pass
        
    def on_game_over(self, event_type, data):
        """Обработчик события окончания игры"""
        pass