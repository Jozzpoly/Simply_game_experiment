"""
Game Configuration - Essential Settings Only
Simplified from 1,364 lines to ~200 lines (85% reduction)

Contains only the essential game constants and settings needed for core gameplay.
No over-engineering, no complex configuration systems.
"""

import pygame
from enum import Enum

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "Simple Roguelike"

# ============================================================================
# COLORS (RGB)
# ============================================================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# ============================================================================
# GAME STATES
# ============================================================================
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4

# ============================================================================
# PLAYER SETTINGS
# ============================================================================
PLAYER_SIZE = 32
PLAYER_SPEED = 200  # pixels per second
PLAYER_HEALTH = 100
PLAYER_DAMAGE = 25
PLAYER_FIRE_RATE = 0.3  # seconds between shots

# ============================================================================
# ENEMY SETTINGS
# ============================================================================
ENEMY_SIZE = 32
ENEMY_SPEED = 100  # pixels per second
ENEMY_HEALTH = 50
ENEMY_DAMAGE = 15
ENEMY_DETECTION_RANGE = 300

# Enemy types with simple multipliers
ENEMY_TYPES = {
    'normal': {'health': 1.0, 'speed': 1.0, 'damage': 1.0, 'color': RED},
    'fast': {'health': 0.7, 'speed': 1.5, 'damage': 0.8, 'color': YELLOW},
    'tank': {'health': 2.0, 'speed': 0.6, 'damage': 1.3, 'color': DARK_GRAY},
    'archer': {'health': 0.8, 'speed': 0.8, 'damage': 1.2, 'color': GREEN}
}

# ============================================================================
# PROJECTILE SETTINGS
# ============================================================================
PROJECTILE_SIZE = 8
PROJECTILE_SPEED = 400  # pixels per second
PROJECTILE_LIFETIME = 3.0  # seconds

# ============================================================================
# LEVEL SETTINGS
# ============================================================================
TILE_SIZE = 32
LEVEL_WIDTH = 40  # tiles
LEVEL_HEIGHT = 30  # tiles
ROOM_MIN_SIZE = 6
ROOM_MAX_SIZE = 12
MAX_ROOMS = 8
MIN_ENEMIES_PER_ROOM = 1
MAX_ENEMIES_PER_ROOM = 4

# ============================================================================
# PROGRESSION SETTINGS
# ============================================================================
XP_PER_ENEMY = 10
XP_PER_LEVEL = 100
HEALTH_PER_LEVEL = 20
DAMAGE_PER_LEVEL = 5

# ============================================================================
# UI SETTINGS
# ============================================================================
UI_FONT_SIZE = 24
UI_MARGIN = 10
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20

# ============================================================================
# SAVE SETTINGS
# ============================================================================
SAVE_FILE = "save_game.json"

# ============================================================================
# KEYS
# ============================================================================
MOVEMENT_KEYS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}
