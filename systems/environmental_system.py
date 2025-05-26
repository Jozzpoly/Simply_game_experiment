"""
Environmental System for managing hazards, special features, and weather effects.

This module handles environmental interactions, hazards, special features,
and dynamic weather systems that affect gameplay.
"""

import pygame
import random
import time
import logging
from typing import Dict, List, Optional, Tuple, Any
from config import *
from utils.constants import *

logger = logging.getLogger(__name__)


class EnvironmentalHazard:
    """Represents an environmental hazard that can affect players and enemies"""
    
    def __init__(self, hazard_type: str, x: int, y: int, config: Dict[str, Any]):
        self.hazard_type = hazard_type
        self.x = x
        self.y = y
        self.config = config
        self.active = True
        self.last_trigger_time = 0
        self.affected_entities = set()
        
        # Create collision rect
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        
        # Visual and effect properties
        self.visual_effect = config.get('visual_effect', None)
        self.damage = config.get('damage', 0)
        self.duration = config.get('duration', 0)
        self.cooldown = config.get('cooldown', 1000)
        
    def update(self, dt: float) -> None:
        """Update hazard state"""
        current_time = pygame.time.get_ticks()
        
        # Handle cooldown
        if current_time - self.last_trigger_time >= self.cooldown:
            self.active = True
            
    def trigger(self, entity) -> bool:
        """Trigger hazard effect on entity"""
        if not self.active:
            return False
            
        current_time = pygame.time.get_ticks()
        entity_id = id(entity)
        
        # Check if entity is already affected (for continuous hazards)
        if entity_id in self.affected_entities:
            return False
            
        # Apply hazard effect based on type
        if self.hazard_type == 'spike_trap':
            return self._trigger_spike_trap(entity)
        elif self.hazard_type == 'poison_gas':
            return self._trigger_poison_gas(entity)
        elif self.hazard_type == 'lava_pool':
            return self._trigger_lava_pool(entity)
        elif self.hazard_type == 'thorn_bush':
            return self._trigger_thorn_bush(entity)
        elif self.hazard_type == 'quicksand':
            return self._trigger_quicksand(entity)
        elif self.hazard_type == 'falling_rocks':
            return self._trigger_falling_rocks(entity)
        elif self.hazard_type == 'crystal_shard':
            return self._trigger_crystal_shard(entity)
        elif self.hazard_type == 'cursed_ground':
            return self._trigger_cursed_ground(entity)
            
        return False
        
    def _trigger_spike_trap(self, entity) -> bool:
        """Trigger spike trap hazard"""
        if random.random() < self.config['trigger_chance']:
            if hasattr(entity, 'take_damage'):
                entity.take_damage(self.damage)
            self.last_trigger_time = pygame.time.get_ticks()
            self.active = False
            return True
        return False
        
    def _trigger_poison_gas(self, entity) -> bool:
        """Trigger poison gas hazard"""
        if hasattr(entity, 'apply_status_effect'):
            entity.apply_status_effect('poison', self.damage, self.duration)
        elif hasattr(entity, 'take_damage'):
            entity.take_damage(self.damage)
        self.affected_entities.add(id(entity))
        return True
        
    def _trigger_lava_pool(self, entity) -> bool:
        """Trigger lava pool hazard"""
        if hasattr(entity, 'take_damage'):
            entity.take_damage(self.damage)
        return True
        
    def _trigger_thorn_bush(self, entity) -> bool:
        """Trigger thorn bush hazard"""
        if hasattr(entity, 'take_damage'):
            entity.take_damage(self.damage)
        if hasattr(entity, 'apply_slow'):
            entity.apply_slow(self.config['slow_effect'], self.duration)
        return True
        
    def _trigger_quicksand(self, entity) -> bool:
        """Trigger quicksand hazard"""
        if hasattr(entity, 'apply_slow'):
            entity.apply_slow(self.config['slow_effect'], 0)  # Continuous until escaped
        return True
        
    def _trigger_falling_rocks(self, entity) -> bool:
        """Trigger falling rocks hazard"""
        if hasattr(entity, 'take_damage'):
            entity.take_damage(self.damage)
        return True
        
    def _trigger_crystal_shard(self, entity) -> bool:
        """Trigger crystal shard hazard"""
        if hasattr(entity, 'take_damage'):
            entity.take_damage(self.damage)
        if hasattr(entity, 'apply_knockback'):
            entity.apply_knockback(self.config['knockback'])
        return True
        
    def _trigger_cursed_ground(self, entity) -> bool:
        """Trigger cursed ground hazard"""
        if hasattr(entity, 'take_damage'):
            entity.take_damage(self.damage)
        if hasattr(entity, 'drain_mana'):
            entity.drain_mana(self.config['mana_drain'])
        return True


