import unittest
import pygame
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from progression.equipment import Equipment, EquipmentManager
from utils.constants import *


class TestEquipment(unittest.TestCase):
    """Test cases for Equipment objects"""
    
    def setUp(self):
        """Set up test environment"""
        self.weapon_stats = {"damage_bonus": 10, "critical_chance": 0.05}
        self.weapon = Equipment("weapon", "Iron Sword", "Common", 1, self.weapon_stats)
        
        self.armor_stats = {"health_bonus": 25, "damage_reduction": 0.1}
        self.armor = Equipment("armor", "Leather Armor", "Uncommon", 2, self.armor_stats)
    
    def test_equipment_initialization(self):
        """Test equipment initialization"""
        self.assertEqual(self.weapon.equipment_type, "weapon")
        self.assertEqual(self.weapon.name, "Iron Sword")
        self.assertEqual(self.weapon.rarity, "Common")
        self.assertEqual(self.weapon.level, 1)
        self.assertEqual(self.weapon.stats, self.weapon_stats)
    
    def test_equipment_stat_bonuses(self):
        """Test equipment stat bonus calculations"""
        # Level 1 weapon should give base stats
        self.assertEqual(self.weapon.get_stat_bonus("damage_bonus"), 10)
        self.assertEqual(self.weapon.get_stat_bonus("critical_chance"), 0.05)
        
        # Level 2 armor should give 2x base stats
        self.assertEqual(self.armor.get_stat_bonus("health_bonus"), 50)  # 25 * 2
        self.assertEqual(self.armor.get_stat_bonus("damage_reduction"), 0.2)  # 0.1 * 2
        
        # Non-existent stat should return 0
        self.assertEqual(self.weapon.get_stat_bonus("non_existent"), 0.0)
    
    def test_equipment_upgrade(self):
        """Test equipment upgrade functionality"""
        initial_level = self.weapon.level
        initial_cost = self.weapon.upgrade_cost
        initial_damage = self.weapon.get_stat_bonus("damage_bonus")
        
        # Upgrade the weapon
        result = self.weapon.upgrade()
        
        self.assertTrue(result)
        self.assertEqual(self.weapon.level, initial_level + 1)
        self.assertGreater(self.weapon.upgrade_cost, initial_cost)
        self.assertEqual(self.weapon.get_stat_bonus("damage_bonus"), initial_damage * 2)
    
    def test_equipment_max_level(self):
        """Test equipment max level constraint"""
        # Upgrade to max level
        while self.weapon.level < 10:
            self.weapon.upgrade()
        
        # Should be at max level
        self.assertEqual(self.weapon.level, 10)
        
        # Should not be able to upgrade further
        result = self.weapon.upgrade()
        self.assertFalse(result)
    
    def test_equipment_display_name(self):
        """Test equipment display name generation"""
        expected_name = "Iron Sword +1 (Common)"
        self.assertEqual(self.weapon.get_display_name(), expected_name)
        
        # Upgrade and test again
        self.weapon.upgrade()
        expected_name = "Iron Sword +2 (Common)"
        self.assertEqual(self.weapon.get_display_name(), expected_name)
    
    def test_equipment_rarity_color(self):
        """Test equipment rarity color mapping"""
        common_color = self.weapon.get_rarity_color()
        self.assertEqual(common_color, EQUIPMENT_RARITY_COLORS["Common"])
        
        uncommon_color = self.armor.get_rarity_color()
        self.assertEqual(uncommon_color, EQUIPMENT_RARITY_COLORS["Uncommon"])
    
    def test_equipment_serialization(self):
        """Test equipment save/load functionality"""
        # Save equipment data
        save_data = self.weapon.to_dict()
        
        # Create new equipment from saved data
        loaded_weapon = Equipment.from_dict(save_data)
        
        # Verify all properties match
        self.assertEqual(loaded_weapon.equipment_type, self.weapon.equipment_type)
        self.assertEqual(loaded_weapon.name, self.weapon.name)
        self.assertEqual(loaded_weapon.rarity, self.weapon.rarity)
        self.assertEqual(loaded_weapon.level, self.weapon.level)
        self.assertEqual(loaded_weapon.stats, self.weapon.stats)


