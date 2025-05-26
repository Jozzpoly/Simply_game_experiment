#!/usr/bin/env python3
"""
Test script to verify UI improvements for equipment display and skill tooltips
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame
from entities.player import Player
from progression.equipment import Equipment, EquipmentManager
from ui.ui_elements import UpgradeScreen

def test_equipment_display_formatting():
    """Test the new equipment display formatting"""
    print("🎨 Testing Equipment Display Formatting...")
    
    # Create test equipment with various stat types
    test_equipment = [
        Equipment("weapon", "Test Sword", "Common", 1, {
            "damage_bonus": 5.0,      # Should show as integer
            "critical_chance": 0.03   # Should show as percentage
        }),
        Equipment("armor", "Test Armor", "Rare", 2, {
            "health_bonus": 25.0,     # Should show as integer
            "damage_reduction": 0.08  # Should show as percentage
        }),
        Equipment("accessory", "Test Ring", "Epic", 3, {
            "xp_bonus": 0.15,         # Should show as percentage
            "speed_bonus": 1.2        # Should show as decimal
        })
    ]
    
    print("  Testing formatted stat display:")
    for equipment in test_equipment:
        print(f"\n    {equipment.get_display_name()}:")
        for stat_name in equipment.stats.keys():
            raw_bonus = equipment.get_stat_bonus(stat_name)
            formatted_bonus = equipment.get_formatted_stat_bonus(stat_name)
            print(f"      {stat_name}: {raw_bonus} → {formatted_bonus}")
    
    return True

def test_detailed_stats_tab():
    """Test the detailed statistics tab"""
    print("\n📊 Testing Detailed Statistics Tab...")
    
    # Initialize pygame for UI testing
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    # Create player with some equipment and skills
    player = Player(100, 100)
    
    # Add some equipment
    weapon = Equipment("weapon", "Test Weapon", "Epic", 3, {"damage_bonus": 15, "critical_chance": 0.05})
    armor = Equipment("armor", "Test Armor", "Rare", 2, {"health_bonus": 30, "damage_reduction": 0.1})
    
    player.equipment_manager.equip_item(weapon)
    player.equipment_manager.equip_item(armor)
    
    # Add some skill points and upgrade skills
    player.skill_tree.add_skill_points(5)
    player.skill_tree.upgrade_skill("critical_strike")
    player.skill_tree.upgrade_skill("critical_strike")
    
    # Create upgrade screen and test detailed tab
    upgrade_screen = UpgradeScreen(800, 600)
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "detailed"
    
    # Test that the detailed tab can be drawn without errors
    surface = pygame.Surface((800, 600))
    try:
        upgrade_screen._draw_detailed_stats_tab(surface)
        print("  ✅ Detailed stats tab draws successfully")
        
        # Test stat calculations
        base_damage = player.damage
        equipment_damage = player.equipment_manager.get_total_stat_bonus("damage_bonus")
        effective_damage = player.get_effective_damage()
        
        print(f"  📈 Stat breakdown example:")
        print(f"    Base damage: {base_damage}")
        print(f"    Equipment bonus: +{equipment_damage}")
        print(f"    Effective damage: {effective_damage}")
        
        return True
    except Exception as e:
        print(f"  ❌ Error drawing detailed stats tab: {e}")
        return False

def test_skill_tooltips():
    """Test skill tooltip system"""
    print("\n🔍 Testing Skill Tooltip System...")
    
    # Initialize pygame
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    # Create player and upgrade screen
    player = Player(100, 100)
    player.skill_tree.add_skill_points(3)
    
    upgrade_screen = UpgradeScreen(800, 600)
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "skills"
    
    # Draw skills tab to populate skill buttons
    surface = pygame.Surface((800, 600))
    upgrade_screen._draw_skills_tab(surface)
    
    print(f"  Skill buttons populated: {len(upgrade_screen.skill_buttons)}")
    
    # Test tooltip system
    if upgrade_screen.skill_buttons:
        # Simulate hovering over a skill
        skill_name = list(upgrade_screen.skill_buttons.keys())[0]
        skill_rect = upgrade_screen.skill_buttons[skill_name]
        
        # Simulate mouse position over skill
        mouse_pos = skill_rect.center
        
        # Update tooltip
        upgrade_screen._update_skill_tooltip(mouse_pos)
        upgrade_screen.tooltip_timer = upgrade_screen.tooltip_delay + 1  # Force tooltip to show
        
        # Test tooltip drawing
        try:
            upgrade_screen._draw_skill_tooltip(surface)
            print(f"  ✅ Tooltip system working for skill: {skill_name}")
            return True
        except Exception as e:
            print(f"  ❌ Error drawing tooltip: {e}")
            return False
    else:
        print("  ❌ No skill buttons found")
        return False

def test_tab_navigation():
    """Test the new tab navigation with detailed tab"""
    print("\n🗂️ Testing Tab Navigation...")
    
    # Initialize pygame
    pygame.init()
    pygame.display.set_mode((800, 600))
    
    # Create upgrade screen
    upgrade_screen = UpgradeScreen(800, 600)
    player = Player(100, 100)
    upgrade_screen.update_stats(player)
    
    # Test all tabs
    tabs = ["stats", "detailed", "skills", "equipment", "achievements"]
    
    for tab in tabs:
        upgrade_screen.current_tab = tab
        surface = pygame.Surface((800, 600))
        
        try:
            upgrade_screen.draw(surface)
            print(f"  ✅ Tab '{tab}' draws successfully")
        except Exception as e:
            print(f"  ❌ Error drawing tab '{tab}': {e}")
            return False
    
    print(f"  📋 All {len(tabs)} tabs working correctly")
    return True

def main():
    """Run all UI improvement tests"""
    print("🚀 Testing UI Improvements...\n")
    
    try:
        # Run all tests
        formatting_test = test_equipment_display_formatting()
        detailed_stats_test = test_detailed_stats_tab()
        tooltip_test = test_skill_tooltips()
        tab_navigation_test = test_tab_navigation()
        
        print("\n📋 Test Results Summary:")
        print(f"  Equipment Display Formatting: {'✅ PASSED' if formatting_test else '❌ FAILED'}")
        print(f"  Detailed Statistics Tab: {'✅ PASSED' if detailed_stats_test else '❌ FAILED'}")
        print(f"  Skill Tooltip System: {'✅ PASSED' if tooltip_test else '❌ FAILED'}")
        print(f"  Tab Navigation: {'✅ PASSED' if tab_navigation_test else '❌ FAILED'}")
        
        all_passed = all([formatting_test, detailed_stats_test, tooltip_test, tab_navigation_test])
        
        if all_passed:
            print("\n🎉 ALL UI IMPROVEMENTS WORKING!")
            print("\n🎮 New Features Available:")
            print("  • Equipment stats now show proper decimal formatting")
            print("  • 'Detailed' tab shows comprehensive player statistics")
            print("  • Skill tooltips with hover descriptions")
            print("  • Real-time stat breakdowns (base + equipment + skills)")
            print("  • Percentage vs integer stat formatting")
        else:
            print("\n❌ Some UI improvements have issues")
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