class SpecialFeature:
    """Represents a special environmental feature that provides benefits"""
    
    def __init__(self, feature_type: str, x: int, y: int, config: Dict[str, Any]):
        self.feature_type = feature_type
        self.x = x
        self.y = y
        self.config = config
        self.active = True
        self.discovered = False
        self.used = False
        
        # Create collision rect
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        
    def interact(self, entity) -> bool:
        """Interact with the special feature"""
        if not self.active or self.used:
            return False
            
        if self.feature_type == 'secret_door':
            return self._interact_secret_door(entity)
        elif self.feature_type == 'treasure_alcove':
            return self._interact_treasure_alcove(entity)
        elif self.feature_type == 'hidden_grove':
            return self._interact_hidden_grove(entity)
        elif self.feature_type == 'crystal_formation':
            return self._interact_crystal_formation(entity)
        elif self.feature_type == 'runic_circle':
            return self._interact_runic_circle(entity)
        elif self.feature_type == 'power_crystal':
            return self._interact_power_crystal(entity)
        elif self.feature_type == 'ancient_tomb':
            return self._interact_ancient_tomb(entity)
            
        return False
        
    def _interact_secret_door(self, entity) -> bool:
        """Interact with secret door"""
        if not self.discovered:
            if random.random() < self.config['discovery_chance']:
                self.discovered = True
                return True
        return False
        
    def _interact_treasure_alcove(self, entity) -> bool:
        """Interact with treasure alcove"""
        if hasattr(entity, 'add_treasure'):
            entity.add_treasure(self.config['loot_multiplier'], self.config['rare_item_chance'])
        self.used = True
        return True
        
    def _interact_hidden_grove(self, entity) -> bool:
        """Interact with hidden grove"""
        if hasattr(entity, 'heal'):
            entity.heal(self.config['healing_rate'])
        if hasattr(entity, 'restore_mana'):
            entity.restore_mana(self.config['mana_regen'])
        return True
        
    def _interact_crystal_formation(self, entity) -> bool:
        """Interact with crystal formation"""
        if hasattr(entity, 'boost_mana'):
            entity.boost_mana(self.config['mana_boost'])
        if hasattr(entity, 'apply_temporary_power'):
            entity.apply_temporary_power('crystal_power', self.config['duration'])
        self.used = True
        return True
        
    def _interact_runic_circle(self, entity) -> bool:
        """Interact with runic circle"""
        if hasattr(entity, 'teleport'):
            entity.teleport(self.config['teleport_destination'])
        return True
        
    def _interact_power_crystal(self, entity) -> bool:
        """Interact with power crystal"""
        if hasattr(entity, 'apply_damage_boost'):
            entity.apply_damage_boost(self.config['damage_boost'], self.config['duration'])
        self.used = True
        return True
        
    def _interact_ancient_tomb(self, entity) -> bool:
        """Interact with ancient tomb"""
        # Chance to spawn undead
        if random.random() < self.config['undead_spawn_chance']:
            # Signal to spawn undead enemies
            return False
            
        # Give treasure
        if hasattr(entity, 'add_epic_treasure'):
            entity.add_epic_treasure()
            
        # Chance for curse
        if random.random() < self.config['curse_chance']:
            if hasattr(entity, 'apply_curse'):
                entity.apply_curse()
                
        self.used = True
        return True


