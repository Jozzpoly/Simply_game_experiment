#!/usr/bin/env python3
"""
Comprehensive functional testing script for enhanced character progression features.
This script tests each feature systematically to verify functionality and identify issues.
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.skill_tree import SkillTree
from progression.equipment import EquipmentManager, Equipment
from progression.achievements import AchievementManager
from ui.ui_elements import UpgradeScreen
from utils.constants import *


def test_skill_synergies():
    """Test skill synergy system functionality"""
    print("🔧 Testing Skill Synergy System...")
    
    player = Player(100, 100)
    skill_tree = player.skill_tree
    
    # Add skill points for testing
    skill_tree.add_skill_points(10)
    
    # Test synergy requirements
    print("  ✓ Testing synergy requirements...")
    initial_synergies = skill_tree.get_active_synergies()
    assert len(initial_synergies) == 0, "Should have no active synergies initially"
    
    # Upgrade skills to activate critical_mastery synergy
    print("  ✓ Upgrading skills for critical_mastery synergy...")
    for _ in range(3):
        skill_tree.upgrade_skill("critical_strike")
    for _ in range(2):
        skill_tree.upgrade_skill("weapon_mastery")
    
    # Check synergy activation
    active_synergies = skill_tree.get_active_synergies()
    assert "critical_mastery" in active_synergies, "Critical mastery synergy should be active"
    
    # Test synergy bonuses
    synergy_bonuses = skill_tree.calculate_synergy_bonuses()
    assert "critical_damage_multiplier" in synergy_bonuses, "Should have critical damage multiplier bonus"
    assert synergy_bonuses["critical_damage_multiplier"] == 0.5, "Bonus should be 0.5"
    
    # Test potential synergies
    potential_synergies = skill_tree.get_potential_synergies()
    print(f"  ✓ Found {len(potential_synergies)} potential synergies")
    
    print("  ✅ Skill synergy system working correctly!")
    return True


def test_equipment_set_bonuses():
    """Test equipment set bonus system"""
    print("🛡️ Testing Equipment Set Bonus System...")
    
    player = Player(100, 100)
    equipment_manager = player.equipment_manager
    
    # Test no set bonus initially
    set_bonuses = equipment_manager.calculate_set_bonuses()
    assert len(set_bonuses) == 0, "Should have no set bonuses initially"
    
    # Create and equip two common items
    print("  ✓ Creating and equipping Common set items...")
    weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 5})
    armor = Equipment("armor", "Common Armor", "Common", 1, {"health_bonus": 10})
    
    equipment_manager.equip_item(weapon)
    equipment_manager.equip_item(armor)
    
    # Check set bonus activation
    set_bonuses = equipment_manager.calculate_set_bonuses()
    expected_bonuses = EQUIPMENT_SET_BONUSES["Common"]
    
    for stat, bonus in expected_bonuses.items():
        assert set_bonuses[stat] == bonus, f"Set bonus for {stat} should be {bonus}"
    
    # Test active set bonus info
    active_sets = equipment_manager.get_active_set_bonuses()
    assert "Common" in active_sets, "Common set should be active"
    assert active_sets["Common"]["count"] == 2, "Should have 2 common items"
    
    # Test total stat bonus includes set bonus
    total_damage = equipment_manager.get_total_stat_bonus("damage_bonus")
    expected_total = 5 + EQUIPMENT_SET_BONUSES["Common"]["damage_bonus"]
    assert total_damage == expected_total, f"Total damage should include set bonus: {expected_total}"
    
    print("  ✅ Equipment set bonus system working correctly!")
    return True


def test_advanced_achievements():
    """Test advanced achievement system with progressive and chain achievements"""
    print("🏆 Testing Advanced Achievement System...")
    
    player = Player(100, 100)
    achievement_manager = player.achievement_manager
    
    # Test progressive achievement
    print("  ✓ Testing progressive achievements...")
    enemy_slayer = achievement_manager.achievements["enemy_slayer"]
    
    # Check initial state
    assert enemy_slayer.achievement_type == "progressive", "Should be progressive achievement"
    assert enemy_slayer.progress == 0, "Should start with 0 progress"
    assert enemy_slayer.max_progress == 100, "Should have max progress of 100"
    
    # Update progress
    enemy_slayer.update_progress(25)
    assert enemy_slayer.progress == 25, "Progress should be 25"
    assert not enemy_slayer.unlocked, "Should not be unlocked yet"
    
    # Complete achievement
    enemy_slayer.update_progress(75)
    assert enemy_slayer.progress == 100, "Progress should be 100"
    
    # Test progress percentage
    assert enemy_slayer.get_progress_percentage() == 100.0, "Should be 100% complete"
    
    # Test chain achievements
    print("  ✓ Testing achievement chains...")
    combat_master = achievement_manager.achievements["combat_master"]
    
    # Should not be available initially
    unlocked_names = []
    assert not combat_master.is_available(unlocked_names), "Should not be available without prerequisites"
    
    # Make prerequisites available
    unlocked_names = ["boss_hunter", "enemy_slayer"]
    assert combat_master.is_available(unlocked_names), "Should be available with prerequisites"
    
    # Test chain completion tracking
    warrior_achievements = ACHIEVEMENT_CHAINS["warrior_path"]["achievements"]
    for ach_name in warrior_achievements:
        if ach_name in achievement_manager.achievements:
            achievement_manager.achievements[ach_name].unlocked = True
    
    achievement_manager.check_achievements({})
    assert "warrior_path" in achievement_manager.completed_chains, "Warrior path should be completed"
    
    print("  ✅ Advanced achievement system working correctly!")
    return True


def test_ui_enhancements():
    """Test UI enhancement functionality"""
    print("🎨 Testing UI Enhancements...")
    
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    player = Player(100, 100)
    upgrade_screen = UpgradeScreen(800, 600)
    upgrade_screen.player = player
    
    # Test equipment stats text generation
    print("  ✓ Testing equipment stats text generation...")
    equipment = Equipment("weapon", "Test Sword", "Common", 2, 
                         {"damage_bonus": 5, "fire_rate_bonus": 10, "critical_chance": 0.05})
    
    stats_text = upgrade_screen._get_equipment_stats_text(equipment)
    assert "Damage Bonus: +10" in stats_text, "Should show damage bonus with level multiplier"
    assert "Fire Rate Bonus: +20" in stats_text, "Should show fire rate bonus with level multiplier"
    
    # Test best item selection
    print("  ✓ Testing best item selection...")
    common_weapon = Equipment("weapon", "Common Sword", "Common", 1, {"damage_bonus": 5})
    rare_weapon = Equipment("weapon", "Rare Sword", "Rare", 2, {"damage_bonus": 8})
    
    player.equipment_manager.add_to_inventory(common_weapon)
    player.equipment_manager.add_to_inventory(rare_weapon)
    
    best_item = upgrade_screen._find_best_item_for_slot(player.equipment_manager, "weapon")
    assert best_item == rare_weapon, "Should select the rare weapon as best"
    
    print("  ✅ UI enhancements working correctly!")
    return True


def test_integration():
    """Test integration of all enhanced systems"""
    print("🔗 Testing System Integration...")
    
    player = Player(100, 100)
    
    # Set up complex progression state
    print("  ✓ Setting up complex progression state...")
    
    # Add skill points and activate synergies
    player.skill_tree.add_skill_points(10)
    for _ in range(3):
        player.skill_tree.upgrade_skill("critical_strike")
    for _ in range(2):
        player.skill_tree.upgrade_skill("weapon_mastery")
    
    # Equip equipment for set bonus
    weapon = Equipment("weapon", "Rare Sword", "Rare", 1, {"damage_bonus": 8})
    armor = Equipment("armor", "Rare Armor", "Rare", 1, {"health_bonus": 20})
    player.equipment_manager.equip_item(weapon)
    player.equipment_manager.equip_item(armor)
    
    # Update achievement progress
    player.stats["enemies_killed"] = 50
    player.achievement_manager.check_achievements(player.stats)
    
    # Verify all systems working together
    print("  ✓ Verifying system integration...")
    
    # Check synergies
    active_synergies = player.skill_tree.get_active_synergies()
    assert len(active_synergies) > 0, "Should have active synergies"
    
    # Check set bonuses
    set_bonuses = player.equipment_manager.get_active_set_bonuses()
    assert "Rare" in set_bonuses, "Should have rare set bonus"
    
    # Check achievement progress
    enemy_slayer = player.achievement_manager.achievements["enemy_slayer"]
    assert enemy_slayer.progress == 50, "Should have 50 enemies killed progress"
    
    # Test save/load integration
    print("  ✓ Testing save/load integration...")
    progression_data = player.get_progression_data()
    
    new_player = Player(100, 100)
    new_player.load_progression_data(progression_data)
    
    # Verify data preservation
    assert new_player.skill_tree.skills["critical_strike"].current_level == 3, "Skill level should be preserved"
    assert new_player.equipment_manager.equipped["weapon"].name == "Rare Sword", "Equipment should be preserved"
    assert new_player.stats["enemies_killed"] == 50, "Stats should be preserved"
    
    print("  ✅ System integration working correctly!")
    return True


def main():
    """Run comprehensive testing of enhanced features"""
    print("🚀 Starting Comprehensive Enhanced Features Testing")
    print("=" * 60)
    
    tests = [
        test_skill_synergies,
        test_equipment_set_bonuses,
        test_advanced_achievements,
        test_ui_enhancements,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test.__name__} failed!")
        except Exception as e:
            failed += 1
            print(f"❌ {test.__name__} failed with exception: {e}")
            import traceback
            traceback.print_exc()
    
    print("=" * 60)
    print(f"🎯 Testing Complete: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ All enhanced features are working correctly!")
        print("🎉 System is production-ready!")
    else:
        print("⚠️ Some issues found - see details above")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
