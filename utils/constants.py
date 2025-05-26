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

# XP System - Enhanced with enemy type variations
XP_PER_ENEMY_BASE = 10
XP_PER_ENEMY_FAST = 8   # Fast enemies give less XP (easier to kill)
XP_PER_ENEMY_TANK = 15  # Tank enemies give more XP (harder to kill)
XP_PER_ENEMY_SNIPER = 18  # Sniper enemies give high XP (dangerous)
XP_PER_ENEMY_BERSERKER = 20  # Berserker enemies give highest XP (very dangerous)
XP_PER_BOSS = 50        # Boss enemies give significant XP
XP_PER_LEVEL = 50
XP_DIFFICULTY_MULTIPLIER = 1.2  # XP multiplier per difficulty level

# Skill Tree System
SKILL_POINTS_PER_LEVEL = 1
MAX_SKILL_LEVEL = 5

# Equipment System
EQUIPMENT_DROP_CHANCE = 0.15  # 15% chance for equipment drop
EQUIPMENT_UPGRADE_COST_BASE = 100  # Base cost to upgrade equipment
EQUIPMENT_RARITY_WEIGHTS = [0.6, 0.25, 0.12, 0.03]  # Common, Uncommon, Rare, Epic

# Achievement System
ACHIEVEMENT_XP_BONUS = 25

# Advanced Achievement Types
ACHIEVEMENT_TYPES = {
    "SIMPLE": "simple",      # Single condition achievement
    "PROGRESSIVE": "progressive",  # Multi-step achievement with progress tracking
    "CHAIN": "chain",        # Achievement that unlocks after completing prerequisites
    "HIDDEN": "hidden"       # Achievement not visible until unlocked
}

# Achievement Chain Definitions
ACHIEVEMENT_CHAINS = {
    "warrior_path": {
        "name": "Path of the Warrior",
        "description": "Master the art of combat",
        "achievements": ["first_blood", "enemy_slayer", "boss_hunter", "combat_master"],
        "chain_reward": {"xp": 500, "skill_points": 5}
    },
    "survivor_path": {
        "name": "Path of the Survivor",
        "description": "Prove your resilience",
        "achievements": ["first_steps", "damage_dealer", "perfectionist", "immortal"],
        "chain_reward": {"xp": 400, "skill_points": 4}
    },
    "explorer_path": {
        "name": "Path of the Explorer",
        "description": "Discover all secrets",
        "achievements": ["collector", "treasure_hunter", "secret_finder", "master_explorer"],
        "chain_reward": {"xp": 300, "skill_points": 3}
    }
}

# Level generation - Enhanced for progressive scaling
LEVEL_WIDTH = 60  # in tiles (base size, will scale with level)
LEVEL_HEIGHT = 45  # in tiles (base size, will scale with level)
ROOM_MAX_SIZE = 12  # Base maximum room size
ROOM_MIN_SIZE = 6   # Base minimum room size
MAX_ROOMS = 35      # Base number of rooms (will scale with level)
MAX_ENEMIES_BASE = 10  # Base number of enemies
ENEMY_SCALING_FACTOR = 2  # Additional enemies per level
MAX_ENEMIES_CAP = 60  # Maximum enemies regardless of level (increased for larger maps)

# Boss enemy settings
BOSS_HEALTH_MULTIPLIER = 3.0  # Boss health multiplier
BOSS_DAMAGE_MULTIPLIER = 1.5  # Boss damage multiplier
BOSS_SIZE_MULTIPLIER = 2.0   # Boss size multiplier (64x64 sprites vs 32x32 regular)
BOSS_SPAWN_LEVEL = 5         # Level interval for boss spawns

# Pathfinding
PATHFINDING_MAX_DISTANCE = 200  # Maximum distance for pathfinding in pixels
RANDOM_MOVE_CHANCE = 0.02  # Chance to change direction during random movement

# Player upgrade system - Enhanced
UPGRADE_POINTS_PER_LEVEL = 1
MAX_HEALTH_UPGRADE = 20  # Health increase per upgrade
MAX_DAMAGE_UPGRADE = 5   # Damage increase per upgrade
MAX_SPEED_UPGRADE = 0.5  # Speed increase per upgrade
FIRE_RATE_UPGRADE = 50   # Fire rate reduction per upgrade (milliseconds)

