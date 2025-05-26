#!/usr/bin/env python3
"""
Test script to verify item collection fixes
"""

import pygame
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from entities.item import HealthPotion, DamageBoost, SpeedBoost, EquipmentItem
from entities.player import Player
from level.level import Level
from utils.audio_manager_disabled import AudioManager as DisabledAudioManager

def test_item_collection():
    """Test that items are properly removed when collected"""
    print("Testing item collection fixes...")

    # Initialize pygame with display
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Create a minimal level for testing
    audio_manager = DisabledAudioManager()
    level = Level(audio_manager)

    # Create a test player
    player = Player(100, 100)
    level.player = player
    level.all_sprites.add(player)

    # Create test items at the same position as player for collision
    health_potion = HealthPotion(100, 100)  # Same position as player
    damage_boost = DamageBoost(100, 100)    # Same position as player
    speed_boost = SpeedBoost(100, 100)      # Same position as player

    # Add items to level
    level.items.add(health_potion, damage_boost, speed_boost)
    level.all_sprites.add(health_potion, damage_boost, speed_boost)

    print(f"Initial items in level: {len(level.items)}")
    print(f"Initial sprites in all_sprites: {len(level.all_sprites)}")

    # Test item collection
    initial_health = player.health
    initial_damage = player.damage
    initial_speed = player.speed

    # Simulate item collection
    level.check_item_collection()

    print(f"After collection - items in level: {len(level.items)}")
    print(f"After collection - sprites in all_sprites: {len(level.all_sprites)}")

    # Verify effects were applied
    print(f"Health: {initial_health} -> {player.health}")
    print(f"Damage: {initial_damage} -> {player.damage}")
    print(f"Speed: {initial_speed} -> {player.speed}")

    # Verify items were removed
    if len(level.items) == 0:
        print("✅ SUCCESS: All items properly removed from items group")
    else:
        print("❌ FAILURE: Items still in items group")

    # Check if sprites were removed from all_sprites (should only have player left)
    if len(level.all_sprites) == 1:
        print("✅ SUCCESS: Items properly removed from all_sprites group")
    else:
        print("❌ FAILURE: Items still in all_sprites group")

    pygame.quit()
    return len(level.items) == 0 and len(level.all_sprites) == 1

def test_equipment_collection():
    """Test equipment item collection"""
    print("\nTesting equipment collection...")

    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Create a minimal level for testing
    audio_manager = DisabledAudioManager()
    level = Level(audio_manager)

    # Create a test player
    player = Player(100, 100)
    level.player = player
    level.all_sprites.add(player)

    # Create a mock equipment object
    class MockEquipment:
        def __init__(self):
            self.equipment_type = "weapon"
            self.name = "Test Sword"
            self.rarity = "Common"

        def get_display_name(self):
            return f"{self.rarity} {self.name}"

    # Create equipment item at same position as player
    equipment = MockEquipment()
    equipment_item = EquipmentItem(100, 100, equipment)

    # Add to level
    level.items.add(equipment_item)
    level.all_sprites.add(equipment_item)

    print(f"Initial items: {len(level.items)}")

    # Test collection
    level.check_item_collection()

    print(f"After collection: {len(level.items)}")

    if len(level.items) == 0:
        print("✅ SUCCESS: Equipment item properly removed")
    else:
        print("❌ FAILURE: Equipment item not removed")

    pygame.quit()
    return len(level.items) == 0

if __name__ == "__main__":
    print("Running item collection tests...\n")

    test1_passed = test_item_collection()
    test2_passed = test_equipment_collection()

    print(f"\n{'='*50}")
    print("TEST RESULTS:")
    print(f"Basic item collection: {'PASS' if test1_passed else 'FAIL'}")
    print(f"Equipment collection: {'PASS' if test2_passed else 'FAIL'}")

    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Item collection fixes are working correctly.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED! Check the implementation.")
        sys.exit(1)
