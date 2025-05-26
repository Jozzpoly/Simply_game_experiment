import pygame
import os
import math

# Initialize pygame
pygame.init()

# Create assets directory if it doesn't exist
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/images/tiles", exist_ok=True)
os.makedirs("assets/images/entities", exist_ok=True)
os.makedirs("assets/images/entities/player", exist_ok=True)
os.makedirs("assets/images/entities/enemy", exist_ok=True)
os.makedirs("assets/images/entities/boss", exist_ok=True)
os.makedirs("assets/images/effects", exist_ok=True)
os.makedirs("assets/images/effects/particles", exist_ok=True)
os.makedirs("assets/images/effects/explosions", exist_ok=True)
os.makedirs("assets/images/ui", exist_ok=True)
os.makedirs("assets/images/ui/buttons", exist_ok=True)
os.makedirs("assets/images/ui/panels", exist_ok=True)
os.makedirs("assets/images/ui/icons", exist_ok=True)

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

# ===== ANIMATION FRAME GENERATION =====

def create_player_animation_frames():
    """Create animation frames for player character"""
    base_player = create_enhanced_player_sprite()

    # Idle animation frames (4 frames with subtle breathing effect)
    for i in range(4):
        frame = base_player.copy()
        # Subtle breathing effect - slight vertical movement
        breathing_offset = int(math.sin(i * math.pi / 2) * 0.5)
        if breathing_offset != 0:
            temp_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            temp_surface.blit(frame, (0, breathing_offset))
            frame = temp_surface

        pygame.image.save(frame, f"assets/images/entities/player/idle_{i}.png")

    # Walking animation frames (8 frames with bob effect)
    for i in range(8):
        frame = base_player.copy()
        # Walking bob effect
        bob_offset = int(math.sin(i * math.pi / 4) * 1.5)
        if bob_offset != 0:
            temp_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            temp_surface.blit(frame, (0, bob_offset))
            frame = temp_surface

        pygame.image.save(frame, f"assets/images/entities/player/walk_{i}.png")

    # Attack animation frames (6 frames with weapon swing)
    for i in range(6):
        frame = base_player.copy()
        # Simple attack effect - weapon glow
        if i in [2, 3]:  # Peak of attack
            # Add weapon glow effect
            glow_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            glow_surface.blit(frame, (0, 0))
            # Add white glow around weapon area
            pygame.draw.rect(glow_surface, (255, 255, 255, 100), (26, 6, 6, 16))
            frame = glow_surface

        pygame.image.save(frame, f"assets/images/entities/player/attack_{i}.png")

def create_enemy_animation_frames():
    """Create animation frames for enemy characters"""
    base_enemy = create_enhanced_enemy_sprite()

    # Idle animation frames (4 frames with menacing sway)
    for i in range(4):
        frame = base_enemy.copy()
        # Menacing sway effect
        sway_offset = int(math.sin(i * math.pi / 2) * 0.8)
        if sway_offset != 0:
            temp_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            temp_surface.blit(frame, (sway_offset, 0))
            frame = temp_surface

        pygame.image.save(frame, f"assets/images/entities/enemy/idle_{i}.png")

    # Walking animation frames (8 frames)
    for i in range(8):
        frame = base_enemy.copy()
        # Walking animation with aggressive movement
        bob_offset = int(math.sin(i * math.pi / 4) * 2)
        if bob_offset != 0:
            temp_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            temp_surface.blit(frame, (0, bob_offset))
            frame = temp_surface

        pygame.image.save(frame, f"assets/images/entities/enemy/walk_{i}.png")

    # Attack animation frames (6 frames)
    for i in range(6):
        frame = base_enemy.copy()
        # Attack effect with weapon glow
        if i in [2, 3]:  # Peak of attack
            glow_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            glow_surface.blit(frame, (0, 0))
            # Add red glow around weapon
            pygame.draw.rect(glow_surface, (255, 0, 0, 120), (24, 8, 8, 12))
            frame = glow_surface

        pygame.image.save(frame, f"assets/images/entities/enemy/attack_{i}.png")