# Skill Tree Categories
SKILL_CATEGORIES = ["combat", "survival", "utility"]

# Combat Skills
COMBAT_SKILLS = {
    "critical_strike": {"max_level": 5, "base_chance": 0.05, "chance_per_level": 0.03},
    "multi_shot": {"max_level": 3, "projectiles_per_level": 1},
    "piercing_shots": {"max_level": 3, "pierce_count_per_level": 1},
    "explosive_shots": {"max_level": 3, "explosion_radius_per_level": 20},
    "weapon_mastery": {"max_level": 5, "damage_bonus_per_level": 0.1}
}

# Survival Skills
SURVIVAL_SKILLS = {
    "armor_mastery": {"max_level": 5, "damage_reduction_per_level": 0.05},
    "health_regeneration": {"max_level": 3, "regen_per_level": 1, "regen_interval": 180},
    "shield_mastery": {"max_level": 3, "shield_bonus_per_level": 0.2},
    "damage_resistance": {"max_level": 5, "resistance_per_level": 0.03},
    "second_wind": {"max_level": 1, "health_threshold": 0.25, "heal_amount": 0.5}
}

# Utility Skills
UTILITY_SKILLS = {
    "movement_mastery": {"max_level": 5, "speed_bonus_per_level": 0.1},
    "resource_efficiency": {"max_level": 3, "xp_bonus_per_level": 0.15},
    "item_magnetism": {"max_level": 3, "range_per_level": 50},
    "detection": {"max_level": 3, "range_bonus_per_level": 100},
    "lucky_find": {"max_level": 3, "drop_chance_bonus_per_level": 0.05}
}

# Skill Synergies - combinations that provide bonus effects
SKILL_SYNERGIES = {
    # Combat synergies
    "critical_mastery": {
        "skills": ["critical_strike", "weapon_mastery"],
        "min_levels": [3, 2],
        "bonus": {"critical_damage_multiplier": 0.5}  # +50% crit damage
    },
    "explosive_expert": {
        "skills": ["explosive_shots", "piercing_shots"],
        "min_levels": [2, 2],
        "bonus": {"explosion_pierce": True}  # Explosions can pierce
    },
    "combat_veteran": {
        "skills": ["critical_strike", "multi_shot", "weapon_mastery"],
        "min_levels": [2, 2, 3],
        "bonus": {"damage_bonus": 0.2, "fire_rate_bonus": 0.15}
    },

    # Survival synergies
    "fortress": {
        "skills": ["armor_mastery", "damage_resistance"],
        "min_levels": [3, 3],
        "bonus": {"damage_reduction": 0.1}  # Additional 10% damage reduction
    },
    "regenerative_defense": {
        "skills": ["health_regeneration", "shield_mastery"],
        "min_levels": [2, 2],
        "bonus": {"regen_multiplier": 1.5}  # 50% faster regeneration
    },
    "survivor": {
        "skills": ["armor_mastery", "health_regeneration", "second_wind"],
        "min_levels": [2, 2, 1],
        "bonus": {"max_health_bonus": 0.25}  # +25% max health
    },

    # Utility synergies
    "treasure_hunter": {
        "skills": ["lucky_find", "detection"],
        "min_levels": [2, 2],
        "bonus": {"rare_drop_chance": 0.1}  # +10% rare drop chance
    },
    "efficiency_master": {
        "skills": ["resource_efficiency", "movement_mastery"],
        "min_levels": [2, 3],
        "bonus": {"xp_bonus": 0.1, "speed_bonus": 0.1}
    },

    # Cross-category synergies
    "battle_mage": {
        "skills": ["explosive_shots", "item_magnetism"],
        "min_levels": [2, 2],
        "bonus": {"explosion_radius": 10}  # +10 explosion radius
    },
    "swift_warrior": {
        "skills": ["movement_mastery", "critical_strike"],
        "min_levels": [3, 2],
        "bonus": {"speed_crit_bonus": 0.02}  # +2% crit per speed point above base
    }
}

