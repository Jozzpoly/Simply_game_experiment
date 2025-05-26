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
    "boss": 0.8,
    # Phase 2 new enemy types
    "mage": 0.8,
    "assassin": 1.8,
    "necromancer": 0.6,
    "golem": 0.4,
    "archer": 0.9,
    "shaman": 0.7,
    "berserker_elite": 1.4,
    "shadow": 2.0
}

# ============================================================================
# PHASE 2: NEW ENEMY TYPES CONFIGURATION
# ============================================================================

# Enhanced Enemy Type System
ENHANCED_ENEMY_TYPES = {
    # Existing types (maintained for compatibility)
    "normal": {
        "health_multiplier": 1.0,
        "damage_multiplier": 1.0,
        "speed_multiplier": 1.0,
        "fire_rate_multiplier": 1.0,
        "detection_radius": 300,
        "preferred_range": 150,
        "special_abilities": [],
        "ai_complexity": 1.0,
        "spawn_weight": 0.3
    },
    "fast": {
        "health_multiplier": 0.6,
        "damage_multiplier": 0.8,
        "speed_multiplier": 1.5,
        "fire_rate_multiplier": 0.8,
        "detection_radius": 350,
        "preferred_range": 100,
        "special_abilities": ["dash_attack"],
        "ai_complexity": 1.2,
        "spawn_weight": 0.2
    },
    "tank": {
        "health_multiplier": 2.0,
        "damage_multiplier": 1.3,
        "speed_multiplier": 0.7,
        "fire_rate_multiplier": 1.5,
        "detection_radius": 250,
        "preferred_range": 80,
        "special_abilities": ["armor_plating"],
        "ai_complexity": 1.0,
        "spawn_weight": 0.15
    },
    "sniper": {
        "health_multiplier": 0.8,
        "damage_multiplier": 1.8,
        "speed_multiplier": 0.9,
        "fire_rate_multiplier": 2.0,
        "detection_radius": 500,
        "preferred_range": 400,
        "special_abilities": ["precision_shot"],
        "ai_complexity": 1.5,
        "spawn_weight": 0.1
    },
    "berserker": {
        "health_multiplier": 1.2,
        "damage_multiplier": 1.5,
        "speed_multiplier": 1.3,
        "fire_rate_multiplier": 0.6,
        "detection_radius": 400,
        "preferred_range": 60,
        "special_abilities": ["rage_mode"],
        "ai_complexity": 1.1,
        "spawn_weight": 0.15
    },

    # Phase 2 New Enemy Types
    "mage": {
        "health_multiplier": 0.7,
        "damage_multiplier": 1.6,
        "speed_multiplier": 0.8,
        "fire_rate_multiplier": 1.8,
        "detection_radius": 450,
        "preferred_range": 300,
        "special_abilities": ["fireball", "ice_shard", "lightning_bolt", "teleport"],
        "ai_complexity": 2.0,
        "spawn_weight": 0.08,
        "mana": 100,
        "spell_cooldowns": {"fireball": 2000, "ice_shard": 1500, "lightning_bolt": 3000, "teleport": 5000}
    },
    "assassin": {
        "health_multiplier": 0.5,
        "damage_multiplier": 2.2,
        "speed_multiplier": 1.8,
        "fire_rate_multiplier": 0.7,
        "detection_radius": 200,
        "preferred_range": 50,
        "special_abilities": ["stealth", "backstab", "poison_blade", "smoke_bomb"],
        "ai_complexity": 2.2,
        "spawn_weight": 0.06,
        "stealth_duration": 3000,
        "backstab_multiplier": 3.0
    },
    "necromancer": {
        "health_multiplier": 0.6,
        "damage_multiplier": 1.0,
        "speed_multiplier": 0.6,
        "fire_rate_multiplier": 2.5,
        "detection_radius": 400,
        "preferred_range": 350,
        "special_abilities": ["summon_skeleton", "drain_life", "curse", "bone_armor"],
        "ai_complexity": 2.5,
        "spawn_weight": 0.04,
        "max_minions": 3,
        "summon_cooldown": 4000
    },
    "golem": {
        "health_multiplier": 3.5,
        "damage_multiplier": 2.0,
        "speed_multiplier": 0.4,
        "fire_rate_multiplier": 3.0,
        "detection_radius": 200,
        "preferred_range": 70,
        "special_abilities": ["ground_slam", "stone_throw", "regeneration", "immunity_physical"],
        "ai_complexity": 1.3,
        "spawn_weight": 0.03,
        "slam_radius": 120,
        "regen_rate": 2
    },
    "archer": {
        "health_multiplier": 0.8,
        "damage_multiplier": 1.4,
        "speed_multiplier": 0.9,
        "fire_rate_multiplier": 1.2,
        "detection_radius": 600,
        "preferred_range": 450,
        "special_abilities": ["piercing_shot", "explosive_arrow", "rapid_fire", "kiting"],
        "ai_complexity": 1.8,
        "spawn_weight": 0.12,
        "arrow_types": ["normal", "piercing", "explosive"],
        "quiver_size": 30
    },
    "shaman": {
        "health_multiplier": 0.9,
        "damage_multiplier": 0.8,
        "speed_multiplier": 0.7,
        "fire_rate_multiplier": 2.0,
        "detection_radius": 350,
        "preferred_range": 250,
        "special_abilities": ["heal_allies", "buff_damage", "buff_speed", "spirit_wolves"],
        "ai_complexity": 2.3,
        "spawn_weight": 0.05,
        "support_range": 200,
        "buff_duration": 10000
    },
    "berserker_elite": {
        "health_multiplier": 1.8,
        "damage_multiplier": 2.5,
        "speed_multiplier": 1.4,
        "fire_rate_multiplier": 0.5,
        "detection_radius": 500,
        "preferred_range": 40,
        "special_abilities": ["blood_frenzy", "whirlwind", "intimidate", "leap_attack"],
        "ai_complexity": 1.7,
        "spawn_weight": 0.02,
        "frenzy_threshold": 0.5,
        "leap_range": 200
    },
    "shadow": {
        "health_multiplier": 0.4,
        "damage_multiplier": 1.8,
        "speed_multiplier": 2.0,
        "fire_rate_multiplier": 0.8,
        "detection_radius": 300,
        "preferred_range": 80,
        "special_abilities": ["shadow_step", "phase_shift", "shadow_clone", "darkness"],
        "ai_complexity": 2.8,
        "spawn_weight": 0.03,
        "teleport_cooldown": 2000,
        "clone_duration": 5000
    }
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

# Level dimensions - Base sizes that scale with level
LEVEL_WIDTH = 60  # in tiles - base width
LEVEL_HEIGHT = 45  # in tiles - base height
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
TERRAIN_ENVIRONMENTAL_HAZARDS_ENABLED = True
TERRAIN_DESTRUCTIBLE_ELEMENTS_ENABLED = True

# Expanded Terrain Types and Textures
TERRAIN_TYPES = {
    # Basic terrain
    'floor': 0,
    'wall': 1,

    # Natural terrain
    'grass': 2,
    'grass_tall': 3,
    'grass_dry': 4,
    'dirt': 5,
    'dirt_rich': 6,
    'dirt_rocky': 7,

    # Stone and mineral
    'stone': 8,
    'stone_rough': 9,
    'stone_smooth': 10,
    'gravel': 11,
    'sand': 12,
    'sand_coarse': 13,

    # Water features
    'water': 14,
    'water_shallow': 15,
    'water_deep': 16,
    'ice': 17,

    # Wood and organic
    'wood': 18,
    'wood_old': 19,
    'wood_rotten': 20,
    'moss': 21,
    'mushroom': 22,

    # Special terrain
    'lava': 23,
    'crystal': 24,
    'metal': 25,
    'bone': 26,
    'ash': 27
}

# Enhanced Biome Configuration with multiple variants
BIOME_TYPES = {
    'dungeon': {
        'primary': 'floor',
        'secondary': 'stone',
        'decoration': 'gravel',
        'hazards': ['spike_trap', 'poison_gas'],
        'special_features': ['secret_door', 'treasure_alcove'],
        'lighting': 'dim',
        'spawn_weight': 1.0
    },
    'forest': {
        'primary': 'grass',
        'secondary': 'dirt',
        'decoration': 'wood',
        'hazards': ['thorn_bush', 'quicksand'],
        'special_features': ['hidden_grove', 'ancient_tree'],
        'lighting': 'natural',
        'spawn_weight': 1.0
    },
    'cave': {
        'primary': 'stone',
        'secondary': 'gravel',
        'decoration': 'water',
        'hazards': ['falling_rocks', 'underground_river'],
        'special_features': ['crystal_formation', 'underground_lake'],
        'lighting': 'dark',
        'spawn_weight': 1.0
    },
    'ruins': {
        'primary': 'stone_smooth',
        'secondary': 'sand',
        'decoration': 'wood_old',
        'hazards': ['crumbling_floor', 'ancient_trap'],
        'special_features': ['runic_circle', 'collapsed_tower'],
        'lighting': 'mystical',
        'spawn_weight': 0.8
    },
    'swamp': {
        'primary': 'dirt_rich',
        'secondary': 'water_shallow',
        'decoration': 'moss',
        'hazards': ['poisonous_bog', 'unstable_ground'],
        'special_features': ['witch_hut', 'dead_tree'],
        'lighting': 'eerie',
        'spawn_weight': 0.7
    },
    'volcanic': {
        'primary': 'ash',
        'secondary': 'stone_rough',
        'decoration': 'lava',
        'hazards': ['lava_pool', 'toxic_fumes'],
        'special_features': ['obsidian_formation', 'fire_geyser'],
        'lighting': 'fiery',
        'spawn_weight': 0.5
    },
    'crystal_cavern': {
        'primary': 'crystal',
        'secondary': 'stone',
        'decoration': 'ice',
        'hazards': ['crystal_shard', 'energy_discharge'],
        'special_features': ['power_crystal', 'teleport_gate'],
        'lighting': 'magical',
        'spawn_weight': 0.3
    },
    'necropolis': {
        'primary': 'bone',
        'secondary': 'ash',
        'decoration': 'metal',
        'hazards': ['cursed_ground', 'soul_drain'],
        'special_features': ['ancient_tomb', 'bone_throne'],
        'lighting': 'cursed',
        'spawn_weight': 0.4
    }
}

# Terrain Generation Parameters
TERRAIN_NOISE_SCALE = 0.1  # Scale for procedural noise
TERRAIN_SMOOTHING_PASSES = 2  # Number of smoothing iterations
TERRAIN_FEATURE_DENSITY = 0.15  # Density of special terrain features
TERRAIN_HAZARD_DENSITY = 0.05  # Density of environmental hazards
TERRAIN_SECRET_DENSITY = 0.02  # Density of secret areas

# Room generation with enhanced variety
ROOM_MAX_SIZE = 12
ROOM_MIN_SIZE = 6
MAX_ROOMS = 35
ROOM_TYPES = ['standard', 'large', 'corridor', 'circular', 'irregular', 'treasure', 'boss', 'puzzle']
ROOM_TYPE_WEIGHTS = [0.4, 0.2, 0.15, 0.1, 0.08, 0.04, 0.02, 0.01]  # Probability weights

# Progressive level scaling with enhanced mechanics
LEVEL_SIZE_SCALING_FACTOR = 1.8  # How much larger each level gets
MAX_LEVEL_SIZE_MULTIPLIER = 8.0  # Maximum size increase
ROOM_DENSITY_PER_LEVEL = 0.1  # Additional room density per level
COMPLEXITY_SCALING_FACTOR = 0.2  # How much more complex each level becomes
HAZARD_SCALING_FACTOR = 0.1  # How many more hazards per level

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
MULTIPLE_EXITS_ENABLED = True  # Allow multiple exit options per level
MAX_EXITS_PER_LEVEL = 3  # Maximum number of exits
EXIT_TYPES = ['stairs_down', 'portal', 'secret_passage', 'teleporter']

# Camera system improvements
CAMERA_FOLLOW_BEYOND_BOUNDARIES = True  # Allow camera to follow player beyond map edges
CAMERA_BOUNDARY_BUFFER = 100  # Pixels of buffer beyond map edges

# Achievement system
ACHIEVEMENT_XP_BONUS = 25

# ============================================================================
# ENVIRONMENTAL HAZARDS AND FEATURES
# ============================================================================

# Environmental Hazards Configuration
ENVIRONMENTAL_HAZARDS = {
    'spike_trap': {
        'damage': 15,
        'trigger_chance': 0.8,
        'visual_warning': True,
        'cooldown': 2000  # ms
    },
    'poison_gas': {
        'damage': 5,
        'duration': 3000,  # ms
        'spread_radius': 64,
        'visual_effect': 'green_cloud'
    },
    'thorn_bush': {
        'damage': 8,
        'slow_effect': 0.5,
        'duration': 1500,
        'visual_effect': 'thorns'
    },
    'quicksand': {
        'damage': 0,
        'slow_effect': 0.2,
        'escape_difficulty': 0.3,
        'visual_effect': 'bubbling'
    },
    'falling_rocks': {
        'damage': 25,
        'warning_time': 1000,  # ms
        'area_size': 96,
        'visual_warning': True
    },
    'lava_pool': {
        'damage': 30,
        'damage_interval': 500,  # ms
        'visual_effect': 'fire_particles'
    },
    'crystal_shard': {
        'damage': 20,
        'knockback': 50,
        'visual_effect': 'crystal_explosion'
    },
    'cursed_ground': {
        'damage': 10,
        'mana_drain': 5,
        'visual_effect': 'dark_aura'
    }
}

# Special Features Configuration
SPECIAL_FEATURES = {
    'secret_door': {
        'discovery_chance': 0.3,
        'requires_key': False,
        'reward_type': 'treasure'
    },
    'treasure_alcove': {
        'loot_multiplier': 2.0,
        'rare_item_chance': 0.4,
        'visual_effect': 'golden_glow'
    },
    'hidden_grove': {
        'healing_rate': 2,  # HP per second
        'mana_regen': 1,
        'duration': 10000  # ms
    },
    'crystal_formation': {
        'mana_boost': 50,
        'temporary_power': True,
        'duration': 30000  # ms
    },
    'runic_circle': {
        'teleport_destination': 'random',
        'activation_cost': 10,  # mana
        'visual_effect': 'magic_circle'
    },
    'power_crystal': {
        'damage_boost': 1.5,
        'duration': 20000,  # ms
        'visual_effect': 'energy_aura'
    },
    'ancient_tomb': {
        'undead_spawn_chance': 0.6,
        'treasure_quality': 'epic',
        'curse_chance': 0.2
    }
}

# Weather and Environmental Effects
WEATHER_SYSTEM_ENABLED = True
WEATHER_TYPES = {
    'clear': {'visibility': 1.0, 'movement_modifier': 1.0, 'spawn_rate': 0.4},
    'rain': {'visibility': 0.8, 'movement_modifier': 0.9, 'spawn_rate': 0.2},
    'fog': {'visibility': 0.6, 'movement_modifier': 1.0, 'spawn_rate': 0.15},
    'storm': {'visibility': 0.7, 'movement_modifier': 0.8, 'spawn_rate': 0.1},
    'blizzard': {'visibility': 0.5, 'movement_modifier': 0.7, 'spawn_rate': 0.05},
    'sandstorm': {'visibility': 0.4, 'movement_modifier': 0.6, 'spawn_rate': 0.05},
    'volcanic_ash': {'visibility': 0.3, 'movement_modifier': 0.8, 'spawn_rate': 0.05}
}
WEATHER_CHANGE_INTERVAL = 120000  # ms - 2 minutes
WEATHER_TRANSITION_TIME = 5000  # ms

# ============================================================================
# PHASE 2: ENHANCED COMBAT SYSTEM
# ============================================================================

# Elemental Damage Types
ELEMENTAL_DAMAGE_TYPES = {
    'physical': {
        'color': (255, 255, 255),
        'particle_effect': 'impact',
        'status_effects': [],
        'damage_multiplier': 1.0
    },
    'fire': {
        'color': (255, 69, 0),
        'particle_effect': 'flames',
        'status_effects': ['burning'],
        'damage_multiplier': 1.2,
        'dot_damage': 3,
        'dot_duration': 3000
    },
    'ice': {
        'color': (135, 206, 235),
        'particle_effect': 'frost',
        'status_effects': ['frozen', 'slowed'],
        'damage_multiplier': 0.9,
        'slow_factor': 0.5,
        'slow_duration': 2000
    },
    'lightning': {
        'color': (255, 255, 0),
        'particle_effect': 'sparks',
        'status_effects': ['stunned'],
        'damage_multiplier': 1.3,
        'chain_targets': 3,
        'stun_duration': 1000
    },
    'poison': {
        'color': (0, 255, 0),
        'particle_effect': 'toxic_cloud',
        'status_effects': ['poisoned'],
        'damage_multiplier': 0.8,
        'dot_damage': 5,
        'dot_duration': 5000
    },
    'dark': {
        'color': (75, 0, 130),
        'particle_effect': 'shadow',
        'status_effects': ['cursed'],
        'damage_multiplier': 1.1,
        'mana_drain': 10
    },
    'holy': {
        'color': (255, 215, 0),
        'particle_effect': 'light_burst',
        'status_effects': ['blessed'],
        'damage_multiplier': 1.4,
        'undead_bonus': 2.0
    }
}

# Status Effects Configuration
STATUS_EFFECTS = {
    'burning': {
        'damage_per_tick': 3,
        'tick_interval': 1000,  # ms
        'max_duration': 5000,
        'visual_effect': 'fire_particles',
        'stackable': True,
        'max_stacks': 5
    },
    'frozen': {
        'movement_multiplier': 0.0,
        'attack_speed_multiplier': 0.0,
        'max_duration': 2000,
        'visual_effect': 'ice_crystals',
        'stackable': False
    },
    'slowed': {
        'movement_multiplier': 0.5,
        'attack_speed_multiplier': 0.7,
        'max_duration': 3000,
        'visual_effect': 'frost_aura',
        'stackable': True,
        'max_stacks': 3
    },
    'stunned': {
        'movement_multiplier': 0.0,
        'attack_speed_multiplier': 0.0,
        'max_duration': 1500,
        'visual_effect': 'lightning_sparks',
        'stackable': False
    },
    'poisoned': {
        'damage_per_tick': 5,
        'tick_interval': 1000,
        'max_duration': 8000,
        'visual_effect': 'poison_bubbles',
        'stackable': True,
        'max_stacks': 10
    },
    'cursed': {
        'damage_multiplier': 1.2,  # Take 20% more damage
        'healing_multiplier': 0.5,  # Heal 50% less
        'max_duration': 10000,
        'visual_effect': 'dark_aura',
        'stackable': False
    },
    'blessed': {
        'damage_multiplier': 0.8,  # Take 20% less damage
        'healing_multiplier': 1.5,  # Heal 50% more
        'max_duration': 15000,
        'visual_effect': 'golden_glow',
        'stackable': False
    }
}

# Combat Mechanics
COMBO_SYSTEM_ENABLED = True
COMBO_WINDOW = 2000  # ms - time window for combo inputs
COMBO_DAMAGE_MULTIPLIER = 1.5  # Damage bonus for successful combos
MAX_COMBO_CHAIN = 5  # Maximum combo chain length

# Tactical Positioning
FLANKING_DAMAGE_BONUS = 1.3  # 30% bonus damage from behind
COVER_DAMAGE_REDUCTION = 0.7  # 30% damage reduction when behind cover
HIGH_GROUND_DAMAGE_BONUS = 1.2  # 20% bonus damage from elevated position

# ============================================================================
# PHASE 2: EXPANDED EQUIPMENT SYSTEM
# ============================================================================

# Equipment Rarity System
EQUIPMENT_RARITIES = {
    'common': {
        'color': (255, 255, 255),  # White
        'stat_multiplier': 1.0,
        'max_enchantments': 0,
        'drop_chance': 0.6,
        'name_prefix': '',
        'name_suffix': ''
    },
    'uncommon': {
        'color': (0, 255, 0),  # Green
        'stat_multiplier': 1.3,
        'max_enchantments': 1,
        'drop_chance': 0.25,
        'name_prefix': 'Fine ',
        'name_suffix': ''
    },
    'rare': {
        'color': (0, 100, 255),  # Blue
        'stat_multiplier': 1.6,
        'max_enchantments': 2,
        'drop_chance': 0.12,
        'name_prefix': 'Superior ',
        'name_suffix': ''
    },
    'epic': {
        'color': (128, 0, 128),  # Purple
        'stat_multiplier': 2.0,
        'max_enchantments': 3,
        'drop_chance': 0.025,
        'name_prefix': 'Epic ',
        'name_suffix': ''
    },
    'legendary': {
        'color': (255, 165, 0),  # Orange
        'stat_multiplier': 2.5,
        'max_enchantments': 4,
        'drop_chance': 0.005,
        'name_prefix': 'Legendary ',
        'name_suffix': ''
    },
    'artifact': {
        'color': (255, 215, 0),  # Gold
        'stat_multiplier': 3.0,
        'max_enchantments': 5,
        'drop_chance': 0.001,
        'name_prefix': 'Artifact ',
        'name_suffix': ' of Power'
    }
}

# Equipment Sets
EQUIPMENT_SETS = {
    'warrior_set': {
        'name': 'Warrior\'s Might',
        'pieces': ['helmet', 'armor', 'weapon', 'boots'],
        'set_bonuses': {
            2: {'damage': 10, 'health': 20},
            3: {'damage': 20, 'health': 40, 'speed': 5},
            4: {'damage': 35, 'health': 80, 'speed': 10, 'special': 'berserker_rage'}
        },
        'color_theme': (220, 20, 60)  # Crimson
    },
    'mage_set': {
        'name': 'Arcane Mastery',
        'pieces': ['hat', 'robe', 'staff', 'boots'],
        'set_bonuses': {
            2: {'damage': 15, 'fire_rate': 10},
            3: {'damage': 30, 'fire_rate': 20, 'mana': 50},
            4: {'damage': 50, 'fire_rate': 35, 'mana': 100, 'special': 'elemental_mastery'}
        },
        'color_theme': (75, 0, 130)  # Indigo
    },
    'assassin_set': {
        'name': 'Shadow Walker',
        'pieces': ['hood', 'cloak', 'daggers', 'boots'],
        'set_bonuses': {
            2: {'speed': 15, 'crit_chance': 10},
            3: {'speed': 25, 'crit_chance': 20, 'stealth_duration': 2000},
            4: {'speed': 40, 'crit_chance': 35, 'stealth_duration': 4000, 'special': 'shadow_step'}
        },
        'color_theme': (64, 64, 64)  # Dark Gray
    },
    'paladin_set': {
        'name': 'Divine Protection',
        'pieces': ['helm', 'plate', 'sword', 'shield'],
        'set_bonuses': {
            2: {'health': 50, 'defense': 15},
            3: {'health': 100, 'defense': 30, 'healing': 25},
            4: {'health': 200, 'defense': 50, 'healing': 50, 'special': 'divine_aura'}
        },
        'color_theme': (255, 215, 0)  # Gold
    },
    'ranger_set': {
        'name': 'Forest Guardian',
        'pieces': ['cap', 'leather', 'bow', 'quiver'],
        'set_bonuses': {
            2: {'fire_rate': 20, 'range': 50},
            3: {'fire_rate': 35, 'range': 100, 'piercing': 1},
            4: {'fire_rate': 50, 'range': 150, 'piercing': 2, 'special': 'multi_shot'}
        },
        'color_theme': (34, 139, 34)  # Forest Green
    }
}

# Enchantments System
ENCHANTMENTS = {
    'sharpness': {
        'name': 'Sharpness',
        'type': 'weapon',
        'max_level': 5,
        'effect_per_level': {'damage': 3},
        'description': 'Increases weapon damage'
    },
    'fire_aspect': {
        'name': 'Fire Aspect',
        'type': 'weapon',
        'max_level': 3,
        'effect_per_level': {'elemental_damage': 'fire'},
        'description': 'Adds fire damage to attacks'
    },
    'frost_bite': {
        'name': 'Frost Bite',
        'type': 'weapon',
        'max_level': 3,
        'effect_per_level': {'elemental_damage': 'ice'},
        'description': 'Adds ice damage and slowing effect'
    },
    'lightning_strike': {
        'name': 'Lightning Strike',
        'type': 'weapon',
        'max_level': 2,
        'effect_per_level': {'elemental_damage': 'lightning'},
        'description': 'Adds lightning damage with chain effect'
    },
    'vampiric': {
        'name': 'Vampiric',
        'type': 'weapon',
        'max_level': 3,
        'effect_per_level': {'life_steal': 5},
        'description': 'Heals player for % of damage dealt'
    },
    'protection': {
        'name': 'Protection',
        'type': 'armor',
        'max_level': 4,
        'effect_per_level': {'defense': 5},
        'description': 'Reduces incoming damage'
    },
    'regeneration': {
        'name': 'Regeneration',
        'type': 'armor',
        'max_level': 3,
        'effect_per_level': {'health_regen': 1},
        'description': 'Slowly regenerates health over time'
    },
    'swiftness': {
        'name': 'Swiftness',
        'type': 'boots',
        'max_level': 3,
        'effect_per_level': {'speed': 8},
        'description': 'Increases movement speed'
    },
    'feather_falling': {
        'name': 'Feather Falling',
        'type': 'boots',
        'max_level': 2,
        'effect_per_level': {'fall_damage_reduction': 25},
        'description': 'Reduces fall damage'
    },
    'mana_efficiency': {
        'name': 'Mana Efficiency',
        'type': 'accessory',
        'max_level': 3,
        'effect_per_level': {'mana_cost_reduction': 10},
        'description': 'Reduces mana costs'
    }
}

# Consumable Items
CONSUMABLE_ITEMS = {
    'health_potion': {
        'name': 'Health Potion',
        'effect': 'heal',
        'value': 50,
        'duration': 0,  # Instant
        'cooldown': 5000,  # 5 seconds
        'stack_size': 10,
        'rarity': 'common'
    },
    'mana_potion': {
        'name': 'Mana Potion',
        'effect': 'restore_mana',
        'value': 75,
        'duration': 0,
        'cooldown': 3000,
        'stack_size': 10,
        'rarity': 'common'
    },
    'strength_elixir': {
        'name': 'Strength Elixir',
        'effect': 'damage_boost',
        'value': 1.5,
        'duration': 30000,  # 30 seconds
        'cooldown': 60000,  # 1 minute
        'stack_size': 5,
        'rarity': 'uncommon'
    },
    'speed_potion': {
        'name': 'Speed Potion',
        'effect': 'speed_boost',
        'value': 1.4,
        'duration': 20000,
        'cooldown': 45000,
        'stack_size': 5,
        'rarity': 'uncommon'
    },
    'invisibility_potion': {
        'name': 'Invisibility Potion',
        'effect': 'stealth',
        'value': 1,
        'duration': 10000,
        'cooldown': 120000,  # 2 minutes
        'stack_size': 3,
        'rarity': 'rare'
    },
    'fire_resistance': {
        'name': 'Fire Resistance Potion',
        'effect': 'elemental_resistance',
        'value': 'fire',
        'duration': 60000,  # 1 minute
        'cooldown': 30000,
        'stack_size': 5,
        'rarity': 'uncommon'
    },
    'antidote': {
        'name': 'Antidote',
        'effect': 'cure_poison',
        'value': 1,
        'duration': 0,
        'cooldown': 1000,
        'stack_size': 10,
        'rarity': 'common'
    },
    'phoenix_feather': {
        'name': 'Phoenix Feather',
        'effect': 'resurrection',
        'value': 1,
        'duration': 0,
        'cooldown': 0,
        'stack_size': 1,
        'rarity': 'legendary'
    }
}

# ============================================================================
# PHASE 3: ADVANCED SYSTEMS & POLISH CONFIGURATION
# ============================================================================

# Advanced Procedural Generation Configuration
ADVANCED_GENERATION_CONFIG = {
    'enabled': True,
    'architectural_themes': {
        'cathedral': {
            'room_height_multiplier': 1.5,
            'corridor_width': 3,
            'pillar_frequency': 0.3,
            'vault_ceiling_chance': 0.4,
            'stained_glass_chance': 0.2
        },
        'fortress': {
            'wall_thickness': 2,
            'tower_frequency': 0.2,
            'battlements_chance': 0.6,
            'courtyard_chance': 0.3,
            'defensive_positions': True
        },
        'cavern': {
            'irregular_walls': True,
            'stalactite_frequency': 0.4,
            'underground_river_chance': 0.1,
            'crystal_formation_chance': 0.3,
            'natural_bridges': True
        },
        'ruins': {
            'broken_wall_chance': 0.4,
            'overgrowth_frequency': 0.5,
            'collapsed_ceiling_chance': 0.2,
            'ancient_mechanism_chance': 0.1,
            'weathering_effects': True
        },
        'laboratory': {
            'equipment_density': 0.6,
            'containment_units': True,
            'ventilation_systems': True,
            'experimental_areas': 0.3,
            'hazardous_materials': True
        },
        'temple': {
            'altar_frequency': 0.2,
            'sacred_geometry': True,
            'ritual_circles': 0.3,
            'divine_light_sources': 0.4,
            'blessing_pools': 0.1
        }
    },
    'narrative_layouts': {
        'enabled': True,
        'story_driven_connections': True,
        'dramatic_reveals': 0.2,
        'climactic_positioning': True,
        'pacing_control': True
    },
    'dynamic_difficulty_zones': {
        'enabled': True,
        'safe_zones': 0.1,
        'challenge_zones': 0.2,
        'elite_zones': 0.05,
        'puzzle_zones': 0.1,
        'ambush_zones': 0.15
    },
    'secret_areas': {
        'enabled': True,
        'hidden_room_chance': 0.15,
        'secret_passage_chance': 0.1,
        'treasure_vault_chance': 0.05,
        'discovery_methods': ['hidden_switch', 'puzzle_solution', 'sequence_activation']
    }
}

# Meta-Progression System Configuration
META_PROGRESSION_CONFIG = {
    'enabled': True,
    'legacy_system': {
        'enabled': True,
        'equipment_inheritance_chance': 0.1,
        'skill_retention_percentage': 0.05,
        'memory_fragments': True,
        'ancestral_bonuses': True
    },
    'meta_currencies': {
        'soul_essence': {
            'gained_on_death': True,
            'gained_on_achievement': True,
            'exchange_rates': {'skill_points': 10, 'equipment_upgrades': 50}
        },
        'knowledge_crystals': {
            'gained_on_discovery': True,
            'gained_on_boss_kill': True,
            'exchange_rates': {'new_abilities': 25, 'biome_unlocks': 100}
        },
        'fate_tokens': {
            'gained_on_rare_events': True,
            'gained_on_perfect_runs': True,
            'exchange_rates': {'destiny_changes': 1, 'miracle_items': 5}
        }
    },
    'unlock_progression': {
        'biome_unlocks': {
            'volcanic_depths': {'requirement': 'defeat_fire_lord', 'cost': 200},
            'frozen_wastes': {'requirement': 'survive_blizzard', 'cost': 150},
            'shadow_realm': {'requirement': 'master_darkness', 'cost': 300},
            'celestial_gardens': {'requirement': 'achieve_enlightenment', 'cost': 500}
        },
        'enemy_unlocks': {
            'ancient_dragon': {'requirement': 'reach_level_50', 'cost': 1000},
            'void_stalker': {'requirement': 'master_all_elements', 'cost': 750},
            'time_weaver': {'requirement': 'complete_temporal_quest', 'cost': 500}
        }
    },
    'mastery_system': {
        'weapon_mastery': {
            'max_level': 100,
            'bonuses_per_level': {'damage': 0.5, 'crit_chance': 0.1},
            'special_unlocks': {25: 'weapon_techniques', 50: 'master_combos', 75: 'legendary_forms', 100: 'transcendent_mastery'}
        },
        'magic_mastery': {
            'max_level': 100,
            'bonuses_per_level': {'spell_power': 0.8, 'mana_efficiency': 0.2},
            'special_unlocks': {25: 'spell_fusion', 50: 'elemental_mastery', 75: 'arcane_secrets', 100: 'reality_manipulation'}
        }
    },
    'prestige_system': {
        'enabled': True,
        'prestige_levels': 10,
        'requirements_per_level': [100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000, 50000],
        'bonuses_per_prestige': {'all_stats': 5, 'xp_gain': 10, 'rare_find_chance': 2}
    }
}

# Enhanced User Experience Configuration
UI_ENHANCEMENT_CONFIG = {
    'modern_ui': {
        'enabled': True,
        'responsive_design': True,
        'animation_speed': 1.0,
        'transition_duration': 300,  # milliseconds
        'smooth_scrolling': True,
        'contextual_tooltips': True
    },
    'visual_effects': {
        'particle_systems': True,
        'dynamic_lighting': True,
        'screen_effects': True,
        'weather_effects': True,
        'cinematic_camera': True,
        'effect_quality': 'high'  # low, medium, high, ultra
    },
    'accessibility': {
        'colorblind_support': True,
        'high_contrast_mode': False,
        'large_text_mode': False,
        'keyboard_navigation': True,
        'screen_reader_support': True,
        'subtitle_support': True
    },
    'customization': {
        'ui_scaling': 1.0,
        'color_themes': ['default', 'dark', 'light', 'high_contrast'],
        'layout_presets': ['compact', 'standard', 'expanded'],
        'hotkey_customization': True
    }
}

# Dynamic Difficulty System Configuration
DIFFICULTY_SYSTEM_CONFIG = {
    'adaptive_difficulty': {
        'enabled': True,
        'assessment_window': 300,  # seconds
        'adjustment_frequency': 60,  # seconds
        'max_adjustment_per_cycle': 0.1,  # 10% max change
        'difficulty_range': [0.5, 2.0],  # 50% to 200% of base difficulty
        'player_skill_factors': ['death_rate', 'completion_time', 'damage_taken', 'accuracy']
    },
    'challenge_modes': {
        'daily_challenge': {
            'enabled': True,
            'seed_rotation': 'daily',
            'special_modifiers': True,
            'leaderboard_integration': True
        },
        'weekly_challenge': {
            'enabled': True,
            'themed_challenges': True,
            'community_goals': True,
            'special_rewards': True
        },
        'custom_modifiers': {
            'speed_run': {'time_limit': True, 'speed_bonus': 2.0},
            'glass_cannon': {'damage_multiplier': 3.0, 'health_multiplier': 0.3},
            'pacifist': {'no_direct_damage': True, 'environmental_only': True},
            'minimalist': {'no_equipment_upgrades': True, 'base_stats_only': True},
            'chaos': {'random_effects_per_room': True, 'unpredictable_mechanics': True}
        }
    },
    'prestige_difficulty': {
        'nightmare_mode': {'enemy_health': 3.0, 'enemy_damage': 2.5, 'enemy_speed': 1.5},
        'hell_mode': {'enemy_health': 5.0, 'enemy_damage': 4.0, 'permadeath': True},
        'transcendent_mode': {'reality_distortion': True, 'physics_alterations': True}
    }
}

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
