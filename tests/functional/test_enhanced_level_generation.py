#!/usr/bin/env python3
"""
Test script for enhanced level generation and enemy AI coordination.
Tests progressive scaling, enemy clustering, and group coordination.
"""

import pygame
import sys
from level.level_generator import LevelGenerator
from entities.enemy import Enemy
from utils.constants import *

def test_progressive_level_scaling():
    """Test that levels scale properly with progression"""
    print("Testing Progressive Level Scaling...")
    print("=" * 50)
    
    # Test different level numbers
    test_levels = [1, 3, 5, 10, 15, 20]
    
    for level_num in test_levels:
        generator = LevelGenerator(current_level=level_num)
        
        print(f"\nLevel {level_num}:")
        print(f"  Map size: {generator.width}x{generator.height}")
        print(f"  Max rooms: {generator.max_rooms}")
        print(f"  Max enemies: {generator.max_enemies}")
        print(f"  Enemy density multiplier: {generator.enemy_density_multiplier:.2f}")
        print(f"  Group size range: {generator.min_group_size}-{generator.max_group_size}")
        
        # Verify scaling is working
        if level_num > 1:
            prev_generator = LevelGenerator(current_level=level_num-1)
            assert generator.width >= prev_generator.width, "Map width should not decrease"
            assert generator.height >= prev_generator.height, "Map height should not decrease"
            assert generator.max_enemies >= prev_generator.max_enemies, "Enemy count should not decrease"
    
    print("\n✅ Progressive level scaling working correctly!")

def test_room_variety_and_scaling():
    """Test room type variety and size scaling"""
    print("\nTesting Room Variety and Scaling...")
    print("=" * 50)
    
    # Test room generation for different levels
    for level_num in [1, 5, 10]:
        generator = LevelGenerator(current_level=level_num)
        
        # Test room property determination
        room_types = {}
        room_sizes = []
        
        for i in range(20):  # Test 20 rooms
            room_type, width, height = generator._determine_room_properties(i)
            
            if room_type not in room_types:
                room_types[room_type] = 0
            room_types[room_type] += 1
            room_sizes.append((width, height))
        
        print(f"\nLevel {level_num} room analysis:")
        print(f"  Room types: {room_types}")
        print(f"  Average room size: {sum(w*h for w,h in room_sizes)/len(room_sizes):.1f} tiles")
        print(f"  Size range: {min(w*h for w,h in room_sizes)}-{max(w*h for w,h in room_sizes)} tiles")
        
        # Verify we have variety
        assert len(room_types) >= 2, f"Level {level_num} should have at least 2 room types"
        
        # Higher levels should have more room types
        if level_num >= 5:
            assert "arena" in room_types or "challenge" in room_types, "Higher levels should have special rooms"
    
    print("\n✅ Room variety and scaling working correctly!")

def test_enemy_clustering_and_formations():
    """Test enemy clustering and formation generation"""
    print("\nTesting Enemy Clustering and Formations...")
    print("=" * 50)
    
    # Initialize pygame for testing
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    
    generator = LevelGenerator(current_level=5)
    tiles, player_pos, enemy_positions, item_positions = generator.generate()
    
    print(f"Generated level with {len(enemy_positions)} enemies")
    print(f"Number of enemy groups: {len(generator.enemy_groups)}")
    
    # Analyze enemy groups
    formation_types = {}
    group_sizes = []
    
    for group in generator.enemy_groups:
        formation = group['formation']
        if formation not in formation_types:
            formation_types[formation] = 0
        formation_types[formation] += 1
        group_sizes.append(len(group['enemies']))
    
    print(f"Formation types used: {formation_types}")
    print(f"Group sizes: min={min(group_sizes)}, max={max(group_sizes)}, avg={sum(group_sizes)/len(group_sizes):.1f}")
    
    # Verify clustering is working
    assert len(generator.enemy_groups) > 0, "Should have enemy groups"
    assert len(formation_types) >= 2, "Should have variety in formations"
    assert max(group_sizes) >= 2, "Should have groups with multiple enemies"
    
    print("✅ Enemy clustering and formations working correctly!")

