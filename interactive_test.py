#!/usr/bin/env python3
"""
Interactive test script to thoroughly investigate the persistent game issues.
This script will run the actual game and test each system interactively.
"""

import pygame
import sys
import os
import time

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.equipment import Equipment, EquipmentManager
from progression.skill_tree import SkillTree
from ui.ui_elements import UpgradeScreen
from utils.constants import *
from game import Game

def test_skill_tree_click_detection():
    """Test skill tree click detection in actual UI"""
    print("🧪 Testing Skill Tree Click Detection...")
    
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Skill Tree Test")
    
    # Create upgrade screen and player
    upgrade_screen = UpgradeScreen(800, 600)
    player = Player(100, 100)
    player.skill_tree.add_skill_points(5)
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "skills"
    
    print(f"  Player has {player.skill_tree.skill_points} skill points")
    
    # Draw the skills tab to populate skill_buttons
    upgrade_screen._draw_skills_tab(screen)
    
    print(f"  Skill buttons populated: {len(upgrade_screen.skill_buttons)}")
    print(f"  Available skills: {list(upgrade_screen.skill_buttons.keys())}")
    
    # Test if skill buttons have valid rectangles
    for skill_name, rect in upgrade_screen.skill_buttons.items():
        print(f"    {skill_name}: rect={rect}")
        if rect.width <= 0 or rect.height <= 0:
            print(f"    ❌ Invalid rectangle for {skill_name}")
        else:
            print(f"    ✅ Valid rectangle for {skill_name}")
    
    # Test click detection logic
    test_skill = "Critical Strike"
    if test_skill in upgrade_screen.skill_buttons:
        rect = upgrade_screen.skill_buttons[test_skill]
        test_pos = rect.center
        
        # Create a mock mouse click event
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=test_pos)
        
        # Test if the skill can be upgraded
        can_upgrade = player.skill_tree.can_upgrade_skill(test_skill)
        print(f"  Can upgrade {test_skill}: {can_upgrade}")
        
        # Test the click handling
        result = upgrade_screen._handle_skills_click(mock_event, player)
        print(f"  Click handling result: {result}")
        
        if result:
            print(f"  ✅ Skill click detection working")
            print(f"  Skill points after click: {player.skill_tree.skill_points}")
        else:
            print(f"  ❌ Skill click detection failed")
    
    pygame.quit()
    print("  ✅ Skill tree click detection test completed\n")

def test_equipment_generation_thoroughly():
    """Test equipment generation with 20+ items"""
    print("🧪 Testing Equipment Generation (20+ items)...")
    
    equipment_manager = EquipmentManager()
    zero_stat_items = []
    
    for i in range(25):
        equipment = equipment_manager.generate_random_equipment("weapon", player_level=5)
        
        print(f"  Equipment {i+1}: {equipment.get_display_name()}")
        
        has_zero_stats = False
        total_effective_value = 0
        
        for stat_name, base_value in equipment.stats.items():
            effective_value = equipment.get_stat_bonus(stat_name)
            total_effective_value += effective_value
            print(f"    {stat_name}: base={base_value}, effective=+{effective_value}")
            
            if effective_value <= 0:
                has_zero_stats = True
                print(f"    ❌ Found zero/negative stat: {stat_name} = {effective_value}")
        
        if has_zero_stats:
            zero_stat_items.append(equipment)
            print(f"    ❌ Equipment has zero stats!")
        elif total_effective_value < 0.1:
            zero_stat_items.append(equipment)
            print(f"    ❌ Equipment has negligible total stats: {total_effective_value}")
        else:
            print(f"    ✅ Equipment has meaningful stats (total: {total_effective_value:.2f})")
    
    print(f"\n  Summary: {len(zero_stat_items)} out of 25 items had zero/negligible stats")
    
    if zero_stat_items:
        print("  ❌ Equipment generation still producing useless items")
        for item in zero_stat_items:
            print(f"    - {item.get_display_name()}: {item.stats}")
    else:
        print("  ✅ All equipment has meaningful stats")
    
    print("  ✅ Equipment generation test completed\n")

def test_ui_layout_done_button():
    """Test UI layout and Done button positioning"""
    print("🧪 Testing UI Layout and Done Button Position...")
    
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    
    # Create upgrade screen
    upgrade_screen = UpgradeScreen(800, 600)
    player = Player(100, 100)
    
    # Add some equipment to inventory to test overlap
    for i in range(10):
        equipment = Equipment("weapon", f"Test Weapon {i}", "Common", 1, {"damage_bonus": 10})
        player.equipment_manager.add_to_inventory(equipment)
    
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "equipment"
    
    # Draw the equipment tab to populate inventory_items
    upgrade_screen._draw_equipment_tab(screen)
    
    print(f"  Done button position: {upgrade_screen.done_button.rect}")
    print(f"  Screen height: {screen.get_height()}")
    print(f"  Inventory items: {len(upgrade_screen.inventory_items)}")
    
    # Check if Done button overlaps with inventory items
    done_rect = upgrade_screen.done_button.rect
    overlaps = []
    
    for item_index, item_data in upgrade_screen.inventory_items.items():
        item_rect = item_data["rect"]
        if done_rect.colliderect(item_rect):
            overlaps.append(item_index)
            print(f"    ❌ Done button overlaps with inventory item {item_index}")
            print(f"      Done button: {done_rect}")
            print(f"      Item rect: {item_rect}")
    
    if overlaps:
        print(f"  ❌ Done button overlaps with {len(overlaps)} inventory items")
    else:
        print(f"  ✅ Done button does not overlap with inventory items")
    
    # Check if Done button is at the bottom of the screen
    bottom_margin = screen.get_height() - (done_rect.y + done_rect.height)
    print(f"  Done button bottom margin: {bottom_margin}px")
    
    if bottom_margin < 10:
        print(f"  ✅ Done button is near the bottom of the screen")
    else:
        print(f"  ⚠️ Done button could be moved closer to the bottom")
    
    pygame.quit()
    print("  ✅ UI layout test completed\n")

def test_actual_game_interaction():
    """Test by running the actual game briefly"""
    print("🧪 Testing Actual Game Interaction...")
    
    try:
        # This will test if the game starts without errors
        game = Game()
        print("  ✅ Game initialized successfully")
        
        # Test if we can access the upgrade screen
        if hasattr(game, 'upgrade_screen'):
            print("  ✅ Upgrade screen accessible")
        else:
            print("  ❌ Upgrade screen not accessible")
        
        # Test if skill notifications work
        if hasattr(game, 'skill_notifications'):
            print("  ✅ Skill notifications system accessible")
        else:
            print("  ❌ Skill notifications system not accessible")
        
    except Exception as e:
        print(f"  ❌ Game initialization failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("  ✅ Actual game interaction test completed\n")

def main():
    """Run comprehensive investigation"""
    print("🔍 COMPREHENSIVE INVESTIGATION OF PERSISTENT ISSUES\n")
    print("=" * 60)
    
    try:
        test_skill_tree_click_detection()
        test_equipment_generation_thoroughly()
        test_ui_layout_done_button()
        test_actual_game_interaction()
        
        print("🎯 INVESTIGATION COMPLETED")
        print("=" * 60)
        print("Check the output above for specific issues that need fixing.")
        
    except Exception as e:
        print(f"❌ Investigation failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
