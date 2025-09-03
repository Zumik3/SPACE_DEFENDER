# SPACE DEFENDER


A Python-based space shooter game built with Pygame.

## Features
- Classic space shooter gameplay
- Enemy ships with different health levels
- Power-up system (health and fire rate boosters)
- Adjustable volume settings for music and sound effects
- Main menu with New Game, Settings, and Exit options
- Improved architecture with object pooling for better performance
- State management system for game states
- Settings persistence between sessions
- Component-based rendering system
- Factory pattern for enemy creation
- Separate music tracks for menu and gameplay

## Controls
- **Arrow Keys**: Move spaceship
- **Enter**: Confirm selection / Restart game
- **ESC**: Return to menu
- **Mouse**: Adjust volume sliders in Settings

## Requirements
- Python 3.x
- Pygame library

## Installation
```bash
pip install pygame
```

## Running the Game
```bash
python main.py
```

## Architecture Overview
The game follows an improved architecture with the following key components:

- **State Management**: Game states (menu, playing, paused, game over) are managed through a dedicated state manager
- **Object Pooling**: Reusable objects (bullets, enemies) are managed through an object pool to reduce garbage collection
- **Component-Based Rendering**: Separate render components for different game entities
- **Factory Pattern**: Enemy creation is handled through a factory for better extensibility
- **Settings Persistence**: Game settings are saved to a JSON file for persistence between sessions
- **Interface-Based Design**: Game objects implement a common interface for consistency
- **Music System**: Centralized music management with fade in/out effects, volume control, and separate tracks for menu and gameplay

## Extending the Game
The modular architecture makes it easy to extend the game with new features:
- Add new enemy types by extending the Enemy class and updating the EnemyFactory
- Create new power-ups by extending the Powerup class
- Implement new game states by adding to the GameState enum and StateManager
- Add new rendering components for different visual effects
- Extend the music system with new tracks or effects