class TestEquipmentManager(unittest.TestCase):
    """Test cases for EquipmentManager"""
    
    def setUp(self):
        """Set up test environment"""
        self.manager = EquipmentManager()
        
        # Create test equipment
        self.weapon1 = Equipment("weapon", "Iron Sword", "Common", 1, {"damage_bonus": 10})
        self.weapon2 = Equipment("weapon", "Steel Sword", "Uncommon", 1, {"damage_bonus": 15})
        self.armor = Equipment("armor", "Leather Armor", "Common", 1, {"health_bonus": 20})
        self.accessory = Equipment("accessory", "Magic Ring", "Rare", 1, {"xp_bonus": 0.1})
    
    def test_equipment_manager_initialization(self):
        """Test equipment manager initialization"""
        # Should have empty equipment slots
        for slot in self.manager.equipped.values():
            self.assertIsNone(slot)
        
        # Should have empty inventory
        self.assertEqual(len(self.manager.inventory), 0)
    
    def test_equip_item(self):
        """Test equipping items"""
        # Equip weapon
        old_weapon = self.manager.equip_item(self.weapon1)
        self.assertIsNone(old_weapon)  # No previous weapon
        self.assertEqual(self.manager.equipped["weapon"], self.weapon1)
        
        # Equip different weapon (should return old one)
        old_weapon = self.manager.equip_item(self.weapon2)
        self.assertEqual(old_weapon, self.weapon1)
        self.assertEqual(self.manager.equipped["weapon"], self.weapon2)
    
    def test_unequip_item(self):
        """Test unequipping items"""
        # Equip and then unequip
        self.manager.equip_item(self.weapon1)
        unequipped = self.manager.unequip_item("weapon")
        
        self.assertEqual(unequipped, self.weapon1)
        self.assertIsNone(self.manager.equipped["weapon"])
        self.assertIn(self.weapon1, self.manager.inventory)
    
    def test_inventory_management(self):
        """Test inventory add/remove functionality"""
        # Add to inventory
        result = self.manager.add_to_inventory(self.weapon1)
        self.assertTrue(result)
        self.assertIn(self.weapon1, self.manager.inventory)
        
        # Remove from inventory
        result = self.manager.remove_from_inventory(self.weapon1)
        self.assertTrue(result)
        self.assertNotIn(self.weapon1, self.manager.inventory)
        
        # Try to remove non-existent item
        result = self.manager.remove_from_inventory(self.weapon2)
        self.assertFalse(result)
    
    def test_inventory_size_limit(self):
        """Test inventory size limitations"""
        # Fill inventory to capacity
        for i in range(self.manager.max_inventory_size):
            item = Equipment("weapon", f"Sword {i}", "Common", 1, {"damage_bonus": 1})
            result = self.manager.add_to_inventory(item)
            self.assertTrue(result)
        
        # Try to add one more (should fail)
        extra_item = Equipment("weapon", "Extra Sword", "Common", 1, {"damage_bonus": 1})
        result = self.manager.add_to_inventory(extra_item)
        self.assertFalse(result)
    
    def test_total_stat_bonuses(self):
        """Test total stat bonus calculations"""
        # Equip multiple items with same stat
        weapon_with_crit = Equipment("weapon", "Crit Sword", "Common", 1, {"critical_chance": 0.05})
        accessory_with_crit = Equipment("accessory", "Crit Ring", "Common", 1, {"critical_chance": 0.03})
        
        self.manager.equip_item(weapon_with_crit)
        self.manager.equip_item(accessory_with_crit)
        
        total_crit = self.manager.get_total_stat_bonus("critical_chance")
        self.assertEqual(total_crit, 0.08)  # 0.05 + 0.03
    
    def test_equipment_upgrade_with_currency(self):
        """Test equipment upgrade with currency system"""
        initial_cost = self.weapon1.upgrade_cost
        
        # Should succeed with enough currency
        success, cost = self.manager.upgrade_equipment(self.weapon1, initial_cost)
        self.assertTrue(success)
        self.assertEqual(cost, initial_cost)
        self.assertEqual(self.weapon1.level, 2)
        
        # Should fail with insufficient currency
        new_cost = self.weapon1.upgrade_cost
        success, cost = self.manager.upgrade_equipment(self.weapon1, new_cost - 1)
        self.assertFalse(success)
        self.assertEqual(cost, 0)
        self.assertEqual(self.weapon1.level, 2)  # Should not have upgraded
    
    def test_random_equipment_generation(self):
        """Test random equipment generation"""
        # Generate multiple pieces of equipment
        for equipment_type in ["weapon", "armor", "accessory"]:
            equipment = self.manager.generate_random_equipment(equipment_type, 5)
            
            self.assertEqual(equipment.equipment_type, equipment_type)
            self.assertIn(equipment.rarity, EQUIPMENT_RARITIES)
            self.assertEqual(equipment.level, 1)
            self.assertGreater(len(equipment.stats), 0)
            
            # Verify stats are appropriate for equipment type
            if equipment_type == "weapon":
                valid_stats = set(WEAPON_BASE_STATS.keys())
            elif equipment_type == "armor":
                valid_stats = set(ARMOR_BASE_STATS.keys())
            else:  # accessory
                valid_stats = set(ACCESSORY_BASE_STATS.keys())
            
            for stat_name in equipment.stats.keys():
                self.assertIn(stat_name, valid_stats)
    
    def test_equipment_manager_serialization(self):
        """Test equipment manager save/load functionality"""
        # Set up equipment manager with some items
        self.manager.equip_item(self.weapon1)
        self.manager.equip_item(self.armor)
        self.manager.add_to_inventory(self.weapon2)
        self.manager.add_to_inventory(self.accessory)
        
        # Save data
        save_data = self.manager.to_dict()
        
        # Create new manager and load data
        new_manager = EquipmentManager()
        new_manager.from_dict(save_data)
        
        # Verify equipped items
        self.assertEqual(new_manager.equipped["weapon"].name, self.weapon1.name)
        self.assertEqual(new_manager.equipped["armor"].name, self.armor.name)
        self.assertIsNone(new_manager.equipped["accessory"])
        
        # Verify inventory
        self.assertEqual(len(new_manager.inventory), 2)
        inventory_names = [item.name for item in new_manager.inventory]
        self.assertIn(self.weapon2.name, inventory_names)
        self.assertIn(self.accessory.name, inventory_names)


