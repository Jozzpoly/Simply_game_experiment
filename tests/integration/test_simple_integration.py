#!/usr/bin/env python3
"""
Simple test to verify environmental integration works.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_imports():
    """Test that we can import all necessary modules"""
    print("Testing imports...")
    
    try:
        from config import ENVIRONMENTAL_HAZARDS, SPECIAL_FEATURES, BIOME_TYPES
        print("✅ Config imports successful")
        print(f"   Hazards: {len(ENVIRONMENTAL_HAZARDS)}")
        print(f"   Features: {len(SPECIAL_FEATURES)}")
        print(f"   Biomes: {len(BIOME_TYPES)}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from entities.environmental_entities import EnvironmentalHazardSprite, SpecialFeatureSprite
        print("✅ Environmental entities import successful")
    except Exception as e:
        print(f"❌ Environmental entities import failed: {e}")
        return False
    
    try:
        from level.level_generator import LevelGenerator
        print("✅ Level generator import successful")
    except Exception as e:
        print(f"❌ Level generator import failed: {e}")
        return False
    
    return True

def test_level_generation():
    """Test basic level generation with environmental elements"""
    print("\nTesting level generation...")
    
    try:
        from level.level_generator import LevelGenerator
        
        # Create generator
        generator = LevelGenerator(current_level=3)
        print("✅ Generator created")
        
        # Generate level
        result = generator.generate()
        print("✅ Level generated")
        
        if len(result) == 9:
            (tiles, player_pos, enemy_positions, item_positions, stairs_positions,
             hazard_positions, special_feature_positions, exit_positions, biome_type) = result
            
            print(f"✅ Enhanced format returned")
            print(f"   Biome: {biome_type}")
            print(f"   Map size: {generator.width}x{generator.height}")
            print(f"   Rooms: {len(generator.rooms)}")
            print(f"   Hazards: {len(hazard_positions)}")
            print(f"   Features: {len(special_feature_positions)}")
            
            return True
        else:
            print(f"⚠️  Old format returned ({len(result)} elements)")
            return False
            
    except Exception as e:
        print(f"❌ Level generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sprite_creation():
    """Test environmental sprite creation"""
    print("\nTesting sprite creation...")
    
    try:
        import pygame
        pygame.init()
        
        from entities.environmental_entities import EnvironmentalHazardSprite, SpecialFeatureSprite
        
        # Test hazard creation
        hazard = EnvironmentalHazardSprite('spike_trap', 100, 100)
        print(f"✅ Hazard created: {hazard.hazard_type}")
        
        # Test feature creation
        feature = SpecialFeatureSprite('treasure_alcove', 200, 200)
        print(f"✅ Feature created: {feature.feature_type}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Sprite creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_player_effects():
    """Test player environmental effects"""
    print("\nTesting player effects...")
    
    try:
        from entities.player import Player
        
        # Create player
        player = Player(100, 100)
        print("✅ Player created")
        
        # Test slow effect
        original_speed = player.get_effective_speed()
        player.apply_slow(0.5, 180)
        slowed_speed = player.get_effective_speed()
        
        print(f"✅ Slow effect: {original_speed:.2f} -> {slowed_speed:.2f}")
        
        # Test damage boost
        original_damage = player.get_effective_damage()
        player.apply_damage_boost(1.5, 300)
        boosted_damage = player.get_effective_damage()
        
        print(f"✅ Damage boost: {original_damage:.2f} -> {boosted_damage:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Player effects failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run simple integration tests"""
    print("Simple Environmental Integration Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test level generation
    if not test_level_generation():
        success = False
    
    # Test sprite creation
    if not test_sprite_creation():
        success = False
    
    # Test player effects
    if not test_player_effects():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Environmental integration is working.")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
