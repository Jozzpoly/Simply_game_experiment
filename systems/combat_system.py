"""
Enhanced Combat System for Phase 2

This module handles:
- Elemental damage types (fire, ice, lightning, poison, dark, holy)
- Status effects and damage over time
- Combo system for skill synergies
- Tactical positioning mechanics
- Advanced damage calculations
"""

import pygame
import random
import math
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from config import *
from utils.constants import *

logger = logging.getLogger(__name__)


class StatusEffect:
    """Represents a status effect applied to an entity"""
    
    def __init__(self, effect_type: str, duration: int, source=None, **kwargs):
        self.effect_type = effect_type
        self.duration = duration
        self.max_duration = duration
        self.source = source
        
        # Get effect configuration
        self.config = STATUS_EFFECTS.get(effect_type, {})
        
        # Effect properties
        self.damage_per_tick = self.config.get('damage_per_tick', 0)
        self.tick_interval = self.config.get('tick_interval', 1000)
        self.movement_multiplier = self.config.get('movement_multiplier', 1.0)
        self.attack_speed_multiplier = self.config.get('attack_speed_multiplier', 1.0)
        self.damage_multiplier = self.config.get('damage_multiplier', 1.0)
        self.healing_multiplier = self.config.get('healing_multiplier', 1.0)
        self.visual_effect = self.config.get('visual_effect', '')
        self.stackable = self.config.get('stackable', False)
        self.max_stacks = self.config.get('max_stacks', 1)
        
        # Stacking properties
        self.stacks = kwargs.get('stacks', 1)
        
        # Timing
        self.last_tick_time = pygame.time.get_ticks()
        
    def update(self, entity) -> bool:
        """Update status effect. Returns True if effect should be removed"""
        current_time = pygame.time.get_ticks()
        
        # Decrease duration
        self.duration -= 1
        
        # Apply damage over time effects
        if (self.damage_per_tick > 0 and 
            current_time - self.last_tick_time >= self.tick_interval):
            
            total_damage = self.damage_per_tick * self.stacks
            if hasattr(entity, 'take_damage'):
                entity.take_damage(total_damage)
            self.last_tick_time = current_time
            
        # Return True if effect should be removed
        return self.duration <= 0
        
    def get_movement_modifier(self) -> float:
        """Get movement speed modifier"""
        if self.stackable:
            # Diminishing returns for stackable effects
            stack_modifier = 1.0 - (1.0 - self.movement_multiplier) * min(self.stacks, self.max_stacks) / self.max_stacks
            return stack_modifier
        return self.movement_multiplier
        
    def get_attack_speed_modifier(self) -> float:
        """Get attack speed modifier"""
        if self.stackable:
            stack_modifier = 1.0 - (1.0 - self.attack_speed_multiplier) * min(self.stacks, self.max_stacks) / self.max_stacks
            return stack_modifier
        return self.attack_speed_multiplier
        
    def get_damage_modifier(self) -> float:
        """Get damage taken modifier"""
        return self.damage_multiplier
        
    def get_healing_modifier(self) -> float:
        """Get healing received modifier"""
        return self.healing_multiplier


class ElementalDamage:
    """Handles elemental damage calculations and effects"""
    
    @staticmethod
    def calculate_damage(base_damage: float, element_type: str, target=None) -> Tuple[float, List[str]]:
        """Calculate elemental damage and return damage + status effects to apply"""
        if element_type not in ELEMENTAL_DAMAGE_TYPES:
            return base_damage, []
            
        element_config = ELEMENTAL_DAMAGE_TYPES[element_type]
        
        # Apply elemental damage multiplier
        final_damage = base_damage * element_config['damage_multiplier']
        
        # Determine status effects to apply
        status_effects = element_config.get('status_effects', [])
        
        # Special elemental effects
        if element_type == 'holy' and hasattr(target, 'enemy_type'):
            # Holy damage bonus against undead
            if target.enemy_type in ['necromancer', 'shadow']:
                final_damage *= element_config.get('undead_bonus', 2.0)
                
        return final_damage, status_effects
        
    @staticmethod
    def get_element_color(element_type: str) -> Tuple[int, int, int]:
        """Get color for elemental damage visualization"""
        return ELEMENTAL_DAMAGE_TYPES.get(element_type, {}).get('color', (255, 255, 255))
        
    @staticmethod
    def get_particle_effect(element_type: str) -> str:
        """Get particle effect name for elemental damage"""
        return ELEMENTAL_DAMAGE_TYPES.get(element_type, {}).get('particle_effect', 'impact')


