import pygame
import os

# Initialize pygame
pygame.init()

# Create assets directory if it doesn't exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/images/tiles", exist_ok=True)
os.makedirs("assets/images/entities", exist_ok=True)
os.makedirs("assets/images/effects", exist_ok=True)
os.makedirs("assets/images/ui", exist_ok=True)

# Enhanced color palette for better visual appeal
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)

# Enhanced color palette
DARK_BLUE = (0, 50, 100)
LIGHT_BLUE = (100, 150, 255)
DARK_RED = (150, 0, 0)
LIGHT_RED = (255, 100, 100)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (205, 133, 63)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIME = (0, 255, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Define asset sizes
TILE_SIZE = 32
ENTITY_SIZE = 32
PROJECTILE_SIZE = 16

def create_enhanced_player_sprite():
    """Create an enhanced player sprite with better pixel art"""
    player_surface = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE), pygame.SRCALPHA)

    # Body (knight-like armor)
    pygame.draw.rect(player_surface, DARK_BLUE, (8, 12, 16, 16))  # Main body
    pygame.draw.rect(player_surface, LIGHT_BLUE, (9, 13, 14, 2))  # Chest highlight
    pygame.draw.rect(player_surface, SILVER, (10, 15, 12, 1))  # Armor line

    # Head/Helmet
    pygame.draw.rect(player_surface, DARK_GRAY, (10, 4, 12, 12))  # Helmet
    pygame.draw.rect(player_surface, LIGHT_GRAY, (11, 5, 10, 2))  # Helmet highlight

    # Visor/Face
    pygame.draw.rect(player_surface, BLACK, (12, 8, 8, 4))  # Visor opening
    pygame.draw.rect(player_surface, RED, (14, 9, 2, 1))  # Eye glow
    pygame.draw.rect(player_surface, RED, (16, 9, 2, 1))  # Eye glow

    # Arms
    pygame.draw.rect(player_surface, DARK_BLUE, (4, 14, 4, 8))  # Left arm
    pygame.draw.rect(player_surface, DARK_BLUE, (24, 14, 4, 8))  # Right arm
    pygame.draw.rect(player_surface, LIGHT_BLUE, (5, 15, 2, 2))  # Left arm highlight
    pygame.draw.rect(player_surface, LIGHT_BLUE, (25, 15, 2, 2))  # Right arm highlight

    # Legs
    pygame.draw.rect(player_surface, DARK_BLUE, (10, 28, 4, 4))  # Left leg
    pygame.draw.rect(player_surface, DARK_BLUE, (18, 28, 4, 4))  # Right leg
    pygame.draw.rect(player_surface, LIGHT_BLUE, (11, 29, 2, 1))  # Left leg highlight
    pygame.draw.rect(player_surface, LIGHT_BLUE, (19, 29, 2, 1))  # Right leg highlight

    # Weapon (sword)
    pygame.draw.rect(player_surface, SILVER, (28, 8, 2, 12))  # Blade
    pygame.draw.rect(player_surface, GOLD, (27, 18, 4, 2))  # Hilt
    pygame.draw.rect(player_surface, WHITE, (28, 9, 2, 1))  # Blade highlight

    return player_surface

# Create enhanced player sprite
player_surface = create_enhanced_player_sprite()
pygame.image.save(player_surface, "assets/images/player.png")