# Equipment Rarities and Stats
EQUIPMENT_RARITIES = ["Common", "Uncommon", "Rare", "Epic"]
EQUIPMENT_RARITY_COLORS = {
    "Common": (200, 200, 200),      # Light Gray
    "Uncommon": (0, 255, 0),        # Green
    "Rare": (0, 100, 255),          # Blue
    "Epic": (128, 0, 128)           # Purple
}

# Equipment Set Bonuses
EQUIPMENT_SET_BONUS_THRESHOLD = 2  # Minimum items needed for set bonus
EQUIPMENT_SET_BONUSES = {
    "Common": {"health_bonus": 10, "damage_bonus": 2},
    "Uncommon": {"health_bonus": 20, "damage_bonus": 5, "speed_bonus": 0.5},
    "Rare": {"health_bonus": 35, "damage_bonus": 8, "speed_bonus": 1.0, "xp_bonus": 0.1},
    "Epic": {"health_bonus": 50, "damage_bonus": 12, "speed_bonus": 1.5, "xp_bonus": 0.2, "critical_chance": 0.05}
}

# Equipment Types
EQUIPMENT_TYPES = ["weapon", "armor", "accessory"]

# Equipment Icon Mapping
EQUIPMENT_ICON_MAPPING = {
    # Weapons
    "Sword": "assets/images/equipment/weapons/sword.png",
    "Rifle": "assets/images/equipment/weapons/rifle.png",
    "Cannon": "assets/images/equipment/weapons/cannon.png",
    "Blaster": "assets/images/equipment/weapons/blaster.png",
    "Launcher": "assets/images/equipment/weapons/launcher.png",

    # Armor
    "Vest": "assets/images/equipment/armor/vest.png",
    "Plate": "assets/images/equipment/armor/plate.png",
    "Mail": "assets/images/equipment/armor/mail.png",
    "Shield": "assets/images/equipment/armor/shield.png",
    "Barrier": "assets/images/equipment/armor/barrier.png",

    # Accessories
    "Ring": "assets/images/equipment/accessories/ring.png",
    "Amulet": "assets/images/equipment/accessories/amulet.png",
    "Charm": "assets/images/equipment/accessories/charm.png",
    "Orb": "assets/images/equipment/accessories/orb.png",
    "Crystal": "assets/images/equipment/accessories/crystal.png"
}

# Weapon Stats
WEAPON_BASE_STATS = {
    "damage_bonus": 0,
    "fire_rate_bonus": 0,
    "critical_chance": 0,
    "projectile_speed": 0
}

# Armor Stats
ARMOR_BASE_STATS = {
    "health_bonus": 0,
    "damage_reduction": 0,
    "speed_bonus": 0,
    "regeneration": 0
}

# Accessory Stats
ACCESSORY_BASE_STATS = {
    "xp_bonus": 0,
    "item_find": 0,
    "skill_cooldown": 0,
    "resource_bonus": 0
}

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
SHIELD_BOOST_IMG = "assets/images/shield_boost.png"
XP_BOOST_IMG = "assets/images/xp_boost.png"
MULTI_SHOT_BOOST_IMG = "assets/images/multi_shot_boost.png"
INVINCIBILITY_BOOST_IMG = "assets/images/invincibility_boost.png"

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

# UI Constants for improved consistency
PAUSE_OVERLAY_ALPHA = 128
PAUSE_TITLE_FONT_SIZE = 72
PAUSE_INSTRUCTION_FONT_SIZE = 36

# Performance and Memory Management
MAX_XP_MESSAGES = 50  # Maximum floating XP messages to prevent memory leaks
SPRITE_CACHE_PADDING = 100  # Padding around screen for sprite culling
VISIBLE_SPRITE_LOG_THRESHOLD = 100  # Log sprite count when above this threshold
SPRITE_CULLING_BUFFER = 64  # Buffer pixels for sprite culling

# Rendering optimization
VISIBLE_SPRITE_CACHE_ENABLED = True  # Enable sprite culling cache
