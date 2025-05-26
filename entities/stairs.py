import pygame
import logging
from typing import Optional
from utils.constants import *
from config import (
    STAIRS_UNLOCK_MESSAGE_DURATION,
    REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS,
    ENEMY_DEFEAT_PERCENTAGE_FOR_STAIRS
)

# Configure logging
logger = logging.getLogger(__name__)

class Stairs(pygame.sprite.Sprite):
    """Stairs entity for level progression"""
    
    def __init__(self, x: int, y: int, stair_type: str = "down"):
        """
        Initialize stairs
        
        Args:
            x: X position in pixels
            y: Y position in pixels  
            stair_type: "up" or "down" stairs
        """
        super().__init__()
        self.stair_type = stair_type
        self.is_unlocked = not REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS  # Unlocked by default if no enemy requirement
        self.unlock_message_timer = 0
        
        # Create visual representation
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        if stair_type == "down":
            # Down stairs - darker color with down arrow pattern
            self.image.fill((100, 50, 0))  # Dark brown
            # Draw simple down arrow pattern
            pygame.draw.polygon(self.image, (200, 150, 100), [
                (TILE_SIZE//4, TILE_SIZE//3),
                (3*TILE_SIZE//4, TILE_SIZE//3),
                (TILE_SIZE//2, 2*TILE_SIZE//3)
            ])
        else:
            # Up stairs - lighter color with up arrow pattern  
            self.image.fill((150, 100, 50))  # Light brown
            # Draw simple up arrow pattern
            pygame.draw.polygon(self.image, (255, 200, 150), [
                (TILE_SIZE//2, TILE_SIZE//3),
                (TILE_SIZE//4, 2*TILE_SIZE//3),
                (3*TILE_SIZE//4, 2*TILE_SIZE//3)
            ])
            
        # Add visual indicator if locked
        if not self.is_unlocked:
            # Draw red X over stairs to indicate locked
            pygame.draw.line(self.image, RED, (4, 4), (TILE_SIZE-4, TILE_SIZE-4), 3)
            pygame.draw.line(self.image, RED, (TILE_SIZE-4, 4), (4, TILE_SIZE-4), 3)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        logger.debug(f"Created {stair_type} stairs at ({x}, {y}), unlocked: {self.is_unlocked}")
    
    def update(self, enemies_remaining: int, total_enemies: int) -> None:
        """Update stairs state based on enemy count"""
        if REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS and not self.is_unlocked:
            # Check if enough enemies have been defeated
            enemies_defeated = total_enemies - enemies_remaining
            defeat_percentage = enemies_defeated / total_enemies if total_enemies > 0 else 1.0
            
            if defeat_percentage >= ENEMY_DEFEAT_PERCENTAGE_FOR_STAIRS:
                self.unlock()
        
        # Update unlock message timer
        if self.unlock_message_timer > 0:
            self.unlock_message_timer -= 1
    
    def unlock(self) -> None:
        """Unlock the stairs and update visual"""
        if not self.is_unlocked:
            self.is_unlocked = True
            self.unlock_message_timer = STAIRS_UNLOCK_MESSAGE_DURATION
            
            # Update visual to remove lock indicator
            self._update_visual()
            
            logger.info(f"{self.stair_type.capitalize()} stairs unlocked!")
    
    def _update_visual(self) -> None:
        """Update the visual representation of the stairs"""
        # Recreate the image without the lock indicator
        if self.stair_type == "down":
            self.image.fill((100, 50, 0))  # Dark brown
            pygame.draw.polygon(self.image, (200, 150, 100), [
                (TILE_SIZE//4, TILE_SIZE//3),
                (3*TILE_SIZE//4, TILE_SIZE//3),
                (TILE_SIZE//2, 2*TILE_SIZE//3)
            ])
        else:
            self.image.fill((150, 100, 50))  # Light brown
            pygame.draw.polygon(self.image, (255, 200, 150), [
                (TILE_SIZE//2, TILE_SIZE//3),
                (TILE_SIZE//4, 2*TILE_SIZE//3),
                (3*TILE_SIZE//4, 2*TILE_SIZE//3)
            ])
            
        # Add glowing effect when unlocked
        if self.is_unlocked:
            # Draw golden border to indicate it's usable
            pygame.draw.rect(self.image, YELLOW, self.image.get_rect(), 2)
    
    def can_use(self) -> bool:
        """Check if stairs can be used"""
        return self.is_unlocked
    
    def get_unlock_message(self) -> Optional[str]:
        """Get unlock message if recently unlocked"""
        if self.unlock_message_timer > 0:
            return f"{self.stair_type.capitalize()} stairs unlocked! Find them to proceed to the next level."
        return None
    
    def check_player_interaction(self, player_rect: pygame.Rect) -> bool:
        """Check if player is interacting with stairs"""
        if not self.is_unlocked:
            return False
            
        # Check collision with player
        return self.rect.colliderect(player_rect)
