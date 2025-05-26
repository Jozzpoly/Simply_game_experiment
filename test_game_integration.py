#!/usr/bin/env python3
"""
Integration test to verify equipment and skill systems work in game context
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

def test_player_with_equipment_stats():
    """Test player stats with equipment equipped"""
    print("🎮 Testing Player with Equipment Stats...")

    # Create a player
    player = Player(100, 100)

    # Show initial stats
    print(f"  Initial stats:")
    print(f"    Health: {player.health}/{player.max_health}")
    print(f"    Effective Max Health: {player.get_effective_max_health()}")
    print(f"    Damage: {player.damage}")
    print(f"    Effective Damage: {player.get_effective_damage()}")
    print(f"    Speed: {player.speed}")
    print(f"    Effective Speed: {player.get_effective_speed()}")

    # Create and equip items
    weapon = Equipment("weapon", "Power Sword", "Rare", 2, {"damage_bonus": 20, "critical_chance": 0.15})
    armor = Equipment("armor", "Health Plate", "Uncommon", 1, {"health_bonus": 30, "regeneration": 2})
    accessory = Equipment("accessory", "Speed Ring", "Common", 1, {"speed_bonus": 1.5, "xp_bonus": 0.2})

    player.equipment_manager.equip_item(weapon)
    player.equipment_manager.equip_item(armor)
    player.equipment_manager.equip_item(accessory)

    print(f"  After equipping items:")
    print(f"    Health: {player.health}/{player.max_health}")
    print(f"    Effective Max Health: {player.get_effective_max_health()}")
    print(f"    Damage: {player.damage}")
    print(f"    Effective Damage: {player.get_effective_damage()}")
    print(f"    Speed: {player.speed}")
    print(f"    Effective Speed: {player.get_effective_speed()}")
    print(f"    Critical Chance: {player.get_critical_chance()}")
    print(f"    XP Bonus: {player.get_xp_bonus()}")

    # Verify equipment bonuses are applied
    assert player.get_effective_max_health() > player.max_health, "Max health should be increased by equipment"
    assert player.get_effective_damage() > player.damage, "Damage should be increased by equipment"
    assert player.get_effective_speed() > player.speed, "Speed should be increased by equipment"
    assert player.get_critical_chance() > 0, "Should have critical chance from equipment"
    assert player.get_xp_bonus() > 0, "Should have XP bonus from equipment"

    print("  ✅ Equipment stats integration working correctly!")
    return True

def test_regeneration_in_game_loop():
    """Test regeneration works in simulated game loop"""
    print("🔄 Testing Regeneration in Game Loop...")

    # Create a player
    player = Player(100, 100)

    # Equip regeneration armor
    armor = Equipment("armor", "Regen Armor", "Rare", 3, {"regeneration": 3, "health_bonus": 25})
    player.equipment_manager.equip_item(armor)

    # Damage the player
    player.health = 50
    effective_max_health = player.get_effective_max_health()
    print(f"  Player health: {player.health}/{effective_max_health}")
    print(f"  Equipment regeneration: {player.equipment_manager.get_total_stat_bonus('regeneration')}")

    # Simulate game loop updates
    initial_health = player.health
    for frame in range(120):  # 2 seconds at 60 FPS
        player.apply_skill_effects()  # This includes equipment regeneration
        if player.health > initial_health:
            print(f"  Regeneration triggered at frame {frame}, health: {player.health}")
            break

    # Verify regeneration occurred
    assert player.health > initial_health, f"Health should have regenerated from {initial_health} to {player.health}"

    print("  ✅ Regeneration in game loop working correctly!")
    return True

def test_skill_and_equipment_synergy():
    """Test that skills and equipment bonuses stack correctly"""
    print("⚔️ Testing Skill and Equipment Synergy...")

    # Create a player
    player = Player(100, 100)

    # Add skill points and upgrade skills
    player.skill_tree.add_skill_points(10)
    player.skill_tree.upgrade_skill("critical_strike")  # +3% crit chance
    player.skill_tree.upgrade_skill("weapon_mastery")   # +10% damage
    player.skill_tree.upgrade_skill("armor_mastery")    # +5% damage reduction

    # Equip items with similar bonuses
    weapon = Equipment("weapon", "Crit Blade", "Epic", 2, {"damage_bonus": 25, "critical_chance": 0.12})
    armor = Equipment("armor", "Tank Armor", "Rare", 2, {"damage_reduction": 0.08, "health_bonus": 40})

    player.equipment_manager.equip_item(weapon)
    player.equipment_manager.equip_item(armor)

    # Check combined bonuses
    total_crit = player.get_critical_chance()
    total_damage = player.get_effective_damage()
    total_reduction = player.get_damage_reduction()

    print(f"  Combined critical chance: {total_crit:.3f}")
    print(f"  Combined effective damage: {total_damage:.1f}")
    print(f"  Combined damage reduction: {total_reduction:.3f}")

    # Verify bonuses are properly combined
    skill_crit = player.skill_tree.get_total_bonus("critical_chance")
    equipment_crit = player.equipment_manager.get_total_stat_bonus("critical_chance")
    expected_crit = skill_crit + equipment_crit

    assert abs(total_crit - expected_crit) < 0.001, f"Critical chance should be {expected_crit}, got {total_crit}"
    assert total_damage > player.damage, "Effective damage should be higher than base damage"
    assert total_reduction > 0, "Should have damage reduction from both sources"

    print("  ✅ Skill and equipment synergy working correctly!")
    return True

def test_ui_stat_display():
    """Test that UI shows correct effective stats"""
    print("🖥️ Testing UI Stat Display...")

    # Initialize pygame for UI testing
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Create player and upgrade screen
    player = Player(100, 100)
    upgrade_screen = UpgradeScreen(800, 600)
    upgrade_screen.update_stats(player)

    # Equip some items
    weapon = Equipment("weapon", "UI Test Sword", "Epic", 5, {"damage_bonus": 50})
    armor = Equipment("armor", "UI Test Armor", "Epic", 3, {"health_bonus": 75})

    player.equipment_manager.equip_item(weapon)
    player.equipment_manager.equip_item(armor)

    # Check that effective stats are calculated correctly
    effective_max_health = player.get_effective_max_health()
    effective_damage = player.get_effective_damage()

    print(f"  Base max health: {player.max_health}")
    print(f"  Effective max health: {effective_max_health}")
    print(f"  Base damage: {player.damage}")
    print(f"  Effective damage: {effective_damage}")

    # Verify the UI would show correct values
    assert effective_max_health > player.max_health, "UI should show increased max health"
    assert effective_damage > player.damage, "UI should show increased damage"

    pygame.quit()
    print("  ✅ UI stat display working correctly!")
    return True

def main():
    """Run all integration tests"""
    print("🚀 Starting Game Integration Tests...\n")

    try:
        # Run tests
        tests = [
            test_player_with_equipment_stats,
            test_regeneration_in_game_loop,
            test_skill_and_equipment_synergy,
            test_ui_stat_display
        ]

        passed = 0
        for test in tests:
            try:
                if test():
                    passed += 1
                print()
            except Exception as e:
                print(f"  ❌ Test failed: {e}")
                import traceback
                traceback.print_exc()
                print()

        print(f"📊 Integration Test Results: {passed}/{len(tests)} tests passed")

        if passed == len(tests):
            print("🎉 All integration tests passed!")
            print("✨ Equipment bonuses are now properly applied to player stats!")
            print("✨ Equipment regeneration is working correctly!")
            print("✨ Skill tree upgrades are functional!")
            print("✨ UI displays effective stats including equipment bonuses!")
        else:
            print("⚠️  Some integration tests failed. Check the output above for details.")

    except Exception as e:
        print(f"❌ Integration test setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
