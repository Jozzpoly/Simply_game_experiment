import unittest
import pygame
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from progression.skill_tree import SkillTree, Skill
from utils.constants import *


class TestSkill(unittest.TestCase):
    """Test cases for individual Skill objects"""
    
    def setUp(self):
        """Set up test environment"""
        self.skill = Skill(
            "test_skill",
            "combat",
            5,
            "A test skill",
            prerequisites=["prereq_skill"],
            stats={"damage_bonus": 0.1}
        )
    
    def test_skill_initialization(self):
        """Test skill initialization"""
        self.assertEqual(self.skill.name, "test_skill")
        self.assertEqual(self.skill.category, "combat")
        self.assertEqual(self.skill.max_level, 5)
        self.assertEqual(self.skill.current_level, 0)
        self.assertEqual(self.skill.description, "A test skill")
        self.assertEqual(self.skill.prerequisites, ["prereq_skill"])
        self.assertFalse(self.skill.unlocked)  # Should be locked due to prerequisites
    
    def test_skill_can_upgrade(self):
        """Test skill upgrade conditions"""
        # Should not be able to upgrade without prerequisites
        self.assertFalse(self.skill.can_upgrade(1, {}))
        
        # Should not be able to upgrade without skill points
        self.assertFalse(self.skill.can_upgrade(0, {"prereq_skill": 1}))
        
        # Should be able to upgrade with prerequisites and skill points
        self.assertTrue(self.skill.can_upgrade(1, {"prereq_skill": 1}))
        
        # Max out the skill
        self.skill.current_level = self.skill.max_level
        self.assertFalse(self.skill.can_upgrade(1, {"prereq_skill": 1}))
    
    def test_skill_upgrade(self):
        """Test skill upgrade functionality"""
        initial_level = self.skill.current_level
        result = self.skill.upgrade()
        
        self.assertTrue(result)
        self.assertEqual(self.skill.current_level, initial_level + 1)
        
        # Test max level constraint
        self.skill.current_level = self.skill.max_level
        result = self.skill.upgrade()
        self.assertFalse(result)
    
    def test_skill_bonus_calculation(self):
        """Test skill bonus calculations"""
        # No bonus at level 0
        self.assertEqual(self.skill.get_current_bonus("damage_bonus"), 0.0)
        
        # Upgrade and check bonus
        self.skill.upgrade()
        self.assertEqual(self.skill.get_current_bonus("damage_bonus"), 0.1)
        
        # Upgrade again
        self.skill.upgrade()
        self.assertEqual(self.skill.get_current_bonus("damage_bonus"), 0.2)
        
        # Non-existent stat should return 0
        self.assertEqual(self.skill.get_current_bonus("non_existent"), 0.0)


