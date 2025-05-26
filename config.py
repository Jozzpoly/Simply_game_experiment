# Centralized Game Configuration
# This file contains commonly accessed game variables and settings for easier maintenance

from enum import Enum, auto
import pygame

# ============================================================================
# DISPLAY AND WINDOW SETTINGS
# ============================================================================

# Window settings
TITLE = "Simple Roguelike"
SCREEN_WIDTH = 1880
SCREEN_HEIGHT = 920
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
PLAYER_BASE_SPEED = 2.0  # Significantly increased from 5 for faster gameplay
PLAYER_DAMAGE = 10
PLAYER_FIRE_RATE = 500  # milliseconds between shots

# Player progression
UPGRADE_POINTS_PER_LEVEL = 1
MAX_HEALTH_UPGRADE = 20
MAX_DAMAGE_UPGRADE = 5
MAX_SPEED_UPGRADE = 0.3  # Reduced from 0.5 to prevent game becoming too difficult
FIRE_RATE_UPGRADE = 50

# ============================================================================
# ENEMY SETTINGS
# ============================================================================

# Enemy base stats
ENEMY_HEALTH = 30
ENEMY_BASE_SPEED = 1.0  # Significantly increased from 3 for more challenging gameplay
ENEMY_DAMAGE = 5
ENEMY_FIRE_RATE = 1000  # milliseconds between shots

# Enemy type speed multipliers
ENEMY_SPEED_MULTIPLIERS = {
    "normal": 1.0,
    "fast": 1.5,
    "tank": 0.7,
    "berserker": 1.3,
    "boss": 0.8
}

# Enemy scaling - Increased density significantly
MAX_ENEMIES_BASE = 50  # Increased from 10
ENEMY_SCALING_FACTOR = 4  # Increased from 2
MAX_ENEMIES_CAP = 120  # Increased from 30

# Boss settings
BOSS_HEALTH_MULTIPLIER = 3.0
BOSS_DAMAGE_MULTIPLIER = 1.5
BOSS_SIZE_MULTIPLIER = 2.0
BOSS_SPAWN_LEVEL = 5

# ============================================================================
# LEVEL GENERATION SETTINGS
# ============================================================================

# Level dimensions
LEVEL_WIDTH = 60  # in tiles
LEVEL_HEIGHT = 45  # in tiles
TILE_SIZE = 32

# Dynamic terrain generation based on camera
DYNAMIC_TERRAIN_ENABLED = True
TERRAIN_GENERATION_RADIUS = 40  # tiles around camera to generate
TERRAIN_CHUNK_SIZE = 16  # tiles per chunk for efficient generation
TERRAIN_CACHE_SIZE = 100  # maximum cached chunks

# Enhanced Terrain System
TERRAIN_VARIETY_ENABLED = True
TERRAIN_BIOME_SYSTEM_ENABLED = True
TERRAIN_DECORATION_DENSITY = 0.3  # 0.0 to 1.0 - density of decorative elements

# Terrain Types and Textures
TERRAIN_TYPES = {
    'floor': 0,
    'wall': 1,
    'grass': 2,
    'dirt': 3,
    'stone': 4,
    'water': 5,
    'wood': 6,
    'sand': 7,
    'gravel': 8
}

# Biome Configuration
BIOME_TYPES = {
    'dungeon': {'primary': 'floor', 'secondary': 'stone', 'decoration': 'gravel'},
    'forest': {'primary': 'grass', 'secondary': 'dirt', 'decoration': 'wood'},
    'cave': {'primary': 'stone', 'secondary': 'gravel', 'decoration': 'water'},
    'ruins': {'primary': 'stone', 'secondary': 'sand', 'decoration': 'wood'},
    'swamp': {'primary': 'dirt', 'secondary': 'water', 'decoration': 'grass'}
}

# Terrain Generation Parameters
TERRAIN_NOISE_SCALE = 0.1  # Scale for procedural noise
TERRAIN_SMOOTHING_PASSES = 2  # Number of smoothing iterations
TERRAIN_FEATURE_DENSITY = 0.15  # Density of special terrain features

# Room generation
ROOM_MAX_SIZE = 12
ROOM_MIN_SIZE = 6
MAX_ROOMS = 35

# Progressive level scaling
LEVEL_SIZE_SCALING_FACTOR = 1.8  # How much larger each level gets
MAX_LEVEL_SIZE_MULTIPLIER = 8.0  # Maximum size increase
ROOM_DENSITY_PER_LEVEL = 0.1  # Additional room density per level

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
# KEYBOARD SHORTCUTS
# ============================================================================

# UI shortcuts
KEY_INVENTORY = pygame.K_i  # Equipment/Inventory screen
KEY_SKILLS = pygame.K_k     # Skills screen
KEY_ACHIEVEMENTS = pygame.K_o  # Achievements screen
KEY_CHARACTER_STATS = pygame.K_c  # Character stats screen
KEY_UPGRADE_MENU = pygame.K_u  # Upgrade menu (existing)
KEY_PAUSE = pygame.K_p      # Pause game (existing)

# Movement keys (for reference)
MOVEMENT_KEYS = {
    'up': [pygame.K_w, pygame.K_UP],
    'down': [pygame.K_s, pygame.K_DOWN],
    'left': [pygame.K_a, pygame.K_LEFT],
    'right': [pygame.K_d, pygame.K_RIGHT]
}

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Memory management
MAX_XP_MESSAGES = 50
SPRITE_CACHE_PADDING = 100
SPRITE_CULLING_BUFFER = 64
VISIBLE_SPRITE_CACHE_ENABLED = True

