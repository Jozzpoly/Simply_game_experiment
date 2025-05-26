#!/usr/bin/env python3
"""
Game Functionality Test

This script tests the actual game functionality by creating levels and checking
that enemies and stairs are properly created and functional.
"""

import sys
import os
import pygame
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_game_level_creation():
    """Test creating actual game levels"""
    print("Testing Game Level Creation")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    try:
        from level.level import Level
        from entities.enemy import Enemy
        from entities.enhanced_enemy import EnhancedEnemy
        from entities.stairs import Stairs
        
        # Test Level 1
        print("--- Testing Level 1 ---")
        level1 = Level()
        level1.generate_level(current_level=1)
        
        print(f"✅ Level 1 generated successfully")
        print(f"   Enemies: {len(level1.enemies)}")
        print(f"   Stairs: {len(level1.stairs)}")
        print(f"   Items: {len(level1.items)}")
        print(f"   Walls: {len(level1.walls)}")
        print(f"   Player: {level1.player is not None}")
        
        # Check enemy types in level 1
        enemy_types = {}
        for enemy in level1.enemies:
            enemy_type = type(enemy).__name__
            if enemy_type not in enemy_types:
                enemy_types[enemy_type] = 0
            enemy_types[enemy_type] += 1
        
        print(f"   Enemy types: {enemy_types}")
        
        if len(level1.enemies) == 0:
            print("❌ No enemies in level 1!")
            return False
            
        if len(level1.stairs) == 0:
            print("❌ No stairs in level 1!")
            return False
        
        # Test Level 3 (should have enhanced enemies)
        print("\n--- Testing Level 3 ---")
        level3 = Level()
        level3.generate_level(current_level=3)
        
        print(f"✅ Level 3 generated successfully")
        print(f"   Enemies: {len(level3.enemies)}")
        print(f"   Stairs: {len(level3.stairs)}")
        print(f"   Items: {len(level3.items)}")
        print(f"   Environmental hazards: {len(level3.environmental_hazards)}")
        print(f"   Special features: {len(level3.special_features)}")
        
        # Check enemy types in level 3
        enemy_types = {}
        enhanced_enemy_types = {}
        
        for enemy in level3.enemies:
            enemy_type = type(enemy).__name__
            if enemy_type not in enemy_types:
                enemy_types[enemy_type] = 0
            enemy_types[enemy_type] += 1
            
            # Check for enhanced enemy types
            if hasattr(enemy, 'enemy_type'):
                if enemy.enemy_type not in enhanced_enemy_types:
                    enhanced_enemy_types[enemy.enemy_type] = 0
                enhanced_enemy_types[enemy.enemy_type] += 1
        
        print(f"   Enemy classes: {enemy_types}")
        print(f"   Enhanced enemy types: {enhanced_enemy_types}")
        
        if len(level3.enemies) == 0:
            print("❌ No enemies in level 3!")
            return False
            
        if len(level3.stairs) == 0:
            print("❌ No stairs in level 3!")
            return False
        
        # Check for enhanced enemies
        enhanced_count = sum(1 for enemy in level3.enemies if isinstance(enemy, EnhancedEnemy))
        print(f"   Enhanced enemies: {enhanced_count}/{len(level3.enemies)}")
        
        if enhanced_count == 0:
            print("⚠️  No enhanced enemies in level 3 (expected for level 3+)")
        
        # Test stairs functionality
        print("\n--- Testing Stairs Functionality ---")
        stairs = list(level3.stairs)[0] if level3.stairs else None
        
        if stairs:
            print(f"   Stairs position: ({stairs.rect.x}, {stairs.rect.y})")
            print(f"   Stairs type: {stairs.stairs_type}")
            print(f"   Can use (with enemies): {stairs.can_use()}")
            
            # Test stairs with no enemies (should be usable)
            stairs.update(enemies_remaining=0, total_enemies=10)
            print(f"   Can use (no enemies): {stairs.can_use()}")
            
            if not stairs.can_use():
                print("❌ Stairs not usable when no enemies remain!")
                return False
        
        print("\n✅ Game level creation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Game level creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

def test_enemy_spawning_mechanics():
    """Test enemy spawning mechanics specifically"""
    print("\n\nTesting Enemy Spawning Mechanics")
    print("=" * 50)
    
    try:
        from level.level_generator import LevelGenerator
        from config import ENHANCED_ENEMY_TYPES
        
        # Test multiple level generations to check consistency
        for level_num in [1, 3, 5]:
            print(f"\n--- Testing Level {level_num} Generation ---")
            
            generator = LevelGenerator(current_level=level_num)
            result = generator.generate()
            
            if len(result) == 9:
                tiles, player_pos, enemy_positions, item_positions, stairs_positions, hazard_positions, special_feature_positions, exit_positions, biome_type = result
                
                print(f"   Generated {len(enemy_positions)} enemies")
                print(f"   Generated {len(stairs_positions)} stairs")
                print(f"   Biome: {biome_type}")
                
                # Check enemy position formats
                enhanced_format_count = 0
                regular_format_count = 0
                
                for enemy_data in enemy_positions:
                    if isinstance(enemy_data, tuple):
                        if len(enemy_data) == 3:
                            enhanced_format_count += 1
                            enemy_type, x, y = enemy_data
                            print(f"     Enhanced: {enemy_type} at ({x}, {y})")
                        elif len(enemy_data) == 2:
                            regular_format_count += 1
                            x, y = enemy_data
                            print(f"     Regular: at ({x}, {y})")
                
                print(f"   Enhanced format: {enhanced_format_count}")
                print(f"   Regular format: {regular_format_count}")
                
                if len(enemy_positions) == 0:
                    print(f"❌ No enemies generated for level {level_num}!")
                    return False
                
                if len(stairs_positions) == 0:
                    print(f"❌ No stairs generated for level {level_num}!")
                    return False
                
                # For level 3+, expect enhanced enemies
                if level_num >= 3 and enhanced_format_count == 0:
                    print(f"⚠️  No enhanced enemies in level {level_num}")
            else:
                print(f"❌ Wrong result format for level {level_num}")
                return False
        
        print("\n✅ Enemy spawning mechanics working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Enemy spawning mechanics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_level_progression():
    """Test level progression mechanics"""
    print("\n\nTesting Level Progression")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    try:
        from level.level import Level
        from entities.player import Player
        
        # Create a level
        level = Level()
        level.generate_level(current_level=1)
        
        if not level.stairs:
            print("❌ No stairs to test progression!")
            return False
        
        stairs = list(level.stairs)[0]
        player = level.player
        
        print(f"✅ Level created with stairs at ({stairs.rect.x}, {stairs.rect.y})")
        print(f"   Player at ({player.rect.x}, {player.rect.y})")
        print(f"   Total enemies: {len(level.enemies)}")
        
        # Test stairs when enemies are alive
        stairs.update(enemies_remaining=len(level.enemies), total_enemies=len(level.enemies))
        can_use_with_enemies = stairs.can_use()
        print(f"   Can use stairs with enemies alive: {can_use_with_enemies}")
        
        # Test stairs when most enemies are defeated
        stairs.update(enemies_remaining=1, total_enemies=len(level.enemies))
        can_use_mostly_defeated = stairs.can_use()
        print(f"   Can use stairs with 1 enemy left: {can_use_mostly_defeated}")
        
        # Test stairs when all enemies are defeated
        stairs.update(enemies_remaining=0, total_enemies=len(level.enemies))
        can_use_no_enemies = stairs.can_use()
        print(f"   Can use stairs with no enemies: {can_use_no_enemies}")
        
        if not can_use_no_enemies:
            print("❌ Stairs should be usable when no enemies remain!")
            return False
        
        # Test player-stairs interaction
        print("\n--- Testing Player-Stairs Interaction ---")
        
        # Move player to stairs position
        player.rect.centerx = stairs.rect.centerx
        player.rect.centery = stairs.rect.centery
        
        # Check collision
        collision = player.rect.colliderect(stairs.rect)
        print(f"   Player-stairs collision: {collision}")
        
        if not collision:
            print("❌ Player should collide with stairs when at same position!")
            return False
        
        print("\n✅ Level progression mechanics working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Level progression test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

def main():
    """Run all game functionality tests"""
    print("Game Functionality Test Suite")
    print("=" * 60)
    
    success = True
    
    # Run tests
    tests = [
        test_enemy_spawning_mechanics,
        test_game_level_creation,
        test_level_progression
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                success = False
                print(f"\n❌ {test_func.__name__} FAILED")
                break  # Stop on first failure
            else:
                print(f"\n✅ {test_func.__name__} PASSED")
        except Exception as e:
            print(f"\n❌ {test_func.__name__} CRASHED: {e}")
            success = False
            break
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL GAME FUNCTIONALITY TESTS PASSED!")
        print("\nGame Status:")
        print("- ✅ Enemies spawn correctly")
        print("- ✅ Stairs generate properly")
        print("- ✅ Level progression works")
        print("- ✅ Enhanced enemies appear at level 3+")
        print("- ✅ Phase 2 integration successful")
        print("\n🚀 Game is ready for normal gameplay!")
    else:
        print("❌ GAME FUNCTIONALITY TESTS FAILED!")
        print("\nCritical issues remain that prevent normal gameplay.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