class TestEquipmentIntegration(unittest.TestCase):
    """Test cases for equipment system integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.manager = EquipmentManager()
    
    def test_equipment_rarity_distribution(self):
        """Test that equipment rarity follows expected distribution"""
        # Generate many pieces of equipment and check distribution
        rarity_counts = {rarity: 0 for rarity in EQUIPMENT_RARITIES}
        
        for _ in range(1000):
            equipment = self.manager.generate_random_equipment("weapon", 1)
            rarity_counts[equipment.rarity] += 1
        
        # Common should be most frequent, Epic should be least frequent
        self.assertGreater(rarity_counts["Common"], rarity_counts["Uncommon"])
        self.assertGreater(rarity_counts["Uncommon"], rarity_counts["Rare"])
        self.assertGreater(rarity_counts["Rare"], rarity_counts["Epic"])
    
    def test_equipment_stat_scaling(self):
        """Test that equipment stats scale properly with rarity and level"""
        # Generate equipment of different rarities
        common_weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 10})
        epic_weapon = Equipment("weapon", "Epic Sword", "Epic", 1, {"damage_bonus": 10})
        
        # Epic should have higher upgrade cost
        self.assertGreater(epic_weapon.upgrade_cost, common_weapon.upgrade_cost)
        
        # Test level scaling
        common_weapon.upgrade()  # Level 2
        epic_weapon.upgrade()    # Level 2
        
        # Both should have doubled their damage bonus
        self.assertEqual(common_weapon.get_stat_bonus("damage_bonus"), 20)
        self.assertEqual(epic_weapon.get_stat_bonus("damage_bonus"), 20)


if __name__ == '__main__':
    # Initialize pygame for tests that might need it
    pygame.init()
    
    # Run tests
    unittest.main()
    
    # Clean up
    pygame.quit()
