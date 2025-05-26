# Centralized Game Configuration
# This file contains commonly accessed game variables and settings for easier maintenance

from enum import Enum, auto

# ============================================================================
# DISPLAY AND WINDOW SETTINGS
# ============================================================================

# Window settings
TITLE = "Simple Roguelike"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
DEFAULT_WINDOWED_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FULLSCREEN_ENABLED = True

# ============================================================================
# CAMERA AND ZOOM SETTINGS
# ============================================================================

# Zoom configuration
DEFAULT_ZOOM_LEVEL = 1.0
MIN_ZOOM_LEVEL = 0.5
MAX_ZOOM_LEVEL = 3.0
ZOOM_SENSITIVITY = 0.1  # How much zoom changes per scroll wheel tick

# ============================================================================
# PLAYER SETTINGS
# ============================================================================

# Player base stats
PLAYER_HEALTH = 100
PLAYER_SPEED = 5
PLAYER_DAMAGE = 10
PLAYER_FIRE_RATE = 500  # milliseconds between shots

# Player progression
UPGRADE_POINTS_PER_LEVEL = 1
MAX_HEALTH_UPGRADE = 20
MAX_DAMAGE_UPGRADE = 5
MAX_SPEED_UPGRADE = 0.5
FIRE_RATE_UPGRADE = 50

# ============================================================================
# ENEMY SETTINGS
# ============================================================================

# Enemy base stats
ENEMY_HEALTH = 30
ENEMY_SPEED = 3
ENEMY_DAMAGE = 5
ENEMY_FIRE_RATE = 1000  # milliseconds between shots

# Enemy scaling
MAX_ENEMIES_BASE = 10
ENEMY_SCALING_FACTOR = 2
MAX_ENEMIES_CAP = 30

# Boss settings
BOSS_HEALTH_MULTIPLIER = 3.0
BOSS_DAMAGE_MULTIPLIER = 1.5
BOSS_SIZE_MULTIPLIER = 1.5
BOSS_SPAWN_LEVEL = 5

# ============================================================================
# LEVEL GENERATION SETTINGS
# ============================================================================

# Level dimensions
LEVEL_WIDTH = 60  # in tiles
LEVEL_HEIGHT = 45  # in tiles
TILE_SIZE = 32

# Room generation
ROOM_MAX_SIZE = 12
ROOM_MIN_SIZE = 6
MAX_ROOMS = 35

# ============================================================================
# ITEM AND LOOT SETTINGS
# ============================================================================

# Item spawn rates
ITEMS_PER_LEVEL = 5
EQUIPMENT_DROP_CHANCE = 0.15

# Item effects
HEALTH_POTION_HEAL = 25
DAMAGE_BOOST_AMOUNT = 5
SPEED_BOOST_AMOUNT = 1
FIRE_RATE_BOOST_AMOUNT = 50

# Special item effects
SHIELD_DURATION = 300  # frames
SHIELD_ABSORPTION = 50
XP_BOOST_AMOUNT = 25
MULTI_SHOT_DURATION = 600  # frames
INVINCIBILITY_DURATION = 180  # frames

# ============================================================================
# EXPERIENCE AND PROGRESSION SETTINGS
# ============================================================================

# XP rewards
XP_PER_ENEMY_BASE = 10
XP_PER_ENEMY_FAST = 8
XP_PER_ENEMY_TANK = 15
XP_PER_BOSS = 50
XP_PER_LEVEL = 50
XP_DIFFICULTY_MULTIPLIER = 1.2

# Skill system
SKILL_POINTS_PER_LEVEL = 1
MAX_SKILL_LEVEL = 5

# ============================================================================
# SCORING SETTINGS
# ============================================================================

ENEMY_KILL_SCORE = 100
ITEM_COLLECT_SCORE = 50
LEVEL_COMPLETE_SCORE = 500

# ============================================================================
# UI AND HUD SETTINGS
# ============================================================================

# HUD transparency
HUD_BACKGROUND_ALPHA = 100  # Reduced from 180 for better transparency

# Progress bar settings
HEALTH_BAR_COLOR = (0, 255, 0)  # Green
XP_BAR_COLOR = (0, 255, 255)    # Cyan

# Pause overlay
PAUSE_OVERLAY_ALPHA = 128
PAUSE_TITLE_FONT_SIZE = 72
PAUSE_INSTRUCTION_FONT_SIZE = 36

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Memory management
MAX_XP_MESSAGES = 50
SPRITE_CACHE_PADDING = 100
SPRITE_CULLING_BUFFER = 64
VISIBLE_SPRITE_CACHE_ENABLED = True

# ============================================================================
# AUDIO SETTINGS
# ============================================================================

# Volume levels
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# ============================================================================
# GAME MECHANICS SETTINGS
# ============================================================================

# Projectile settings
PROJECTILE_SPEED = 10

# Pathfinding
PATHFINDING_MAX_DISTANCE = 200
RANDOM_MOVE_CHANCE = 0.02

# Equipment
EQUIPMENT_UPGRADE_COST_BASE = 100
EQUIPMENT_SET_BONUS_THRESHOLD = 2

# Achievement system
ACHIEVEMENT_XP_BONUS = 25

# ============================================================================
# GAME STATES
# ============================================================================

class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    UPGRADE = auto()
    PAUSE = auto()

# ============================================================================
# COLORS
# ============================================================================

# Basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Equipment rarity colors
EQUIPMENT_RARITY_COLORS = {
    "Common": (200, 200, 200),      # Light Gray
    "Uncommon": (0, 255, 0),        # Green
    "Rare": (0, 100, 255),          # Blue
    "Epic": (128, 0, 128)           # Purple
}
