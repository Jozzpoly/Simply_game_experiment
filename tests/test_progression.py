import unittest
import pygame
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from progression.skill_tree import SkillTree, Skill
from progression.equipment import Equipment, EquipmentManager
from progression.achievements import Achievement, AchievementManager
from utils.constants import *


class TestSkillTree(unittest.TestCase):
    """Test cases for the SkillTree system"""

    def setUp(self):
        """Set up test environment"""
        self.skill_tree = SkillTree()

    def test_skill_tree_initialization(self):
        """Test that skill tree initializes correctly"""
        self.assertEqual(self.skill_tree.skill_points, 0)
        self.assertGreater(len(self.skill_tree.skills), 0)

        # Check that some basic skills exist
        self.assertIn("critical_strike", self.skill_tree.skills)
        self.assertIn("armor_mastery", self.skill_tree.skills)
        self.assertIn("movement_mastery", self.skill_tree.skills)

    def test_add_skill_points(self):
        """Test adding skill points"""
        initial_points = self.skill_tree.skill_points
        self.skill_tree.add_skill_points(5)
        self.assertEqual(self.skill_tree.skill_points, initial_points + 5)

    def test_upgrade_skill(self):
        """Test upgrading a skill"""
        # Add skill points
        self.skill_tree.add_skill_points(3)

        # Upgrade critical strike (should be available from start)
        initial_level = self.skill_tree.skills["critical_strike"].current_level
        result = self.skill_tree.upgrade_skill("critical_strike")

        self.assertTrue(result)
        self.assertEqual(self.skill_tree.skills["critical_strike"].current_level, initial_level + 1)
        self.assertEqual(self.skill_tree.skill_points, 2)  # Should have used 1 point

    def test_skill_prerequisites(self):
        """Test that skill prerequisites work correctly"""
        # Add skill points
        self.skill_tree.add_skill_points(5)

        # Try to upgrade multi_shot without critical_strike
        result = self.skill_tree.upgrade_skill("multi_shot")
        self.assertFalse(result)  # Should fail due to prerequisites

        # Upgrade critical_strike first
        self.skill_tree.upgrade_skill("critical_strike")

        # Now multi_shot should be available
        result = self.skill_tree.upgrade_skill("multi_shot")
        self.assertTrue(result)

    def test_skill_bonuses(self):
        """Test that skill bonuses are calculated correctly"""
        # Add skill points and upgrade critical strike
        self.skill_tree.add_skill_points(3)
        self.skill_tree.upgrade_skill("critical_strike")

        # Check that critical chance bonus is applied
        crit_bonus = self.skill_tree.get_total_bonus("critical_chance")
        self.assertGreater(crit_bonus, 0)

    def test_save_load_skill_tree(self):
        """Test saving and loading skill tree data"""
        # Add points and upgrade some skills
        self.skill_tree.add_skill_points(5)
        self.skill_tree.upgrade_skill("critical_strike")
        self.skill_tree.upgrade_skill("armor_mastery")

        # Save data
        save_data = self.skill_tree.to_dict()

        # Create new skill tree and load data
        new_skill_tree = SkillTree()
        new_skill_tree.from_dict(save_data)

        # Verify data was loaded correctly
        self.assertEqual(new_skill_tree.skill_points, self.skill_tree.skill_points)
        self.assertEqual(
            new_skill_tree.skills["critical_strike"].current_level,
            self.skill_tree.skills["critical_strike"].current_level
        )


