#!/usr/bin/env python3
"""
Test script to verify equipment and skill system fixes
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.equipment import Equipment, EquipmentManager
from progression.skill_tree import SkillTree

def test_equipment_health_bonus():
    """Test that equipment health bonuses are properly applied"""
    print("🧪 Testing Equipment Health Bonus System...")
    
    # Create a player
    player = Player(100, 100)
    initial_max_health = player.max_health
    print(f"  Initial max health: {initial_max_health}")
    
    # Create armor with health bonus
    armor = Equipment("armor", "Health Armor", "Common", 1, {"health_bonus": 50})
    print(f"  Created armor with +{armor.get_stat_bonus('health_bonus')} health")
    
    # Equip the armor
    player.equipment_manager.equip_item(armor)
    
    # Check effective max health
    effective_max_health = player.get_effective_max_health()
    print(f"  Effective max health after equipping armor: {effective_max_health}")
    
    # Verify the bonus is applied
    expected_health = initial_max_health + armor.get_stat_bonus('health_bonus')
    assert effective_max_health == expected_health, f"Expected {expected_health}, got {effective_max_health}"
    
    print("  ✅ Equipment health bonus working correctly!")
    return True

def test_equipment_regeneration():
    """Test that equipment regeneration is properly applied"""
    print("🧪 Testing Equipment Regeneration System...")
    
    # Create a player
    player = Player(100, 100)
    
    # Damage the player
    player.health = 50
    print(f"  Player health reduced to: {player.health}")
    
    # Create armor with regeneration
    armor = Equipment("armor", "Regen Armor", "Common", 1, {"regeneration": 5})
    print(f"  Created armor with +{armor.get_stat_bonus('regeneration')} regeneration")
    
    # Equip the armor
    player.equipment_manager.equip_item(armor)
    
    # Simulate multiple update cycles to trigger regeneration
    initial_health = player.health
    for i in range(70):  # Should trigger regeneration after 60 frames
        player.apply_skill_effects()
    
    print(f"  Health after regeneration cycles: {player.health}")
    
    # Verify regeneration occurred
    assert player.health > initial_health, f"Health should have increased from {initial_health} to {player.health}"
    
    print("  ✅ Equipment regeneration working correctly!")
    return True

def test_skill_tree_upgrade():
    """Test that skill tree upgrades work correctly"""
    print("🧪 Testing Skill Tree Upgrade System...")
    
    # Create a skill tree
    skill_tree = SkillTree()
    
    # Add skill points
    skill_tree.add_skill_points(5)
    print(f"  Added 5 skill points, total: {skill_tree.skill_points}")
    
    # Check if critical strike can be upgraded
    can_upgrade = skill_tree.can_upgrade_skill("critical_strike")
    print(f"  Can upgrade critical_strike: {can_upgrade}")
    
    # Upgrade critical strike
    if can_upgrade:
        success = skill_tree.upgrade_skill("critical_strike")
        print(f"  Upgrade critical_strike result: {success}")
        print(f"  Skill points after upgrade: {skill_tree.skill_points}")
        print(f"  Critical strike level: {skill_tree.skills['critical_strike'].current_level}")
        
        # Check bonus
        crit_bonus = skill_tree.get_total_bonus("critical_chance")
        print(f"  Critical chance bonus: {crit_bonus}")
        
        assert success, "Skill upgrade should have succeeded"
        assert skill_tree.skill_points == 4, "Should have 4 skill points remaining"
        assert crit_bonus > 0, "Should have critical chance bonus"
    
    print("  ✅ Skill tree upgrade working correctly!")
    return True

def test_integrated_systems():
    """Test that equipment and skills work together"""
    print("🧪 Testing Integrated Equipment and Skill Systems...")
    
    # Create a player
    player = Player(100, 100)
    
    # Add skill points and upgrade a skill
    player.skill_tree.add_skill_points(3)
    player.skill_tree.upgrade_skill("critical_strike")
    
    # Equip weapon with critical chance
    weapon = Equipment("weapon", "Crit Sword", "Rare", 2, {"critical_chance": 0.1, "damage_bonus": 15})
    player.equipment_manager.equip_item(weapon)
    
    # Check combined bonuses
    total_crit_chance = player.get_critical_chance()
    total_damage = player.get_effective_damage()
    
    print(f"  Total critical chance (skill + equipment): {total_crit_chance}")
    print(f"  Total effective damage: {total_damage}")
    
    # Verify bonuses are combined
    skill_crit = player.skill_tree.get_total_bonus("critical_chance")
    equipment_crit = player.equipment_manager.get_total_stat_bonus("critical_chance")
    expected_crit = skill_crit + equipment_crit
    
    assert abs(total_crit_chance - expected_crit) < 0.001, f"Expected {expected_crit}, got {total_crit_chance}"
    assert total_damage > player.damage, "Effective damage should be higher than base damage"
    
    print("  ✅ Integrated systems working correctly!")
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Equipment and Skill System Tests...\n")
    
    try:
        # Initialize pygame (required for some components)
        pygame.init()
        
        # Run tests
        tests = [
            test_equipment_health_bonus,
            test_equipment_regeneration,
            test_skill_tree_upgrade,
            test_integrated_systems
        ]
        
        passed = 0
        for test in tests:
            try:
                if test():
                    passed += 1
                print()
            except Exception as e:
                print(f"  ❌ Test failed: {e}")
                print()
        
        print(f"📊 Test Results: {passed}/{len(tests)} tests passed")
        
        if passed == len(tests):
            print("🎉 All tests passed! Equipment and skill systems are working correctly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
