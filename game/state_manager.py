import pygame
from utils.constants import *


class GameStateManager:
    """Класс для управления состоянием игры"""
    
    def __init__(self):
        self.current_state = "menu"  # "menu", "playing", "game_over"
        self.score = 0
        self.player_lives = 3
        
    def set_state(self, state):
        """Установка текущего состояния игры"""
        if state in ["menu", "playing", "game_over"]:
            self.current_state = state
            
    def get_state(self):
        """Получение текущего состояния игры"""
        return self.current_state
        
    def is_menu(self):
        """Проверка, находится ли игра в состоянии меню"""
        return self.current_state == "menu"
        
    def is_playing(self):
        """Проверка, идет ли игра"""
        return self.current_state == "playing"
        
    def is_game_over(self):
        """Проверка, закончилась ли игра"""
        return self.current_state == "game_over"
        
    def start_game(self):
        """Начало новой игры"""
        self.current_state = "playing"
        self.score = 0
        self.player_lives = 3
        
    def game_over(self):
        """Завершение игры"""
        self.current_state = "game_over"
        
    def return_to_menu(self):
        """Возврат в главное меню"""
        self.current_state = "menu"
        
    def update_score(self, points):
        """Обновление счета"""
        self.score += points
        
    def lose_life(self):
        """Потеря жизни"""
        self.player_lives -= 1
        return self.player_lives <= 0
        
    def make_player_invincible(self):
        """Сделать игрока неуязвимым"""
        pass  # Эта логика будет в классе Player
        
    def get_score(self):
        """Получение текущего счета"""
        return self.score
        
    def get_lives(self):
        """Получение количества жизней"""
        return self.player_lives
        
    def reset(self):
        """Сброс состояния игры"""
        self.score = 0
        self.player_lives = 3