class TestSkillTreeIntegration(unittest.TestCase):
    """Test cases for SkillTree integration and complex scenarios"""
    
    def setUp(self):
        """Set up test environment"""
        self.skill_tree = SkillTree()
    
    def test_skill_tree_categories(self):
        """Test that all skill categories are represented"""
        combat_skills = self.skill_tree.get_skills_by_category("combat")
        survival_skills = self.skill_tree.get_skills_by_category("survival")
        utility_skills = self.skill_tree.get_skills_by_category("utility")
        
        self.assertGreater(len(combat_skills), 0)
        self.assertGreater(len(survival_skills), 0)
        self.assertGreater(len(utility_skills), 0)
    
    def test_skill_prerequisite_chain(self):
        """Test complex prerequisite chains"""
        # Add enough skill points
        self.skill_tree.add_skill_points(10)
        
        # Explosive shots requires both multi_shot and piercing_shots
        # which both require critical_strike
        
        # Should not be able to upgrade explosive_shots initially
        self.assertFalse(self.skill_tree.can_upgrade_skill("explosive_shots"))
        
        # Upgrade critical_strike
        self.assertTrue(self.skill_tree.upgrade_skill("critical_strike"))
        
        # Now multi_shot and piercing_shots should be available
        self.assertTrue(self.skill_tree.can_upgrade_skill("multi_shot"))
        self.assertTrue(self.skill_tree.can_upgrade_skill("piercing_shots"))
        
        # Upgrade both prerequisites
        self.assertTrue(self.skill_tree.upgrade_skill("multi_shot"))
        self.assertTrue(self.skill_tree.upgrade_skill("piercing_shots"))
        
        # Now explosive_shots should be available
        self.assertTrue(self.skill_tree.can_upgrade_skill("explosive_shots"))
        self.assertTrue(self.skill_tree.upgrade_skill("explosive_shots"))
    
    def test_skill_tree_total_bonuses(self):
        """Test that total bonuses are calculated correctly across multiple skills"""
        self.skill_tree.add_skill_points(5)
        
        # Upgrade multiple skills that affect damage
        self.skill_tree.upgrade_skill("critical_strike")  # Affects critical_chance
        self.skill_tree.upgrade_skill("weapon_mastery")   # Affects damage_bonus
        
        # Check individual bonuses
        crit_bonus = self.skill_tree.get_total_bonus("critical_chance")
        damage_bonus = self.skill_tree.get_total_bonus("damage_bonus")
        
        self.assertGreater(crit_bonus, 0)
        self.assertGreater(damage_bonus, 0)
    
    def test_skill_tree_max_level_skills(self):
        """Test maxing out skills"""
        # Add enough points to max out a skill
        self.skill_tree.add_skill_points(10)
        
        skill_name = "critical_strike"
        max_level = self.skill_tree.skills[skill_name].max_level
        
        # Upgrade to max level
        for _ in range(max_level):
            result = self.skill_tree.upgrade_skill(skill_name)
            self.assertTrue(result)
        
        # Should not be able to upgrade further
        result = self.skill_tree.upgrade_skill(skill_name)
        self.assertFalse(result)
        
        # Verify skill is at max level
        self.assertEqual(self.skill_tree.skills[skill_name].current_level, max_level)
    
    def test_skill_tree_point_management(self):
        """Test skill point management"""
        initial_points = self.skill_tree.skill_points
        
        # Add points
        self.skill_tree.add_skill_points(5)
        self.assertEqual(self.skill_tree.skill_points, initial_points + 5)
        
        # Upgrade a skill (should consume 1 point)
        self.skill_tree.upgrade_skill("critical_strike")
        self.assertEqual(self.skill_tree.skill_points, initial_points + 4)
        
        # Try to upgrade without points
        self.skill_tree.skill_points = 0
        result = self.skill_tree.upgrade_skill("armor_mastery")
        self.assertFalse(result)
    
    def test_skill_tree_persistence(self):
        """Test skill tree save/load functionality"""
        # Set up a skill tree with some upgrades
        self.skill_tree.add_skill_points(5)
        self.skill_tree.upgrade_skill("critical_strike")
        self.skill_tree.upgrade_skill("armor_mastery")
        self.skill_tree.upgrade_skill("movement_mastery")
        
        # Save the state
        save_data = self.skill_tree.to_dict()
        
        # Create a new skill tree and load the state
        new_skill_tree = SkillTree()
        new_skill_tree.from_dict(save_data)
        
        # Verify all data was preserved
        self.assertEqual(new_skill_tree.skill_points, self.skill_tree.skill_points)
        
        for skill_name in ["critical_strike", "armor_mastery", "movement_mastery"]:
            original_level = self.skill_tree.skills[skill_name].current_level
            loaded_level = new_skill_tree.skills[skill_name].current_level
            self.assertEqual(loaded_level, original_level)
        
        # Verify learned skills dictionary
        self.assertEqual(new_skill_tree.learned_skills, self.skill_tree.learned_skills)
    
    def test_skill_availability_updates(self):
        """Test that skill availability updates correctly when prerequisites are met"""
        self.skill_tree.add_skill_points(3)
        
        # Initially, multi_shot should not be available
        multi_shot = self.skill_tree.skills["multi_shot"]
        self.assertFalse(multi_shot.unlocked)
        
        # Upgrade critical_strike (prerequisite for multi_shot)
        self.skill_tree.upgrade_skill("critical_strike")
        
        # Now multi_shot should be unlocked
        self.assertTrue(multi_shot.unlocked)


class TestSkillEffects(unittest.TestCase):
    """Test cases for specific skill effects and mechanics"""
    
    def setUp(self):
        """Set up test environment"""
        self.skill_tree = SkillTree()
        self.skill_tree.add_skill_points(20)  # Plenty of points for testing
    
    def test_combat_skill_effects(self):
        """Test combat skill effects"""
        # Test critical strike
        self.skill_tree.upgrade_skill("critical_strike")
        crit_chance = self.skill_tree.get_total_bonus("critical_chance")
        expected_crit = COMBAT_SKILLS["critical_strike"]["chance_per_level"]
        self.assertEqual(crit_chance, expected_crit)
        
        # Test weapon mastery
        self.skill_tree.upgrade_skill("weapon_mastery")
        damage_bonus = self.skill_tree.get_total_bonus("damage_bonus")
        expected_damage = COMBAT_SKILLS["weapon_mastery"]["damage_bonus_per_level"]
        self.assertEqual(damage_bonus, expected_damage)
    
    def test_survival_skill_effects(self):
        """Test survival skill effects"""
        # Test armor mastery
        self.skill_tree.upgrade_skill("armor_mastery")
        damage_reduction = self.skill_tree.get_total_bonus("damage_reduction")
        expected_reduction = SURVIVAL_SKILLS["armor_mastery"]["damage_reduction_per_level"]
        self.assertEqual(damage_reduction, expected_reduction)
        
        # Test health regeneration
        self.skill_tree.upgrade_skill("health_regeneration")
        regen_amount = self.skill_tree.get_total_bonus("regen_amount")
        expected_regen = SURVIVAL_SKILLS["health_regeneration"]["regen_per_level"]
        self.assertEqual(regen_amount, expected_regen)
    
    def test_utility_skill_effects(self):
        """Test utility skill effects"""
        # Test movement mastery
        self.skill_tree.upgrade_skill("movement_mastery")
        speed_bonus = self.skill_tree.get_total_bonus("speed_bonus")
        expected_speed = UTILITY_SKILLS["movement_mastery"]["speed_bonus_per_level"]
        self.assertEqual(speed_bonus, expected_speed)
        
        # Test resource efficiency
        self.skill_tree.upgrade_skill("resource_efficiency")
        xp_bonus = self.skill_tree.get_total_bonus("xp_bonus")
        expected_xp = UTILITY_SKILLS["resource_efficiency"]["xp_bonus_per_level"]
        self.assertEqual(xp_bonus, expected_xp)


if __name__ == '__main__':
    # Initialize pygame for tests that might need it
    pygame.init()
    
    # Run tests
    unittest.main()
    
    # Clean up
    pygame.quit()
