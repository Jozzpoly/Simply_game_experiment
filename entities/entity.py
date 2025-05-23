import pygame
from utils.constants import *

class Entity(pygame.sprite.Sprite):
    """Base class for all game entities"""

    def __init__(self, x, y, image_path, health=100):
        super().__init__()

        # Load image with error handling
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {image_path}")
            print(f"Error details: {e}")
            # Create a fallback colored rectangle
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 255))  # Magenta for missing textures

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0

        # Health
        self.max_health = health
        self.health = health

        # Combat
        self.last_shot_time = 0
        self.fire_rate = 0  # milliseconds between shots
        self.damage = 0

    def move(self, dx, dy, walls):
        """Move the entity, checking for collisions with walls"""
        # Store original position to revert if needed
        original_x = self.rect.x
        original_y = self.rect.y

        # Store original collision rect position if it exists
        if hasattr(self, 'collision_rect'):
            original_collision_x = self.collision_rect.x
            original_collision_y = self.collision_rect.y

        # Entity may have a custom collision rect (like the player)
        # We'll check for it with hasattr below

        # Move in x direction
        self.rect.x += dx
        if hasattr(self, 'collision_rect'):
            self.collision_rect.x += dx

        # Check for wall collisions in x direction
        if hasattr(self, 'collision_rect'):
            # Use a temporary sprite for collision detection with the smaller rect
            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = self.collision_rect
            wall_hit_list = pygame.sprite.spritecollide(temp_sprite, walls, False)
        else:
            wall_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for wall in wall_hit_list:
            if dx > 0:  # Moving right
                if hasattr(self, 'collision_rect'):
                    offset = self.rect.right - self.collision_rect.right
                    self.rect.right = wall.rect.left + offset
                    self.collision_rect.right = wall.rect.left
                else:
                    self.rect.right = wall.rect.left
            else:  # Moving left
                if hasattr(self, 'collision_rect'):
                    offset = self.collision_rect.left - self.rect.left
                    self.rect.left = wall.rect.right - offset
                    self.collision_rect.left = wall.rect.right
                else:
                    self.rect.left = wall.rect.right

        # Move in y direction
        self.rect.y += dy
        if hasattr(self, 'collision_rect'):
            self.collision_rect.y += dy

        # Check for wall collisions in y direction
        if hasattr(self, 'collision_rect'):
            temp_sprite.rect = self.collision_rect
            wall_hit_list = pygame.sprite.spritecollide(temp_sprite, walls, False)
        else:
            wall_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for wall in wall_hit_list:
            if dy > 0:  # Moving down
                if hasattr(self, 'collision_rect'):
                    offset = self.rect.bottom - self.collision_rect.bottom
                    self.rect.bottom = wall.rect.top + offset
                    self.collision_rect.bottom = wall.rect.top
                else:
                    self.rect.bottom = wall.rect.top
            else:  # Moving up
                if hasattr(self, 'collision_rect'):
                    offset = self.collision_rect.top - self.rect.top
                    self.rect.top = wall.rect.bottom - offset
                    self.collision_rect.top = wall.rect.bottom
                else:
                    self.rect.top = wall.rect.bottom

        # If we're still stuck in a wall after both movements, revert to original position
        if hasattr(self, 'collision_rect'):
            temp_sprite.rect = self.collision_rect
            if pygame.sprite.spritecollideany(temp_sprite, walls):
                self.rect.x = original_x
                self.rect.y = original_y
                self.collision_rect.x = original_collision_x
                self.collision_rect.y = original_collision_y
        else:
            if pygame.sprite.spritecollideany(self, walls):
                self.rect.x = original_x
                self.rect.y = original_y

    def take_damage(self, amount):
        """Reduce health by the given amount"""
        self.health -= amount
        if self.health <= 0:
            self.kill()
            return True  # Entity died
        return False  # Entity still alive

    def heal(self, amount):
        """Increase health by the given amount, up to max_health"""
        self.health = min(self.health + amount, self.max_health)

    def can_shoot(self):
        """Check if enough time has passed to shoot again"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.fire_rate:
            self.last_shot_time = current_time
            return True
        return False

    def update(self):
        """Update method to be overridden by subclasses"""
        pass

    def draw_health_bar(self, surface, offset_x=0, offset_y=0):
        """Draw a health bar above the entity"""
        bar_width = self.rect.width
        bar_height = 5
        x = self.rect.x - offset_x
        y = self.rect.y - offset_y - 10  # 10 pixels above the entity

        # Background (red)
        pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))

        # Foreground (green) - represents current health
        health_width = int(bar_width * (self.health / self.max_health))
        pygame.draw.rect(surface, GREEN, (x, y, health_width, bar_height))
