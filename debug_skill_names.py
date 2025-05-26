#!/usr/bin/env python3
"""
Debug script to check skill name mismatches
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.skill_tree import SkillTree
from ui.ui_elements import UpgradeScreen

def debug_skill_names():
    """Debug skill name mismatches"""
    print("🔍 Debugging Skill Name Mismatches...")
    
    # Create skill tree
    skill_tree = SkillTree()
    skill_tree.add_skill_points(5)
    
    print("Skills in skill_tree.skills dictionary:")
    for key, skill in skill_tree.skills.items():
        print(f"  Key: '{key}' -> Skill Name: '{skill.name}' -> Unlocked: {skill.unlocked}")
    
    print("\nTesting skill upgrade with different name formats:")
    
    # Test with internal key
    test_key = "critical_strike"
    can_upgrade_key = skill_tree.can_upgrade_skill(test_key)
    print(f"  Can upgrade '{test_key}': {can_upgrade_key}")
    
    # Test with display name
    test_name = "Critical Strike"
    can_upgrade_name = skill_tree.can_upgrade_skill(test_name)
    print(f"  Can upgrade '{test_name}': {can_upgrade_name}")
    
    # Check if skill is unlocked
    if test_key in skill_tree.skills:
        skill = skill_tree.skills[test_key]
        print(f"  Skill '{test_key}' details:")
        print(f"    - Unlocked: {skill.unlocked}")
        print(f"    - Current level: {skill.current_level}")
        print(f"    - Max level: {skill.max_level}")
        print(f"    - Prerequisites: {skill.prerequisites}")
    
    # Test UI skill buttons
    pygame.init()
    pygame.font.init()
    pygame.display.set_mode((800, 600))
    
    upgrade_screen = UpgradeScreen(800, 600)
    player = Player(100, 100)
    player.skill_tree.add_skill_points(5)
    upgrade_screen.update_stats(player)
    upgrade_screen.current_tab = "skills"
    
    # Draw to populate skill_buttons
    surface = pygame.Surface((800, 600))
    upgrade_screen._draw_skills_tab(surface)
    
    print(f"\nUI skill_buttons keys:")
    for button_key in upgrade_screen.skill_buttons.keys():
        print(f"  Button key: '{button_key}'")
        
        # Check if this matches any skill in the skill tree
        matches_internal = button_key in skill_tree.skills
        matches_display = any(skill.name == button_key for skill in skill_tree.skills.values())
        
        print(f"    - Matches internal key: {matches_internal}")
        print(f"    - Matches display name: {matches_display}")
        
        if matches_display:
            # Find the internal key for this display name
            for internal_key, skill in skill_tree.skills.items():
                if skill.name == button_key:
                    print(f"    - Internal key: '{internal_key}'")
                    can_upgrade = skill_tree.can_upgrade_skill(internal_key)
                    print(f"    - Can upgrade (internal): {can_upgrade}")
                    break
    
    pygame.quit()

if __name__ == "__main__":
    debug_skill_names()
