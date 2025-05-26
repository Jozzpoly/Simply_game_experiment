#!/usr/bin/env python3
"""
Critical Issues Diagnostic Test

This script identifies and tests critical gameplay issues:
1. Enemy spawning problems
2. Level progression issues
3. Import and integration problems
"""

import sys
import os
import logging

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_enemy_spawning_system():
    """Test enemy spawning and creation system"""
    print("Testing Enemy Spawning System")
    print("=" * 50)
    
    try:
        # Test basic imports
        from level.level_generator import LevelGenerator
        from level.level import Level
        from entities.enemy import Enemy
        print("✅ Basic imports successful")
        
        # Test enhanced enemy import
        try:
            from entities.enhanced_enemy import EnhancedEnemy
            print("✅ EnhancedEnemy import successful")
        except Exception as e:
            print(f"❌ EnhancedEnemy import failed: {e}")
            return False
        
        # Test config imports
        try:
            from config import ENHANCED_ENEMY_TYPES
            print(f"✅ Config import successful - {len(ENHANCED_ENEMY_TYPES)} enemy types")
        except Exception as e:
            print(f"❌ Config import failed: {e}")
            return False
        
        # Test level generation
        print("\n--- Testing Level Generation ---")
        generator = LevelGenerator(current_level=3)  # Level 3 should have enhanced enemies
        
        try:
            result = generator.generate()
            print(f"✅ Level generation successful")
            
            if len(result) == 9:
                tiles, player_pos, enemy_positions, item_positions, stairs_positions, hazard_positions, special_feature_positions, exit_positions, biome_type = result
                print(f"✅ Enhanced format returned")
                print(f"   Enemy positions: {len(enemy_positions)}")
                print(f"   Stairs positions: {len(stairs_positions)}")
                print(f"   Exit positions: {len(exit_positions)}")
                
                # Check enemy position format
                if enemy_positions:
                    first_enemy = enemy_positions[0]
                    print(f"   First enemy format: {type(first_enemy)} - {first_enemy}")
                    
                    if isinstance(first_enemy, tuple) and len(first_enemy) == 3:
                        enemy_type, x, y = first_enemy
                        print(f"   ✅ Enhanced enemy format: {enemy_type} at ({x}, {y})")
                    else:
                        print(f"   ⚠️  Old enemy format detected")
                else:
                    print(f"   ❌ No enemies generated!")
                    return False
                    
            else:
                print(f"❌ Wrong return format: {len(result)} elements")
                return False
                
        except Exception as e:
            print(f"❌ Level generation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test enemy creation
        print("\n--- Testing Enemy Creation ---")
        try:
            level = Level()
            level.generate_level(current_level=3)
            
            enemy_count = len(level.enemies)
            print(f"✅ Level created with {enemy_count} enemies")
            
            if enemy_count == 0:
                print("❌ No enemies spawned in level!")
                return False
            
            # Check enemy types
            enhanced_count = 0
            regular_count = 0
            
            for enemy in level.enemies:
                if isinstance(enemy, EnhancedEnemy):
                    enhanced_count += 1
                    print(f"   ✅ Enhanced enemy: {enemy.enemy_type}")
                elif isinstance(enemy, Enemy):
                    regular_count += 1
                    print(f"   ✅ Regular enemy")
                else:
                    print(f"   ❌ Unknown enemy type: {type(enemy)}")
            
            print(f"   Enhanced enemies: {enhanced_count}")
            print(f"   Regular enemies: {regular_count}")
            
            if enhanced_count == 0 and level.current_level >= 3:
                print("❌ No enhanced enemies spawned at level 3+!")
                return False
                
        except Exception as e:
            print(f"❌ Enemy creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("\n✅ Enemy spawning system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Enemy spawning test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_level_progression_system():
    """Test level progression and stairs system"""
    print("\n\nTesting Level Progression System")
    print("=" * 50)
    
    try:
        from level.level import Level
        from entities.stairs import Stairs
        from config import STAIRS_ENABLED, MULTIPLE_EXITS_ENABLED
        
        print(f"✅ Imports successful")
        print(f"   Stairs enabled: {STAIRS_ENABLED}")
        print(f"   Multiple exits enabled: {MULTIPLE_EXITS_ENABLED}")
        
        # Test level generation with stairs
        print("\n--- Testing Stairs Generation ---")
        level = Level()
        level.generate_level(current_level=1)
        
        stairs_count = len(level.stairs)
        print(f"✅ Level created with {stairs_count} stairs")
        
        if stairs_count == 0:
            print("❌ No stairs generated!")
            
            # Check if stairs positions were generated
            if hasattr(level.generator, 'stairs_positions'):
                stairs_pos_count = len(level.generator.stairs_positions)
                print(f"   Stairs positions in generator: {stairs_pos_count}")
                
                if stairs_pos_count > 0:
                    print("   ⚠️  Stairs positions generated but not created as sprites")
                    return False
            
            # Check if exit positions were generated
            if hasattr(level.generator, 'exit_positions'):
                exit_pos_count = len(level.generator.exit_positions)
                print(f"   Exit positions in generator: {exit_pos_count}")
                
                if exit_pos_count > 0:
                    print("   ⚠️  Exit positions generated but not used")
                    
            return False
        
        # Test stairs functionality
        print("\n--- Testing Stairs Functionality ---")
        for stairs in level.stairs:
            print(f"   ✅ Stairs at ({stairs.rect.x}, {stairs.rect.y})")
            print(f"      Can use: {stairs.can_use()}")
            print(f"      Unlocked: {stairs.is_unlocked}")
            
        # Test stairs unlock conditions
        if level.stairs:
            stairs = list(level.stairs)[0]
            
            # Test with no enemies defeated
            stairs.update(enemies_remaining=10, total_enemies=10)
            print(f"   Stairs locked with 0% enemies defeated: {not stairs.can_use()}")
            
            # Test with enough enemies defeated
            stairs.update(enemies_remaining=2, total_enemies=10)
            print(f"   Stairs unlocked with 80% enemies defeated: {stairs.can_use()}")
        
        print("\n✅ Level progression system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Level progression test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_issues():
    """Test integration between systems"""
    print("\n\nTesting System Integration")
    print("=" * 50)
    
    try:
        # Test full game flow simulation
        from level.level import Level
        
        print("--- Testing Full Level Flow ---")
        
        # Create level 1 (should use regular enemies)
        level1 = Level()
        level1.generate_level(current_level=1)
        
        enemy_count_1 = len(level1.enemies)
        stairs_count_1 = len(level1.stairs)
        
        print(f"✅ Level 1: {enemy_count_1} enemies, {stairs_count_1} stairs")
        
        # Create level 3 (should use enhanced enemies)
        level3 = Level()
        level3.generate_level(current_level=3)
        
        enemy_count_3 = len(level3.enemies)
        stairs_count_3 = len(level3.stairs)
        
        print(f"✅ Level 3: {enemy_count_3} enemies, {stairs_count_3} stairs")
        
        # Check that both levels have content
        if enemy_count_1 == 0 or enemy_count_3 == 0:
            print("❌ Some levels have no enemies!")
            return False
            
        if stairs_count_1 == 0 or stairs_count_3 == 0:
            print("❌ Some levels have no stairs!")
            return False
        
        # Test enemy type distribution
        enhanced_enemies_level3 = 0
        for enemy in level3.enemies:
            if hasattr(enemy, 'enemy_type') and enemy.enemy_type in ['mage', 'assassin', 'necromancer', 'golem', 'archer', 'shaman', 'berserker_elite', 'shadow']:
                enhanced_enemies_level3 += 1
        
        print(f"   Level 3 enhanced enemies: {enhanced_enemies_level3}/{enemy_count_3}")
        
        if enhanced_enemies_level3 == 0:
            print("❌ No enhanced enemies in level 3!")
            return False
        
        print("\n✅ System integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_validation():
    """Test configuration completeness"""
    print("\n\nTesting Configuration Validation")
    print("=" * 50)
    
    try:
        from config import (ENHANCED_ENEMY_TYPES, STAIRS_ENABLED, MULTIPLE_EXITS_ENABLED,
                           REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS, ENEMY_DEFEAT_PERCENTAGE_FOR_STAIRS)
        
        print("✅ All config imports successful")
        
        # Validate enhanced enemy types
        required_types = ['mage', 'assassin', 'necromancer', 'golem', 'archer', 'shaman', 'berserker_elite', 'shadow']
        missing_types = []
        
        for enemy_type in required_types:
            if enemy_type not in ENHANCED_ENEMY_TYPES:
                missing_types.append(enemy_type)
            else:
                config = ENHANCED_ENEMY_TYPES[enemy_type]
                required_keys = ['health_multiplier', 'damage_multiplier', 'speed_multiplier', 'spawn_weight']
                for key in required_keys:
                    if key not in config:
                        print(f"❌ Missing key '{key}' in {enemy_type} config")
                        return False
        
        if missing_types:
            print(f"❌ Missing enemy types: {missing_types}")
            return False
        
        print(f"✅ All {len(required_types)} enhanced enemy types configured")
        
        # Validate stairs configuration
        print(f"✅ Stairs configuration:")
        print(f"   Enabled: {STAIRS_ENABLED}")
        print(f"   Require enemy defeat: {REQUIRE_ENEMY_PERCENTAGE_FOR_STAIRS}")
        print(f"   Defeat percentage: {ENEMY_DEFEAT_PERCENTAGE_FOR_STAIRS}")
        print(f"   Multiple exits: {MULTIPLE_EXITS_ENABLED}")
        
        print("\n✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all critical issue tests"""
    print("Critical Issues Diagnostic Test")
    print("=" * 60)
    
    success = True
    
    # Run all tests
    tests = [
        test_config_validation,
        test_enemy_spawning_system,
        test_level_progression_system,
        test_integration_issues
    ]
    
    for test_func in tests:
        try:
            if not test_func():
                success = False
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ All critical issue tests passed!")
        print("Game should be functional for normal progression.")
    else:
        print("❌ Critical issues detected!")
        print("Game may not function properly.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
