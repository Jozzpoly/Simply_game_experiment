"""
Enhanced Equipment System for Phase 2

This module handles:
- Equipment rarity system (common to artifact)
- Equipment sets with powerful bonuses
- Enchantments system
- Legendary items with unique effects
- Consumable items with tactical uses
"""

import pygame
import random
import logging
from typing import Dict, List, Optional, Tuple, Any
from config import *
from utils.constants import *

logger = logging.getLogger(__name__)


class Enchantment:
    """Represents an enchantment on equipment"""
    
    def __init__(self, enchantment_type: str, level: int = 1):
        self.enchantment_type = enchantment_type
        self.level = level
        self.config = ENCHANTMENTS.get(enchantment_type, {})
        self.max_level = self.config.get('max_level', 1)
        self.effect_per_level = self.config.get('effect_per_level', {})
        
    def get_effects(self) -> Dict[str, Any]:
        """Get the effects of this enchantment at current level"""
        effects = {}
        for effect_type, base_value in self.effect_per_level.items():
            if isinstance(base_value, (int, float)):
                effects[effect_type] = base_value * self.level
            else:
                effects[effect_type] = base_value
        return effects
        
    def get_description(self) -> str:
        """Get description of the enchantment"""
        base_desc = self.config.get('description', 'Unknown enchantment')
        if self.level > 1:
            return f"{self.config.get('name', self.enchantment_type)} {self.level}: {base_desc}"
        return f"{self.config.get('name', self.enchantment_type)}: {base_desc}"


