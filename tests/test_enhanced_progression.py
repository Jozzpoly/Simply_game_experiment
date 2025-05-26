"""
Comprehensive tests for enhanced character progression features including
skill synergies, equipment set bonuses, and advanced achievements.
"""

import unittest
import pygame
from progression.skill_tree import SkillTree
from progression.equipment import EquipmentManager, Equipment
from progression.achievements import AchievementManager, Achievement
from utils.constants import *


class TestSkillSynergies(unittest.TestCase):
    """Test skill synergy system"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()  # Initialize pygame for tests
        self.skill_tree = SkillTree()

    def test_synergy_requirements_check(self):
        """Test that synergy requirements are properly checked"""
        # Test critical_mastery synergy (requires critical_strike level 3, weapon_mastery level 2)
        synergy_data = SKILL_SYNERGIES["critical_mastery"]

        # Should not be active initially
        self.assertFalse(self.skill_tree._check_synergy_requirements(synergy_data))

        # Add skill points and upgrade skills
        self.skill_tree.add_skill_points(10)

        # Upgrade critical_strike to level 3
        for _ in range(3):
            self.skill_tree.upgrade_skill("critical_strike")

        # Should still not be active (weapon_mastery not high enough)
        self.assertFalse(self.skill_tree._check_synergy_requirements(synergy_data))

        # Upgrade weapon_mastery to level 2
        for _ in range(2):
            self.skill_tree.upgrade_skill("weapon_mastery")

        # Should now be active
        self.assertTrue(self.skill_tree._check_synergy_requirements(synergy_data))

    def test_synergy_bonuses_calculation(self):
        """Test that synergy bonuses are calculated correctly"""
        # Set up critical_mastery synergy
        self.skill_tree.add_skill_points(10)

        # Upgrade required skills
        for _ in range(3):
            self.skill_tree.upgrade_skill("critical_strike")
        for _ in range(2):
            self.skill_tree.upgrade_skill("weapon_mastery")

        # Check synergy bonuses
        synergy_bonuses = self.skill_tree.calculate_synergy_bonuses()
        self.assertIn("critical_damage_multiplier", synergy_bonuses)
        self.assertEqual(synergy_bonuses["critical_damage_multiplier"], 0.5)

    def test_active_synergies_tracking(self):
        """Test that active synergies are properly tracked"""
        self.skill_tree.add_skill_points(10)

        # Initially no active synergies
        active_synergies = self.skill_tree.get_active_synergies()
        self.assertEqual(len(active_synergies), 0)

        # Activate critical_mastery synergy
        for _ in range(3):
            self.skill_tree.upgrade_skill("critical_strike")
        for _ in range(2):
            self.skill_tree.upgrade_skill("weapon_mastery")

        active_synergies = self.skill_tree.get_active_synergies()
        self.assertIn("critical_mastery", active_synergies)
        self.assertEqual(active_synergies["critical_mastery"]["name"], "Critical Mastery")

    def test_potential_synergies_tracking(self):
        """Test that potential synergies are tracked correctly"""
        self.skill_tree.add_skill_points(5)

        # Partially upgrade skills for critical_mastery
        for _ in range(2):
            self.skill_tree.upgrade_skill("critical_strike")

        potential_synergies = self.skill_tree.get_potential_synergies()
        self.assertIn("critical_mastery", potential_synergies)

        # Check progress tracking
        progress = potential_synergies["critical_mastery"]["progress"]
        critical_strike_progress = next(p for p in progress if p["skill"] == "critical_strike")
        self.assertEqual(critical_strike_progress["current"], 2)
        self.assertEqual(critical_strike_progress["required"], 3)
        self.assertFalse(critical_strike_progress["met"])


class TestEquipmentSetBonuses(unittest.TestCase):
    """Test equipment set bonus system"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.equipment_manager = EquipmentManager()

    def test_set_bonus_calculation(self):
        """Test that set bonuses are calculated correctly"""
        # Create two common items
        weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 5})
        armor = Equipment("armor", "Common Armor", "Common", 1, {"health_bonus": 10})

        # Equip both items
        self.equipment_manager.equip_item(weapon)
        self.equipment_manager.equip_item(armor)

        # Check set bonuses
        set_bonuses = self.equipment_manager.calculate_set_bonuses()
        expected_bonuses = EQUIPMENT_SET_BONUSES["Common"]

        for stat, bonus in expected_bonuses.items():
            self.assertEqual(set_bonuses[stat], bonus)

    def test_mixed_rarity_sets(self):
        """Test that mixed rarity items don't create invalid set bonuses"""
        # Create items of different rarities
        weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 5})
        armor = Equipment("armor", "Rare Armor", "Rare", 1, {"health_bonus": 20})

        self.equipment_manager.equip_item(weapon)
        self.equipment_manager.equip_item(armor)

        # Should not have any set bonuses (need 2+ items of same rarity)
        set_bonuses = self.equipment_manager.calculate_set_bonuses()
        self.assertEqual(len(set_bonuses), 0)

    def test_active_set_bonuses_info(self):
        """Test that active set bonus information is correct"""
        # Create three rare items
        weapon = Equipment("weapon", "Rare Sword", "Rare", 1, {"damage_bonus": 8})
        armor = Equipment("armor", "Rare Armor", "Rare", 1, {"health_bonus": 20})
        accessory = Equipment("accessory", "Rare Ring", "Rare", 1, {"xp_bonus": 0.1})

        self.equipment_manager.equip_item(weapon)
        self.equipment_manager.equip_item(armor)
        self.equipment_manager.equip_item(accessory)

        active_sets = self.equipment_manager.get_active_set_bonuses()
        self.assertIn("Rare", active_sets)
        self.assertEqual(active_sets["Rare"]["count"], 3)
        self.assertEqual(active_sets["Rare"]["bonuses"], EQUIPMENT_SET_BONUSES["Rare"])

    def test_total_stat_bonus_with_sets(self):
        """Test that total stat bonuses include set bonuses"""
        # Create two common items
        weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 5})
        armor = Equipment("armor", "Common Armor", "Common", 1, {"damage_bonus": 3})

        self.equipment_manager.equip_item(weapon)
        self.equipment_manager.equip_item(armor)

        # Total damage bonus should be individual bonuses + set bonus
        total_damage = self.equipment_manager.get_total_stat_bonus("damage_bonus")
        expected = 5 + 3 + EQUIPMENT_SET_BONUSES["Common"]["damage_bonus"]
        self.assertEqual(total_damage, expected)


