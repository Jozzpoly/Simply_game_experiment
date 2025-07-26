"""
Projectile System - Simple Implementation
Handles bullets/projectiles for both player and enemies.
"""

import pygame
import math
from config import *
from utils.constants import distance

class Projectile(pygame.sprite.Sprite):
    """Simple projectile class for bullets and arrows"""
    
    def __init__(self, x, y, target_x, target_y, damage, owner_type='player', color=WHITE):
        super().__init__()
        
        # Create simple projectile surface
        self.image = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Calculate direction to target
        dx = target_x - x
        dy = target_y - y
        distance_to_target = math.sqrt(dx * dx + dy * dy)
        
        if distance_to_target > 0:
            self.velocity_x = (dx / distance_to_target) * PROJECTILE_SPEED
            self.velocity_y = (dy / distance_to_target) * PROJECTILE_SPEED
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
        self.damage = damage
        self.owner_type = owner_type  # 'player' or 'enemy'
        self.lifetime = PROJECTILE_LIFETIME
        self.start_pos = (x, y)
    
    def update(self, dt):
        """Update projectile position and lifetime"""
        # Move projectile
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
        
        # Decrease lifetime
        self.lifetime -= dt
        
        # Remove if lifetime expired or traveled too far
        if self.lifetime <= 0:
            self.kill()
            return
        
        # Remove if traveled too far (safety check)
        current_distance = distance(self.start_pos, self.rect.center)
        if current_distance > SCREEN_WIDTH + SCREEN_HEIGHT:
            self.kill()
    
    def check_wall_collision(self, walls):
        """Check collision with walls and remove projectile if hit"""
        if pygame.sprite.spritecollide(self, walls, False):
            self.kill()
            return True
        return False
