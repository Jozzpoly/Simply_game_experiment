#!/usr/bin/env python3
"""
Basic Functionality Test

This script tests the most basic functionality to identify critical issues.
"""

import sys
import os
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging to see debug messages
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_basic_level_generation():
    """Test basic level generation"""
    print("Testing Basic Level Generation")
    print("=" * 40)
    
    try:
        from level.level_generator import LevelGenerator
        
        # Test level 1 generation
        print("--- Level 1 Generation ---")
        generator1 = LevelGenerator(current_level=1)
        result1 = generator1.generate()
        
        print(f"✅ Level 1 generated: {len(result1)} elements")
        
        if len(result1) == 9:
            tiles, player_pos, enemy_positions, item_positions, stairs_positions, hazard_positions, special_feature_positions, exit_positions, biome_type = result1
            
            print(f"   Tiles: {len(tiles)}x{len(tiles[0]) if tiles else 0}")
            print(f"   Player pos: {player_pos}")
            print(f"   Enemies: {len(enemy_positions)}")
            print(f"   Items: {len(item_positions)}")
            print(f"   Stairs: {len(stairs_positions)}")
            print(f"   Biome: {biome_type}")
            
            if len(enemy_positions) == 0:
                print("❌ No enemies generated for level 1!")
                return False
                
            if len(stairs_positions) == 0:
                print("❌ No stairs generated for level 1!")
                return False
        
        # Test level 3 generation (should have enhanced enemies)
        print("\n--- Level 3 Generation ---")
        generator3 = LevelGenerator(current_level=3)
        result3 = generator3.generate()
        
        print(f"✅ Level 3 generated: {len(result3)} elements")
        
        if len(result3) == 9:
            tiles, player_pos, enemy_positions, item_positions, stairs_positions, hazard_positions, special_feature_positions, exit_positions, biome_type = result3
            
            print(f"   Enemies: {len(enemy_positions)}")
            print(f"   Stairs: {len(stairs_positions)}")
            print(f"   Biome: {biome_type}")
            
            # Check enemy format
            if enemy_positions:
                first_enemy = enemy_positions[0]
                print(f"   First enemy: {first_enemy}")
                
                if isinstance(first_enemy, tuple) and len(first_enemy) == 3:
                    enemy_type, x, y = first_enemy
                    print(f"   ✅ Enhanced enemy format: {enemy_type}")
                else:
                    print(f"   ⚠️  Old enemy format")
            
            if len(enemy_positions) == 0:
                print("❌ No enemies generated for level 3!")
                return False
                
            if len(stairs_positions) == 0:
                print("❌ No stairs generated for level 3!")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Level generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_level_creation():
    """Test basic level creation with Level class"""
    print("\n\nTesting Basic Level Creation")
    print("=" * 40)
    
    try:
        from level.level import Level
        
        # Test level 1
        print("--- Level 1 Creation ---")
        level1 = Level()
        level1.generate_level(current_level=1)
        
        enemy_count = len(level1.enemies)
        stairs_count = len(level1.stairs)
        
        print(f"✅ Level 1 created")
        print(f"   Enemies: {enemy_count}")
        print(f"   Stairs: {stairs_count}")
        
        if enemy_count == 0:
            print("❌ No enemies in level 1!")
            return False
            
        if stairs_count == 0:
            print("❌ No stairs in level 1!")
            return False
        
        # Test level 3
        print("\n--- Level 3 Creation ---")
        level3 = Level()
        level3.generate_level(current_level=3)
        
        enemy_count = len(level3.enemies)
        stairs_count = len(level3.stairs)
        
        print(f"✅ Level 3 created")
        print(f"   Enemies: {enemy_count}")
        print(f"   Stairs: {stairs_count}")
        
        # Check enemy types
        enhanced_count = 0
        regular_count = 0
        
        for enemy in level3.enemies:
            if hasattr(enemy, 'enemy_type'):
                if enemy.enemy_type in ['mage', 'assassin', 'necromancer', 'golem', 'archer', 'shaman', 'berserker_elite', 'shadow']:
                    enhanced_count += 1
                else:
                    regular_count += 1
            else:
                regular_count += 1
        
        print(f"   Enhanced enemies: {enhanced_count}")
        print(f"   Regular enemies: {regular_count}")
        
        if enemy_count == 0:
            print("❌ No enemies in level 3!")
            return False
            
        if stairs_count == 0:
            print("❌ No stairs in level 3!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Level creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_values():
    """Test critical config values"""
    print("\n\nTesting Config Values")
    print("=" * 40)
    
    try:
        from config import (STAIRS_ENABLED, MAX_ENEMIES_BASE, ENEMY_SCALING_FACTOR, 
                           MULTIPLE_EXITS_ENABLED, REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS)
        
        print(f"✅ Config imported")
        print(f"   STAIRS_ENABLED: {STAIRS_ENABLED}")
        print(f"   MAX_ENEMIES_BASE: {MAX_ENEMIES_BASE}")
        print(f"   ENEMY_SCALING_FACTOR: {ENEMY_SCALING_FACTOR}")
        print(f"   MULTIPLE_EXITS_ENABLED: {MULTIPLE_EXITS_ENABLED}")
        print(f"   REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS: {REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS}")
        
        if not STAIRS_ENABLED:
            print("❌ Stairs are disabled!")
            return False
            
        if MAX_ENEMIES_BASE <= 0:
            print("❌ No base enemies configured!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_enemy_imports():
    """Test enemy class imports"""
    print("\n\nTesting Enemy Imports")
    print("=" * 40)
    
    try:
        from entities.enemy import Enemy
        print("✅ Enemy class imported")
        
        from entities.enhanced_enemy import EnhancedEnemy
        print("✅ EnhancedEnemy class imported")
        
        # Test creating enemies
        enemy1 = Enemy(100, 100, 1)
        print(f"✅ Regular enemy created: {type(enemy1)}")
        
        enemy2 = EnhancedEnemy(200, 200, 3, 'mage')
        print(f"✅ Enhanced enemy created: {type(enemy2)}, type: {enemy2.enemy_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enemy import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic functionality tests"""
    print("Basic Functionality Test Suite")
    print("=" * 50)
    
    success = True
    
    # Run tests in order
    tests = [
        test_config_values,
        test_enemy_imports,
        test_basic_level_generation,
        test_basic_level_creation
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                success = False
                print(f"\n❌ {test_func.__name__} FAILED")
                break  # Stop on first failure for easier debugging
            else:
                print(f"\n✅ {test_func.__name__} PASSED")
        except Exception as e:
            print(f"\n❌ {test_func.__name__} CRASHED: {e}")
            success = False
            break
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All basic functionality tests passed!")
        print("Game should have enemies and stairs working.")
    else:
        print("❌ Basic functionality tests failed!")
        print("Critical issues need to be fixed.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