def create_enhanced_enemy_sprite():
    """Create an enhanced enemy sprite (orc-like creature)"""
    enemy_surface = pygame.Surface((ENTITY_SIZE, ENTITY_SIZE), pygame.SRCALPHA)

    # Body (dark armor/clothing)
    pygame.draw.rect(enemy_surface, DARK_RED, (8, 14, 16, 14))  # Main body
    pygame.draw.rect(enemy_surface, BLACK, (9, 15, 14, 2))  # Dark clothing
    pygame.draw.rect(enemy_surface, DARK_GRAY, (10, 17, 12, 1))  # Belt/armor

    # Head (orc-like)
    pygame.draw.rect(enemy_surface, DARK_RED, (10, 6, 12, 10))  # Head
    pygame.draw.rect(enemy_surface, RED, (11, 7, 10, 2))  # Head highlight

    # Face features
    pygame.draw.rect(enemy_surface, BLACK, (12, 10, 2, 2))  # Left eye
    pygame.draw.rect(enemy_surface, BLACK, (18, 10, 2, 2))  # Right eye
    pygame.draw.rect(enemy_surface, RED, (13, 11, 1, 1))  # Eye glow
    pygame.draw.rect(enemy_surface, RED, (19, 11, 1, 1))  # Eye glow
    pygame.draw.rect(enemy_surface, BLACK, (14, 13, 4, 2))  # Mouth/tusks

    # Arms
    pygame.draw.rect(enemy_surface, DARK_RED, (4, 16, 4, 8))  # Left arm
    pygame.draw.rect(enemy_surface, DARK_RED, (24, 16, 4, 8))  # Right arm

    # Legs
    pygame.draw.rect(enemy_surface, DARK_RED, (10, 28, 4, 4))  # Left leg
    pygame.draw.rect(enemy_surface, DARK_RED, (18, 28, 4, 4))  # Right leg

    # Weapon (axe)
    pygame.draw.rect(enemy_surface, DARK_BROWN, (28, 12, 2, 8))  # Handle
    pygame.draw.rect(enemy_surface, DARK_GRAY, (26, 10, 6, 4))  # Axe head
    pygame.draw.rect(enemy_surface, GRAY, (27, 11, 4, 2))  # Axe highlight

    return enemy_surface

# Create enhanced enemy sprite
enemy_surface = create_enhanced_enemy_sprite()
pygame.image.save(enemy_surface, "assets/images/enemy.png")

def create_enhanced_wall_sprite():
    """Create an enhanced wall sprite with stone texture"""
    wall_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Base stone color
    pygame.draw.rect(wall_surface, GRAY, (0, 0, TILE_SIZE, TILE_SIZE))

    # Stone blocks pattern
    pygame.draw.rect(wall_surface, DARK_GRAY, (0, 0, 16, 16))  # Top-left block
    pygame.draw.rect(wall_surface, LIGHT_GRAY, (16, 0, 16, 16))  # Top-right block
    pygame.draw.rect(wall_surface, LIGHT_GRAY, (0, 16, 16, 16))  # Bottom-left block
    pygame.draw.rect(wall_surface, DARK_GRAY, (16, 16, 16, 16))  # Bottom-right block

    # Mortar lines
    pygame.draw.rect(wall_surface, BLACK, (0, 15, TILE_SIZE, 2))  # Horizontal mortar
    pygame.draw.rect(wall_surface, BLACK, (15, 0, 2, TILE_SIZE))  # Vertical mortar

    # Highlights and shadows for depth
    pygame.draw.rect(wall_surface, WHITE, (1, 1, 14, 1))  # Top-left highlight
    pygame.draw.rect(wall_surface, WHITE, (17, 1, 14, 1))  # Top-right highlight
    pygame.draw.rect(wall_surface, BLACK, (1, 14, 14, 1))  # Top-left shadow
    pygame.draw.rect(wall_surface, BLACK, (17, 30, 14, 1))  # Bottom-right shadow

    # Border
    pygame.draw.rect(wall_surface, BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 1)

    return wall_surface

def create_enhanced_floor_sprite():
    """Create an enhanced floor sprite with stone tile pattern"""
    floor_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Base floor color
    pygame.draw.rect(floor_surface, LIGHT_BROWN, (0, 0, TILE_SIZE, TILE_SIZE))

    # Stone tile pattern
    pygame.draw.rect(floor_surface, BROWN, (2, 2, 12, 12))  # Top-left tile
    pygame.draw.rect(floor_surface, DARK_BROWN, (18, 2, 12, 12))  # Top-right tile
    pygame.draw.rect(floor_surface, DARK_BROWN, (2, 18, 12, 12))  # Bottom-left tile
    pygame.draw.rect(floor_surface, BROWN, (18, 18, 12, 12))  # Bottom-right tile

    # Tile highlights
    pygame.draw.rect(floor_surface, LIGHT_BROWN, (3, 3, 10, 1))  # Top-left highlight
    pygame.draw.rect(floor_surface, LIGHT_BROWN, (19, 3, 10, 1))  # Top-right highlight

    # Grout lines
    pygame.draw.rect(floor_surface, DARK_BROWN, (0, 15, TILE_SIZE, 2))  # Horizontal grout
    pygame.draw.rect(floor_surface, DARK_BROWN, (15, 0, 2, TILE_SIZE))  # Vertical grout

    # Subtle border
    pygame.draw.rect(floor_surface, DARK_BROWN, (0, 0, TILE_SIZE, TILE_SIZE), 1)

    return floor_surface