class ComboSystem:
    """Handles combo attacks and skill synergies"""
    
    def __init__(self):
        self.enabled = COMBO_SYSTEM_ENABLED
        self.combo_window = COMBO_WINDOW
        self.damage_multiplier = COMBO_DAMAGE_MULTIPLIER
        self.max_chain = MAX_COMBO_CHAIN
        
        # Combo tracking
        self.current_combo = []
        self.last_action_time = 0
        self.combo_count = 0
        
    def add_action(self, action: str, timestamp: int = None) -> bool:
        """Add an action to the combo chain"""
        if not self.enabled:
            return False
            
        if timestamp is None:
            timestamp = pygame.time.get_ticks()
            
        # Check if within combo window
        if timestamp - self.last_action_time > self.combo_window:
            self.reset_combo()
            
        # Add action to combo
        self.current_combo.append(action)
        self.last_action_time = timestamp
        
        # Check for valid combo
        if len(self.current_combo) >= 2:
            combo_bonus = self._check_combo_validity()
            if combo_bonus > 0:
                self.combo_count += 1
                return True
                
        # Reset if combo is too long
        if len(self.current_combo) >= self.max_chain:
            self.reset_combo()
            
        return False
        
    def _check_combo_validity(self) -> float:
        """Check if current combo is valid and return damage bonus"""
        # Define valid combo patterns
        valid_combos = {
            ('attack', 'special'): 1.2,
            ('special', 'attack'): 1.3,
            ('attack', 'attack', 'special'): 1.5,
            ('special', 'special'): 1.4,
            ('dash', 'attack'): 1.3,
            ('block', 'attack'): 1.25
        }
        
        # Check for matching patterns
        combo_tuple = tuple(self.current_combo[-len(self.current_combo):])
        for pattern, bonus in valid_combos.items():
            if len(combo_tuple) >= len(pattern):
                if combo_tuple[-len(pattern):] == pattern:
                    return bonus
                    
        return 0
        
    def get_combo_multiplier(self) -> float:
        """Get current combo damage multiplier"""
        if self.combo_count == 0:
            return 1.0
            
        # Increasing bonus with combo count
        base_multiplier = self.damage_multiplier
        combo_bonus = 1.0 + (self.combo_count * 0.1)  # 10% per combo
        return min(base_multiplier * combo_bonus, 3.0)  # Cap at 3x damage
        
    def reset_combo(self) -> None:
        """Reset the combo chain"""
        self.current_combo.clear()
        self.combo_count = 0
        self.last_action_time = 0


class TacticalPositioning:
    """Handles tactical positioning mechanics"""
    
    @staticmethod
    def calculate_positional_bonus(attacker_pos: Tuple[float, float], 
                                 target_pos: Tuple[float, float],
                                 target_facing: float = 0) -> float:
        """Calculate damage bonus based on positioning"""
        # Calculate angle between attacker and target
        dx = attacker_pos[0] - target_pos[0]
        dy = attacker_pos[1] - target_pos[1]
        attack_angle = math.atan2(dy, dx)
        
        # Calculate relative angle (0 = front, π = back)
        relative_angle = abs(attack_angle - target_facing)
        if relative_angle > math.pi:
            relative_angle = 2 * math.pi - relative_angle
            
        # Flanking bonus (attacking from behind)
        if relative_angle > math.pi * 0.75:  # Within 45 degrees of back
            return FLANKING_DAMAGE_BONUS
        elif relative_angle > math.pi * 0.5:  # Side attack
            return 1.1  # 10% bonus for side attacks
            
        return 1.0  # No bonus for frontal attacks
        
    @staticmethod
    def check_cover(entity_pos: Tuple[float, float], 
                   attacker_pos: Tuple[float, float],
                   walls: pygame.sprite.Group) -> bool:
        """Check if entity has cover from attacker"""
        # Simple line-of-sight check
        # This is a simplified version - could be enhanced with raycasting
        
        # Calculate distance
        distance = math.sqrt((entity_pos[0] - attacker_pos[0])**2 + 
                           (entity_pos[1] - attacker_pos[1])**2)
        
        # Check for walls between positions (simplified)
        steps = int(distance / 10)  # Check every 10 pixels
        if steps == 0:
            return False
            
        dx = (entity_pos[0] - attacker_pos[0]) / steps
        dy = (entity_pos[1] - attacker_pos[1]) / steps
        
        for i in range(1, steps):
            check_x = attacker_pos[0] + dx * i
            check_y = attacker_pos[1] + dy * i
            
            # Check if this position intersects with any wall
            check_rect = pygame.Rect(check_x - 5, check_y - 5, 10, 10)
            for wall in walls:
                if wall.rect.colliderect(check_rect):
                    return True
                    
        return False
        
    @staticmethod
    def get_cover_damage_reduction() -> float:
        """Get damage reduction when behind cover"""
        return COVER_DAMAGE_REDUCTION


