"""
Player Entity - Simplified Implementation
Reduced from 753 lines to ~200 lines (73% reduction)

Core player functionality without over-engineering:
- Movement and collision
- Health and combat
- Simple leveling system
- Basic shooting mechanics
"""

import pygame
import math
from config import *
from utils.constants import distance, clamp
from entities.projectile import Projectile

class Player(pygame.sprite.Sprite):
    """Simple player class with essential functionality"""
    
    def __init__(self, x, y):
        super().__init__()
        
        # Create simple player sprite
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Stats
        self.max_health = PLAYER_HEALTH
        self.health = self.max_health
        self.damage = PLAYER_DAMAGE
        self.speed = PLAYER_SPEED
        
        # Progression
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = XP_PER_LEVEL
        
        # Combat
        self.last_shot_time = 0
        self.fire_rate = PLAYER_FIRE_RATE
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
    
    def update(self, dt, keys_pressed, walls):
        """Update player state"""
        self.handle_movement(dt, keys_pressed, walls)
        self.update_shooting_cooldown(dt)
    
    def handle_movement(self, dt, keys_pressed, walls):
        """Handle player movement with collision detection"""
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Check movement keys
        for key, (dx, dy) in MOVEMENT_KEYS.items():
            if keys_pressed[key]:
                self.velocity_x += dx
                self.velocity_y += dy
        
        # Normalize diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x *= 0.707  # 1/sqrt(2)
            self.velocity_y *= 0.707
        
        # Apply speed
        self.velocity_x *= self.speed * dt
        self.velocity_y *= self.speed * dt
        
        # Move and check collisions
        self.move_with_collision(walls)
    
    def move_with_collision(self, walls):
        """Move player with wall collision detection"""
        # Try horizontal movement
        old_x = self.rect.x
        self.rect.x += self.velocity_x
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = old_x
        
        # Try vertical movement
        old_y = self.rect.y
        self.rect.y += self.velocity_y
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y = old_y
        
        # Keep player on screen
        self.rect.x = clamp(self.rect.x, 0, SCREEN_WIDTH - PLAYER_SIZE)
        self.rect.y = clamp(self.rect.y, 0, SCREEN_HEIGHT - PLAYER_SIZE)
    
    def update_shooting_cooldown(self, dt):
        """Update shooting cooldown timer"""
        if self.last_shot_time > 0:
            self.last_shot_time -= dt
    
    def can_shoot(self):
        """Check if player can shoot"""
        return self.last_shot_time <= 0
    
    def shoot(self, target_x, target_y):
        """Create a projectile towards target position"""
        if not self.can_shoot():
            return None
        
        self.last_shot_time = self.fire_rate
        
        # Create projectile from player center
        projectile = Projectile(
            self.rect.centerx, 
            self.rect.centery,
            target_x, 
            target_y,
            self.damage,
            'player',
            WHITE
        )
        
        return projectile
    
    def take_damage(self, amount):
        """Take damage and return True if player died"""
        self.health -= amount
        self.health = max(0, self.health)
        return self.health <= 0
    
    def heal(self, amount):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
    
    def add_xp(self, amount):
        """Add experience points and handle leveling"""
        self.xp += amount
        
        # Check for level up
        while self.xp >= self.xp_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the player"""
        self.xp -= self.xp_to_next_level
        self.level += 1
        
        # Increase stats
        self.max_health += HEALTH_PER_LEVEL
        self.health = self.max_health  # Full heal on level up
        self.damage += DAMAGE_PER_LEVEL
        
        # Increase XP requirement for next level
        self.xp_to_next_level = XP_PER_LEVEL * self.level
    
    def get_health_percentage(self):
        """Get health as percentage for UI"""
        return self.health / self.max_health if self.max_health > 0 else 0
    
    def get_xp_percentage(self):
        """Get XP progress as percentage for UI"""
        return self.xp / self.xp_to_next_level if self.xp_to_next_level > 0 else 0

    def get_stats(self):
        """Get player stats for display"""
        return {
            'level': self.level,
            'health': self.health,
            'max_health': self.max_health,
            'damage': self.damage,
            'xp': self.xp,
            'xp_to_next': self.xp_to_next_level
        }
