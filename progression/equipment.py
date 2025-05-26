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
        """Generate stats for equipment based on rarity and player level"""
        stats = {}
        rarity_index = EQUIPMENT_RARITIES.index(rarity)
        rarity_multiplier = 1.0 + (rarity_index * 0.5)  # 1.0, 1.5, 2.0, 2.5
        level_multiplier = 1.0 + (player_level * 0.1)

        for stat_name in base_stats:
            if random.random() < 0.7:  # 70% chance for each stat to appear
                base_value = self._get_base_stat_value(stat_name)
                stat_value = base_value * rarity_multiplier * level_multiplier
                stat_value *= random.uniform(0.8, 1.2)  # Add some randomness
                stats[stat_name] = round(stat_value, 2)

        return stats

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
        """Get total bonus for a stat from all equipped items"""
        total = 0.0
        for equipment in self.equipped.values():
            if equipment:
                total += equipment.get_stat_bonus(stat_name)
        return total

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