class EnhancedEquipment:
    """Enhanced equipment with rarity, enchantments, and set bonuses"""
    
    def __init__(self, equipment_type: str, base_stats: Dict[str, int], 
                 rarity: str = "common", level: int = 1):
        self.equipment_type = equipment_type
        self.base_stats = base_stats.copy()
        self.rarity = rarity
        self.level = level
        
        # Rarity configuration
        self.rarity_config = EQUIPMENT_RARITIES.get(rarity, EQUIPMENT_RARITIES['common'])
        
        # Apply rarity multiplier to stats
        stat_multiplier = self.rarity_config['stat_multiplier']
        for stat in self.base_stats:
            self.base_stats[stat] = int(self.base_stats[stat] * stat_multiplier)
        
        # Enchantments
        self.enchantments: List[Enchantment] = []
        self.max_enchantments = self.rarity_config['max_enchantments']
        
        # Set information
        self.set_name = None
        self.set_piece_type = None
        
        # Generate random enchantments for higher rarity items
        if self.max_enchantments > 0:
            self._generate_random_enchantments()
            
        # Generate name
        self.name = self._generate_name()
        
    def _generate_random_enchantments(self) -> None:
        """Generate random enchantments based on rarity"""
        # Get applicable enchantments for this equipment type
        applicable_enchantments = [
            ench_type for ench_type, config in ENCHANTMENTS.items()
            if config.get('type') == self.equipment_type or config.get('type') == 'any'
        ]
        
        if not applicable_enchantments:
            return
            
        # Number of enchantments to add
        num_enchantments = random.randint(1, self.max_enchantments)
        
        # Add random enchantments
        selected_enchantments = random.sample(
            applicable_enchantments, 
            min(num_enchantments, len(applicable_enchantments))
        )
        
        for ench_type in selected_enchantments:
            max_level = ENCHANTMENTS[ench_type]['max_level']
            # Higher rarity items get higher level enchantments
            if self.rarity == 'legendary' or self.rarity == 'artifact':
                level = random.randint(max(1, max_level - 1), max_level)
            elif self.rarity == 'epic':
                level = random.randint(max(1, max_level - 2), max_level)
            else:
                level = random.randint(1, max(1, max_level // 2))
                
            self.enchantments.append(Enchantment(ench_type, level))
            
    def _generate_name(self) -> str:
        """Generate equipment name based on rarity and enchantments"""
        base_name = self.equipment_type.replace('_', ' ').title()
        
        prefix = self.rarity_config.get('name_prefix', '')
        suffix = self.rarity_config.get('name_suffix', '')
        
        # Add enchantment-based modifiers
        if self.enchantments:
            primary_enchant = self.enchantments[0]
            if primary_enchant.enchantment_type == 'fire_aspect':
                prefix = 'Flaming ' + prefix
            elif primary_enchant.enchantment_type == 'frost_bite':
                prefix = 'Frozen ' + prefix
            elif primary_enchant.enchantment_type == 'lightning_strike':
                prefix = 'Shocking ' + prefix
            elif primary_enchant.enchantment_type == 'vampiric':
                prefix = 'Vampiric ' + prefix
                
        return f"{prefix}{base_name}{suffix}".strip()
        
    def get_total_stats(self) -> Dict[str, Any]:
        """Get total stats including enchantment bonuses"""
        total_stats = self.base_stats.copy()
        
        # Add enchantment effects
        for enchantment in self.enchantments:
            effects = enchantment.get_effects()
            for effect_type, value in effects.items():
                if effect_type in total_stats:
                    total_stats[effect_type] += value
                else:
                    total_stats[effect_type] = value
                    
        return total_stats
        
    def get_color(self) -> Tuple[int, int, int]:
        """Get color based on rarity"""
        return self.rarity_config['color']
        
    def add_enchantment(self, enchantment: Enchantment) -> bool:
        """Add an enchantment if possible"""
        if len(self.enchantments) >= self.max_enchantments:
            return False
            
        # Check if enchantment type already exists
        for existing in self.enchantments:
            if existing.enchantment_type == enchantment.enchantment_type:
                # Upgrade existing enchantment
                if existing.level < existing.max_level:
                    existing.level = min(existing.level + 1, existing.max_level)
                    return True
                return False
                
        self.enchantments.append(enchantment)
        return True
        
    def get_description(self) -> List[str]:
        """Get full description of the equipment"""
        lines = [self.name]
        lines.append(f"Rarity: {self.rarity.title()}")
        lines.append(f"Level: {self.level}")
        lines.append("")
        
        # Base stats
        lines.append("Stats:")
        total_stats = self.get_total_stats()
        for stat, value in total_stats.items():
            if isinstance(value, (int, float)) and stat not in ['elemental_damage']:
                lines.append(f"  {stat.replace('_', ' ').title()}: +{value}")
                
        # Enchantments
        if self.enchantments:
            lines.append("")
            lines.append("Enchantments:")
            for enchantment in self.enchantments:
                lines.append(f"  {enchantment.get_description()}")
                
        return lines


class EquipmentSet:
    """Manages equipment sets and their bonuses"""
    
    def __init__(self, set_name: str):
        self.set_name = set_name
        self.config = EQUIPMENT_SETS.get(set_name, {})
        self.required_pieces = self.config.get('pieces', [])
        self.set_bonuses = self.config.get('set_bonuses', {})
        self.color_theme = self.config.get('color_theme', (255, 255, 255))
        
    def get_active_bonuses(self, equipped_pieces: List[str]) -> Dict[str, Any]:
        """Get active set bonuses based on equipped pieces"""
        # Count matching pieces
        matching_pieces = sum(1 for piece in equipped_pieces if piece in self.required_pieces)
        
        # Get applicable bonuses
        active_bonuses = {}
        for piece_count, bonuses in self.set_bonuses.items():
            if matching_pieces >= piece_count:
                active_bonuses.update(bonuses)
                
        return active_bonuses
        
    def get_description(self, equipped_pieces: List[str]) -> List[str]:
        """Get description of set bonuses"""
        lines = [f"{self.config.get('name', self.set_name)}"]
        lines.append(f"Pieces: {len(equipped_pieces)}/{len(self.required_pieces)}")
        lines.append("")
        
        matching_pieces = sum(1 for piece in equipped_pieces if piece in self.required_pieces)
        
        for piece_count, bonuses in sorted(self.set_bonuses.items()):
            active = matching_pieces >= piece_count
            status = "✓" if active else " "
            lines.append(f"{status} ({piece_count}) pieces:")
            
            for bonus_type, value in bonuses.items():
                if bonus_type == 'special':
                    lines.append(f"    Special: {value}")
                else:
                    lines.append(f"    {bonus_type.replace('_', ' ').title()}: +{value}")
                    
        return lines


class ConsumableItem:
    """Represents a consumable item"""
    
    def __init__(self, item_type: str, quantity: int = 1):
        self.item_type = item_type
        self.quantity = quantity
        self.config = CONSUMABLE_ITEMS.get(item_type, {})
        
        self.name = self.config.get('name', item_type.replace('_', ' ').title())
        self.effect = self.config.get('effect', '')
        self.value = self.config.get('value', 0)
        self.duration = self.config.get('duration', 0)
        self.cooldown = self.config.get('cooldown', 0)
        self.stack_size = self.config.get('stack_size', 1)
        self.rarity = self.config.get('rarity', 'common')
        
        # Cooldown tracking
        self.last_used_time = 0
        
    def can_use(self) -> bool:
        """Check if item can be used"""
        current_time = pygame.time.get_ticks()
        return (self.quantity > 0 and 
                current_time - self.last_used_time >= self.cooldown)
                
    def use(self, target) -> bool:
        """Use the consumable item on target"""
        if not self.can_use():
            return False
            
        # Apply effect based on type
        success = False
        
        if self.effect == 'heal':
            if hasattr(target, 'heal'):
                target.heal(self.value)
                success = True
        elif self.effect == 'restore_mana':
            if hasattr(target, 'mana'):
                target.mana = min(target.max_mana, target.mana + self.value)
                success = True
        elif self.effect == 'damage_boost':
            if hasattr(target, 'apply_damage_boost'):
                target.apply_damage_boost(self.value, self.duration)
                success = True
        elif self.effect == 'speed_boost':
            if hasattr(target, 'apply_speed_boost'):
                target.apply_speed_boost(self.value, self.duration)
                success = True
        elif self.effect == 'stealth':
            if hasattr(target, 'apply_stealth'):
                target.apply_stealth(self.duration)
                success = True
        elif self.effect == 'cure_poison':
            if hasattr(target, 'cure_status_effect'):
                target.cure_status_effect('poisoned')
                success = True
        elif self.effect == 'resurrection':
            if hasattr(target, 'resurrect'):
                target.resurrect()
                success = True
                
        if success:
            self.quantity -= 1
            self.last_used_time = pygame.time.get_ticks()
            
        return success
        
    def get_color(self) -> Tuple[int, int, int]:
        """Get color based on rarity"""
        return EQUIPMENT_RARITIES.get(self.rarity, EQUIPMENT_RARITIES['common'])['color']


class EnhancedEquipmentManager:
    """Manages the enhanced equipment system"""
    
    def __init__(self):
        self.equipment_sets = {}
        self.consumables = {}
        
        # Load equipment sets
        for set_name in EQUIPMENT_SETS:
            self.equipment_sets[set_name] = EquipmentSet(set_name)
            
    def create_random_equipment(self, equipment_type: str, level: int = 1) -> EnhancedEquipment:
        """Create random equipment with appropriate rarity"""
        # Determine rarity based on level and random chance
        rarity_chances = []
        rarities = []
        
        for rarity, config in EQUIPMENT_RARITIES.items():
            # Adjust drop chance based on level
            level_modifier = min(level / 10.0, 2.0)  # Max 2x chance at level 10+
            adjusted_chance = config['drop_chance'] * level_modifier
            
            rarity_chances.append(adjusted_chance)
            rarities.append(rarity)
            
        # Normalize chances
        total_chance = sum(rarity_chances)
        normalized_chances = [chance / total_chance for chance in rarity_chances]
        
        # Select rarity
        selected_rarity = random.choices(rarities, weights=normalized_chances)[0]
        
        # Generate base stats based on equipment type and level
        base_stats = self._generate_base_stats(equipment_type, level)
        
        return EnhancedEquipment(equipment_type, base_stats, selected_rarity, level)
        
    def _generate_base_stats(self, equipment_type: str, level: int) -> Dict[str, int]:
        """Generate base stats for equipment"""
        # Base stat templates
        stat_templates = {
            'weapon': {'damage': 10, 'fire_rate': 5},
            'armor': {'health': 20, 'defense': 5},
            'helmet': {'health': 10, 'defense': 3},
            'boots': {'speed': 5, 'health': 5},
            'accessory': {'damage': 5, 'health': 10},
            'shield': {'defense': 10, 'health': 15}
        }
        
        base_template = stat_templates.get(equipment_type, {'health': 10})
        
        # Scale with level
        scaled_stats = {}
        for stat, base_value in base_template.items():
            scaled_value = base_value + (level - 1) * 2
            scaled_stats[stat] = scaled_value
            
        return scaled_stats
        
    def create_consumable(self, item_type: str, quantity: int = 1) -> ConsumableItem:
        """Create a consumable item"""
        return ConsumableItem(item_type, quantity)
        
    def get_set_bonuses(self, equipped_items: List[EnhancedEquipment]) -> Dict[str, Any]:
        """Calculate total set bonuses from equipped items"""
        # Group items by set
        set_pieces = {}
        
        for item in equipped_items:
            if item.set_name:
                if item.set_name not in set_pieces:
                    set_pieces[item.set_name] = []
                set_pieces[item.set_name].append(item.set_piece_type or item.equipment_type)
                
        # Calculate bonuses
        total_bonuses = {}
        
        for set_name, pieces in set_pieces.items():
            if set_name in self.equipment_sets:
                set_bonuses = self.equipment_sets[set_name].get_active_bonuses(pieces)
                for bonus_type, value in set_bonuses.items():
                    if bonus_type in total_bonuses:
                        total_bonuses[bonus_type] += value
                    else:
                        total_bonuses[bonus_type] = value
                        
        return total_bonuses
        
    def assign_to_set(self, equipment: EnhancedEquipment, set_name: str) -> bool:
        """Assign equipment to a set"""
        if set_name not in EQUIPMENT_SETS:
            return False
            
        set_config = EQUIPMENT_SETS[set_name]
        if equipment.equipment_type in set_config['pieces']:
            equipment.set_name = set_name
            equipment.set_piece_type = equipment.equipment_type
            
            # Apply set color theme
            equipment.color_theme = set_config['color_theme']
            return True
            
        return False
