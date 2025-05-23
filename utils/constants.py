# Game constants
from enum import Enum, auto

TITLE = "Simple Roguelike"
# Increased default window size for better modern display compatibility
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Display settings
DEFAULT_WINDOWED_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FULLSCREEN_ENABLED = True

# Game states
class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    UPGRADE = auto()
    PAUSE = auto()

# Colors
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

# Game settings
TILE_SIZE = 32
PLAYER_SPEED = 5
ENEMY_SPEED = 3
PROJECTILE_SPEED = 10
PLAYER_HEALTH = 100
ENEMY_HEALTH = 30
PLAYER_DAMAGE = 10
ENEMY_DAMAGE = 5
PLAYER_FIRE_RATE = 500  # milliseconds between shots
ENEMY_FIRE_RATE = 1000  # milliseconds between shots

# Item settings
HEALTH_POTION_HEAL = 25
ITEMS_PER_LEVEL = 5  # Increased from 3
DAMAGE_BOOST_AMOUNT = 5
SPEED_BOOST_AMOUNT = 1
FIRE_RATE_BOOST_AMOUNT = 50  # milliseconds reduction

# New item effects
SHIELD_DURATION = 300  # frames (5 seconds at 60 FPS)
SHIELD_ABSORPTION = 50  # damage absorbed
XP_BOOST_AMOUNT = 25   # bonus XP
MULTI_SHOT_DURATION = 600  # frames (10 seconds)
INVINCIBILITY_DURATION = 180  # frames (3 seconds)

# Score settings
ENEMY_KILL_SCORE = 100
ITEM_COLLECT_SCORE = 50
LEVEL_COMPLETE_SCORE = 500
XP_PER_ENEMY = 10
XP_PER_LEVEL = 50

# Level generation
LEVEL_WIDTH = 60  # in tiles (increased for fullscreen support)
LEVEL_HEIGHT = 45  # in tiles (increased for fullscreen support)
ROOM_MAX_SIZE = 12  # Increased from 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 35  # Increased for larger levels
MAX_ENEMIES_BASE = 10  # Base number of enemies
ENEMY_SCALING_FACTOR = 2  # Additional enemies per level
MAX_ENEMIES_CAP = 30  # Maximum enemies regardless of level

# Boss enemy settings
BOSS_HEALTH_MULTIPLIER = 3.0  # Boss health multiplier
BOSS_DAMAGE_MULTIPLIER = 1.5  # Boss damage multiplier
BOSS_SIZE_MULTIPLIER = 1.5   # Boss size multiplier
BOSS_SPAWN_LEVEL = 5         # Level interval for boss spawns

# Pathfinding
PATHFINDING_MAX_DISTANCE = 200  # Maximum distance for pathfinding in pixels
RANDOM_MOVE_CHANCE = 0.02  # Chance to change direction during random movement

# Player upgrade system
UPGRADE_POINTS_PER_LEVEL = 1
MAX_HEALTH_UPGRADE = 20  # Health increase per upgrade
MAX_DAMAGE_UPGRADE = 5   # Damage increase per upgrade
MAX_SPEED_UPGRADE = 0.5  # Speed increase per upgrade
FIRE_RATE_UPGRADE = 50   # Fire rate reduction per upgrade (milliseconds)

# Asset paths
PLAYER_IMG = "assets/images/player.png"
ENEMY_IMG = "assets/images/enemy.png"
WALL_IMG = "assets/images/wall.png"
FLOOR_IMG = "assets/images/floor.png"
PLAYER_PROJECTILE_IMG = "assets/images/player_projectile.png"
ENEMY_PROJECTILE_IMG = "assets/images/enemy_projectile.png"
HEALTH_POTION_IMG = "assets/images/health_potion.png"
DAMAGE_BOOST_IMG = "assets/images/damage_boost.png"
SPEED_BOOST_IMG = "assets/images/speed_boost.png"
FIRE_RATE_BOOST_IMG = "assets/images/fire_rate_boost.png"

# Audio settings
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Audio paths
PLAYER_SHOOT_SOUND = "assets/sounds/player_shoot.wav"
ENEMY_SHOOT_SOUND = "assets/sounds/enemy_shoot.wav"
ENEMY_DEATH_SOUND = "assets/sounds/enemy_death.wav"
ITEM_COLLECT_SOUND = "assets/sounds/item_collect.wav"
LEVEL_UP_SOUND = "assets/sounds/level_up.wav"
PLAYER_HURT_SOUND = "assets/sounds/player_hurt.wav"
BACKGROUND_MUSIC = "assets/sounds/background_music.ogg"
MENU_MUSIC = "assets/sounds/menu_music.ogg"
