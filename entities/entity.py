import pygame
import os
import logging
from typing import Tuple
from utils.constants import *

# Configure logging for entity module
logger = logging.getLogger(__name__)

class Entity(pygame.sprite.Sprite):
    """Base class for all game entities with improved resource loading and type safety"""

    def __init__(self, x: int, y: int, image_path: str, health: int = 100) -> None:
        """Initialize entity with robust image loading and error handling"""
        super().__init__()

        # Load image with comprehensive error handling
        self.image = self._load_image_safely(image_path)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement
        self.velocity: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.speed: float = 0

        # Health
        self.max_health: int = health
        self.health: int = health

        # Combat
        self.last_shot_time: int = 0
        self.fire_rate: int = 0  # milliseconds between shots
        self.damage: int = 0

    def _load_image_safely(self, image_path: str) -> pygame.Surface:
        """Load image with comprehensive error handling and fallback options"""
        # First, validate the path
        if not image_path:
            logger.warning("Empty image path provided, using fallback")
            return self._create_fallback_image()

        # Check if file exists
        if not os.path.exists(image_path):
            logger.warning(f"Image file not found: {image_path}")
            return self._create_fallback_image()

        # Try to load the image
        try:
            image = pygame.image.load(image_path).convert_alpha()
            logger.debug(f"Successfully loaded image: {image_path}")
            return image
        except pygame.error as e:
            logger.error(f"Pygame error loading image {image_path}: {e}")
            return self._create_fallback_image()
        except Exception as e:
            logger.error(f"Unexpected error loading image {image_path}: {e}")
            return self._create_fallback_image()

    def _create_fallback_image(self, size: Tuple[int, int] = (TILE_SIZE, TILE_SIZE)) -> pygame.Surface:
        """Create a fallback image when the original cannot be loaded"""
        try:
            image = pygame.Surface(size)
            image.fill((255, 0, 255))  # Magenta for missing textures
            # Add a simple pattern to make it more obvious this is a fallback
            pygame.draw.rect(image, (255, 255, 255), (2, 2, size[0]-4, size[1]-4), 2)
            return image
        except Exception as e:
            logger.critical(f"Failed to create fallback image: {e}")
            # Last resort: create minimal surface
            return pygame.Surface((32, 32))

    def move(self, dx: float, dy: float, walls: pygame.sprite.Group) -> None:
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
        self.rect.x += int(dx)
        if hasattr(self, 'collision_rect'):
            self.collision_rect.x += int(dx)

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
        self.rect.y += int(dy)
        if hasattr(self, 'collision_rect'):
            self.collision_rect.y += int(dy)

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

    def take_damage(self, amount: int) -> bool:
        """Reduce health by the given amount"""
        self.health = max(0, self.health - amount)
        if self.health <= 0:
            logger.debug(f"Entity at {self.rect.center} died from {amount} damage")
            self.kill()
            return True  # Entity died
        return False  # Entity still alive

    def heal(self, amount: int) -> None:
        """Increase health by the given amount, up to max_health"""
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        if self.health > old_health:
            logger.debug(f"Entity healed for {self.health - old_health} HP")

    def can_shoot(self) -> bool:
        """Check if enough time has passed to shoot again"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.fire_rate:
            self.last_shot_time = current_time
            return True
        return False

    def update(self) -> None:
        """Update method to be overridden by subclasses"""
        pass

    def draw_health_bar(self, surface: pygame.Surface, offset_x: int = 0, offset_y: int = 0) -> None:
        """Draw a health bar above the entity"""
        if self.health <= 0 or self.health >= self.max_health:
            return  # Don't draw health bar for dead entities or full health

        bar_width = self.rect.width
        bar_height = 5
        x = self.rect.x - offset_x
        y = self.rect.y - offset_y - 10  # 10 pixels above the entity

        # Background (red)
        pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))

        # Foreground (green) - represents current health
        health_width = int(bar_width * (self.health / self.max_health))
        if health_width > 0:
            pygame.draw.rect(surface, GREEN, (x, y, health_width, bar_height))