class WeatherSystem:
    """Manages dynamic weather effects"""
    
    def __init__(self):
        self.enabled = WEATHER_SYSTEM_ENABLED
        self.current_weather = 'clear'
        self.weather_timer = 0
        self.transition_timer = 0
        self.transitioning = False
        self.next_weather = None
        
    def update(self, dt: float) -> None:
        """Update weather system"""
        if not self.enabled:
            return
            
        self.weather_timer += dt * 1000  # Convert to ms
        
        if self.transitioning:
            self.transition_timer += dt * 1000
            if self.transition_timer >= WEATHER_TRANSITION_TIME:
                self.current_weather = self.next_weather
                self.transitioning = False
                self.transition_timer = 0
                self.weather_timer = 0
        elif self.weather_timer >= WEATHER_CHANGE_INTERVAL:
            self._change_weather()
            
    def _change_weather(self) -> None:
        """Change to a new weather type"""
        weather_types = list(WEATHER_TYPES.keys())
        weights = [WEATHER_TYPES[w]['spawn_rate'] for w in weather_types]
        
        # Choose new weather (different from current)
        available_weather = [w for w in weather_types if w != self.current_weather]
        available_weights = [WEATHER_TYPES[w]['spawn_rate'] for w in available_weather]
        
        if available_weather:
            self.next_weather = random.choices(available_weather, weights=available_weights)[0]
            self.transitioning = True
            self.transition_timer = 0
            
    def get_current_effects(self) -> Dict[str, float]:
        """Get current weather effects"""
        if not self.enabled:
            return {'visibility': 1.0, 'movement_modifier': 1.0}
            
        return WEATHER_TYPES.get(self.current_weather, WEATHER_TYPES['clear'])
        
    def force_weather(self, weather_type: str) -> None:
        """Force a specific weather type"""
        if weather_type in WEATHER_TYPES:
            self.current_weather = weather_type
            self.weather_timer = 0
            self.transitioning = False


class EnvironmentalManager:
    """Main manager for all environmental systems"""
    
    def __init__(self):
        self.hazards: List[EnvironmentalHazard] = []
        self.special_features: List[SpecialFeature] = []
        self.weather_system = WeatherSystem()
        
    def add_hazard(self, hazard_type: str, x: int, y: int) -> None:
        """Add an environmental hazard"""
        if hazard_type in ENVIRONMENTAL_HAZARDS:
            config = ENVIRONMENTAL_HAZARDS[hazard_type]
            hazard = EnvironmentalHazard(hazard_type, x, y, config)
            self.hazards.append(hazard)
            
    def add_special_feature(self, feature_type: str, x: int, y: int) -> None:
        """Add a special feature"""
        if feature_type in SPECIAL_FEATURES:
            config = SPECIAL_FEATURES[feature_type]
            feature = SpecialFeature(feature_type, x, y, config)
            self.special_features.append(feature)
            
    def update(self, dt: float) -> None:
        """Update all environmental systems"""
        # Update hazards
        for hazard in self.hazards:
            hazard.update(dt)
            
        # Update weather
        self.weather_system.update(dt)
        
    def check_entity_interactions(self, entity) -> List[str]:
        """Check for entity interactions with environmental elements"""
        interactions = []
        
        # Check hazard collisions
        for hazard in self.hazards:
            if hazard.rect.colliderect(entity.rect):
                if hazard.trigger(entity):
                    interactions.append(f"hazard_{hazard.hazard_type}")
                    
        # Check special feature interactions
        for feature in self.special_features:
            if feature.rect.colliderect(entity.rect):
                if feature.interact(entity):
                    interactions.append(f"feature_{feature.feature_type}")
                    
        return interactions
        
    def get_weather_effects(self) -> Dict[str, float]:
        """Get current weather effects"""
        return self.weather_system.get_current_effects()
        
    def clear_all(self) -> None:
        """Clear all environmental elements"""
        self.hazards.clear()
        self.special_features.clear()