class TestAdvancedAchievements(unittest.TestCase):
    """Test advanced achievement system with chains and progressive achievements"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.achievement_manager = AchievementManager()

    def test_progressive_achievement_progress(self):
        """Test that progressive achievements track progress correctly"""
        # Get the enemy_slayer achievement (progressive, max 100)
        enemy_slayer = self.achievement_manager.achievements["enemy_slayer"]

        # Initially no progress
        self.assertEqual(enemy_slayer.progress, 0)
        self.assertFalse(enemy_slayer.unlocked)

        # Update progress
        self.assertFalse(enemy_slayer.update_progress(50))  # Should not unlock yet
        self.assertEqual(enemy_slayer.progress, 50)
        self.assertFalse(enemy_slayer.unlocked)

        # Complete the achievement
        self.assertTrue(enemy_slayer.update_progress(50))  # Should unlock now
        self.assertEqual(enemy_slayer.progress, 100)

    def test_achievement_chains(self):
        """Test that achievement chains work correctly"""
        # Test combat_master chain achievement
        combat_master = self.achievement_manager.achievements["combat_master"]

        # Should not be available initially (prerequisites not met)
        unlocked_names = []
        self.assertFalse(combat_master.is_available(unlocked_names))

        # Unlock prerequisites
        unlocked_names = ["boss_hunter", "enemy_slayer"]
        self.assertTrue(combat_master.is_available(unlocked_names))

    def test_achievement_progress_percentage(self):
        """Test achievement progress percentage calculation"""
        enemy_slayer = self.achievement_manager.achievements["enemy_slayer"]

        # Test various progress levels
        enemy_slayer.progress = 0
        self.assertEqual(enemy_slayer.get_progress_percentage(), 0.0)

        enemy_slayer.progress = 25
        self.assertEqual(enemy_slayer.get_progress_percentage(), 25.0)

        enemy_slayer.progress = 100
        self.assertEqual(enemy_slayer.get_progress_percentage(), 100.0)

    def test_chain_completion_tracking(self):
        """Test that achievement chains are tracked when completed"""
        # Manually unlock all achievements in warrior_path chain
        warrior_achievements = ACHIEVEMENT_CHAINS["warrior_path"]["achievements"]

        for ach_name in warrior_achievements:
            if ach_name in self.achievement_manager.achievements:
                self.achievement_manager.achievements[ach_name].unlocked = True

        # Check achievements (should detect completed chain)
        self.achievement_manager.check_achievements({})

        # Warrior path should be completed
        self.assertIn("warrior_path", self.achievement_manager.completed_chains)

    def test_achievement_serialization(self):
        """Test that enhanced achievements save and load correctly"""
        # Set up some achievement progress
        enemy_slayer = self.achievement_manager.achievements["enemy_slayer"]
        enemy_slayer.progress = 75

        # Complete a chain
        self.achievement_manager.completed_chains.append("warrior_path")

        # Save and load
        save_data = self.achievement_manager.to_dict()
        new_manager = AchievementManager()
        new_manager.from_dict(save_data)

        # Verify data was preserved
        new_enemy_slayer = new_manager.achievements["enemy_slayer"]
        self.assertEqual(new_enemy_slayer.progress, 75)
        self.assertIn("warrior_path", new_manager.completed_chains)


class TestUIEnhancements(unittest.TestCase):
    """Test UI enhancements for equipment management"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        pygame.display.set_mode((800, 600))  # Need display for UI tests
        from ui.ui_elements import UpgradeScreen
        from entities.player import Player

        self.upgrade_screen = UpgradeScreen(800, 600)
        self.player = Player(100, 100)

    def test_equipment_stats_text_generation(self):
        """Test that equipment stats text is generated correctly"""
        equipment = Equipment("weapon", "Test Sword", "Common", 2,
                            {"damage_bonus": 5, "fire_rate_bonus": 10, "critical_chance": 0.05})

        stats_text = self.upgrade_screen._get_equipment_stats_text(equipment)

        # Should show first 2 stats with level multiplier
        self.assertIn("Damage Bonus: +10", stats_text)  # 5 * 2
        self.assertIn("Fire Rate Bonus: +20", stats_text)  # 10 * 2

    def test_best_item_selection(self):
        """Test that best item selection works correctly"""
        # Add items to inventory
        common_weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 5})
        rare_weapon = Equipment("weapon", "Rare Sword", "Rare", 2, {"damage_bonus": 8})

        self.player.equipment_manager.add_to_inventory(common_weapon)
        self.player.equipment_manager.add_to_inventory(rare_weapon)

        # Should select the rare weapon (higher score)
        best_item = self.upgrade_screen._find_best_item_for_slot(
            self.player.equipment_manager, "weapon")

        self.assertEqual(best_item, rare_weapon)

    def test_equipment_interaction_simulation(self):
        """Test equipment interaction simulation"""
        # Add item to inventory
        weapon = Equipment("weapon", "Test Sword", "Common", 1, {"damage_bonus": 5})
        self.player.equipment_manager.add_to_inventory(weapon)

        # Simulate clicking on inventory item
        # This would normally be done through pygame events, but we can test the logic
        old_item = self.player.equipment_manager.equip_item(weapon)

        # Should equip successfully
        self.assertEqual(self.player.equipment_manager.equipped["weapon"], weapon)
        self.assertNotIn(weapon, self.player.equipment_manager.inventory)