class TestEquipment(unittest.TestCase):
    """Test cases for the Equipment system"""

    def setUp(self):
        """Set up test environment"""
        self.equipment_manager = EquipmentManager()

    def test_equipment_creation(self):
        """Test creating equipment"""
        weapon = Equipment("weapon", "Test Sword", "Common", 1, {"damage_bonus": 5})

        self.assertEqual(weapon.equipment_type, "weapon")
        self.assertEqual(weapon.name, "Test Sword")
        self.assertEqual(weapon.rarity, "Common")
        self.assertEqual(weapon.level, 1)
        self.assertEqual(weapon.get_stat_bonus("damage_bonus"), 5)

    def test_equipment_upgrade(self):
        """Test upgrading equipment"""
        weapon = Equipment("weapon", "Test Sword", "Common", 1, {"damage_bonus": 5})

        initial_level = weapon.level
        initial_cost = weapon.upgrade_cost

        result = weapon.upgrade()
        self.assertTrue(result)
        self.assertEqual(weapon.level, initial_level + 1)
        self.assertEqual(weapon.get_stat_bonus("damage_bonus"), 10)  # Should double with level
        self.assertGreater(weapon.upgrade_cost, initial_cost)

    def test_equipment_manager_equip(self):
        """Test equipping items"""
        weapon = Equipment("weapon", "Test Sword", "Common", 1, {"damage_bonus": 5})

        # Equip the weapon
        old_weapon = self.equipment_manager.equip_item(weapon)
        self.assertIsNone(old_weapon)  # No previous weapon
        self.assertEqual(self.equipment_manager.equipped["weapon"], weapon)

    def test_equipment_stat_bonuses(self):
        """Test that equipment stat bonuses are calculated correctly"""
        weapon = Equipment("weapon", "Test Sword", "Common", 2, {"damage_bonus": 5})
        armor = Equipment("armor", "Test Armor", "Common", 1, {"damage_bonus": 3})

        self.equipment_manager.equip_item(weapon)
        self.equipment_manager.equip_item(armor)

        total_damage_bonus = self.equipment_manager.get_total_stat_bonus("damage_bonus")
        # 5*2 + 3*1 + Common set bonus (2) = 15
        expected_bonus = 10 + 3 + EQUIPMENT_SET_BONUSES["Common"]["damage_bonus"]
        self.assertEqual(total_damage_bonus, expected_bonus)

    def test_random_equipment_generation(self):
        """Test generating random equipment"""
        equipment = self.equipment_manager.generate_random_equipment("weapon", 5)

        self.assertEqual(equipment.equipment_type, "weapon")
        self.assertIn(equipment.rarity, EQUIPMENT_RARITIES)
        self.assertEqual(equipment.level, 1)  # Should start at level 1
        self.assertGreater(len(equipment.stats), 0)  # Should have some stats


class TestAchievements(unittest.TestCase):
    """Test cases for the Achievement system"""

    def setUp(self):
        """Set up test environment"""
        self.achievement_manager = AchievementManager()

    def test_achievement_initialization(self):
        """Test that achievements initialize correctly"""
        self.assertGreater(len(self.achievement_manager.achievements), 0)

        # Check that some basic achievements exist
        self.assertIn("first_steps", self.achievement_manager.achievements)
        self.assertIn("first_blood", self.achievement_manager.achievements)

    def test_achievement_unlock(self):
        """Test unlocking achievements"""
        # Create test stats that should unlock "first_steps"
        test_stats = {"player_level": 2}

        newly_unlocked = self.achievement_manager.check_achievements(test_stats)

        # Should unlock "first_steps" achievement
        achievement_names = [ach.name for ach in newly_unlocked]
        self.assertIn("First Steps", achievement_names)

    def test_achievement_rewards(self):
        """Test that achievement rewards are given correctly"""
        achievement = self.achievement_manager.achievements["first_steps"]

        # Unlock the achievement
        rewards = achievement.unlock()

        self.assertGreater(rewards["xp"], 0)
        self.assertTrue(achievement.unlocked)

    def test_achievement_progress_tracking(self):
        """Test achievement progress tracking"""
        unlocked, total = self.achievement_manager.get_achievement_progress()

        self.assertGreaterEqual(unlocked, 0)
        self.assertGreater(total, 0)
        self.assertLessEqual(unlocked, total)

    def test_save_load_achievements(self):
        """Test saving and loading achievement data"""
        # Unlock an achievement
        test_stats = {"player_level": 2}
        self.achievement_manager.check_achievements(test_stats)

        # Save data
        save_data = self.achievement_manager.to_dict()

        # Create new manager and load data
        new_manager = AchievementManager()
        new_manager.from_dict(save_data)

        # Verify achievement is still unlocked
        self.assertTrue(new_manager.achievements["first_steps"].unlocked)


if __name__ == '__main__':
    # Initialize pygame for tests that might need it
    pygame.init()

    # Run tests
    unittest.main()

    # Clean up
    pygame.quit()