# Performance Monitoring
PERFORMANCE_MONITORING_ENABLED = True
PERFORMANCE_LOG_INTERVAL = 300  # frames between performance logs
FPS_TARGET = 60  # Target FPS for performance optimization
FPS_WARNING_THRESHOLD = 45  # Log warning if FPS drops below this
MEMORY_MONITORING_ENABLED = True
MEMORY_WARNING_THRESHOLD = 500  # MB - warn if memory usage exceeds this

# Adaptive Performance System
ADAPTIVE_PERFORMANCE_ENABLED = True
AUTO_REDUCE_ENEMIES_ON_LAG = True
AUTO_REDUCE_PARTICLES_ON_LAG = True
AUTO_REDUCE_EFFECTS_ON_LAG = True
PERFORMANCE_ADJUSTMENT_THRESHOLD = 40  # FPS threshold for automatic adjustments

# Rendering optimization
MAX_VISIBLE_ENEMIES = 50  # Limit enemies rendered at once
PARTICLE_SYSTEM_ENABLED = True
MAX_PARTICLES = 200
ANIMATION_FRAME_SKIP = 0  # Skip frames for performance (0 = no skip)

# Enemy Performance Optimization
ENEMY_AI_OPTIMIZATION_ENABLED = True
ENEMY_AI_UPDATE_DISTANCE = 800  # pixels - enemies beyond this distance use simplified AI
ENEMY_AI_SLEEP_DISTANCE = 1200  # pixels - enemies beyond this distance sleep
ENEMY_AI_UPDATE_FREQUENCY_DISTANT = 10  # frames between updates for distant enemies
ENEMY_AI_UPDATE_FREQUENCY_CLOSE = 1  # frames between updates for close enemies
ENEMY_LOD_SYSTEM_ENABLED = True  # Level of Detail system for enemies
ENEMY_CULLING_ENABLED = True  # Completely disable enemies very far away
ENEMY_CULLING_DISTANCE = 2000  # pixels - enemies beyond this are completely disabled
MAX_ACTIVE_ENEMIES = 100  # Maximum number of enemies that can be active at once

# Camera performance
CAMERA_SMOOTH_FOLLOW = True
CAMERA_FOLLOW_SPEED = 0.1  # 0.1 = smooth, 1.0 = instant

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

# Pathfinding and AI behavior
PATHFINDING_MAX_DISTANCE = 200
RANDOM_MOVE_CHANCE = 0.02
ENEMY_DETECTION_RADIUS = 300  # pixels
ENEMY_ATTACK_RANGE = 150  # pixels
ENEMY_GROUP_COORDINATION_RANGE = 100  # pixels for group behavior
ENEMY_RETREAT_HEALTH_THRESHOLD = 0.2  # retreat when health below 20%
ENEMY_AGGRESSION_SCALING = 0.1  # aggression increase per level
ENEMY_FORMATION_SPACING = 40  # pixels between enemies in formation
ENEMY_PATROL_RADIUS = 80  # pixels for patrol behavior
ENEMY_IDLE_DURATION_MIN = 1000  # milliseconds
ENEMY_IDLE_DURATION_MAX = 3000  # milliseconds

# Equipment
EQUIPMENT_UPGRADE_COST_BASE = 100
EQUIPMENT_SET_BONUS_THRESHOLD = 2

# ============================================================================
# LEVEL COMPLETION SETTINGS
# ============================================================================

# Stair system for level progression
STAIRS_ENABLED = True
REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS = True  # Require defeating % of enemies to unlock stairs
ENEMY_DEFEAT_PERCENTAGE_FOR_STAIRS = 0.5  # 50% of enemies must be defeated
STAIRS_UNLOCK_MESSAGE_DURATION = 180  # 3 seconds at 60 FPS

# Camera system improvements
CAMERA_FOLLOW_BEYOND_BOUNDARIES = True  # Allow camera to follow player beyond map edges
CAMERA_BOUNDARY_BUFFER = 100  # Pixels of buffer beyond map edges

# Achievement system
ACHIEVEMENT_XP_BONUS = 25

# ============================================================================
# ADVANCED GAME BALANCE
# ============================================================================

# Difficulty scaling
DIFFICULTY_SCALING_ENABLED = True
DIFFICULTY_INCREASE_PER_LEVEL = 0.15  # 15% increase per level
MAX_DIFFICULTY_MULTIPLIER = 5.0  # Cap difficulty scaling

# Combat balance
CRITICAL_HIT_CHANCE = 0.05  # 5% base critical hit chance
CRITICAL_HIT_MULTIPLIER = 2.0  # 2x damage on critical hits
DODGE_CHANCE_BASE = 0.02  # 2% base dodge chance
BLOCK_CHANCE_BASE = 0.03  # 3% base block chance

# Loot and rewards scaling
LOOT_QUALITY_SCALING = 0.1  # Better loot quality per level
RARE_ITEM_CHANCE_BASE = 0.05  # 5% base chance for rare items
EQUIPMENT_DURABILITY_ENABLED = False  # Equipment degradation system

# Visual feedback settings
DAMAGE_NUMBER_DISPLAY = True
DAMAGE_NUMBER_DURATION = 60  # frames
SCREEN_SHAKE_ENABLED = True
SCREEN_SHAKE_INTENSITY = 2  # pixels
FLASH_EFFECT_ENABLED = True

# Minimap settings
MINIMAP_ENABLED = True
MINIMAP_SIZE = 150  # pixels
MINIMAP_TRANSPARENCY = 180  # alpha value
MINIMAP_UPDATE_FREQUENCY = 5  # frames between updates

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
