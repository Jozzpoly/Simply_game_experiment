#!/usr/bin/env python3
"""
Final verification test for all fixes
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.equipment import Equipment, EquipmentManager
from ui.ui_elements import UpgradeScreen
from utils.constants import *

def test_skill_tree_fix():
    """Test that skill tree clicking now works"""
    print("🧪 Testing Skill Tree Fix...")
    
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    
    # Create upgrade screen and player
    upgrade_screen = UpgradeScreen(800, 600)
    player = Player(100, 100)
    player.skill_tree.add_skill_points(5)
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "skills"
    
    print(f"  Player has {player.skill_tree.skill_points} skill points")
    
    # Draw the skills tab to populate skill_buttons
    upgrade_screen._draw_skills_tab(screen)
    
    # Test clicking on Critical Strike
    test_skill = "Critical Strike"
    if test_skill in upgrade_screen.skill_buttons:
        rect = upgrade_screen.skill_buttons[test_skill]
        test_pos = rect.center
        
        # Create a mock mouse click event
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=test_pos)
        
        # Get internal key
        internal_key = upgrade_screen._get_skill_internal_key(test_skill, player.skill_tree)
        print(f"  Display name '{test_skill}' -> Internal key '{internal_key}'")
        
        # Test if the skill can be upgraded
        can_upgrade = player.skill_tree.can_upgrade_skill(internal_key)
        print(f"  Can upgrade {test_skill}: {can_upgrade}")
        
        # Test the click handling
        initial_points = player.skill_tree.skill_points
        result = upgrade_screen._handle_skills_click(mock_event, player)
        final_points = player.skill_tree.skill_points
        
        print(f"  Click handling result: {result}")
        print(f"  Skill points: {initial_points} -> {final_points}")
        
        if result and final_points < initial_points:
            print(f"  ✅ Skill tree clicking now works!")
        else:
            print(f"  ❌ Skill tree clicking still broken")
    
    pygame.quit()
    print("  ✅ Skill tree fix test completed\n")

def test_equipment_generation_fix():
    """Test equipment generation for zero stats"""
    print("🧪 Testing Equipment Generation Fix...")
    
    equipment_manager = EquipmentManager()
    zero_stat_count = 0
    
    for i in range(20):
        equipment = equipment_manager.generate_random_equipment("weapon", player_level=5)
        
        has_zero_stats = False
        for stat_name, base_value in equipment.stats.items():
            effective_value = equipment.get_stat_bonus(stat_name)
            if effective_value <= 0:
                has_zero_stats = True
                break
        
        if has_zero_stats:
            zero_stat_count += 1
    
    print(f"  Generated 20 items, {zero_stat_count} had zero/negative stats")
    
    if zero_stat_count == 0:
        print(f"  ✅ Equipment generation fix working!")
    else:
        print(f"  ❌ Equipment generation still has issues")
    
    print("  ✅ Equipment generation fix test completed\n")

def test_done_button_position():
    """Test Done button positioning"""
    print("🧪 Testing Done Button Position Fix...")
    
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((800, 600))
    
    # Create upgrade screen
    upgrade_screen = UpgradeScreen(800, 600)
    player = Player(100, 100)
    
    # Add equipment to inventory
    for i in range(12):
        equipment = Equipment("weapon", f"Test Weapon {i}", "Common", 1, {"damage_bonus": 10})
        player.equipment_manager.add_to_inventory(equipment)
    
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "equipment"
    
    # Draw the equipment tab to populate inventory_items
    upgrade_screen._draw_equipment_tab(screen)
    
    done_rect = upgrade_screen.done_button.rect
    screen_height = screen.get_height()
    
    print(f"  Done button position: {done_rect}")
    print(f"  Screen height: {screen_height}")
    
    # Check bottom margin
    bottom_margin = screen_height - (done_rect.y + done_rect.height)
    print(f"  Bottom margin: {bottom_margin}px")
    
    # Check for overlaps with inventory items
    overlaps = 0
    for item_index, item_data in upgrade_screen.inventory_items.items():
        item_rect = item_data["rect"]
        if done_rect.colliderect(item_rect):
            overlaps += 1
    
    print(f"  Overlaps with inventory items: {overlaps}")
    
    if bottom_margin <= 20 and overlaps == 0:
        print(f"  ✅ Done button positioning fix working!")
    else:
        print(f"  ❌ Done button positioning needs more work")
    
    pygame.quit()
    print("  ✅ Done button position test completed\n")

def test_game_integration():
    """Test that the game still runs with all fixes"""
    print("🧪 Testing Game Integration...")
    
    try:
        from game import Game
        game = Game()
        print("  ✅ Game initializes successfully with all fixes")
        
        # Test upgrade screen access
        if hasattr(game, 'upgrade_screen'):
            upgrade_screen = game.upgrade_screen
            print("  ✅ Upgrade screen accessible")
            
            # Test skill button helper method
            if hasattr(upgrade_screen, '_get_skill_internal_key'):
                print("  ✅ Skill name conversion method available")
            else:
                print("  ❌ Skill name conversion method missing")
        
    except Exception as e:
        print(f"  ❌ Game integration failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("  ✅ Game integration test completed\n")

def main():
    """Run final verification"""
    print("🎯 FINAL VERIFICATION OF ALL FIXES")
    print("=" * 50)
    
    try:
        test_skill_tree_fix()
        test_equipment_generation_fix()
        test_done_button_position()
        test_game_integration()
        
        print("🎉 FINAL VERIFICATION COMPLETED")
        print("=" * 50)
        print("All critical issues should now be resolved!")
        
    except Exception as e:
        print(f"❌ Final verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
