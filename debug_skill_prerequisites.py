#!/usr/bin/env python3
"""
Debug script to check skill prerequisite system
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from progression.skill_tree import SkillTree

def debug_skill_prerequisites():
    """Debug the skill prerequisite system"""
    print("🔍 Debugging Skill Prerequisites...")
    
    # Create a fresh skill tree
    skill_tree = SkillTree()
    
    # Check initial state of piercing_shots
    piercing_shots = skill_tree.skills["piercing_shots"]
    critical_strike = skill_tree.skills["critical_strike"]
    
    print(f"Critical Strike:")
    print(f"  Prerequisites: {critical_strike.prerequisites}")
    print(f"  Unlocked: {critical_strike.unlocked}")
    print(f"  Current Level: {critical_strike.current_level}")
    print()
    
    print(f"Piercing Shots:")
    print(f"  Prerequisites: {piercing_shots.prerequisites}")
    print(f"  Unlocked: {piercing_shots.unlocked}")
    print(f"  Current Level: {piercing_shots.current_level}")
    print()
    
    print(f"Learned Skills: {skill_tree.learned_skills}")
    print()
    
    # The issue: piercing_shots should be locked because critical_strike is not learned
    if piercing_shots.unlocked and piercing_shots.prerequisites:
        print("❌ BUG: Piercing Shots is unlocked despite having unmet prerequisites!")
        
        # Check if prerequisites are actually met
        prereqs_met = True
        for prereq in piercing_shots.prerequisites:
            if prereq not in skill_tree.learned_skills or skill_tree.learned_skills[prereq] < 1:
                print(f"  Prerequisite '{prereq}' not met (not in learned_skills or level < 1)")
                prereqs_met = False
        
        if not prereqs_met:
            print("  Prerequisites are NOT met, but skill is still unlocked!")
    else:
        print("✅ Piercing Shots is correctly locked")
    
    # Test upgrading critical strike and see if piercing shots unlocks
    print("\n🔧 Testing prerequisite unlocking...")
    skill_tree.add_skill_points(5)
    
    print(f"Added skill points. Total: {skill_tree.skill_points}")
    
    # Upgrade critical strike
    success = skill_tree.upgrade_skill("critical_strike")
    print(f"Upgraded critical_strike: {success}")
    print(f"Critical Strike level: {critical_strike.current_level}")
    print(f"Learned skills: {skill_tree.learned_skills}")
    
    # Check if piercing shots is now unlocked
    print(f"Piercing Shots unlocked after critical_strike upgrade: {piercing_shots.unlocked}")
    
    if piercing_shots.unlocked:
        print("✅ Piercing Shots correctly unlocked after prerequisite met")
    else:
        print("❌ Piercing Shots still locked despite prerequisite being met")

if __name__ == "__main__":
    debug_skill_prerequisites()
