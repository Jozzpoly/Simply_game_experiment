"""
Environmental entities for hazards and special features.

This module contains sprite classes for environmental hazards and special features
that can be placed in levels and interact with players and enemies.
"""

import pygame
import random
import logging
from typing import Dict, Any, Optional
from utils.constants import *
from config import *

logger = logging.getLogger(__name__)


class EnvironmentalHazardSprite(pygame.sprite.Sprite):
    """Sprite class for environmental hazards that can damage entities"""
    
    def __init__(self, hazard_type: str, x: int, y: int):
        super().__init__()
        self.hazard_type = hazard_type
        self.config = ENVIRONMENTAL_HAZARDS.get(hazard_type, {})
        
        # Create visual representation
        self.image = self._create_hazard_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Hazard properties
        self.active = True
        self.last_trigger_time = 0
        self.affected_entities = set()
        self.damage = self.config.get('damage', 0)
        self.cooldown = self.config.get('cooldown', 1000)
        self.visual_warning = self.config.get('visual_warning', False)
        
        # Animation properties
        self.animation_timer = 0
        self.warning_active = False
        
    def _create_hazard_image(self) -> pygame.Surface:
        """Create visual representation for the hazard"""
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        if self.hazard_type == 'spike_trap':
            # Gray base with dark spikes
            pygame.draw.rect(surface, (100, 100, 100), (0, 0, TILE_SIZE, TILE_SIZE))
            # Draw spikes
            for i in range(4):
                for j in range(4):
                    x = i * 8 + 4
                    y = j * 8 + 4
                    pygame.draw.polygon(surface, (60, 60, 60), 
                                      [(x, y+6), (x+3, y), (x+6, y+6)])
                                      
        elif self.hazard_type == 'poison_gas':
            # Green translucent cloud
            pygame.draw.circle(surface, (0, 255, 0, 100), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            pygame.draw.circle(surface, (0, 200, 0, 80), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2)
                             
        elif self.hazard_type == 'lava_pool':
            # Red-orange lava with bubbles
            pygame.draw.rect(surface, (255, 69, 0), (0, 0, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, (255, 140, 0), (2, 2, TILE_SIZE-4, TILE_SIZE-4))
            # Add bubbles
            for _ in range(5):
                x = random.randint(4, TILE_SIZE-4)
                y = random.randint(4, TILE_SIZE-4)
                pygame.draw.circle(surface, (255, 200, 0), (x, y), 2)
                
        elif self.hazard_type == 'thorn_bush':
            # Dark green bush with thorns
            pygame.draw.circle(surface, (0, 100, 0), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            # Add thorns
            for _ in range(8):
                angle = random.random() * 6.28
                x = int(TILE_SIZE//2 + 12 * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
                y = int(TILE_SIZE//2 + 12 * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
                pygame.draw.circle(surface, (139, 69, 19), (x, y), 2)
                
        elif self.hazard_type == 'quicksand':
            # Brown swirling pattern
            pygame.draw.rect(surface, (160, 82, 45), (0, 0, TILE_SIZE, TILE_SIZE))
            pygame.draw.circle(surface, (139, 69, 19), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
                             
        elif self.hazard_type == 'crystal_shard':
            # Purple crystal formation
            points = [(TILE_SIZE//2, 4), (TILE_SIZE-4, TILE_SIZE//2), 
                     (TILE_SIZE//2, TILE_SIZE-4), (4, TILE_SIZE//2)]
            pygame.draw.polygon(surface, (147, 112, 219), points)
            pygame.draw.polygon(surface, (138, 43, 226), points, 2)
            
        elif self.hazard_type == 'cursed_ground':
            # Dark purple with mystical symbols
            pygame.draw.rect(surface, (75, 0, 130), (0, 0, TILE_SIZE, TILE_SIZE))
            # Add mystical runes
            pygame.draw.circle(surface, (148, 0, 211), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4, 2)
                             
        else:
            # Default hazard appearance
            pygame.draw.rect(surface, (255, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE))
            
        return surface
        
    def update(self, dt: float = 1.0/60.0) -> None:
        """Update hazard state and animations"""
        current_time = pygame.time.get_ticks()
        
        # Handle cooldown
        if current_time - self.last_trigger_time >= self.cooldown:
            self.active = True
            
        # Update animation
        self.animation_timer += dt * 1000  # Convert to ms
        
        # Handle warning animation for hazards with visual warnings
        if self.visual_warning and self.hazard_type == 'falling_rocks':
            warning_duration = self.config.get('warning_time', 1000)
            if self.animation_timer % (warning_duration * 2) < warning_duration:
                self.warning_active = True
            else:
                self.warning_active = False
                
    def trigger(self, entity) -> bool:
        """Trigger hazard effect on entity"""
        if not self.active:
            return False
            
        current_time = pygame.time.get_ticks()
        entity_id = id(entity)
        
        # Check if entity is already affected (for continuous hazards)
        if entity_id in self.affected_entities:
            return False
            
        # Apply damage if entity has take_damage method
        if hasattr(entity, 'take_damage') and self.damage > 0:
            entity.take_damage(self.damage)
            
        # Apply special effects based on hazard type
        if self.hazard_type == 'thorn_bush' and hasattr(entity, 'apply_slow'):
            entity.apply_slow(self.config.get('slow_effect', 0.5), 
                            self.config.get('duration', 1500))
        elif self.hazard_type == 'quicksand' and hasattr(entity, 'apply_slow'):
            entity.apply_slow(self.config.get('slow_effect', 0.2), 0)
        elif self.hazard_type == 'crystal_shard' and hasattr(entity, 'apply_knockback'):
            entity.apply_knockback(self.config.get('knockback', 50))
            
        # Set cooldown
        self.last_trigger_time = current_time
        self.active = False
        
        # Add to affected entities for continuous hazards
        if self.hazard_type in ['poison_gas', 'lava_pool', 'cursed_ground']:
            self.affected_entities.add(entity_id)
            
        return True
        
    def draw_warning(self, surface: pygame.Surface, camera_offset_x: float, camera_offset_y: float) -> None:
        """Draw warning indicator for hazards with visual warnings"""
        if self.visual_warning and self.warning_active:
            screen_x = self.rect.x - camera_offset_x
            screen_y = self.rect.y - camera_offset_y
            
            # Draw flashing red outline
            warning_rect = pygame.Rect(screen_x - 2, screen_y - 2, 
                                     TILE_SIZE + 4, TILE_SIZE + 4)
            pygame.draw.rect(surface, (255, 0, 0), warning_rect, 3)


class SpecialFeatureSprite(pygame.sprite.Sprite):
    """Sprite class for special environmental features that provide benefits"""
    
    def __init__(self, feature_type: str, x: int, y: int):
        super().__init__()
        self.feature_type = feature_type
        self.config = SPECIAL_FEATURES.get(feature_type, {})
        
        # Create visual representation
        self.image = self._create_feature_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Feature properties
        self.active = True
        self.discovered = False
        self.used = False
        self.interaction_cooldown = 0
        
        # Animation properties
        self.animation_timer = 0
        self.glow_intensity = 0
        
    def _create_feature_image(self) -> pygame.Surface:
        """Create visual representation for the feature"""
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        
        if self.feature_type == 'secret_door':
            # Stone wall with subtle markings (only visible when discovered)
            pygame.draw.rect(surface, (105, 105, 105), (0, 0, TILE_SIZE, TILE_SIZE))
            if self.discovered:
                pygame.draw.rect(surface, (139, 69, 19), (4, 4, TILE_SIZE-8, TILE_SIZE-8))
                
        elif self.feature_type == 'treasure_alcove':
            # Golden alcove with treasure
            pygame.draw.rect(surface, (255, 215, 0), (0, 0, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, (255, 255, 0), (4, 4, TILE_SIZE-8, TILE_SIZE-8))
            # Add treasure chest
            pygame.draw.rect(surface, (139, 69, 19), (8, 12, 16, 12))
            pygame.draw.rect(surface, (255, 215, 0), (10, 14, 12, 8))
            
        elif self.feature_type == 'hidden_grove':
            # Lush green area with healing aura
            pygame.draw.circle(surface, (0, 255, 0), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2)
            pygame.draw.circle(surface, (144, 238, 144), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
            # Add sparkles
            for _ in range(6):
                x = random.randint(4, TILE_SIZE-4)
                y = random.randint(4, TILE_SIZE-4)
                pygame.draw.circle(surface, (255, 255, 255), (x, y), 1)
                
        elif self.feature_type == 'crystal_formation':
            # Blue crystal with energy
            points = [(TILE_SIZE//2, 2), (TILE_SIZE-2, TILE_SIZE//2), 
                     (TILE_SIZE//2, TILE_SIZE-2), (2, TILE_SIZE//2)]
            pygame.draw.polygon(surface, (0, 191, 255), points)
            pygame.draw.polygon(surface, (135, 206, 235), points, 3)
            
        elif self.feature_type == 'runic_circle':
            # Mystical circle with runes
            pygame.draw.circle(surface, (138, 43, 226), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2, 3)
            pygame.draw.circle(surface, (75, 0, 130), 
                             (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3, 2)
            # Add inner symbols
            for i in range(4):
                angle = i * 1.57  # 90 degrees in radians
                x = int(TILE_SIZE//2 + 8 * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
                y = int(TILE_SIZE//2 + 8 * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
                pygame.draw.circle(surface, (148, 0, 211), (x, y), 2)
                
        elif self.feature_type == 'power_crystal':
            # Red energy crystal
            points = [(TILE_SIZE//2, 4), (TILE_SIZE-4, TILE_SIZE//2), 
                     (TILE_SIZE//2, TILE_SIZE-4), (4, TILE_SIZE//2)]
            pygame.draw.polygon(surface, (255, 0, 0), points)
            pygame.draw.polygon(surface, (255, 69, 0), points, 2)
            
        elif self.feature_type == 'ancient_tomb':
            # Dark stone tomb
            pygame.draw.rect(surface, (64, 64, 64), (0, 0, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(surface, (105, 105, 105), (2, 2, TILE_SIZE-4, TILE_SIZE-4))
            # Add cross or symbol
            pygame.draw.line(surface, (139, 69, 19), 
                           (TILE_SIZE//2, 6), (TILE_SIZE//2, TILE_SIZE-6), 3)
            pygame.draw.line(surface, (139, 69, 19), 
                           (6, TILE_SIZE//2), (TILE_SIZE-6, TILE_SIZE//2), 3)
                           
        else:
            # Default feature appearance
            pygame.draw.rect(surface, (0, 255, 255), (0, 0, TILE_SIZE, TILE_SIZE))
            
        return surface
        
    def update(self, dt: float = 1.0/60.0) -> None:
        """Update feature state and animations"""
        self.animation_timer += dt * 1000  # Convert to ms
        
        # Update glow effect for active features
        if self.active and not self.used:
            self.glow_intensity = (pygame.math.Vector2(1, 0).rotate_rad(
                self.animation_timer * 0.005).x + 1) * 0.5
                
        # Handle interaction cooldown
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= dt * 1000
            
    def interact(self, entity) -> bool:
        """Interact with the special feature"""
        if not self.active or self.used or self.interaction_cooldown > 0:
            return False
            
        # Handle discovery for secret features
        if self.feature_type == 'secret_door' and not self.discovered:
            discovery_chance = self.config.get('discovery_chance', 0.3)
            if random.random() < discovery_chance:
                self.discovered = True
                return True
            return False
            
        # Apply feature effects
        success = False
        
        if self.feature_type == 'treasure_alcove':
            # Give treasure (handled by game logic)
            success = True
            self.used = True
            
        elif self.feature_type == 'hidden_grove':
            # Healing effect
            if hasattr(entity, 'heal'):
                heal_amount = self.config.get('healing_rate', 2)
                entity.heal(heal_amount)
                success = True
                
        elif self.feature_type == 'crystal_formation':
            # Mana boost (if entity has mana)
            if hasattr(entity, 'mana'):
                mana_boost = self.config.get('mana_boost', 50)
                entity.mana = min(entity.max_mana, entity.mana + mana_boost)
                success = True
                self.used = True
                
        elif self.feature_type == 'power_crystal':
            # Damage boost
            if hasattr(entity, 'apply_damage_boost'):
                boost = self.config.get('damage_boost', 1.5)
                duration = self.config.get('duration', 20000)
                entity.apply_damage_boost(boost, duration)
                success = True
                self.used = True
                
        # Set interaction cooldown
        if success:
            self.interaction_cooldown = 1000  # 1 second cooldown
            
        return success
        
    def draw_glow(self, surface: pygame.Surface, camera_offset_x: float, camera_offset_y: float) -> None:
        """Draw glow effect for active features"""
        if self.active and not self.used and self.glow_intensity > 0:
            screen_x = self.rect.x - camera_offset_x
            screen_y = self.rect.y - camera_offset_y
            
            # Draw glow effect
            glow_color = (255, 255, 255, int(self.glow_intensity * 100))
            glow_rect = pygame.Rect(screen_x - 2, screen_y - 2, 
                                  TILE_SIZE + 4, TILE_SIZE + 4)
            
            # Create glow surface
            glow_surface = pygame.Surface((TILE_SIZE + 4, TILE_SIZE + 4), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, 
                           (0, 0, TILE_SIZE + 4, TILE_SIZE + 4), 2)
            surface.blit(glow_surface, (screen_x - 2, screen_y - 2))