def create_boss_animation_frames():
    """Create animation frames for boss enemies"""
    # Create a larger, more imposing boss sprite
    boss_surface = pygame.Surface((64, 64), pygame.SRCALPHA)

    # Boss body (larger and more detailed)
    pygame.draw.rect(boss_surface, DARK_RED, (16, 24, 32, 28))  # Main body
    pygame.draw.rect(boss_surface, BLACK, (18, 26, 28, 4))  # Dark armor
    pygame.draw.rect(boss_surface, DARK_GRAY, (20, 30, 24, 2))  # Armor details

    # Boss head (larger and more menacing)
    pygame.draw.rect(boss_surface, DARK_RED, (20, 8, 24, 20))  # Head
    pygame.draw.rect(boss_surface, RED, (22, 10, 20, 4))  # Head highlight

    # Glowing eyes
    pygame.draw.rect(boss_surface, RED, (24, 16, 4, 4))  # Left eye
    pygame.draw.rect(boss_surface, RED, (36, 16, 4, 4))  # Right eye
    pygame.draw.rect(boss_surface, WHITE, (25, 17, 2, 2))  # Eye glow
    pygame.draw.rect(boss_surface, WHITE, (37, 17, 2, 2))  # Eye glow

    # Boss arms (larger)
    pygame.draw.rect(boss_surface, DARK_RED, (8, 28, 8, 16))  # Left arm
    pygame.draw.rect(boss_surface, DARK_RED, (48, 28, 8, 16))  # Right arm

    # Boss legs
    pygame.draw.rect(boss_surface, DARK_RED, (20, 52, 8, 8))  # Left leg
    pygame.draw.rect(boss_surface, DARK_RED, (36, 52, 8, 8))  # Right leg

    # Boss weapon (massive axe)
    pygame.draw.rect(boss_surface, DARK_BROWN, (56, 16, 4, 20))  # Handle
    pygame.draw.rect(boss_surface, DARK_GRAY, (52, 12, 12, 8))  # Axe head
    pygame.draw.rect(boss_surface, GRAY, (54, 14, 8, 4))  # Axe highlight

    # Idle animation frames (6 frames with intimidating presence)
    for i in range(6):
        frame = boss_surface.copy()
        # Intimidating breathing effect
        breathing_offset = int(math.sin(i * math.pi / 3) * 1)
        if breathing_offset != 0:
            temp_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            temp_surface.blit(frame, (0, breathing_offset))
            frame = temp_surface

        # Add pulsing red aura
        if i % 2 == 0:
            aura_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            aura_surface.blit(frame, (0, 0))
            pygame.draw.rect(aura_surface, (255, 0, 0, 30), (0, 0, 64, 64))
            frame = aura_surface

        pygame.image.save(frame, f"assets/images/entities/boss/idle_{i}.png")

    # Attack animation frames (8 frames with devastating swing)
    for i in range(8):
        frame = boss_surface.copy()
        # Massive attack animation
        if i in [3, 4, 5]:  # Peak of attack
            glow_surface = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            glow_surface.blit(frame, (0, 0))
            # Massive weapon glow
            pygame.draw.rect(glow_surface, (255, 100, 100, 150), (48, 8, 16, 24))
            frame = glow_surface

        pygame.image.save(frame, f"assets/images/entities/boss/attack_{i}.png")

# ===== UI ELEMENT GENERATION =====

def create_modern_button_styles():
    """Create modern button styles with gradients and effects"""
    button_sizes = [(200, 50), (150, 40), (120, 30)]
    button_states = ["normal", "hover", "pressed", "disabled"]

    for size in button_sizes:
        width, height = size
        for state in button_states:
            button_surface = pygame.Surface((width, height), pygame.SRCALPHA)

            if state == "normal":
                # Modern gradient button
                for y in range(height):
                    alpha = 1.0 - (y / height) * 0.3
                    color = (int(70 * alpha), int(130 * alpha), int(180 * alpha))
                    pygame.draw.line(button_surface, color, (2, y), (width-3, y))

                # Border
                pygame.draw.rect(button_surface, (50, 100, 150), (0, 0, width, height), 2)

            elif state == "hover":
                # Brighter hover state
                for y in range(height):
                    alpha = 1.0 - (y / height) * 0.2
                    color = (int(90 * alpha), int(150 * alpha), int(200 * alpha))
                    pygame.draw.line(button_surface, color, (2, y), (width-3, y))

                # Glowing border
                pygame.draw.rect(button_surface, (100, 150, 255), (0, 0, width, height), 2)

            elif state == "pressed":
                # Pressed/active state
                for y in range(height):
                    alpha = 1.0 - (y / height) * 0.4
                    color = (int(50 * alpha), int(100 * alpha), int(140 * alpha))
                    pygame.draw.line(button_surface, color, (2, y), (width-3, y))

                pygame.draw.rect(button_surface, (30, 80, 120), (0, 0, width, height), 2)

            elif state == "disabled":
                # Grayed out disabled state
                for y in range(height):
                    alpha = 1.0 - (y / height) * 0.3
                    color = (int(80 * alpha), int(80 * alpha), int(80 * alpha))
                    pygame.draw.line(button_surface, color, (2, y), (width-3, y))

                pygame.draw.rect(button_surface, (60, 60, 60), (0, 0, width, height), 2)

            # Add subtle inner highlight
            pygame.draw.line(button_surface, (255, 255, 255, 50), (2, 2), (width-3, 2))

            filename = f"assets/images/ui/buttons/button_{width}x{height}_{state}.png"
            pygame.image.save(button_surface, filename)

