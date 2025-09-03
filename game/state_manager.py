import pygame
from utils.constants import *
from .state_machine import GameState


class GameStateManager:
    """Класс для управления состоянием игры"""
    
    def __init__(self):
        self.current_state = GameState.MENU  # Используем перечисление из конечного автомата
        self.score = 0
        self.player_lives = 3
        self.level = 1
        self.is_paused = False
        
    def set_state(self, state: GameState):
        """Установка текущего состояния игры"""
        self.current_state = state
            
    def get_state(self) -> GameState:
        """Получение текущего состояния игры"""
        return self.current_state
        
    def is_menu(self) -> bool:
        """Проверка, находится ли игра в состоянии меню"""
        return self.current_state == GameState.MENU
        
    def is_playing(self) -> bool:
        """Проверка, идет ли игра"""
        return self.current_state == GameState.PLAYING
        
    def is_game_over(self) -> bool:
        """Проверка, закончилась ли игра"""
        return self.current_state == GameState.GAME_OVER
        
    def is_paused(self) -> bool:
        """Проверка, поставлена ли игра на паузу"""
        return self.is_paused
        
    def start_game(self):
        """Начало новой игры"""
        self.current_state = GameState.PLAYING
        self.score = 0
        self.player_lives = 3
        self.level = 1
        self.is_paused = False
        
    def pause_game(self):
        """Постановка игры на паузу"""
        if self.current_state == GameState.PLAYING:
            self.is_paused = True
            self.current_state = GameState.PAUSED
            
    def resume_game(self):
        """Продолжение игры"""
        if self.current_state == GameState.PAUSED:
            self.is_paused = False
            self.current_state = GameState.PLAYING
            
    def game_over(self):
        """Завершение игры"""
        self.current_state = GameState.GAME_OVER
        
    def return_to_menu(self):
        """Возврат в главное меню"""
        self.current_state = GameState.MENU
        self.is_paused = False
        
    def update_score(self, points):
        """Обновление счета"""
        self.score += points
        
    def lose_life(self):
        """Потеря жизни"""
        self.player_lives -= 1
        return self.player_lives <= 0
        
    def gain_life(self):
        """Получение дополнительной жизни"""
        self.player_lives += 1
        
    def next_level(self):
        """Переход на следующий уровень"""
        self.level += 1
        
    def get_score(self):
        """Получение текущего счета"""
        return self.score
        
    def get_lives(self):
        """Получение количества жизней"""
        return self.player_lives
        
    def get_level(self):
        """Получение текущего уровня"""
        return self.level
        
    def reset(self):
        """Сброс состояния игры"""
        self.score = 0
        self.player_lives = 3
        self.level = 1
        self.is_paused = False