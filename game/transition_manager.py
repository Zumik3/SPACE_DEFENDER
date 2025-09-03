import pygame
from typing import Callable, Optional


class TransitionManager:
    """Менеджер для управления плавными переходами между состояниями"""
    
    def __init__(self, screen):
        self.screen = screen
        self.transitioning = False
        self.transition_progress = 0.0
        self.transition_duration = 500  # мс
        self.transition_start_time = 0
        self.transition_callback: Optional[Callable] = None
        self.transition_type = "fade"  # "fade", "slide", "zoom"
        
    def start_transition(self, transition_type: str = "fade", duration: int = 500, callback: Optional[Callable] = None):
        """Начинает плавный переход"""
        self.transitioning = True
        self.transition_progress = 0.0
        self.transition_duration = duration
        self.transition_start_time = pygame.time.get_ticks()
        self.transition_callback = callback
        self.transition_type = transition_type
        
    def update(self):
        """Обновляет состояние перехода"""
        if not self.transitioning:
            return
            
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.transition_start_time
        
        if elapsed_time >= self.transition_duration:
            self.transition_progress = 1.0
            self.transitioning = False
            # Вызываем callback после завершения перехода
            if self.transition_callback:
                self.transition_callback()
        else:
            self.transition_progress = elapsed_time / self.transition_duration
            
    def draw(self):
        """Отрисовывает эффект перехода"""
        if not self.transitioning:
            return
            
        if self.transition_type == "fade":
            self._draw_fade_transition()
        elif self.transition_type == "slide":
            self._draw_slide_transition()
        elif self.transition_type == "zoom":
            self._draw_zoom_transition()
            
    def _draw_fade_transition(self):
        """Отрисовывает переход с затуханием"""
        from utils.constants import screen_width, screen_height, black
        
        # Создаем поверхность для затухания
        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill(black)
        
        # Вычисляем прозрачность
        alpha = int(self.transition_progress * 255)
        fade_surface.set_alpha(alpha)
        
        # Рисуем поверхность
        self.screen.blit(fade_surface, (0, 0))
        
    def _draw_slide_transition(self):
        """Отрисовывает переход со сдвигом"""
        # Пока не реализован
        pass
        
    def _draw_zoom_transition(self):
        """Отрисовывает переход с масштабированием"""
        # Пока не реализован
        pass
        
    def is_transitioning(self) -> bool:
        """Проверяет, выполняется ли переход"""
        return self.transitioning
        
    def get_transition_progress(self) -> float:
        """Возвращает прогресс перехода (0.0 - 1.0)"""
        return self.transition_progress