import pygame
from level.level_generator import LevelGenerator
from entities.player import Player
from entities.enemy import Enemy
from entities.boss_enemy import BossEnemy
from entities.item import create_random_item
from utils.constants import *
from utils.visual_effects import VisualEffectsManager
from utils.animation_system import AnimationManager

class Tile(pygame.sprite.Sprite):
    """A tile in the level (wall or floor)"""

    def __init__(self, x, y, is_wall=False):
        super().__init__()

        # Load image based on tile type
        if is_wall:
            self.image = pygame.image.load(WALL_IMG).convert_alpha()
            self.is_wall = True
        else:
            self.image = pygame.image.load(FLOOR_IMG).convert_alpha()
            self.is_wall = False

        # Set position
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Level:
    """Manages the current level with improved features"""

    def __init__(self, audio_manager=None):
        # Audio manager for sound effects
        self.audio_manager = audio_manager

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        # Level generator
        self.generator = None
        self.current_level = 1

        # Player
        self.player = None
        self.player_level_up = False  # Flag to indicate player leveled up

        # Camera offset
        self.camera_offset_x = 0
        self.camera_offset_y = 0

        # Minimap
        self.minimap_surface = None
        self.minimap_base_surface = None  # Store the base minimap without player position
        self.minimap_scale = 0.1  # Scale factor for minimap
        self.last_player_minimap_pos = (0, 0)  # Store last player position on minimap

        # Enhanced visual systems
        self.visual_effects = VisualEffectsManager()
        self.animation_manager = AnimationManager()

        # XP gain message (will be migrated to animation manager)
        self.xp_messages = []
        self.message_duration = 60  # frames

    def generate_level(self, current_level=1, player=None):
        """Generate a new level with the current level number"""
        # Store current level
        self.current_level = current_level

        try:
            # Create level generator with current level
            self.generator = LevelGenerator(current_level=current_level)

            # Clear all sprite groups
            self.all_sprites.empty()
            self.walls.empty()
            self.floors.empty()
            self.enemies.empty()
            self.projectiles.empty()
            self.items.empty()

            # Clear messages
            self.xp_messages = []

            # Generate new level
            tiles, player_pos, enemy_positions, item_positions = self.generator.generate()
        except Exception as e:
            print(f"Error generating level: {e}")
            # Create a fallback level if generation fails
            self._create_fallback_level()
            return

        # Create tiles
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == 1:  # Wall
                    wall = Tile(x, y, is_wall=True)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                else:  # Floor
                    floor = Tile(x, y, is_wall=False)
                    self.floors.add(floor)
                    self.all_sprites.add(floor)

        # Create player or use existing player
        player_x = player_pos[0] * TILE_SIZE
        player_y = player_pos[1] * TILE_SIZE

        if player:
            # Use existing player but update position
            self.player = player
            self.player.rect.x = player_x
            self.player.rect.y = player_y
            if hasattr(self.player, 'collision_rect'):
                self.player.collision_rect.center = self.player.rect.center
        else:
            # Create new player
            self.player = Player(player_x, player_y)

        # Set player's reference to this level for visual effects and interactions
        # This uses current_level_ref to avoid confusion with player.level (which is the player's experience level)
        self.player.current_level_ref = self

        # Set audio manager reference for the player
        if hasattr(self, 'audio_manager') and self.audio_manager:
            self.player.audio_manager = self.audio_manager

        self.all_sprites.add(self.player)

        # Create enemies with level-based scaling
        for pos in enemy_positions:
            # Check if this is a boss enemy
            if isinstance(pos, tuple) and len(pos) == 2 and pos[0] == "boss":
                # Create boss enemy
                boss_pos = pos[1]
                enemy_x = boss_pos[0] * TILE_SIZE
                enemy_y = boss_pos[1] * TILE_SIZE
                enemy = BossEnemy(enemy_x, enemy_y, difficulty_level=current_level)
            else:
                # Create regular enemy
                enemy_x = pos[0] * TILE_SIZE
                enemy_y = pos[1] * TILE_SIZE
                enemy = Enemy(enemy_x, enemy_y, difficulty_level=current_level)

            # Set audio manager reference for the enemy
            if hasattr(self, 'audio_manager') and self.audio_manager:
                enemy.audio_manager = self.audio_manager

            # Set visual effects reference for the enemy
            if hasattr(self, 'visual_effects') and self.visual_effects:
                enemy.visual_effects = self.visual_effects

            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Create items (now with different types)
        for pos in item_positions:
            item_x = pos[0] * TILE_SIZE
            item_y = pos[1] * TILE_SIZE

            # Create a random item using our factory function
            item = create_random_item(item_x, item_y)
            self.items.add(item)
            self.all_sprites.add(item)

        # Generate minimap
        self.generate_minimap(tiles)

    def update(self, game=None, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Update all entities in the level"""
        # Update player
        self.player.update(self.walls)

        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.walls, self.projectiles)

        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(self.walls, self.enemies, self.player, game)

            # Check if an enemy was killed by this projectile
            if projectile.is_player_projectile and hasattr(projectile, 'killed_enemy') and projectile.killed_enemy:
                # Add XP to player
                xp_gained = XP_PER_ENEMY
                leveled_up = self.player.add_xp(xp_gained)

                # Add floating XP message
                self.add_floating_text(f"+{xp_gained} XP", projectile.rect.centerx, projectile.rect.centery, YELLOW)

                # Set flag if player leveled up
                if leveled_up:
                    self.player_level_up = True

                # Clear the flag so we don't add XP multiple times
                projectile.killed_enemy = False

        # Update items
        for item in self.items:
            item.update()

        # Check for item collection
        self.check_item_collection(game)

        # Update XP messages
        self.update_messages()

        # Update camera position to follow player
        self.update_camera(screen_width, screen_height)

        # Update minimap with player position
        self.update_minimap()

        # Update visual effects and animations
        self.visual_effects.update()
        self.animation_manager.update()

    def update_messages(self):
        """Update floating messages"""
        # Update each message
        for i in range(len(self.xp_messages) - 1, -1, -1):
            message = self.xp_messages[i]

            # Move message
            message['x'] += message['velocity'].x
            message['y'] += message['velocity'].y

            # Decrease duration
            message['duration'] -= 1

            # Remove if duration is over
            if message['duration'] <= 0:
                self.xp_messages.pop(i)

    def update_camera(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        """Update camera position to center on player"""
        self.camera_offset_x = self.player.rect.centerx - screen_width // 2
        self.camera_offset_y = self.player.rect.centery - screen_height // 2

        # Clamp camera to level boundaries, but handle cases where screen is larger than level
        level_pixel_width = self.generator.width * TILE_SIZE
        level_pixel_height = self.generator.height * TILE_SIZE

        # Only clamp if the level is larger than the screen
        if level_pixel_width > screen_width:
            self.camera_offset_x = max(0, min(self.camera_offset_x, level_pixel_width - screen_width))
        else:
            # Center the level on screen if level is smaller than screen
            self.camera_offset_x = -(screen_width - level_pixel_width) // 2

        if level_pixel_height > screen_height:
            self.camera_offset_y = max(0, min(self.camera_offset_y, level_pixel_height - screen_height))
        else:
            # Center the level on screen if level is smaller than screen
            self.camera_offset_y = -(screen_height - level_pixel_height) // 2

    def update_minimap(self):
        """Update player position on minimap without regenerating the whole map"""
        if self.minimap_base_surface and self.player:
            # Create a fresh copy of the base minimap
            self.minimap_surface = self.minimap_base_surface.copy()

            # Calculate new player position
            player_minimap_x = int(self.player.rect.centerx * self.minimap_scale)
            player_minimap_y = int(self.player.rect.centery * self.minimap_scale)

            # Update last known position
            self.last_player_minimap_pos = (player_minimap_x, player_minimap_y)

            # Draw player on minimap
            pygame.draw.circle(self.minimap_surface, GREEN, self.last_player_minimap_pos, 2)

    def add_floating_text(self, text, x, y, color, duration=None, velocity=None):
        """Add floating text with customizable parameters"""
        if duration is None:
            duration = self.message_duration

        if velocity is None:
            velocity = pygame.math.Vector2(0, -1)  # Default: move upward

        self.xp_messages.append({
            'text': text,
            'x': x,
            'y': y,
            'color': color,
            'duration': duration,
            'velocity': velocity
        })

    def _create_fallback_level(self):
        """Create a simple fallback level in case of generation failure"""
        # Create a simple 20x15 room with walls around the edges
        width, height = 20, 15
        tiles = [[0 for _ in range(width)] for _ in range(height)]

        # Add walls around the edges
        for x in range(width):
            tiles[0][x] = 1  # Top wall
            tiles[height-1][x] = 1  # Bottom wall

        for y in range(height):
            tiles[y][0] = 1  # Left wall
            tiles[y][width-1] = 1  # Right wall

        # Create a simple LevelGenerator with these tiles
        self.generator = LevelGenerator(width=width, height=height, current_level=self.current_level)
        self.generator.tiles = tiles
        self.generator.width = width
        self.generator.height = height

        # Set player position in the center
        player_pos = (width // 2, height // 2)

        # Create tiles
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                if tile == 1:  # Wall
                    wall = Tile(x, y, is_wall=True)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                else:  # Floor
                    floor = Tile(x, y, is_wall=False)
                    self.floors.add(floor)
                    self.all_sprites.add(floor)

        # Create player
        player_x = player_pos[0] * TILE_SIZE
        player_y = player_pos[1] * TILE_SIZE
        self.player = Player(player_x, player_y)
        # Set player's reference to this level for visual effects and interactions
        # This uses current_level_ref to avoid confusion with player.level (which is the player's experience level)
        self.player.current_level_ref = self

        # Set audio manager reference for the player
        if hasattr(self, 'audio_manager') and self.audio_manager:
            self.player.audio_manager = self.audio_manager

        self.all_sprites.add(self.player)

        # Add a message about the fallback level
        self.add_floating_text("Emergency level generated!",
                              player_x, player_y - 50,
                              RED,
                              duration=120)

        # Generate minimap for the fallback level
        self.generate_minimap(tiles)

    def draw(self, screen, score=0, current_level=1):
        """Draw the level and all entities"""
        # Get current screen dimensions
        screen_width, screen_height = screen.get_size()

        # Fill background with a dark pattern instead of pure black
        screen.fill((20, 20, 20))  # Very dark gray instead of pure black

        # Draw a subtle background pattern to fill empty areas
        self._draw_background_pattern(screen, screen_width, screen_height)

        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            # Only draw sprites that are within the visible area (optimization)
            sprite_x = sprite.rect.x - self.camera_offset_x
            sprite_y = sprite.rect.y - self.camera_offset_y

            if (-sprite.rect.width <= sprite_x <= screen_width and
                -sprite.rect.height <= sprite_y <= screen_height):
                screen.blit(sprite.image, (sprite_x, sprite_y))

        # Draw projectiles with trails and camera offset
        for projectile in self.projectiles:
            if hasattr(projectile, 'draw'):
                projectile.draw(screen, self.camera_offset_x, self.camera_offset_y)
            else:
                # Fallback for projectiles without custom draw method
                screen.blit(projectile.image, (projectile.rect.x - self.camera_offset_x, projectile.rect.y - self.camera_offset_y))

        # Draw health bars for entities
        for enemy in self.enemies:
            enemy.draw_health_bar(screen, self.camera_offset_x, self.camera_offset_y)

        # Draw XP messages
        font = pygame.font.SysFont(None, 20)
        for message in self.xp_messages:
            text_surface = font.render(message['text'], True, message['color'])
            text_rect = text_surface.get_rect(center=(
                message['x'] - self.camera_offset_x,
                message['y'] - self.camera_offset_y
            ))
            screen.blit(text_surface, text_rect)

        # Draw player health bar at fixed position on screen
        pygame.draw.rect(screen, RED, (10, 10, 200, 20))
        health_width = int(200 * (self.player.health / self.player.max_health))
        pygame.draw.rect(screen, GREEN, (10, 10, health_width, 20))

        # Draw health text
        font = pygame.font.SysFont(None, 24)
        health_text = font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
        screen.blit(health_text, (15, 12))

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (screen_width - 150, 12))

        # Draw current level
        level_text = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(level_text, (screen_width - 150, 40))

        # Draw player level and XP
        player_level_text = font.render(f"Player Lv: {self.player.level}", True, CYAN)
        screen.blit(player_level_text, (10, 40))

        # XP bar
        xp_bar_width = 200
        pygame.draw.rect(screen, GRAY, (10, 70, xp_bar_width, 10))
        xp_width = int(xp_bar_width * (self.player.xp / self.player.xp_to_next_level))
        pygame.draw.rect(screen, CYAN, (10, 70, xp_width, 10))

        # XP text
        xp_text = font.render(f"XP: {self.player.xp}/{self.player.xp_to_next_level}", True, CYAN)
        screen.blit(xp_text, (15, 85))

        # Draw upgrade points if available
        if self.player.upgrade_points > 0:
            upgrade_text = font.render(f"Upgrade Points: {self.player.upgrade_points}", True, YELLOW)
            screen.blit(upgrade_text, (screen_width // 2 - 100, 12))

        # Draw special effect indicators
        effect_y = 110
        if hasattr(self.player, 'shield_health') and self.player.shield_health > 0:
            shield_text = font.render(f"Shield: {self.player.shield_health}", True, CYAN)
            screen.blit(shield_text, (10, effect_y))
            effect_y += 25

        if hasattr(self.player, 'multi_shot_duration') and self.player.multi_shot_duration > 0:
            multi_text = font.render(f"Multi-Shot: {self.player.multi_shot_duration // 60}s", True, ORANGE)
            screen.blit(multi_text, (10, effect_y))
            effect_y += 25

        if hasattr(self.player, 'invincibility_duration') and self.player.invincibility_duration > 0:
            invincible_text = font.render(f"Invincible: {self.player.invincibility_duration // 60}s", True, YELLOW)
            screen.blit(invincible_text, (10, effect_y))

        # Draw minimap in the corner (player position is already drawn on the minimap surface)
        if self.minimap_surface:
            minimap_rect = self.minimap_surface.get_rect()
            minimap_rect.bottomright = (screen_width - 10, screen_height - 10)
            screen.blit(self.minimap_surface, minimap_rect)

        # Draw visual effects and animations
        self.visual_effects.draw(screen, self.camera_offset_x, self.camera_offset_y)
        self.animation_manager.draw_floating_texts(screen, self.camera_offset_x, self.camera_offset_y)

    def handle_player_shoot(self, target_x, target_y):
        """Handle player shooting at the target position"""
        # Adjust target position for camera offset
        adjusted_x = target_x + self.camera_offset_x
        adjusted_y = target_y + self.camera_offset_y

        # Try to shoot
        return self.player.shoot(adjusted_x, adjusted_y, self.projectiles)

    def check_item_collection(self, game=None):
        """Check if player has collected any items"""
        # Use the player's collision rect if available for more accurate collision detection
        if hasattr(self.player, 'collision_rect'):
            # Create a temporary sprite for collision detection
            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = self.player.collision_rect

            # Check for collisions with items
            collected_items = pygame.sprite.spritecollide(temp_sprite, self.items, False)
        else:
            # Fallback to regular sprite collision if no collision_rect is available
            collected_items = pygame.sprite.spritecollide(self.player, self.items, False)

        # Process collected items
        for item in collected_items:
            if item.collect(self.player) and game:
                # Add score for collecting an item
                game.score += ITEM_COLLECT_SCORE

                # Add floating message
                self.add_floating_text(f"Collected {item.name}", item.rect.centerx, item.rect.centery, GREEN)

                # Play item collection sound
                if self.audio_manager:
                    self.audio_manager.play_sound('item_collect')

    def generate_minimap(self, tiles):
        """Generate a minimap from the level tiles"""
        # Calculate minimap dimensions
        minimap_width = int(self.generator.width * TILE_SIZE * self.minimap_scale)
        minimap_height = int(self.generator.height * TILE_SIZE * self.minimap_scale)

        # Create base minimap surface with transparency (without player position)
        self.minimap_base_surface = pygame.Surface((minimap_width, minimap_height), pygame.SRCALPHA)
        self.minimap_base_surface.fill((0, 0, 0, 128))  # Semi-transparent black background

        # Draw tiles on minimap
        for y, row in enumerate(tiles):
            for x, tile in enumerate(row):
                # Calculate pixel position
                pixel_x = int(x * TILE_SIZE * self.minimap_scale)
                pixel_y = int(y * TILE_SIZE * self.minimap_scale)

                # Draw pixel based on tile type
                if tile == 1:  # Wall
                    pygame.draw.rect(self.minimap_base_surface, GRAY,
                                    (pixel_x, pixel_y,
                                     max(1, int(TILE_SIZE * self.minimap_scale)),
                                     max(1, int(TILE_SIZE * self.minimap_scale))))
                else:  # Floor
                    pygame.draw.rect(self.minimap_base_surface, WHITE,
                                    (pixel_x, pixel_y,
                                     max(1, int(TILE_SIZE * self.minimap_scale)),
                                     max(1, int(TILE_SIZE * self.minimap_scale))))

        # Draw room centers for better visibility
        for room in self.generator.rooms:
            center_x = int(room.center_x * TILE_SIZE * self.minimap_scale)
            center_y = int(room.center_y * TILE_SIZE * self.minimap_scale)

            # Different colors for different room types
            if room.room_type == "normal":
                color = WHITE
            elif room.room_type == "treasure":
                color = YELLOW
            elif room.room_type == "challenge":
                color = RED
            elif room.room_type == "boss":
                color = PURPLE
            else:
                color = WHITE

            pygame.draw.circle(self.minimap_base_surface, color, (center_x, center_y), 2)

        # Create the initial minimap surface (a copy of the base)
        self.minimap_surface = self.minimap_base_surface.copy()

        # Initialize player position
        if self.player:
            player_minimap_x = int(self.player.rect.centerx * self.minimap_scale)
            player_minimap_y = int(self.player.rect.centery * self.minimap_scale)
            self.last_player_minimap_pos = (player_minimap_x, player_minimap_y)
            pygame.draw.circle(self.minimap_surface, GREEN, self.last_player_minimap_pos, 2)

    def _draw_background_pattern(self, screen, screen_width, screen_height):
        """Draw a subtle background pattern to fill areas outside the level"""
        # Create a subtle grid pattern for areas outside the level
        grid_size = TILE_SIZE
        grid_color = (30, 30, 30)  # Slightly lighter than background

        # Calculate the visible area considering camera offset
        start_x = int(self.camera_offset_x // grid_size) * grid_size
        start_y = int(self.camera_offset_y // grid_size) * grid_size

        # Draw vertical lines
        for x in range(start_x - grid_size, start_x + screen_width + grid_size, grid_size):
            screen_x = x - self.camera_offset_x
            if 0 <= screen_x <= screen_width:
                pygame.draw.line(screen, grid_color, (screen_x, 0), (screen_x, screen_height))

        # Draw horizontal lines
        for y in range(start_y - grid_size, start_y + screen_height + grid_size, grid_size):
            screen_y = y - self.camera_offset_y
            if 0 <= screen_y <= screen_height:
                pygame.draw.line(screen, grid_color, (0, screen_y), (screen_width, screen_y))