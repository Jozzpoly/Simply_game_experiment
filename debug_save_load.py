#!/usr/bin/env python3
"""
Debug script to check save/load system
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.player import Player
from progression.equipment import Equipment

def debug_save_load():
    """Debug the save/load system"""
    print("🔍 Debugging Save/Load System...")
    
    # Create a player and set up progression state
    player = Player(100, 100)
    
    print("Setting up progression state...")
    player.skill_tree.add_skill_points(5)
    success = player.skill_tree.upgrade_skill("critical_strike")
    print(f"Upgraded critical_strike: {success}")
    print(f"Critical strike level: {player.skill_tree.skills['critical_strike'].current_level}")
    print(f"Critical strike unlocked: {player.skill_tree.skills['critical_strike'].unlocked}")
    print(f"Learned skills: {player.skill_tree.learned_skills}")
    
    # Equip an item
    weapon = Equipment("weapon", "Save Test", "Rare", 2, {"damage_bonus": 15})
    player.equipment_manager.equip_item(weapon)
    print(f"Equipped weapon: {weapon.name}")
    
    # Set some stats
    player.stats["enemies_killed"] = 25
    player.achievement_manager.check_achievements(player.stats)
    print(f"Set enemies_killed to: {player.stats['enemies_killed']}")
    
    # Save progression data
    print("\nSaving progression data...")
    progression_data = player.get_progression_data()
    print(f"Saved skill tree data: {progression_data['skill_tree']}")
    print(f"Saved equipment data keys: {list(progression_data['equipment_manager'].keys())}")
    print(f"Saved stats: {progression_data['stats']}")
    
    # Create new player and load data
    print("\nCreating new player and loading data...")
    new_player = Player(100, 100)
    
    print("Before loading:")
    print(f"  Critical strike level: {new_player.skill_tree.skills['critical_strike'].current_level}")
    print(f"  Critical strike unlocked: {new_player.skill_tree.skills['critical_strike'].unlocked}")
    print(f"  Learned skills: {new_player.skill_tree.learned_skills}")
    print(f"  Equipped weapon: {new_player.equipment_manager.equipped['weapon']}")
    print(f"  Enemies killed: {new_player.stats['enemies_killed']}")
    
    new_player.load_progression_data(progression_data)
    
    print("After loading:")
    print(f"  Critical strike level: {new_player.skill_tree.skills['critical_strike'].current_level}")
    print(f"  Critical strike unlocked: {new_player.skill_tree.skills['critical_strike'].unlocked}")
    print(f"  Learned skills: {new_player.skill_tree.learned_skills}")
    print(f"  Equipped weapon: {new_player.equipment_manager.equipped['weapon']}")
    if new_player.equipment_manager.equipped['weapon']:
        print(f"    Weapon name: {new_player.equipment_manager.equipped['weapon'].name}")
    print(f"  Enemies killed: {new_player.stats['enemies_killed']}")
    
    # Verify data was preserved
    print("\nVerification:")
    if new_player.skill_tree.skills["critical_strike"].current_level == 1:
        print("✅ Skill levels preserved correctly")
    else:
        print(f"❌ Skill levels not preserved: {new_player.skill_tree.skills['critical_strike'].current_level} vs 1")
    
    if new_player.equipment_manager.equipped["weapon"]:
        if new_player.equipment_manager.equipped["weapon"].name == "Save Test":
            print("✅ Equipment data preserved correctly")
        else:
            print(f"❌ Equipment name not preserved: {new_player.equipment_manager.equipped['weapon'].name} vs Save Test")
    else:
        print("❌ Equipped items not preserved")
    
    if new_player.stats["enemies_killed"] == 25:
        print("✅ Achievement stats preserved correctly")
    else:
        print(f"❌ Achievement stats not preserved: {new_player.stats['enemies_killed']} vs 25")

if __name__ == "__main__":
    debug_save_load()
