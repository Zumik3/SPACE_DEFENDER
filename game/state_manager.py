from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"

class StateManager:
    def __init__(self):
        self.current_state = GameState.MENU
        
    def set_state(self, state):
        self.current_state = state
        
    def get_state(self):
        return self.current_state