def create_ui_panels():
    """Create modern UI panel backgrounds"""
    panel_sizes = [(400, 300), (600, 400), (800, 600)]

    for width, height in panel_sizes:
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Semi-transparent dark background
        panel_surface.fill((20, 20, 30, 200))

        # Modern border with gradient
        border_color = (100, 150, 200)
        pygame.draw.rect(panel_surface, border_color, (0, 0, width, height), 3)

        # Inner border highlight
        pygame.draw.rect(panel_surface, (150, 200, 255, 100), (2, 2, width-4, height-4), 1)

        # Corner accents
        corner_size = 20
        pygame.draw.rect(panel_surface, (150, 200, 255), (0, 0, corner_size, corner_size))
        pygame.draw.rect(panel_surface, (150, 200, 255), (width-corner_size, 0, corner_size, corner_size))
        pygame.draw.rect(panel_surface, (150, 200, 255), (0, height-corner_size, corner_size, corner_size))
        pygame.draw.rect(panel_surface, (150, 200, 255), (width-corner_size, height-corner_size, corner_size, corner_size))

        filename = f"assets/images/ui/panels/panel_{width}x{height}.png"
        pygame.image.save(panel_surface, filename)

def create_ui_icons():
    """Create modern UI icons"""
    icon_size = 32

    # Health icon
    health_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    pygame.draw.circle(health_icon, RED, (icon_size//2, icon_size//2), icon_size//2 - 2)
    pygame.draw.rect(health_icon, WHITE, (icon_size//2 - 8, icon_size//2 - 2, 16, 4))
    pygame.draw.rect(health_icon, WHITE, (icon_size//2 - 2, icon_size//2 - 8, 4, 16))
    pygame.image.save(health_icon, "assets/images/ui/icons/health.png")

    # Mana/Energy icon
    mana_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    pygame.draw.circle(mana_icon, BLUE, (icon_size//2, icon_size//2), icon_size//2 - 2)
    # Lightning bolt shape
    points = [(icon_size//2 - 4, 6), (icon_size//2 + 2, icon_size//2 - 2),
              (icon_size//2 - 2, icon_size//2 - 2), (icon_size//2 + 4, icon_size - 6)]
    pygame.draw.polygon(mana_icon, WHITE, points)
    pygame.image.save(mana_icon, "assets/images/ui/icons/mana.png")

    # XP icon
    xp_icon = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)
    pygame.draw.circle(xp_icon, GOLD, (icon_size//2, icon_size//2), icon_size//2 - 2)
    # Star shape
    star_points = []
    for i in range(10):
        angle = i * math.pi / 5
        if i % 2 == 0:
            radius = icon_size//2 - 6
        else:
            radius = icon_size//2 - 12
        x = icon_size//2 + int(radius * math.cos(angle - math.pi/2))
        y = icon_size//2 + int(radius * math.sin(angle - math.pi/2))
        star_points.append((x, y))
    pygame.draw.polygon(xp_icon, WHITE, star_points)
    pygame.image.save(xp_icon, "assets/images/ui/icons/xp.png")

def create_particle_effects():
    """Create particle effect sprites"""
    particle_sizes = [4, 8, 12, 16]
    particle_colors = [
        ("fire", ORANGE, RED),
        ("magic", CYAN, BLUE),
        ("heal", GREEN, LIME),
        ("dark", PURPLE, BLACK)
    ]

    for size in particle_sizes:
        for name, color1, color2 in particle_colors:
            particle = pygame.Surface((size, size), pygame.SRCALPHA)

            # Create gradient particle
            center = size // 2
            for radius in range(center, 0, -1):
                alpha = int(255 * (radius / center))
                if radius == center:
                    current_color = (*color2, alpha)
                else:
                    # Blend between colors
                    blend = radius / center
                    blended_color = (
                        int(color1[0] * blend + color2[0] * (1 - blend)),
                        int(color1[1] * blend + color2[1] * (1 - blend)),
                        int(color1[2] * blend + color2[2] * (1 - blend)),
                        alpha
                    )
                    current_color = blended_color

                # Draw circle with alpha
                temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, current_color[:3], (center, center), radius)
                temp_surface.set_alpha(current_color[3])
                particle.blit(temp_surface, (0, 0))

            filename = f"assets/images/effects/particles/{name}_{size}.png"
            pygame.image.save(particle, filename)

# Generate all UI elements
create_modern_button_styles()
create_ui_panels()
create_ui_icons()
create_particle_effects()

# Generate all animation frames
create_player_animation_frames()
create_enemy_animation_frames()
create_boss_animation_frames()

print("Enhanced assets, UI elements, and animation frames generated successfully!")

# Quit pygame
pygame.quit()