class CombatManager:
    """Main combat system manager"""
    
    def __init__(self):
        self.combo_system = ComboSystem()
        self.active_status_effects = {}  # entity_id -> list of status effects
        
    def apply_damage(self, attacker, target, base_damage: float, 
                    element_type: str = "physical", 
                    walls: pygame.sprite.Group = None) -> float:
        """Apply damage with all combat system enhancements"""
        
        # Calculate elemental damage
        elemental_damage, status_effects = ElementalDamage.calculate_damage(
            base_damage, element_type, target)
        
        # Calculate positional bonuses
        positional_bonus = 1.0
        if hasattr(attacker, 'rect') and hasattr(target, 'rect'):
            attacker_pos = attacker.rect.center
            target_pos = target.rect.center
            target_facing = getattr(target, 'facing', 0)
            
            positional_bonus = TacticalPositioning.calculate_positional_bonus(
                attacker_pos, target_pos, target_facing)
            
            # Check for cover
            if walls and TacticalPositioning.check_cover(target_pos, attacker_pos, walls):
                positional_bonus *= TacticalPositioning.get_cover_damage_reduction()
        
        # Apply combo multiplier
        combo_multiplier = self.combo_system.get_combo_multiplier()
        
        # Calculate final damage
        final_damage = elemental_damage * positional_bonus * combo_multiplier
        
        # Apply damage to target
        if hasattr(target, 'take_damage'):
            target.take_damage(int(final_damage), element_type)
        
        # Apply status effects
        target_id = id(target)
        for effect_type in status_effects:
            self.apply_status_effect(target, effect_type, 
                                   STATUS_EFFECTS[effect_type]['max_duration'])
        
        return final_damage
        
    def apply_status_effect(self, entity, effect_type: str, duration: int, 
                          stacks: int = 1) -> None:
        """Apply a status effect to an entity"""
        entity_id = id(entity)
        
        if entity_id not in self.active_status_effects:
            self.active_status_effects[entity_id] = []
            
        # Check if effect already exists
        existing_effect = None
        for effect in self.active_status_effects[entity_id]:
            if effect.effect_type == effect_type:
                existing_effect = effect
                break
                
        if existing_effect:
            if existing_effect.stackable:
                # Add stacks
                existing_effect.stacks = min(
                    existing_effect.stacks + stacks,
                    existing_effect.max_stacks
                )
                # Refresh duration
                existing_effect.duration = max(existing_effect.duration, duration)
            else:
                # Refresh duration for non-stackable effects
                existing_effect.duration = max(existing_effect.duration, duration)
        else:
            # Create new effect
            new_effect = StatusEffect(effect_type, duration, stacks=stacks)
            self.active_status_effects[entity_id].append(new_effect)
            
    def update_status_effects(self, entity) -> None:
        """Update all status effects for an entity"""
        entity_id = id(entity)
        
        if entity_id not in self.active_status_effects:
            return
            
        # Update effects and remove expired ones
        active_effects = []
        for effect in self.active_status_effects[entity_id]:
            if not effect.update(entity):
                active_effects.append(effect)
                
        self.active_status_effects[entity_id] = active_effects
        
        # Clean up if no effects remain
        if not self.active_status_effects[entity_id]:
            del self.active_status_effects[entity_id]
            
    def get_entity_modifiers(self, entity) -> Dict[str, float]:
        """Get all active modifiers for an entity"""
        entity_id = id(entity)
        
        if entity_id not in self.active_status_effects:
            return {
                'movement_multiplier': 1.0,
                'attack_speed_multiplier': 1.0,
                'damage_multiplier': 1.0,
                'healing_multiplier': 1.0
            }
            
        # Combine all effect modifiers
        movement_mult = 1.0
        attack_speed_mult = 1.0
        damage_mult = 1.0
        healing_mult = 1.0
        
        for effect in self.active_status_effects[entity_id]:
            movement_mult *= effect.get_movement_modifier()
            attack_speed_mult *= effect.get_attack_speed_modifier()
            damage_mult *= effect.get_damage_modifier()
            healing_mult *= effect.get_healing_modifier()
            
        return {
            'movement_multiplier': movement_mult,
            'attack_speed_multiplier': attack_speed_mult,
            'damage_multiplier': damage_mult,
            'healing_multiplier': healing_mult
        }
        
    def add_combo_action(self, action: str) -> bool:
        """Add action to combo system"""
        return self.combo_system.add_action(action)
        
    def reset_combo(self) -> None:
        """Reset combo system"""
        self.combo_system.reset_combo()
        
    def draw_status_effects(self, entity, surface: pygame.Surface, 
                          camera_offset_x: float, camera_offset_y: float) -> None:
        """Draw visual indicators for status effects"""
        entity_id = id(entity)
        
        if entity_id not in self.active_status_effects:
            return
            
        screen_x = entity.rect.x - camera_offset_x
        screen_y = entity.rect.y - camera_offset_y
        
        # Draw effect indicators
        effect_offset = 0
        for effect in self.active_status_effects[entity_id]:
            color = self._get_effect_color(effect.effect_type)
            
            # Draw small colored circle above entity
            pygame.draw.circle(surface, color,
                             (int(screen_x + entity.rect.width//2 + effect_offset),
                              int(screen_y - 10)),
                             4)
            effect_offset += 10
            
    def _get_effect_color(self, effect_type: str) -> Tuple[int, int, int]:
        """Get color for status effect indicator"""
        colors = {
            'burning': (255, 69, 0),
            'frozen': (135, 206, 235),
            'slowed': (173, 216, 230),
            'stunned': (255, 255, 0),
            'poisoned': (0, 255, 0),
            'cursed': (75, 0, 130),
            'blessed': (255, 215, 0)
        }
        return colors.get(effect_type, (255, 255, 255))
