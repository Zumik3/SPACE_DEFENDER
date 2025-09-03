import pygame
pygame.font.init()

from utils.constants import init_fonts, screen_width, screen_height
init_fonts()

from game import Game, GameManager, StateMachine, GameState
from ui.menu import Menu
from ui.settings import Settings
from ui.game_over import GameOverScreen
from utils.settings_manager import SettingsManager

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SPACE DEFENDER")
    
    settings_manager = SettingsManager()
    # Создаем GameManager, который будет управлять всеми компонентами игры
    game_manager = GameManager(screen, settings_manager)
    menu = Menu(screen, game_manager.get_event_manager())
    settings = Settings(screen, game_manager.get_sound_manager(), settings_manager)
    game_over_screen = GameOverScreen(screen, game_manager.get_event_manager())
    
    # Создаем конечный автомат для управления состояниями
    state_machine = StateMachine()
    
    # Переменные для управления переходами
    should_start_game = False
    game_final_score = 0
    
    # Устанавливаем обработчики состояний
    def handle_menu_state():
        menu.draw()
        action = menu.handle_events()
        
        if action == "new_game":
            global should_start_game
            should_start_game = True
            start_state_transition(GameState.PLAYING)
        elif action == "settings":
            start_state_transition(GameState.SETTINGS)
        elif action == "exit":
            start_state_transition(GameState.QUIT)
            
    def handle_settings_state():
        settings.draw()
        action = settings.handle_events()
        
        if action == "back" or action == "exit":
            start_state_transition(GameState.MENU)
            
    def handle_playing_state():
        global should_start_game, game_final_score
        # Если нужно начать игру
        if should_start_game:
            # Останавливаем музыку меню и запускаем игру
            game_manager.get_sound_manager().stop_menu_music()
            # Сбрасываем состояние игры перед запуском
            game_manager.get_state_manager().reset()
            # Запускаем игру через GameManager и получаем финальный счет
            game_final_score = game_manager.start_game()
            # После завершения игры переходим к экрану окончания игры
            start_state_transition(GameState.GAME_OVER)
            should_start_game = False
        
    def handle_game_over_state():
        """Обработчик состояния окончания игры"""
        global game_final_score
        game_over_screen.draw(game_final_score)
        action = game_over_screen.handle_events()
        
        if action == "restart":
            global should_start_game
            should_start_game = True
            # Сбрасываем финальный счет перед новой игрой
            game_final_score = 0
            start_state_transition(GameState.PLAYING)
        elif action == "main_menu":
            start_state_transition(GameState.MENU)
        elif action == "exit":
            start_state_transition(GameState.QUIT)
        elif action == "redraw":
            # Перерисовываем экран
            game_over_screen.draw(game_final_score)
            
    def handle_quit_state():
        game_manager.get_sound_manager().stop_all_music()
        pygame.quit()
        quit()
        
    def start_state_transition(new_state: GameState):
        """Начинает переход в новое состояние"""
        state_machine.transition_to(new_state)
        
    # Устанавливаем обработчики входа в состояния
    def on_enter_menu():
        # Запускаем музыку меню, если она не играет
        if not pygame.mixer.get_busy():
            game_manager.get_sound_manager().play_menu_music(-1)
        
    def on_exit_menu():
        # Останавливаем музыку меню только при переходе в игру или выходе
        current_state = state_machine.get_current_state()
        if current_state == GameState.PLAYING or current_state == GameState.QUIT:
            game_manager.get_sound_manager().stop_menu_music()
            
    def on_enter_settings():
        # В настройках музыка меню продолжает играть
        pass
        
    def on_exit_settings():
        # При выходе из настроек музыка меню продолжает играть
        pass
        
    def on_enter_game_over():
        """Обработчик входа в состояние окончания игры"""
        # Останавливаем музыку игры, если она играет
        if pygame.mixer.get_busy():
            game_manager.get_sound_manager().stop_music()
        
    def on_exit_game_over():
        """Обработчик выхода из состояния окончания игры"""
        # Ничего не делаем
        pass
        
    # Регистрируем обработчики
    state_machine.set_state_handler(GameState.MENU, handle_menu_state)
    state_machine.set_state_handler(GameState.SETTINGS, handle_settings_state)
    state_machine.set_state_handler(GameState.PLAYING, handle_playing_state)
    state_machine.set_state_handler(GameState.GAME_OVER, handle_game_over_state)
    state_machine.set_state_handler(GameState.QUIT, handle_quit_state)
    
    state_machine.set_state_enter_handler(GameState.MENU, on_enter_menu)
    state_machine.set_state_exit_handler(GameState.MENU, on_exit_menu)
    state_machine.set_state_enter_handler(GameState.SETTINGS, on_enter_settings)
    state_machine.set_state_exit_handler(GameState.SETTINGS, on_exit_settings)
    state_machine.set_state_enter_handler(GameState.GAME_OVER, on_enter_game_over)
    state_machine.set_state_exit_handler(GameState.GAME_OVER, on_exit_game_over)
    
    # Начинаем с меню и вызываем обработчик входа в состояние
    state_machine.transition_to(GameState.MENU)
    on_enter_menu()
    
    while True:
        # Обновляем текущее состояние
        state_machine.update()
        
        pygame.time.Clock().tick(60)