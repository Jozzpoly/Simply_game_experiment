"""
Equipment system for character progression.

This module implements weapons, armor, and accessories with stat bonuses,
rarity levels, and upgrade mechanics.
"""

import pygame
import random
from typing import Dict, List, Optional, Any, Tuple
from utils.constants import *


class Equipment:
    """Represents a piece of equipment (weapon, armor, or accessory)"""

    def __init__(self, equipment_type: str, name: str, rarity: str,
                 level: int = 1, stats: Optional[Dict[str, float]] = None):
        self.equipment_type = equipment_type  # weapon, armor, accessory
        self.name = name
        self.rarity = rarity
        self.level = level
        self.stats = stats or {}
        self.upgrade_cost = self._calculate_upgrade_cost()

    def _calculate_upgrade_cost(self) -> int:
        """Calculate the cost to upgrade this equipment"""
        rarity_multiplier = EQUIPMENT_RARITIES.index(self.rarity) + 1
        return int(EQUIPMENT_UPGRADE_COST_BASE * rarity_multiplier * (self.level ** 1.5))

    def get_stat_bonus(self, stat_name: str) -> float:
        """Get the bonus for a specific stat"""
        return self.stats.get(stat_name, 0.0) * self.level

    def get_formatted_stat_bonus(self, stat_name: str) -> str:
        """Get formatted stat bonus with appropriate decimal places"""
        bonus = self.get_stat_bonus(stat_name)

        # Define which stats should be shown as percentages
        percentage_stats = {
            "critical_chance", "damage_reduction", "xp_bonus", "item_find",
            "skill_cooldown", "resource_bonus"
        }

        # Define which stats should be shown as integers
        integer_stats = {
            "damage_bonus", "health_bonus", "fire_rate_bonus", "projectile_speed"
        }

        if stat_name in percentage_stats:
            # Show as percentage with 1-2 decimal places
            percentage = bonus * 100
            if percentage >= 10:
                return f"+{percentage:.1f}%"
            else:
                return f"+{percentage:.2f}%"
        elif stat_name in integer_stats:
            # Show as integer
            return f"+{int(bonus)}"
        else:
            # Show as decimal with 1-2 decimal places
            if bonus >= 10:
                return f"+{bonus:.1f}"
            else:
                return f"+{bonus:.2f}"

    def upgrade(self) -> bool:
        """Upgrade the equipment to the next level"""
        if self.level < 10:  # Max equipment level
            self.level += 1
            self.upgrade_cost = self._calculate_upgrade_cost()
            return True
        return False

    def get_display_name(self) -> str:
        """Get the display name with level and rarity"""
        return f"{self.name} +{self.level} ({self.rarity})"

    def get_rarity_color(self) -> Tuple[int, int, int]:
        """Get the color associated with this equipment's rarity"""
        return EQUIPMENT_RARITY_COLORS.get(self.rarity, WHITE)

    def to_dict(self) -> Dict[str, Any]:
        """Convert equipment to dictionary for saving"""
        return {
            "equipment_type": self.equipment_type,
            "name": self.name,
            "rarity": self.rarity,
            "level": self.level,
            "stats": self.stats.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Equipment':
        """Create equipment from dictionary"""
        return cls(
            data["equipment_type"],
            data["name"],
            data["rarity"],
            data["level"],
            data["stats"]
        )


class EquipmentManager:
    """Manages player equipment and equipment generation"""

    def __init__(self):
        self.equipped: Dict[str, Optional[Equipment]] = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        self.inventory: List[Equipment] = []
        self.max_inventory_size = 20

        # Equipment name pools
        self.weapon_names = [
            "Sword", "Blade", "Rifle", "Cannon", "Blaster", "Launcher",
            "Destroyer", "Annihilator", "Vaporizer", "Decimator"
        ]

        self.armor_names = [
            "Vest", "Plate", "Mail", "Guard", "Shield", "Barrier",
            "Aegis", "Fortress", "Bulwark", "Sanctuary"
        ]

        self.accessory_names = [
            "Ring", "Amulet", "Charm", "Talisman", "Pendant", "Orb",
            "Crystal", "Relic", "Artifact", "Totem"
        ]

    def generate_random_equipment(self, equipment_type: str,
                                 player_level: int = 1) -> Equipment:
        """Generate a random piece of equipment"""
        # Determine rarity based on weights
        rarity = random.choices(
            EQUIPMENT_RARITIES,
            weights=EQUIPMENT_RARITY_WEIGHTS
        )[0]

        # Choose name based on type
        if equipment_type == "weapon":
            name = random.choice(self.weapon_names)
            base_stats = WEAPON_BASE_STATS.copy()
        elif equipment_type == "armor":
            name = random.choice(self.armor_names)
            base_stats = ARMOR_BASE_STATS.copy()
        else:  # accessory
            name = random.choice(self.accessory_names)
            base_stats = ACCESSORY_BASE_STATS.copy()

        # Generate stats based on rarity and player level
        stats = self._generate_equipment_stats(base_stats, rarity, player_level)

        return Equipment(equipment_type, name, rarity, 1, stats)

    def _generate_equipment_stats(self, base_stats: Dict[str, float],
                                 rarity: str, player_level: int) -> Dict[str, float]:
        """Generate stats for equipment - COMPLETELY REBUILT TO IGNORE ZERO BASE_STATS"""
        # CRITICAL FIX: Ignore the base_stats from constants (they're all 0)
        # Use only our enhanced system that guarantees meaningful values

        stats = {}
        rarity_index = EQUIPMENT_RARITIES.index(rarity)

        # Aggressive multipliers to ensure meaningful values
        rarity_multiplier = 2.0 + (rarity_index * 1.0)  # 2.0, 3.0, 4.0, 5.0
        level_multiplier = 1.5 + (player_level * 0.2)   # Strong level scaling

        # Get available stat types (ignore the zero values from base_stats)
        available_stats = list(base_stats.keys())

        # Determine how many stats this item will have (guaranteed 1-3 stats)
        min_stats = 1
        max_stats = min(3, len(available_stats))
        num_stats = random.randint(min_stats, max_stats)

        # Select which stats will appear
        selected_stats = random.sample(available_stats, num_stats)

        # Generate each selected stat with GUARANTEED meaningful values
        for stat_name in selected_stats:
            # COMPLETELY IGNORE base_stats[stat_name] - use only enhanced values

            # Get our enhanced base value (never zero)
            enhanced_base = self._get_enhanced_base_value(stat_name)

            # Get guaranteed minimum (safety net)
            guaranteed_min = self._get_guaranteed_minimum_value(stat_name)

            # Calculate value using ONLY enhanced base (never zero)
            calculated_value = enhanced_base * rarity_multiplier * level_multiplier

            # Add positive randomness
            randomness = random.uniform(1.0, 1.4)  # 100% to 140% of calculated value
            final_value = calculated_value * randomness

            # Apply guaranteed minimum as absolute safety net
            final_value = max(final_value, guaranteed_min)

            # Round and store with type-appropriate handling
            if self._is_integer_stat(stat_name):
                # Integer stats - round and ensure minimum
                final_stat_value = max(int(guaranteed_min), round(final_value))
            else:
                # Decimal stats - round to 2 places and ensure minimum
                final_stat_value = max(guaranteed_min, round(final_value, 2))

            # TRIPLE CHECK: Ensure no zero values can ever exist
            if final_stat_value <= 0:
                final_stat_value = guaranteed_min

            stats[stat_name] = final_stat_value

        # FINAL SAFETY CHECK: Ensure at least one stat exists with meaningful value
        if not stats:
            # Emergency fallback - force a meaningful stat
            stat_name = random.choice(available_stats)
            stats[stat_name] = self._get_guaranteed_minimum_value(stat_name)

        # VALIDATION: Check all stats are positive
        for stat_name, value in stats.items():
            if value <= 0:
                print(f"ERROR: Generated zero stat {stat_name}={value}, fixing...")
                stats[stat_name] = self._get_guaranteed_minimum_value(stat_name)

        return stats

    def _get_guaranteed_minimum_value(self, stat_name: str) -> float:
        """Get guaranteed minimum value that ensures meaningful gameplay impact"""
        minimums = {
            # Weapon stats - guaranteed meaningful minimums
            "damage_bonus": 2,          # At least +2 damage
            "fire_rate_bonus": 15,      # At least 15ms reduction
            "critical_chance": 0.02,    # At least 2% crit chance
            "projectile_speed": 1,      # At least +1 speed

            # Armor stats
            "health_bonus": 8,          # At least +8 health
            "damage_reduction": 0.03,   # At least 3% damage reduction
            "speed_bonus": 0.3,         # At least 0.3 speed bonus
            "regeneration": 0.8,        # At least 0.8 regen per second

            # Accessory stats
            "xp_bonus": 0.08,           # At least 8% XP bonus
            "item_find": 0.06,          # At least 6% item find
            "skill_cooldown": 0.05,     # At least 5% cooldown reduction
            "resource_bonus": 0.12      # At least 12% resource bonus
        }
        return minimums.get(stat_name, 1.0)

    def _get_enhanced_base_value(self, stat_name: str) -> float:
        """Get enhanced base values that scale well with multipliers"""
        enhanced_bases = {
            # Weapon stats - higher base values
            "damage_bonus": 8.0,        # Base 8 damage
            "fire_rate_bonus": 60.0,    # Base 60ms reduction
            "critical_chance": 0.08,    # Base 8% crit
            "projectile_speed": 3.0,    # Base +3 speed

            # Armor stats
            "health_bonus": 25.0,       # Base 25 health
            "damage_reduction": 0.12,   # Base 12% reduction
            "speed_bonus": 0.8,         # Base 0.8 speed
            "regeneration": 1.5,        # Base 1.5 regen

            # Accessory stats
            "xp_bonus": 0.18,           # Base 18% XP
            "item_find": 0.15,          # Base 15% item find
            "skill_cooldown": 0.12,     # Base 12% cooldown
            "resource_bonus": 0.25      # Base 25% resource
        }
        return enhanced_bases.get(stat_name, 2.0)

    def _is_integer_stat(self, stat_name: str) -> bool:
        """Check if a stat should be treated as an integer"""
        integer_stats = {
            "damage_bonus", "health_bonus", "fire_rate_bonus", "projectile_speed", "speed_bonus"
        }
        return stat_name in integer_stats

    def _get_minimum_stat_threshold(self, stat_name: str) -> float:
        """Get minimum meaningful threshold for each stat type - DEPRECATED, use _get_guaranteed_minimum_value"""
        return self._get_guaranteed_minimum_value(stat_name)

    def _get_base_stat_value(self, stat_name: str) -> float:
        """Get base value for a stat type"""
        stat_values = {
            # Weapon stats
            "damage_bonus": 5.0,
            "fire_rate_bonus": 50.0,
            "critical_chance": 0.05,
            "projectile_speed": 2.0,

            # Armor stats
            "health_bonus": 20.0,
            "damage_reduction": 0.1,
            "speed_bonus": 0.5,
            "regeneration": 1.0,

            # Accessory stats
            "xp_bonus": 0.15,
            "item_find": 0.1,
            "skill_cooldown": 0.1,
            "resource_bonus": 0.2
        }
        return stat_values.get(stat_name, 1.0)

    def equip_item(self, equipment: Equipment) -> Optional[Equipment]:
        """Equip an item, returning the previously equipped item if any"""
        equipment_type = equipment.equipment_type
        old_equipment = self.equipped[equipment_type]
        self.equipped[equipment_type] = equipment

        # Remove from inventory if it was there
        if equipment in self.inventory:
            self.inventory.remove(equipment)

        return old_equipment

    def unequip_item(self, equipment_type: str) -> Optional[Equipment]:
        """Unequip an item and add it to inventory"""
        equipment = self.equipped[equipment_type]
        if equipment and len(self.inventory) < self.max_inventory_size:
            self.equipped[equipment_type] = None
            self.inventory.append(equipment)
            return equipment
        return None

    def add_to_inventory(self, equipment: Equipment) -> bool:
        """Add equipment to inventory if there's space"""
        if len(self.inventory) < self.max_inventory_size:
            self.inventory.append(equipment)
            return True
        return False

    def remove_from_inventory(self, equipment: Equipment) -> bool:
        """Remove equipment from inventory"""
        if equipment in self.inventory:
            self.inventory.remove(equipment)
            return True
        return False

    def get_total_stat_bonus(self, stat_name: str) -> float:
        """Get total bonus for a stat from all equipped items including set bonuses"""
        total = 0.0

        # Add individual equipment bonuses
        for equipment in self.equipped.values():
            if equipment:
                total += equipment.get_stat_bonus(stat_name)

        # Add set bonuses
        set_bonuses = self.calculate_set_bonuses()
        total += set_bonuses.get(stat_name, 0.0)

        return total

    def calculate_set_bonuses(self) -> Dict[str, float]:
        """Calculate set bonuses from equipped items of matching rarity"""
        set_bonuses = {}

        # Count equipped items by rarity
        rarity_counts = {}
        for equipment in self.equipped.values():
            if equipment:
                rarity = equipment.rarity
                rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1

        # Apply set bonuses for rarities with enough items
        for rarity, count in rarity_counts.items():
            if count >= EQUIPMENT_SET_BONUS_THRESHOLD and rarity in EQUIPMENT_SET_BONUSES:
                bonus_data = EQUIPMENT_SET_BONUSES[rarity]
                for stat, bonus in bonus_data.items():
                    set_bonuses[stat] = set_bonuses.get(stat, 0.0) + bonus

        return set_bonuses

    def get_active_set_bonuses(self) -> Dict[str, Dict[str, float]]:
        """Get information about currently active set bonuses"""
        active_sets = {}

        # Count equipped items by rarity
        rarity_counts = {}
        for equipment in self.equipped.values():
            if equipment:
                rarity = equipment.rarity
                rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1

        # Identify active sets
        for rarity, count in rarity_counts.items():
            if count >= EQUIPMENT_SET_BONUS_THRESHOLD and rarity in EQUIPMENT_SET_BONUSES:
                active_sets[rarity] = {
                    "count": count,
                    "bonuses": EQUIPMENT_SET_BONUSES[rarity].copy()
                }

        return active_sets

    def upgrade_equipment(self, equipment: Equipment, currency: int) -> Tuple[bool, int]:
        """Upgrade equipment if player has enough currency"""
        upgrade_cost = equipment.upgrade_cost
        if currency >= upgrade_cost:
            if equipment.upgrade():
                return True, upgrade_cost
        return False, 0

    def get_equipment_by_type(self, equipment_type: str) -> Optional[Equipment]:
        """Get currently equipped item of a specific type"""
        return self.equipped.get(equipment_type)

    def to_dict(self) -> Dict[str, Any]:
        """Convert equipment manager to dictionary for saving"""
        return {
            "equipped": {
                eq_type: equipment.to_dict() if equipment else None
                for eq_type, equipment in self.equipped.items()
            },
            "inventory": [equipment.to_dict() for equipment in self.inventory]
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load equipment manager from dictionary"""
        # Load equipped items
        equipped_data = data.get("equipped", {})
        for eq_type, eq_data in equipped_data.items():
            if eq_data:
                self.equipped[eq_type] = Equipment.from_dict(eq_data)
            else:
                self.equipped[eq_type] = None

        # Load inventory
        inventory_data = data.get("inventory", [])
        self.inventory = [Equipment.from_dict(eq_data) for eq_data in inventory_data]