class TestIntegration(unittest.TestCase):
    """Integration tests for all enhanced progression features"""

    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        from entities.player import Player
        self.player = Player(100, 100)

    def test_full_progression_integration(self):
        """Test that all progression systems work together"""
        # Add skill points and upgrade skills for synergy
        self.player.skill_tree.add_skill_points(10)

        # Upgrade skills to activate critical_mastery synergy
        for _ in range(3):
            self.player.skill_tree.upgrade_skill("critical_strike")
        for _ in range(2):
            self.player.skill_tree.upgrade_skill("weapon_mastery")

        # Equip equipment for set bonus
        weapon = Equipment("weapon", "Rare Sword", "Rare", 1, {"damage_bonus": 8})
        armor = Equipment("armor", "Rare Armor", "Rare", 1, {"health_bonus": 20})

        self.player.equipment_manager.equip_item(weapon)
        self.player.equipment_manager.equip_item(armor)

        # Update achievement progress
        self.player.stats["enemies_killed"] = 50
        self.player.achievement_manager.check_achievements(self.player.stats)

        # Verify all systems are working
        # Check synergies
        active_synergies = self.player.skill_tree.get_active_synergies()
        self.assertGreater(len(active_synergies), 0)

        # Check set bonuses
        set_bonuses = self.player.equipment_manager.get_active_set_bonuses()
        self.assertIn("Rare", set_bonuses)

        # Check achievement progress
        enemy_slayer = self.player.achievement_manager.achievements["enemy_slayer"]
        self.assertEqual(enemy_slayer.progress, 50)

    def test_save_load_integration(self):
        """Test that all enhanced features save and load correctly"""
        # Set up complex progression state
        self.player.skill_tree.add_skill_points(5)
        self.player.skill_tree.upgrade_skill("critical_strike")

        weapon = Equipment("weapon", "Test Sword", "Rare", 2, {"damage_bonus": 10})
        self.player.equipment_manager.equip_item(weapon)

        self.player.stats["enemies_killed"] = 25
        self.player.achievement_manager.check_achievements(self.player.stats)

        # Save progression data
        progression_data = self.player.get_progression_data()

        # Create new player and load data
        from entities.player import Player
        new_player = Player(100, 100)
        new_player.load_progression_data(progression_data)

        # Verify all data was preserved
        self.assertEqual(new_player.skill_tree.skills["critical_strike"].current_level, 1)
        self.assertEqual(new_player.equipment_manager.equipped["weapon"].name, "Test Sword")
        self.assertEqual(new_player.stats["enemies_killed"], 25)


if __name__ == '__main__':
    unittest.main()