# Create enhanced tile sprites
wall_surface = create_enhanced_wall_sprite()
pygame.image.save(wall_surface, "assets/images/wall.png")

floor_surface = create_enhanced_floor_sprite()
pygame.image.save(floor_surface, "assets/images/floor.png")

def create_enhanced_player_projectile():
    """Create an enhanced player projectile (magic bolt)"""
    projectile = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE), pygame.SRCALPHA)

    # Core energy
    pygame.draw.circle(projectile, CYAN, (PROJECTILE_SIZE//2, PROJECTILE_SIZE//2), 6)
    pygame.draw.circle(projectile, LIGHT_BLUE, (PROJECTILE_SIZE//2, PROJECTILE_SIZE//2), 4)
    pygame.draw.circle(projectile, WHITE, (PROJECTILE_SIZE//2, PROJECTILE_SIZE//2), 2)

    # Energy sparks
    pygame.draw.rect(projectile, CYAN, (2, PROJECTILE_SIZE//2-1, 2, 2))
    pygame.draw.rect(projectile, CYAN, (PROJECTILE_SIZE-4, PROJECTILE_SIZE//2-1, 2, 2))
    pygame.draw.rect(projectile, CYAN, (PROJECTILE_SIZE//2-1, 2, 2, 2))
    pygame.draw.rect(projectile, CYAN, (PROJECTILE_SIZE//2-1, PROJECTILE_SIZE-4, 2, 2))

    return projectile

def create_enhanced_enemy_projectile():
    """Create an enhanced enemy projectile (dark energy)"""
    projectile = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE), pygame.SRCALPHA)

    # Core dark energy
    pygame.draw.circle(projectile, DARK_RED, (PROJECTILE_SIZE//2, PROJECTILE_SIZE//2), 6)
    pygame.draw.circle(projectile, RED, (PROJECTILE_SIZE//2, PROJECTILE_SIZE//2), 4)
    pygame.draw.circle(projectile, ORANGE, (PROJECTILE_SIZE//2, PROJECTILE_SIZE//2), 2)

    # Dark sparks
    pygame.draw.rect(projectile, DARK_RED, (1, PROJECTILE_SIZE//2-1, 3, 2))
    pygame.draw.rect(projectile, DARK_RED, (PROJECTILE_SIZE-4, PROJECTILE_SIZE//2-1, 3, 2))
    pygame.draw.rect(projectile, DARK_RED, (PROJECTILE_SIZE//2-1, 1, 2, 3))
    pygame.draw.rect(projectile, DARK_RED, (PROJECTILE_SIZE//2-1, PROJECTILE_SIZE-4, 2, 3))

    return projectile

def create_enhanced_health_potion():
    """Create an enhanced health potion sprite"""
    potion = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Bottle
    pygame.draw.rect(potion, LIGHT_GRAY, (12, 8, 8, 20))  # Main bottle
    pygame.draw.rect(potion, DARK_GRAY, (11, 8, 1, 20))  # Left shadow
    pygame.draw.rect(potion, DARK_GRAY, (20, 8, 1, 20))  # Right shadow
    pygame.draw.rect(potion, WHITE, (13, 9, 1, 18))  # Highlight

    # Cork/stopper
    pygame.draw.rect(potion, DARK_BROWN, (13, 6, 6, 4))  # Cork
    pygame.draw.rect(potion, LIGHT_BROWN, (14, 7, 4, 1))  # Cork highlight

    # Liquid
    pygame.draw.rect(potion, RED, (13, 12, 6, 14))  # Red liquid
    pygame.draw.rect(potion, LIGHT_RED, (13, 12, 6, 2))  # Liquid surface
    pygame.draw.rect(potion, DARK_RED, (13, 24, 6, 2))  # Liquid bottom

    # Label
    pygame.draw.rect(potion, WHITE, (10, 16, 12, 6))  # Label background
    pygame.draw.rect(potion, RED, (11, 17, 10, 1))  # Label line
    pygame.draw.rect(potion, RED, (11, 19, 10, 1))  # Label line
    pygame.draw.rect(potion, RED, (11, 21, 10, 1))  # Label line

    return potion

# Create enhanced projectile sprites
player_projectile = create_enhanced_player_projectile()
pygame.image.save(player_projectile, "assets/images/player_projectile.png")

enemy_projectile = create_enhanced_enemy_projectile()
pygame.image.save(enemy_projectile, "assets/images/enemy_projectile.png")

# Create enhanced health potion
health_potion = create_enhanced_health_potion()
pygame.image.save(health_potion, "assets/images/health_potion.png")

def create_damage_boost_sprite():
    """Create a damage boost item sprite (sword icon)"""
    item = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Sword blade
    pygame.draw.rect(item, SILVER, (14, 4, 4, 20))  # Main blade
    pygame.draw.rect(item, WHITE, (15, 5, 2, 18))  # Blade highlight
    pygame.draw.rect(item, DARK_GRAY, (13, 4, 1, 20))  # Blade shadow

    # Crossguard
    pygame.draw.rect(item, GOLD, (10, 22, 12, 3))  # Crossguard
    pygame.draw.rect(item, YELLOW, (11, 23, 10, 1))  # Crossguard highlight

    # Handle
    pygame.draw.rect(item, DARK_BROWN, (14, 25, 4, 6))  # Handle
    pygame.draw.rect(item, LIGHT_BROWN, (15, 26, 2, 4))  # Handle highlight

    # Pommel
    pygame.draw.circle(item, GOLD, (16, 30), 2)  # Pommel
    pygame.draw.circle(item, YELLOW, (16, 29), 1)  # Pommel highlight

    return item

def create_speed_boost_sprite():
    """Create a speed boost item sprite (boot icon)"""
    item = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Boot main body
    pygame.draw.rect(item, DARK_BROWN, (8, 16, 16, 12))  # Main boot
    pygame.draw.rect(item, LIGHT_BROWN, (9, 17, 14, 2))  # Boot highlight

    # Boot sole
    pygame.draw.rect(item, BLACK, (6, 26, 20, 4))  # Sole
    pygame.draw.rect(item, DARK_GRAY, (7, 27, 18, 2))  # Sole highlight

    # Laces
    pygame.draw.rect(item, WHITE, (10, 18, 2, 1))  # Lace 1
    pygame.draw.rect(item, WHITE, (14, 20, 2, 1))  # Lace 2
    pygame.draw.rect(item, WHITE, (18, 22, 2, 1))  # Lace 3

    # Speed lines (motion effect)
    pygame.draw.rect(item, CYAN, (2, 12, 4, 1))  # Speed line 1
    pygame.draw.rect(item, CYAN, (4, 14, 6, 1))  # Speed line 2
    pygame.draw.rect(item, CYAN, (3, 16, 5, 1))  # Speed line 3

    return item

def create_fire_rate_boost_sprite():
    """Create a fire rate boost item sprite (clock/timer icon)"""
    item = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

    # Clock face
    pygame.draw.circle(item, GOLD, (16, 16), 10)  # Outer ring
    pygame.draw.circle(item, YELLOW, (16, 16), 8)  # Inner face
    pygame.draw.circle(item, WHITE, (16, 16), 6)  # Center face

    # Clock hands
    pygame.draw.rect(item, BLACK, (15, 10, 2, 6))  # Hour hand
    pygame.draw.rect(item, BLACK, (16, 8, 1, 8))  # Minute hand

    # Clock numbers (simplified)
    pygame.draw.rect(item, BLACK, (15, 8, 2, 1))  # 12
    pygame.draw.rect(item, BLACK, (23, 15, 1, 2))  # 3
    pygame.draw.rect(item, BLACK, (15, 23, 2, 1))  # 6
    pygame.draw.rect(item, BLACK, (8, 15, 1, 2))  # 9

    # Center dot
    pygame.draw.circle(item, BLACK, (16, 16), 1)

    return item

# Create additional item sprites
damage_boost = create_damage_boost_sprite()
pygame.image.save(damage_boost, "assets/images/damage_boost.png")

speed_boost = create_speed_boost_sprite()
pygame.image.save(speed_boost, "assets/images/speed_boost.png")

fire_rate_boost = create_fire_rate_boost_sprite()
pygame.image.save(fire_rate_boost, "assets/images/fire_rate_boost.png")

print("Enhanced assets generated successfully!")

# Quit pygame
pygame.quit()
