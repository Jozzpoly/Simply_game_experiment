#!/usr/bin/env python3
"""
Comprehensive analysis of the character progression system to identify issues,
inconsistencies, and integration problems.
"""

import pygame
import sys
import os
import random

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.equipment import Equipment, EquipmentManager
from progression.skill_tree import SkillTree
from progression.achievements import AchievementManager
from utils.constants import *

class ProgressionAnalyzer:
    """Comprehensive analyzer for the progression system"""

    def __init__(self):
        self.issues_found = []
        self.warnings = []
        self.test_results = {}

    def log_issue(self, category: str, description: str, severity: str = "ERROR"):
        """Log an issue found during analysis"""
        issue = {
            "category": category,
            "description": description,
            "severity": severity
        }
        if severity == "ERROR":
            self.issues_found.append(issue)
        else:
            self.warnings.append(issue)
        print(f"  {severity}: {description}")

    def test_equipment_system_integration(self):
        """Test all equipment stats and their integration"""
        print("🔧 Testing Equipment System Integration...")

        player = Player(100, 100)

        # Test all equipment stat types
        stat_tests = {
            "damage_bonus": {"type": "weapon", "expected_method": "get_effective_damage"},
            "health_bonus": {"type": "armor", "expected_method": "get_effective_max_health"},
            "regeneration": {"type": "armor", "expected_method": "apply_skill_effects"},
            "critical_chance": {"type": "weapon", "expected_method": "get_critical_chance"},
            "speed_bonus": {"type": "armor", "expected_method": "get_effective_speed"},
            "fire_rate_bonus": {"type": "weapon", "expected_method": "get_effective_fire_rate"},
            "damage_reduction": {"type": "armor", "expected_method": "get_damage_reduction"},
            "xp_bonus": {"type": "accessory", "expected_method": "get_xp_bonus"},
            "projectile_speed": {"type": "weapon", "expected_method": None},  # Not implemented
            "item_find": {"type": "accessory", "expected_method": None},  # Used in level generation
            "skill_cooldown": {"type": "accessory", "expected_method": None},  # Not implemented
            "resource_bonus": {"type": "accessory", "expected_method": None}  # Not implemented
        }

        for stat_name, test_info in stat_tests.items():
            # Create equipment with this stat
            equipment = Equipment(test_info["type"], f"Test {stat_name}", "Common", 1, {stat_name: 10})
            player.equipment_manager.equip_item(equipment)

            # Check if stat is properly applied
            if test_info["expected_method"]:
                try:
                    method = getattr(player, test_info["expected_method"])
                    result = method()
                    if stat_name in ["damage_bonus", "health_bonus", "speed_bonus"]:
                        # These should increase the base value
                        if result <= getattr(player, stat_name.replace("_bonus", "")):
                            self.log_issue("Equipment", f"{stat_name} not properly applied in {test_info['expected_method']}")
                    elif stat_name == "regeneration":
                        # Test regeneration by simulating frames
                        initial_health = player.health = 50
                        for _ in range(70):  # Should trigger regen
                            player.apply_skill_effects()
                        if player.health <= initial_health:
                            self.log_issue("Equipment", f"Equipment regeneration not working")
                except Exception as e:
                    self.log_issue("Equipment", f"Error testing {stat_name}: {e}")
            else:
                self.log_issue("Equipment", f"{stat_name} stat not implemented in player calculations", "WARNING")

            # Unequip for next test
            player.equipment_manager.unequip_item(test_info["type"])

        # Test set bonuses
        self._test_equipment_set_bonuses(player)

        # Test equipment upgrade system
        self._test_equipment_upgrades(player)

        self.test_results["equipment_system"] = True

    def _test_equipment_set_bonuses(self, player):
        """Test equipment set bonus system"""
        print("  Testing equipment set bonuses...")

        # Test each rarity set bonus
        for rarity in EQUIPMENT_RARITIES:
            # Equip 2 items of same rarity
            weapon = Equipment("weapon", f"{rarity} Weapon", rarity, 1, {"damage_bonus": 5})
            armor = Equipment("armor", f"{rarity} Armor", rarity, 1, {"health_bonus": 10})

            player.equipment_manager.equip_item(weapon)
            player.equipment_manager.equip_item(armor)

            # Check set bonuses
            set_bonuses = player.equipment_manager.calculate_set_bonuses()
            expected_bonuses = EQUIPMENT_SET_BONUSES.get(rarity, {})

            if not set_bonuses and expected_bonuses:
                self.log_issue("Equipment", f"{rarity} set bonus not activated with 2 items")

            for bonus_stat, expected_value in expected_bonuses.items():
                if bonus_stat not in set_bonuses:
                    self.log_issue("Equipment", f"{rarity} set missing {bonus_stat} bonus")
                elif abs(set_bonuses[bonus_stat] - expected_value) > 0.001:
                    self.log_issue("Equipment", f"{rarity} set {bonus_stat} bonus incorrect: {set_bonuses[bonus_stat]} vs {expected_value}")

            # Clear equipment
            player.equipment_manager.unequip_item("weapon")
            player.equipment_manager.unequip_item("armor")

    def _test_equipment_upgrades(self, player):
        """Test equipment upgrade system"""
        print("  Testing equipment upgrade system...")

        equipment = Equipment("weapon", "Upgrade Test", "Common", 1, {"damage_bonus": 10})
        initial_bonus = equipment.get_stat_bonus("damage_bonus")
        initial_cost = equipment.upgrade_cost

        # Test upgrade
        success = equipment.upgrade()
        if not success:
            self.log_issue("Equipment", "Equipment upgrade failed")
            return

        # Check level increased
        if equipment.level != 2:
            self.log_issue("Equipment", f"Equipment level not increased: {equipment.level}")

        # Check stat bonus scaled with level
        new_bonus = equipment.get_stat_bonus("damage_bonus")
        if new_bonus != initial_bonus * 2:  # Should be doubled at level 2
            self.log_issue("Equipment", f"Equipment stat bonus not scaled with level: {new_bonus} vs {initial_bonus * 2}")

        # Check upgrade cost increased
        if equipment.upgrade_cost <= initial_cost:
            self.log_issue("Equipment", "Equipment upgrade cost not increased")

    def test_skill_tree_system_validation(self):
        """Test all skill tree functionality"""
        print("🌳 Testing Skill Tree System...")

        skill_tree = SkillTree()

        # Test all skills exist and have proper structure
        expected_skills = []
        for category in ["combat", "survival", "utility"]:
            category_skills = skill_tree.get_skills_by_category(category)
            if not category_skills:
                self.log_issue("Skills", f"No skills found in {category} category")
            expected_skills.extend([skill.name for skill in category_skills])

        # Test skill prerequisites
        self._test_skill_prerequisites(skill_tree)

        # Test skill synergies
        self._test_skill_synergies(skill_tree)

        # Test skill point management
        self._test_skill_point_management(skill_tree)

        self.test_results["skill_tree_system"] = True

    def _test_skill_prerequisites(self, skill_tree):
        """Test skill prerequisite system"""
        print("  Testing skill prerequisites...")

        # Find skills with prerequisites
        skills_with_prereqs = [skill for skill in skill_tree.skills.values() if skill.prerequisites]

        # First, test initial state - skills with unmet prerequisites should be locked
        for skill in skills_with_prereqs:
            # Check that prerequisites exist
            for prereq in skill.prerequisites:
                if prereq not in skill_tree.skills:
                    self.log_issue("Skills", f"Skill {skill.name} has invalid prerequisite: {prereq}")

            # Check if prerequisites are actually met
            prereqs_met = True
            for prereq in skill.prerequisites:
                if prereq not in skill_tree.learned_skills or skill_tree.learned_skills[prereq] < 1:
                    prereqs_met = False
                    break

            # Test that skill is locked when prerequisites are not met
            if not prereqs_met and skill.unlocked:
                self.log_issue("Skills", f"Skill {skill.name} should be locked due to unmet prerequisites")

        # Now test unlocking after meeting prerequisites (use a fresh skill tree for each test)
        for skill in skills_with_prereqs:
            # Create a fresh skill tree for this test
            test_skill_tree = SkillTree()
            test_skill_tree.add_skill_points(20)  # More points for complex prerequisite chains

            # Recursively upgrade all prerequisites and their prerequisites
            def upgrade_prerequisites_recursively(skill_name):
                if skill_name in test_skill_tree.skills:
                    skill_obj = test_skill_tree.skills[skill_name]
                    # First upgrade this skill's prerequisites
                    for prereq in skill_obj.prerequisites:
                        upgrade_prerequisites_recursively(prereq)
                    # Then upgrade this skill itself
                    test_skill_tree.upgrade_skill(skill_name)

            # Upgrade all prerequisites recursively
            for prereq in skill.prerequisites:
                upgrade_prerequisites_recursively(prereq)

            # Find the skill by name (need to find the key, not use the display name)
            test_skill = None
            for skill_key, skill_obj in test_skill_tree.skills.items():
                if skill_obj.name == skill.name:
                    test_skill = skill_obj
                    break

            if test_skill and not test_skill.unlocked:
                # Check if all prerequisites were actually met
                all_prereqs_met = True
                for prereq in skill.prerequisites:
                    if prereq not in test_skill_tree.learned_skills or test_skill_tree.learned_skills[prereq] < 1:
                        all_prereqs_met = False
                        break

                if all_prereqs_met:
                    self.log_issue("Skills", f"Skill {skill.name} not unlocked after meeting prerequisites")

    def _test_skill_synergies(self, skill_tree):
        """Test skill synergy system"""
        print("  Testing skill synergies...")

        skill_tree.add_skill_points(20)

        for synergy_name, synergy_data in SKILL_SYNERGIES.items():
            required_skills = synergy_data["skills"]
            min_levels = synergy_data["min_levels"]

            # Upgrade required skills to minimum levels
            for skill_name, min_level in zip(required_skills, min_levels):
                if skill_name in skill_tree.skills:
                    for _ in range(min_level):
                        if not skill_tree.upgrade_skill(skill_name):
                            break

            # Check if synergy is active
            active_synergies = skill_tree.get_active_synergies()
            if synergy_name not in active_synergies:
                # Check if all requirements were actually met
                all_met = True
                for skill_name, min_level in zip(required_skills, min_levels):
                    if skill_name not in skill_tree.skills:
                        all_met = False
                        break
                    if skill_tree.skills[skill_name].current_level < min_level:
                        all_met = False
                        break

                if all_met:
                    self.log_issue("Skills", f"Synergy {synergy_name} not activated despite meeting requirements")

    def _test_skill_point_management(self, skill_tree):
        """Test skill point allocation and consumption"""
        print("  Testing skill point management...")

        initial_points = skill_tree.skill_points
        skill_tree.add_skill_points(5)

        if skill_tree.skill_points != initial_points + 5:
            self.log_issue("Skills", f"Skill points not added correctly: {skill_tree.skill_points} vs {initial_points + 5}")

        # Test upgrading a skill
        upgradeable_skills = [name for name, skill in skill_tree.skills.items()
                            if skill.unlocked and skill.current_level < skill.max_level]

        if upgradeable_skills:
            skill_name = upgradeable_skills[0]
            points_before = skill_tree.skill_points
            level_before = skill_tree.skills[skill_name].current_level

            success = skill_tree.upgrade_skill(skill_name)
            if not success:
                self.log_issue("Skills", f"Failed to upgrade available skill: {skill_name}")
            else:
                if skill_tree.skill_points != points_before - 1:
                    self.log_issue("Skills", f"Skill points not consumed correctly: {skill_tree.skill_points} vs {points_before - 1}")
                if skill_tree.skills[skill_name].current_level != level_before + 1:
                    self.log_issue("Skills", f"Skill level not increased: {skill_tree.skills[skill_name].current_level} vs {level_before + 1}")

    def test_achievement_system_integration(self):
        """Test achievement system functionality"""
        print("🏆 Testing Achievement System...")

        player = Player(100, 100)
        achievement_manager = player.achievement_manager

        # Test achievement triggering
        self._test_achievement_triggers(player)

        # Test progressive achievements
        self._test_progressive_achievements(player)

        # Test achievement chains
        self._test_achievement_chains(player)

        # Test achievement rewards
        self._test_achievement_rewards(player)

        self.test_results["achievement_system"] = True

    def _test_achievement_triggers(self, player):
        """Test that achievements trigger correctly"""
        print("  Testing achievement triggers...")

        # Test level-based achievement
        player.stats["player_level"] = 2
        newly_unlocked = player.achievement_manager.check_achievements(player.stats)

        first_steps = player.achievement_manager.achievements.get("first_steps")
        if first_steps and not first_steps.unlocked:
            self.log_issue("Achievements", "first_steps achievement not triggered at level 2")

        # Test combat achievement
        player.stats["enemies_killed"] = 1
        newly_unlocked = player.achievement_manager.check_achievements(player.stats)

        first_blood = player.achievement_manager.achievements.get("first_blood")
        if first_blood and not first_blood.unlocked:
            self.log_issue("Achievements", "first_blood achievement not triggered after killing enemy")

    def _test_progressive_achievements(self, player):
        """Test progressive achievement system"""
        print("  Testing progressive achievements...")

        enemy_slayer = player.achievement_manager.achievements.get("enemy_slayer")
        if enemy_slayer:
            # Set progress
            player.stats["enemies_killed"] = 50
            player.achievement_manager.check_achievements(player.stats)

            if enemy_slayer.progress != 50:
                self.log_issue("Achievements", f"Progressive achievement progress not updated: {enemy_slayer.progress} vs 50")

            # Complete achievement
            player.stats["enemies_killed"] = 100
            player.achievement_manager.check_achievements(player.stats)

            if not enemy_slayer.unlocked:
                self.log_issue("Achievements", "Progressive achievement not unlocked when reaching max progress")

    def _test_achievement_chains(self, player):
        """Test achievement chain system"""
        print("  Testing achievement chains...")

        # Test that chain achievements are locked initially
        combat_master = player.achievement_manager.achievements.get("combat_master")
        if combat_master and combat_master.unlocked:
            self.log_issue("Achievements", "Chain achievement unlocked without prerequisites")

        # Test chain completion detection
        for chain_name, chain_data in ACHIEVEMENT_CHAINS.items():
            required_achievements = chain_data["achievements"]

            # Manually unlock all required achievements
            for ach_name in required_achievements:
                if ach_name in player.achievement_manager.achievements:
                    player.achievement_manager.achievements[ach_name].unlocked = True

            # Check achievements to trigger chain completion
            player.achievement_manager.check_achievements(player.stats)

            if chain_name not in player.achievement_manager.completed_chains:
                self.log_issue("Achievements", f"Achievement chain {chain_name} not completed despite all requirements met")

    def _test_achievement_rewards(self, player):
        """Test achievement reward system"""
        print("  Testing achievement rewards...")

        initial_xp = player.xp
        initial_skill_points = player.skill_tree.skill_points

        # Create a test achievement with rewards
        test_achievement = player.achievement_manager.achievements.get("first_steps")
        if test_achievement and not test_achievement.unlocked:
            # Trigger the achievement
            player.stats["player_level"] = 2
            newly_unlocked = player.achievement_manager.check_achievements(player.stats)

            # Check if rewards were applied
            if player.xp <= initial_xp:
                self.log_issue("Achievements", "Achievement XP reward not applied")
            if player.skill_tree.skill_points <= initial_skill_points:
                self.log_issue("Achievements", "Achievement skill point reward not applied")

    def test_cross_system_interactions(self):
        """Test how all systems interact together"""
        print("🔄 Testing Cross-System Interactions...")

        player = Player(100, 100)

        # Test equipment + skill bonuses stacking
        self._test_stat_stacking(player)

        # Test save/load integration
        self._test_save_load_integration(player)

        # Test UI integration
        self._test_ui_integration(player)

        self.test_results["cross_system_interactions"] = True

    def _test_stat_stacking(self, player):
        """Test that equipment and skill bonuses stack correctly"""
        print("  Testing stat bonus stacking...")

        # Add equipment bonuses
        weapon = Equipment("weapon", "Test Weapon", "Common", 1, {"damage_bonus": 10, "critical_chance": 0.1})
        player.equipment_manager.equip_item(weapon)

        # Add skill bonuses
        player.skill_tree.add_skill_points(5)
        player.skill_tree.upgrade_skill("critical_strike")  # Adds critical chance
        player.skill_tree.upgrade_skill("weapon_mastery")   # Adds damage bonus

        # Test combined critical chance
        total_crit = player.get_critical_chance()
        equipment_crit = player.equipment_manager.get_total_stat_bonus("critical_chance")
        skill_crit = player.skill_tree.get_total_bonus("critical_chance")
        expected_crit = equipment_crit + skill_crit

        if abs(total_crit - expected_crit) > 0.001:
            self.log_issue("Cross-System", f"Critical chance stacking incorrect: {total_crit} vs {expected_crit}")

        # Test combined damage (more complex due to multiplicative bonuses)
        total_damage = player.get_effective_damage()
        equipment_damage = player.equipment_manager.get_total_stat_bonus("damage_bonus")
        skill_damage_mult = player.skill_tree.get_total_bonus("damage_bonus")
        expected_damage = (player.damage + equipment_damage) * (1.0 + skill_damage_mult)

        if abs(total_damage - expected_damage) > 0.001:
            self.log_issue("Cross-System", f"Damage stacking incorrect: {total_damage} vs {expected_damage}")

    def _test_save_load_integration(self, player):
        """Test save/load functionality for all progression systems"""
        print("  Testing save/load integration...")

        # Use a fresh player to avoid interference from previous tests
        test_player = Player(100, 100)

        # Set up complex progression state
        test_player.skill_tree.add_skill_points(5)
        test_player.skill_tree.upgrade_skill("critical_strike")

        weapon = Equipment("weapon", "Save Test", "Rare", 2, {"damage_bonus": 15})
        test_player.equipment_manager.equip_item(weapon)

        test_player.stats["enemies_killed"] = 25
        test_player.achievement_manager.check_achievements(test_player.stats)

        # Save progression data
        progression_data = test_player.get_progression_data()

        # Create new player and load data
        new_player = Player(100, 100)
        new_player.load_progression_data(progression_data)

        # Verify data was preserved
        actual_level = new_player.skill_tree.skills["critical_strike"].current_level
        if actual_level != 1:
            self.log_issue("Save/Load", f"Skill levels not preserved: got {actual_level}, expected 1")

        if not new_player.equipment_manager.equipped["weapon"]:
            self.log_issue("Save/Load", "Equipped items not preserved")
        elif new_player.equipment_manager.equipped["weapon"].name != "Save Test":
            self.log_issue("Save/Load", "Equipment data not preserved correctly")

        if new_player.stats["enemies_killed"] != 25:
            self.log_issue("Save/Load", "Achievement stats not preserved")

    def _test_ui_integration(self, player):
        """Test UI integration with progression systems"""
        print("  Testing UI integration...")

        # Test that effective stats are calculated correctly for UI
        weapon = Equipment("weapon", "UI Test", "Epic", 3, {"damage_bonus": 20})
        armor = Equipment("armor", "UI Test", "Epic", 2, {"health_bonus": 40})

        player.equipment_manager.equip_item(weapon)
        player.equipment_manager.equip_item(armor)

        # Check effective stats methods exist and work
        try:
            effective_damage = player.get_effective_damage()
            effective_health = player.get_effective_max_health()
            effective_speed = player.get_effective_speed()
            effective_fire_rate = player.get_effective_fire_rate()

            if effective_damage <= player.damage:
                self.log_issue("UI", "Effective damage not higher than base damage")
            if effective_health <= player.max_health:
                self.log_issue("UI", "Effective max health not higher than base health")

        except Exception as e:
            self.log_issue("UI", f"Error calculating effective stats: {e}")

    def test_game_balance_and_edge_cases(self):
        """Test edge cases and balance issues"""
        print("⚖️ Testing Game Balance and Edge Cases...")

        player = Player(100, 100)

        # Test maximum level scenarios
        self._test_max_level_scenarios(player)

        # Test stat caps and limits
        self._test_stat_caps(player)

        # Test overflow/underflow protection
        self._test_overflow_protection(player)

        self.test_results["balance_and_edge_cases"] = True

    def _test_max_level_scenarios(self, player):
        """Test maximum level scenarios"""
        print("  Testing maximum level scenarios...")

        # Test max skill levels
        player.skill_tree.add_skill_points(100)
        for skill_name, skill in player.skill_tree.skills.items():
            if skill.unlocked:
                for _ in range(skill.max_level):
                    player.skill_tree.upgrade_skill(skill_name)

                if skill.current_level != skill.max_level:
                    self.log_issue("Balance", f"Skill {skill_name} not at max level: {skill.current_level}/{skill.max_level}")

                # Try to upgrade beyond max
                if player.skill_tree.upgrade_skill(skill_name):
                    self.log_issue("Balance", f"Skill {skill_name} upgraded beyond max level")

        # Test max equipment level
        equipment = Equipment("weapon", "Max Test", "Common", 1, {"damage_bonus": 10})
        for _ in range(20):  # Try to upgrade beyond max
            if not equipment.upgrade():
                break

        if equipment.level > 10:  # Max equipment level is 10
            self.log_issue("Balance", f"Equipment upgraded beyond max level: {equipment.level}")

    def _test_stat_caps(self, player):
        """Test stat caps and limits"""
        print("  Testing stat caps and limits...")

        # Test damage reduction cap (should be 90%)
        armor1 = Equipment("armor", "Tank1", "Epic", 10, {"damage_reduction": 0.5})
        armor2 = Equipment("weapon", "Tank2", "Epic", 10, {"damage_reduction": 0.5})  # Weapon with armor stat for testing

        player.equipment_manager.equip_item(armor1)
        # Can't equip two armors, so test with skills
        player.skill_tree.add_skill_points(20)
        for _ in range(5):
            player.skill_tree.upgrade_skill("armor_mastery")
            player.skill_tree.upgrade_skill("damage_resistance")

        damage_reduction = player.get_damage_reduction()
        if damage_reduction > 0.9:
            self.log_issue("Balance", f"Damage reduction exceeds cap: {damage_reduction}")

        # Test fire rate minimum (should be 100ms)
        weapon = Equipment("weapon", "Speed", "Epic", 10, {"fire_rate_bonus": 1000})
        player.equipment_manager.equip_item(weapon)

        fire_rate = player.get_effective_fire_rate()
        if fire_rate < 100:
            self.log_issue("Balance", f"Fire rate below minimum: {fire_rate}")

    def _test_overflow_protection(self, player):
        """Test protection against overflow/underflow"""
        print("  Testing overflow protection...")

        # Test with extreme values
        extreme_equipment = Equipment("weapon", "Extreme", "Epic", 10, {
            "damage_bonus": 999999,
            "critical_chance": 999999,
            "health_bonus": 999999
        })

        player.equipment_manager.equip_item(extreme_equipment)

        try:
            # These should not crash or produce invalid results
            damage = player.get_effective_damage()
            health = player.get_effective_max_health()
            crit = player.get_critical_chance()

            # Check for reasonable bounds
            if damage < 0 or damage > 1000000:
                self.log_issue("Balance", f"Extreme damage value: {damage}", "WARNING")
            if health < 0 or health > 1000000:
                self.log_issue("Balance", f"Extreme health value: {health}", "WARNING")
            if crit < 0 or crit > 100:  # 100% crit should be reasonable max
                self.log_issue("Balance", f"Extreme critical chance: {crit}", "WARNING")

        except Exception as e:
            self.log_issue("Balance", f"Overflow caused crash: {e}")

    def run_comprehensive_analysis(self):
        """Run all tests and provide comprehensive report"""
        print("🚀 Starting Comprehensive Character Progression Analysis...\n")

        try:
            pygame.init()  # Required for some components

            # Run all test categories
            self.test_equipment_system_integration()
            print()
            self.test_skill_tree_system_validation()
            print()
            self.test_achievement_system_integration()
            print()
            self.test_cross_system_interactions()
            print()
            self.test_game_balance_and_edge_cases()
            print()

            # Generate comprehensive report
            self._generate_report()

        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            pygame.quit()

    def _generate_report(self):
        """Generate comprehensive analysis report"""
        print("📊 COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 50)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)

        print(f"Tests Completed: {passed_tests}/{total_tests}")
        print(f"Issues Found: {len(self.issues_found)}")
        print(f"Warnings: {len(self.warnings)}")
        print()

        if self.issues_found:
            print("🔴 CRITICAL ISSUES:")
            for issue in self.issues_found:
                print(f"  [{issue['category']}] {issue['description']}")
            print()

        if self.warnings:
            print("🟡 WARNINGS:")
            for warning in self.warnings:
                print(f"  [{warning['category']}] {warning['description']}")
            print()

        if not self.issues_found and not self.warnings:
            print("🎉 NO ISSUES FOUND!")
            print("✨ All progression systems are working correctly!")
        else:
            print(f"⚠️  Found {len(self.issues_found)} critical issues and {len(self.warnings)} warnings")
            print("🔧 See analysis output above for details on each issue")

def main():
    """Run the comprehensive progression analysis"""
    analyzer = ProgressionAnalyzer()
    analyzer.run_comprehensive_analysis()

if __name__ == "__main__":
    main()
