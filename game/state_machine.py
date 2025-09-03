from enum import Enum
from typing import Dict, Callable, Optional


class GameState(Enum):
    """Перечисление всех возможных состояний игры"""
    MENU = "menu"
    SETTINGS = "settings"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    QUIT = "quit"


class StateTransition:
    """Класс для представления перехода между состояниями"""
    
    def __init__(self, from_state: GameState, to_state: GameState, condition: Optional[Callable] = None):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition


class StateMachine:
    """Конечный автомат для управления состояниями игры"""
    
    def __init__(self):
        self.current_state: GameState = GameState.MENU
        self.previous_state: Optional[GameState] = None
        self.transitions: Dict[tuple, StateTransition] = {}
        self.state_handlers: Dict[GameState, Callable] = {}
        self.state_exit_handlers: Dict[GameState, Callable] = {}
        self.state_enter_handlers: Dict[GameState, Callable] = {}
        
        # Определяем допустимые переходы между состояниями
        self._define_transitions()
        
    def _define_transitions(self):
        """Определяем допустимые переходы между состояниями"""
        # Из меню можно перейти в игру, настройки или выйти
        self.add_transition(GameState.MENU, GameState.PLAYING)
        self.add_transition(GameState.MENU, GameState.SETTINGS)
        self.add_transition(GameState.MENU, GameState.QUIT)
        
        # Из настроек можно вернуться в меню или выйти
        self.add_transition(GameState.SETTINGS, GameState.MENU)
        self.add_transition(GameState.SETTINGS, GameState.QUIT)
        
        # Из игры можно перейти в завершение игры или выйти
        self.add_transition(GameState.PLAYING, GameState.GAME_OVER)
        self.add_transition(GameState.PLAYING, GameState.QUIT)
        
        # Из завершения игры можно перезапустить игру, вернуться в меню или выйти
        self.add_transition(GameState.GAME_OVER, GameState.PLAYING)
        self.add_transition(GameState.GAME_OVER, GameState.MENU)
        self.add_transition(GameState.GAME_OVER, GameState.QUIT)
        
    def add_transition(self, from_state: GameState, to_state: GameState, condition: Optional[Callable] = None):
        """Добавляет переход между состояниями"""
        transition = StateTransition(from_state, to_state, condition)
        self.transitions[(from_state, to_state)] = transition
        
    def can_transition(self, from_state: GameState, to_state: GameState) -> bool:
        """Проверяет, возможен ли переход между состояниями"""
        transition_key = (from_state, to_state)
        if transition_key not in self.transitions:
            return False
            
        transition = self.transitions[transition_key]
        if transition.condition:
            return transition.condition()
            
        return True
        
    def transition_to(self, new_state: GameState) -> bool:
        """Выполняет переход в новое состояние"""
        if not self.can_transition(self.current_state, new_state):
            return False
            
        # Вызываем обработчик выхода из текущего состояния
        if self.current_state in self.state_exit_handlers:
            self.state_exit_handlers[self.current_state]()
            
        # Сохраняем предыдущее состояние
        self.previous_state = self.current_state
        
        # Устанавливаем новое состояние
        self.current_state = new_state
        
        # Вызываем обработчик входа в новое состояние
        if self.current_state in self.state_enter_handlers:
            self.state_enter_handlers[self.current_state]()
            
        return True
        
    def set_state_handler(self, state: GameState, handler: Callable):
        """Устанавливает обработчик для состояния"""
        self.state_handlers[state] = handler
        
    def set_state_enter_handler(self, state: GameState, handler: Callable):
        """Устанавливает обработчик входа в состояние"""
        self.state_enter_handlers[state] = handler
        
    def set_state_exit_handler(self, state: GameState, handler: Callable):
        """Устанавливает обработчик выхода из состояния"""
        self.state_exit_handlers[state] = handler
        
    def update(self):
        """Обновляет текущее состояние"""
        if self.current_state in self.state_handlers:
            return self.state_handlers[self.current_state]()
            
        return None
        
    def get_current_state(self) -> GameState:
        """Возвращает текущее состояние"""
        return self.current_state
        
    def get_previous_state(self) -> Optional[GameState]:
        """Возвращает предыдущее состояние"""
        return self.previous_state
        
    def is_state(self, state: GameState) -> bool:
        """Проверяет, является ли текущее состояние указанным"""
        return self.current_state == state