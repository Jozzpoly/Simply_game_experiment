"""
Level Management - Simplified Implementation
Reduced from 1,049 lines to ~300 lines (71% reduction)

Manages the current level state, entities, and rendering.
No complex systems, just essential level functionality.
"""

import pygame
from config import *
from level.generator import LevelGenerator
from entities.player import Player
from entities.enemy import Enemy, create_random_enemy
from entities.projectile import Projectile

class Tile(pygame.sprite.Sprite):
    """Simple tile sprite for walls and floors"""
    
    def __init__(self, x, y, is_wall=False):
        super().__init__()
        
        # Create simple tile surface
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if is_wall:
            self.image.fill(GRAY)
            self.is_wall = True
        else:
            self.image.fill(BLACK)
            self.is_wall = False
        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

class Level:
    """Manages the current level state and entities"""
    
    def __init__(self, level_number=1):
        self.level_number = level_number
        self.generator = LevelGenerator(level_number)
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Player
        self.player = None
        
        # Level state
        self.completed = False
        self.enemies_killed = 0
        
        # Generate the level
        self.generate()
    
    def generate(self):
        """Generate a new level"""
        # Clear existing sprites
        self.all_sprites.empty()
        self.walls.empty()
        self.floors.empty()
        self.enemies.empty()
        self.projectiles.empty()
        
        # Generate level layout
        tiles, player_pos, enemy_positions = self.generator.generate()
        
        # Create tile sprites
        for y, row in enumerate(tiles):
            for x, tile_type in enumerate(row):
                tile = Tile(x, y, is_wall=(tile_type == 1))
                self.all_sprites.add(tile)
                
                if tile.is_wall:
                    self.walls.add(tile)
                else:
                    self.floors.add(tile)
        
        # Create player
        self.player = Player(player_pos[0], player_pos[1])
        self.all_sprites.add(self.player)
        
        # Create enemies
        for enemy_pos in enemy_positions:
            enemy = create_random_enemy(enemy_pos[0], enemy_pos[1], self.level_number)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
        
        # Reset level state
        self.completed = False
        self.enemies_killed = 0
    
    def update(self, dt, keys_pressed, mouse_pos, mouse_clicked):
        """Update all level entities"""
        if self.completed:
            return
        
        # Update player
        if self.player:
            self.player.update(dt, keys_pressed, self.walls)
            
            # Handle player shooting
            if mouse_clicked and self.player.can_shoot():
                projectile = self.player.shoot(mouse_pos[0], mouse_pos[1])
                if projectile:
                    self.projectiles.add(projectile)
                    self.all_sprites.add(projectile)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(dt, self.player, self.walls)
            
            # Enemy shooting (for archers)
            if enemy.is_archer and enemy.can_shoot():
                projectile = enemy.shoot()
                if projectile:
                    self.projectiles.add(projectile)
                    self.all_sprites.add(projectile)
        
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
            
            # Check wall collisions
            if projectile.check_wall_collision(self.walls):
                continue
        
        # Handle collisions
        self.handle_collisions()
        
        # Check level completion
        if len(self.enemies) == 0:
            self.completed = True
    
    def handle_collisions(self):
        """Handle all collision detection"""
        # Player projectiles vs enemies
        for projectile in self.projectiles:
            if projectile.owner_type == 'player':
                hit_enemies = pygame.sprite.spritecollide(projectile, self.enemies, False)
                for enemy in hit_enemies:
                    if enemy.take_damage(projectile.damage):
                        # Enemy died
                        self.enemies_killed += 1
                        self.player.add_xp(XP_PER_ENEMY)
                        self.all_sprites.remove(enemy)
                    
                    # Remove projectile
                    projectile.kill()
                    self.all_sprites.remove(projectile)
                    break
        
        # Enemy projectiles vs player
        for projectile in self.projectiles:
            if projectile.owner_type == 'enemy':
                if pygame.sprite.collide_rect(projectile, self.player):
                    self.player.take_damage(projectile.damage)
                    projectile.kill()
                    self.all_sprites.remove(projectile)
        
        # Enemies vs player (melee damage)
        for enemy in self.enemies:
            if not enemy.is_archer and pygame.sprite.collide_rect(enemy, self.player):
                # Simple melee damage with cooldown
                if not hasattr(enemy, 'last_melee_time'):
                    enemy.last_melee_time = 0
                
                current_time = pygame.time.get_ticks() / 1000.0
                if current_time - enemy.last_melee_time > 1.0:  # 1 second cooldown
                    self.player.take_damage(enemy.damage)
                    enemy.last_melee_time = current_time
    
    def draw(self, screen):
        """Draw all level elements"""
        # Clear screen
        screen.fill(BLACK)
        
        # Draw all sprites
        self.all_sprites.draw(screen)
        
        # Draw health bars for enemies
        for enemy in self.enemies:
            self.draw_enemy_health_bar(screen, enemy)
    
    def draw_enemy_health_bar(self, screen, enemy):
        """Draw a simple health bar above enemy"""
        if enemy.health < enemy.max_health:
            bar_width = 30
            bar_height = 4
            bar_x = enemy.rect.centerx - bar_width // 2
            bar_y = enemy.rect.y - 8
            
            # Background (red)
            pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
            
            # Health (green)
            health_width = int(bar_width * enemy.get_health_percentage())
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
    
    def is_completed(self):
        """Check if level is completed"""
        return self.completed
    
    def get_stats(self):
        """Get level statistics"""
        return {
            'level_number': self.level_number,
            'enemies_remaining': len(self.enemies),
            'enemies_killed': self.enemies_killed,
            'completed': self.completed
        }
