"""
Enemy System - Consolidated Implementation
Reduced from 1,696 lines (3 files) to ~200 lines (84% reduction)

Simple enemy AI with 4 basic types:
- Normal: Balanced stats
- Fast: Quick but fragile
- Tank: Slow but tough
- Archer: Ranged attacker
"""

import pygame
import math
import random
from config import *
from utils.constants import distance, normalize_vector
from entities.projectile import Projectile

class Enemy(pygame.sprite.Sprite):
    """Simple enemy with basic AI"""
    
    def __init__(self, x, y, enemy_type='normal'):
        super().__init__()
        
        # Get enemy type configuration
        self.type = enemy_type
        self.config = ENEMY_TYPES[enemy_type]
        
        # Create simple enemy sprite
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(self.config['color'])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Stats based on type
        self.max_health = int(ENEMY_HEALTH * self.config['health'])
        self.health = self.max_health
        self.speed = ENEMY_SPEED * self.config['speed']
        self.damage = int(ENEMY_DAMAGE * self.config['damage'])
        
        # AI state
        self.target = None
        self.last_shot_time = 0
        self.fire_rate = 2.0  # seconds between shots
        self.detection_range = ENEMY_DETECTION_RANGE
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Archer-specific
        self.is_archer = (enemy_type == 'archer')
        self.preferred_distance = 150 if self.is_archer else 32
    
    def update(self, dt, player, walls):
        """Update enemy AI and movement"""
        self.update_ai(dt, player)
        self.move_with_collision(dt, walls)
        self.update_shooting_cooldown(dt)
    
    def update_ai(self, dt, player):
        """Simple AI: move towards player if in range"""
        if not player:
            return
        
        # Check if player is in detection range
        dist_to_player = distance(self.rect.center, player.rect.center)
        
        if dist_to_player <= self.detection_range:
            self.target = player
            
            # Calculate direction to player
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            
            # Normalize direction
            direction = normalize_vector((dx, dy))
            
            # Different behavior for archers
            if self.is_archer:
                # Archers try to maintain distance
                if dist_to_player < self.preferred_distance:
                    # Move away from player
                    direction = (-direction[0], -direction[1])
                elif dist_to_player > self.preferred_distance + 50:
                    # Move towards player
                    pass  # direction already correct
                else:
                    # Stay in position
                    direction = (0, 0)
            
            # Set velocity
            self.velocity_x = direction[0] * self.speed
            self.velocity_y = direction[1] * self.speed
        else:
            self.target = None
            self.velocity_x = 0
            self.velocity_y = 0
    
    def move_with_collision(self, dt, walls):
        """Move enemy with wall collision detection"""
        # Try horizontal movement
        old_x = self.rect.x
        self.rect.x += self.velocity_x * dt
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.x = old_x
            self.velocity_x = 0
        
        # Try vertical movement
        old_y = self.rect.y
        self.rect.y += self.velocity_y * dt
        if pygame.sprite.spritecollide(self, walls, False):
            self.rect.y = old_y
            self.velocity_y = 0
    
    def update_shooting_cooldown(self, dt):
        """Update shooting cooldown timer"""
        if self.last_shot_time > 0:
            self.last_shot_time -= dt
    
    def can_shoot(self):
        """Check if enemy can shoot"""
        return self.last_shot_time <= 0 and self.target is not None
    
    def shoot(self):
        """Create a projectile towards the target"""
        if not self.can_shoot():
            return None
        
        self.last_shot_time = self.fire_rate
        
        # Create projectile towards target
        projectile = Projectile(
            self.rect.centerx,
            self.rect.centery,
            self.target.rect.centerx,
            self.target.rect.centery,
            self.damage,
            'enemy',
            self.config['color']
        )
        
        return projectile
    
    def take_damage(self, amount):
        """Take damage and return True if enemy died"""
        self.health -= amount
        self.health = max(0, self.health)
        
        if self.health <= 0:
            self.kill()
            return True
        return False
    
    def get_health_percentage(self):
        """Get health as percentage for UI"""
        return self.health / self.max_health if self.max_health > 0 else 0

def create_random_enemy(x, y, level=1):
    """Create a random enemy based on level"""
    # Weight enemy types based on level
    weights = {
        'normal': 0.4,
        'fast': 0.3,
        'tank': 0.2,
        'archer': 0.1
    }
    
    # Adjust weights based on level
    if level > 3:
        weights['fast'] += 0.1
        weights['archer'] += 0.1
        weights['normal'] -= 0.2
    
    if level > 6:
        weights['tank'] += 0.1
        weights['archer'] += 0.1
        weights['normal'] -= 0.2
    
    # Choose enemy type
    enemy_types = list(weights.keys())
    enemy_weights = list(weights.values())
    enemy_type = random.choices(enemy_types, weights=enemy_weights)[0]
    
    return Enemy(x, y, enemy_type)
