#!/usr/bin/env python3
"""
Debug skill click handling step by step
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from ui.ui_elements import UpgradeScreen

def debug_skill_click():
    """Debug skill click step by step"""
    print("🔍 Debugging Skill Click Handling...")
    
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
    
    # Draw the skills tab to populate skill_buttons
    upgrade_screen._draw_skills_tab(screen)
    
    # Test clicking on Critical Strike
    test_skill = "Critical Strike"
    if test_skill in upgrade_screen.skill_buttons:
        rect = upgrade_screen.skill_buttons[test_skill]
        test_pos = rect.center
        
        print(f"  Testing skill: {test_skill}")
        print(f"  Button rect: {rect}")
        print(f"  Click position: {test_pos}")
        
        # Create a mock mouse click event
        mock_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=test_pos)
        
        print(f"  Mock event: {mock_event}")
        print(f"  Event type: {mock_event.type}")
        print(f"  Event button: {mock_event.button}")
        print(f"  Event pos: {mock_event.pos}")
        
        # Step through the click handling manually
        print("\n  Step-by-step click handling:")
        
        # Check event type and button
        if mock_event.type == pygame.MOUSEBUTTONDOWN and mock_event.button == 1:
            print("    ✅ Event type and button check passed")
            
            mouse_pos = mock_event.pos
            print(f"    Mouse position: {mouse_pos}")
            
            # Check if any skill was clicked
            for skill_display_name, skill_rect in upgrade_screen.skill_buttons.items():
                if skill_rect.collidepoint(mouse_pos):
                    print(f"    ✅ Found clicked skill: {skill_display_name}")
                    
                    # Convert display name to internal key
                    skill_internal_key = upgrade_screen._get_skill_internal_key(skill_display_name, player.skill_tree)
                    print(f"    Internal key: {skill_internal_key}")
                    
                    if skill_internal_key:
                        print("    ✅ Internal key found")
                        
                        # Check if skill can be upgraded using internal key
                        can_upgrade = player.skill_tree.can_upgrade_skill(skill_internal_key)
                        print(f"    Can upgrade: {can_upgrade}")
                        
                        if can_upgrade:
                            print("    ✅ Skill can be upgraded")
                            
                            # Try to upgrade
                            initial_points = player.skill_tree.skill_points
                            upgrade_result = player.skill_tree.upgrade_skill(skill_internal_key)
                            final_points = player.skill_tree.skill_points
                            
                            print(f"    Upgrade result: {upgrade_result}")
                            print(f"    Points: {initial_points} -> {final_points}")
                            
                            if upgrade_result:
                                print("    ✅ Skill upgraded successfully")
                                return f"skill_{skill_display_name}"
                            else:
                                print("    ❌ Skill upgrade failed")
                        else:
                            print("    ❌ Skill cannot be upgraded")
                    else:
                        print("    ❌ Internal key not found")
                    break
            else:
                print("    ❌ No skill clicked")
        else:
            print("    ❌ Event type or button check failed")
        
        # Now test the actual method
        print("\n  Testing actual _handle_skills_click method:")
        initial_points = player.skill_tree.skill_points
        result = upgrade_screen._handle_skills_click(mock_event, player)
        final_points = player.skill_tree.skill_points
        
        print(f"    Method result: {result}")
        print(f"    Points: {initial_points} -> {final_points}")
    
    pygame.quit()

if __name__ == "__main__":
    debug_skill_click()
