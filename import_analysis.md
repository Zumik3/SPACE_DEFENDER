# Анализ импортов в проекте SPACE_DEFENDER

## Общие замечания:
1. В проекте используются как абсолютные, так и относительные импорты
2. Некоторые импорты не соответствуют стандарту PEP 8 (порядок, группировка)
3. Есть дублирующиеся импорты в некоторых файлах
4. Некоторые импорты расположены не в начале файла

## Файлы и их импорты:

### main.py
```python
import pygame
import sys
from game.game_manager import GameManager
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE
```

### game/__init__.py
```python
# Пустой файл
```

### game/game_logic.py
```python
import random
import pygame
from core.player import Player
from core.bullet import Bullet
from core.enemy_factory import EnemyFactory
from core.powerup import Powerup
from utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, ENEMY_SPEED, 
    BULLET_SPEED, POWERUP_SPEED, ENEMY_SPAWN_EVENT, 
    PLAYER_SHOOT_EVENT, ENEMY_SHOOT_EVENT, FONT
)
```

### game/game_manager.py
```python
import pygame
from game.state_manager import StateManager
from game.renderer import Renderer
from game.event_handler import EventHandler
from game.object_pool_manager import ObjectPoolManager
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from utils.sound_manager import SoundManager
```

### game/event_handler.py
```python
import pygame
from core.bullet import Bullet
from utils.constants import PLAYER_SHOOT_EVENT, ENEMY_SHOOT_EVENT
```

### game/object_pool.py
```python
# Нет импортов
```

### game/object_pool_manager.py
```python
from game.object_pool import ObjectPool
```

### game/renderer.py
```python
import pygame
from ui.render_components import (
    draw_player_component,
    draw_enemy_component,
    draw_bullet_component,
    draw_powerup_component,
    draw_starfield_component,
    draw_hud_component
)
from utils.constants import BLACK
```

### game/state_manager.py
```python
# Нет импортов
```

### game/state_machine.py
```python
# Нет импортов
```

### game/transition_manager.py
```python
# Нет импортов
```

### core/__init__.py
```python
# Пустой файл
```

### core/base_enemy.py
```python
import pygame
from core.game_object import GameObject
from utils.constants import ENEMY_WIDTH, ENEMY_HEIGHT
```

### core/bullet.py
```python
import pygame
from core.game_object import GameObject
from utils.constants import BULLET_WIDTH, BULLET_HEIGHT
```

### core/enemy_factory.py
```python
from core.normal_enemy import NormalEnemy
from core.strong_enemy import StrongEnemy
```

### core/game_object.py
```python
import pygame
```

### core/normal_enemy.py
```python
import random
from core.base_enemy import BaseEnemy
from utils.constants import ENEMY_WIDTH, ENEMY_HEIGHT, WHITE
```

### core/player.py
```python
import pygame
from core.game_object import GameObject
from utils.constants import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, 
    PLAYER_SHOOT_EVENT, BULLET_WIDTH, BULLET_HEIGHT
)
```

### core/powerup.py
```python
import pygame
from core.game_object import GameObject
from utils.constants import POWERUP_WIDTH, POWERUP_HEIGHT
```

### core/strong_enemy.py
```python
import random
from core.base_enemy import BaseEnemy
from core.bullet import Bullet
from utils.constants import ENEMY_WIDTH, ENEMY_HEIGHT, WHITE
```

### ui/__init__.py
```python
# Пустой файл
```

### ui/hub.py
```python
import pygame
from ui.ui_screen import UIScreen
from ui.menu import Menu
from ui.settings import Settings
from utils.constants import WHITE
```

### ui/menu.py
```python
import pygame
from ui.ui_screen import UIScreen
from utils.constants import WHITE, FONT
```

### ui/pixel_title.py
```python
import pygame
from utils.constants import WHITE
```

### ui/render_component.py
```python
import pygame
# Пустой файл
```

### ui/render_components.py
```python
import pygame
from utils.constants import WHITE, RED, BLUE
```

### ui/renderer.py
```python
import pygame
from utils.constants import BLACK, WHITE
```

### ui/settings.py
```python
import pygame
from ui.ui_screen import UIScreen
from utils.constants import WHITE
from utils.settings_manager import SettingsManager
```

### ui/ui_screen.py
```python
import pygame
```

### utils/__init__.py
```python
# Пустой файл
```

### utils/constants.py
```python
import pygame
```

### utils/event_manager.py
```python
import pygame
```

### utils/settings_manager.py
```python
import json
import os
```

### utils/sound_manager.py
```python
import pygame
import os
```

### assets/__init__.py
```python
# Пустой файл
```