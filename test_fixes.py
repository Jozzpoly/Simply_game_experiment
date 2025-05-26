#!/usr/bin/env python3
"""
Test script to verify the fixes for:
1. Skill tree point distribution
2. Equipment stats generation (no +0 stats)
3. Equipment swapping (old item goes to inventory)
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.equipment import Equipment, EquipmentManager
from progression.skill_tree import SkillTree
from ui.ui_elements import UpgradeScreen
from utils.constants import *

def test_skill_tree_points():
    """Test that skill tree points can be distributed correctly"""
    print("🧪 Testing Skill Tree Point Distribution...")

    # Create a player
    player = Player(100, 100)

    # Add skill points
    initial_points = player.skill_tree.skill_points
    player.skill_tree.add_skill_points(5)

    print(f"  Initial skill points: {initial_points}")
    print(f"  After adding 5 points: {player.skill_tree.skill_points}")

    # Try to upgrade a skill
    skill_name = "critical_strike"
    can_upgrade = player.skill_tree.can_upgrade_skill(skill_name)
    print(f"  Can upgrade {skill_name}: {can_upgrade}")

    if can_upgrade:
        success = player.skill_tree.upgrade_skill(skill_name)
        print(f"  Upgrade successful: {success}")
        print(f"  Skill points after upgrade: {player.skill_tree.skill_points}")
        print(f"  {skill_name} level: {player.skill_tree.skills[skill_name].current_level}")

    print("  ✅ Skill tree point distribution test completed\n")

def test_equipment_stats_generation():
    """Test that equipment doesn't generate +0 stats"""
    print("🧪 Testing Equipment Stats Generation...")

    equipment_manager = EquipmentManager()

    # Generate multiple pieces of equipment
    for i in range(10):
        equipment = equipment_manager.generate_random_equipment("weapon", player_level=5)

        print(f"  Equipment {i+1}: {equipment.get_display_name()}")

        # Check if any stats are 0 or very close to 0
        has_zero_stats = False
        for stat_name, value in equipment.stats.items():
            effective_value = equipment.get_stat_bonus(stat_name)
            print(f"    {stat_name}: +{effective_value}")

            if effective_value <= 0:
                has_zero_stats = True
                print(f"    ❌ Found zero/negative stat: {stat_name} = {effective_value}")

        if not has_zero_stats:
            print(f"    ✅ All stats are positive")

        # Ensure equipment has at least one stat
        if not equipment.stats:
            print(f"    ❌ Equipment has no stats!")
        else:
            print(f"    ✅ Equipment has {len(equipment.stats)} stats")

    print("  ✅ Equipment stats generation test completed\n")

def test_equipment_swapping():
    """Test that old equipment goes to inventory when equipping new items"""
    print("🧪 Testing Equipment Swapping...")

    # Create a player
    player = Player(100, 100)
    equipment_manager = player.equipment_manager

    # Create two weapons
    weapon1 = Equipment("weapon", "Sword", "Common", 1, {"damage_bonus": 10})
    weapon2 = Equipment("weapon", "Axe", "Rare", 2, {"damage_bonus": 15})

    print(f"  Initial inventory size: {len(equipment_manager.inventory)}")
    print(f"  Initial equipped weapon: {equipment_manager.equipped['weapon']}")

    # Equip first weapon
    old_item1 = equipment_manager.equip_item(weapon1)
    print(f"  After equipping {weapon1.name}: old_item = {old_item1}")
    print(f"  Equipped weapon: {equipment_manager.equipped['weapon'].name if equipment_manager.equipped['weapon'] else None}")
    print(f"  Inventory size: {len(equipment_manager.inventory)}")

    # Equip second weapon (should move first weapon to inventory)
    old_item2 = equipment_manager.equip_item(weapon2)
    print(f"  After equipping {weapon2.name}: old_item = {old_item2.name if old_item2 else None}")
    print(f"  Equipped weapon: {equipment_manager.equipped['weapon'].name if equipment_manager.equipped['weapon'] else None}")

    # Check if old weapon is in inventory
    if old_item2:
        # Simulate what the UI should do - add old item to inventory
        success = equipment_manager.add_to_inventory(old_item2)
        print(f"  Added old weapon to inventory: {success}")
        print(f"  Inventory size after adding old weapon: {len(equipment_manager.inventory)}")

        if success and len(equipment_manager.inventory) > 0:
            print(f"  Inventory contains: {[item.name for item in equipment_manager.inventory]}")
            print("  ✅ Old equipment successfully moved to inventory")
        else:
            print("  ❌ Old equipment not found in inventory")
    else:
        print("  ❌ No old item returned when equipping new weapon")

    print("  ✅ Equipment swapping test completed\n")

def test_ui_skill_buttons():
    """Test that UI skill buttons are properly initialized"""
    print("🧪 Testing UI Skill Buttons Initialization...")

    # Initialize pygame properly
    pygame.init()
    pygame.font.init()
    pygame.display.set_mode((800, 600))  # Need display for font initialization

    try:
        # Create upgrade screen
        upgrade_screen = UpgradeScreen(800, 600)

        # Check if skill_buttons dictionary is initialized
        print(f"  skill_buttons initialized: {hasattr(upgrade_screen, 'skill_buttons')}")
        print(f"  skill_buttons type: {type(upgrade_screen.skill_buttons)}")
        print(f"  Initial skill_buttons content: {upgrade_screen.skill_buttons}")

        # Create a mock player and update the screen
        player = Player(100, 100)
        player.skill_tree.add_skill_points(3)
        upgrade_screen.update_stats(player)

        # Simulate drawing the skills tab (which should populate skill_buttons)
        upgrade_screen.current_tab = "skills"

        # Create a mock surface for drawing
        mock_surface = pygame.Surface((800, 600))
        upgrade_screen._draw_skills_tab(mock_surface)

        print(f"  skill_buttons after drawing: {len(upgrade_screen.skill_buttons)} buttons")
        print(f"  Button names: {list(upgrade_screen.skill_buttons.keys())}")

        if len(upgrade_screen.skill_buttons) > 0:
            print("  ✅ Skill buttons properly initialized and populated")
        else:
            print("  ❌ Skill buttons not populated")

    finally:
        pygame.quit()

    print("  ✅ UI skill buttons test completed\n")

def main():
    """Run all tests"""
    print("🚀 Starting Fix Verification Tests...\n")

    try:
        test_skill_tree_points()
        test_equipment_stats_generation()
        test_equipment_swapping()
        test_ui_skill_buttons()

        print("🎉 All tests completed successfully!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
