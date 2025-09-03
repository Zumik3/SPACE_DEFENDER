# SPACE DEFENDER Game Project Context

## Project Overview

This is a Python-based space shooter game built using the Pygame library. The player controls a spaceship at the bottom of the screen, shooting upwards to destroy enemy ships while avoiding their bullets and collecting power-ups. The game features a starfield background, lives system, scoring, and different enemy types.

### Core Components

- **Main Entry Point**: `main.py` initializes the game and starts the main loop.
- **Game Logic**: The `Game` class in `game/game_logic.py` manages the game state, entities, collisions, scoring, and game flow (including the game over screen and restart).
- **Menu System**: The `Menu` class in `ui/menu.py` provides the main menu with options for starting a new game, accessing settings, and exiting.
- **Settings**: The `Settings` class in `ui/settings.py` provides volume controls for music and sound effects.
- **Rendering**: The `Renderer` class in `ui/renderer.py` handles all visual drawing, including the player ship, enemies, power-ups, bullets, starfield background, score, and lives. It uses pixel-art style drawing functions.
- **Sound**: The `SoundManager` class in `utils/sound_manager.py` handles playing background music and sound effects.
- **Core Entities**:
  - `core/player.py`: Defines the `Player` class, handling movement, shooting, invincibility, and drawing.
  - `core/enemy.py`: Defines the `Enemy` class, with two types ('normal' and 'strong'), handling movement, shooting (for 'strong'), drawing, and scoring.
  - `core/bullet.py`: Defines the `Bullet` class for both player and enemy projectiles, handling movement, drawing, and collision detection.
  - `core/powerup.py`: Defines the `Powerup` class hierarchy, with 'health' and 'fire_rate' types, handling movement and drawing using simple pixel art.
- **Constants and Configuration**: `utils/constants.py` holds game settings like screen dimensions, colors, entity sizes, speeds, event timers, and font definitions.

## Building and Running

1.  **Prerequisites**: Ensure Python 3.x and Pygame are installed. You can typically install Pygame using `pip install pygame`.
2.  **Running the Game**: Execute the main script: `python main.py`.
3.  **Controls**:
    - **Left Arrow Key**: Move player ship left.
    - **Right Arrow Key**: Move player ship right.
    - **ENTER**: Restart the game after Game Over.

## Development Conventions

- The code is structured into packages (`core`, `game`, `ui`, `utils`) to separate concerns.
- Constants are centralized in `utils/constants.py` for easy configuration and consistency.
- Classes generally handle their own state updates (`update` method) and rendering (`draw` method or specific drawing functions in `Renderer`).
- Pygame's event system and timers are used for shooting and enemy spawning.
- Simple pixel-art style is used for drawing game entities directly with `pygame.draw` functions, defined within the `Renderer` and `Powerup` classes.
- Sound effects and music are managed by the `SoundManager`.
- Menu system is implemented in `ui/menu.py` to provide a user interface for starting games, accessing settings, and exiting.
- Settings system is implemented in `ui/settings.py` to control music and sound effects volume.

## Code Writing Principles

- **SOLID**:
  - **Single Responsibility Principle (SRP)**: Каждый класс должен иметь только одну причину для изменения.
  - **Open/Closed Principle (OCP)**: Классы должны быть открыты для расширения, но закрыты для модификации.
  - **Liskov Substitution Principle (LSP)**: Объекты в программе должны быть заменяемыми на экземпляры их подтипов без изменения правильности выполнения программы.
  - **Interface Segregation Principle (ISP)**: Клиенты не должны зависеть от интерфейсов, которые они не используют.
  - **Dependency Inversion Principle (DIP)**: Зависимости должны строиться относительно абстракций, а не деталей.

- **DRY (Don't Repeat Yourself)**: Не повторяйся - избегать дублирования кода, вынося повторяющуюся логику в функции или классы.

- **KISS (Keep It Simple, Stupid)**: Делай это проще - код должен быть простым и понятным, избегая ненужной сложности.

- **YAGNI (You Aren't Gonna Need It)**: Тебе это не понадобится - не добавляй функциональность, которая пока не нужна.

## Recent Improvements

1. **Architecture Refactoring**:
   - Removed duplicate methods in Game class
   - Implemented State Management system for better game flow control
   - Added Object Pooling for bullets and enemies to improve performance
   - Created Component-based rendering system for better separation of concerns
   - Implemented Factory pattern for enemy creation

2. **Performance Improvements**:
   - Object pooling reduces garbage collection overhead
   - Reusable starfield objects in renderer
   - More efficient collision detection

3. **Extensibility Enhancements**:
   - GameObject interface for consistent entity behavior
   - EnemyFactory for easy addition of new enemy types
   - RenderComponent system for flexible rendering
   - SettingsManager for persistent configuration

4. **Music System Improvements**:
   - Centralized music management in SoundManager
   - Proper fade in/out effects for music transitions
   - Volume control synchronization with settings
   - Separation of music and visual fade effects
   - Separate music tracks for menu and gameplay
   - Automatic music switching between menu and game states

5. **Maintainability Improvements**:
   - Better code organization with clear separation of concerns
   - Reduced coupling between components
   - More consistent event handling
   - Improved documentation and comments