def test_enemy_ai_coordination():
    """Test enemy AI coordination and roles"""
    print("\nTesting Enemy AI Coordination...")
    print("=" * 50)
    
    # Create a group of enemies
    enemies = []
    roles_assigned = {}
    
    for i in range(8):
        enemy = Enemy(100 + i * 50, 100, difficulty_level=3)
        enemies.append(enemy)
        
        role = enemy.role
        if role not in roles_assigned:
            roles_assigned[role] = 0
        roles_assigned[role] += 1
        
        print(f"Enemy {i+1}: Type={enemy.enemy_type}, Role={role}, "
              f"Aggression={enemy.aggression_level:.2f}")
    
    print(f"\nRoles assigned: {roles_assigned}")
    
    # Set up group coordination
    group_id = "test_group_1"
    for enemy in enemies:
        enemy.set_group_info(group_id, enemies)
    
    # Verify group setup
    for i, enemy in enumerate(enemies):
        assert enemy.group_id == group_id, f"Enemy {i} should have correct group ID"
        assert len(enemy.group_members) == len(enemies) - 1, f"Enemy {i} should know about other group members"
        assert hasattr(enemy, 'role'), f"Enemy {i} should have a role"
        assert hasattr(enemy, 'coordination_range'), f"Enemy {i} should have coordination range"
    
    # Test role variety
    assert len(roles_assigned) >= 3, "Should have variety in roles"
    
    print("✅ Enemy AI coordination working correctly!")

def test_level_generation_integration():
    """Test complete level generation with all enhancements"""
    print("\nTesting Complete Level Generation Integration...")
    print("=" * 50)
    
    # Test multiple levels to ensure consistency
    for level_num in [1, 3, 7, 12]:
        print(f"\nGenerating level {level_num}...")
        
        generator = LevelGenerator(current_level=level_num)
        tiles, player_pos, enemy_positions, item_positions = generator.generate()
        
        # Verify basic generation worked
        assert player_pos is not None, f"Level {level_num} should have player start position"
        assert len(enemy_positions) > 0, f"Level {level_num} should have enemies"
        assert len(generator.rooms) > 0, f"Level {level_num} should have rooms"
        
        # Verify scaling
        expected_min_enemies = MAX_ENEMIES_BASE + (level_num - 1) * ENEMY_SCALING_FACTOR
        assert len(enemy_positions) >= min(expected_min_enemies, generator.max_enemies), \
               f"Level {level_num} should have appropriate enemy count"
        
        # Verify enemy groups exist
        assert len(generator.enemy_groups) > 0, f"Level {level_num} should have enemy groups"
        
        # Check for boss enemies on boss levels
        if level_num % 5 == 0:
            boss_found = any(pos[0] == "boss" for pos in enemy_positions if isinstance(pos, tuple) and len(pos) == 2)
            assert boss_found, f"Level {level_num} should have a boss enemy"
        
        print(f"  ✓ Level {level_num}: {len(enemy_positions)} enemies, "
              f"{len(generator.enemy_groups)} groups, "
              f"{len(generator.rooms)} rooms")
    
    print("\n✅ Complete level generation integration working correctly!")

def main():
    """Run all enhanced level generation tests"""
    print("Enhanced Level Generation Test Suite")
    print("=" * 60)
    
    try:
        test_progressive_level_scaling()
        test_room_variety_and_scaling()
        test_enemy_clustering_and_formations()
        test_enemy_ai_coordination()
        test_level_generation_integration()
        
        print("\n" + "=" * 60)
        print("🎉 ALL ENHANCED LEVEL GENERATION TESTS PASSED! 🎉")
        print("=" * 60)
        print("\nEnhanced Features Verified:")
        print("✅ Progressive map scaling with level advancement")
        print("✅ Dynamic enemy density scaling")
        print("✅ Enemy clustering with tactical formations")
        print("✅ Room variety and size scaling")
        print("✅ Enemy AI coordination and roles")
        print("✅ Group formation patterns (line, circle, wedge, etc.)")
        print("✅ Integration with existing systems")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
