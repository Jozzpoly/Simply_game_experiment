#!/usr/bin/env python3
"""
Test only config and basic imports without pygame.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_config():
    """Test config imports"""
    print("Testing config...")
    
    try:
        from config import ENVIRONMENTAL_HAZARDS, SPECIAL_FEATURES, BIOME_TYPES
        print("✅ Config imported successfully")
        
        print(f"\nEnvironmental Hazards ({len(ENVIRONMENTAL_HAZARDS)}):")
        for hazard_name, config in ENVIRONMENTAL_HAZARDS.items():
            damage = config.get('damage', 0)
            print(f"  {hazard_name}: {damage} damage")
        
        print(f"\nSpecial Features ({len(SPECIAL_FEATURES)}):")
        for feature_name, config in SPECIAL_FEATURES.items():
            print(f"  {feature_name}: {len(config)} properties")
        
        print(f"\nBiomes ({len(BIOME_TYPES)}):")
        for biome_name, config in BIOME_TYPES.items():
            hazards = config.get('hazards', [])
            features = config.get('special_features', [])
            print(f"  {biome_name}: {len(hazards)} hazards, {len(features)} features")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_terrain_types():
    """Test terrain types"""
    print("\nTesting terrain types...")
    
    try:
        from config import TERRAIN_TYPES
        print(f"✅ Terrain types imported: {len(TERRAIN_TYPES)} types")
        
        # Check for new terrain types
        new_types = ['grass_tall', 'dirt_rich', 'stone_smooth', 'lava', 'crystal']
        found_new = 0
        
        for terrain_type in new_types:
            if terrain_type in TERRAIN_TYPES:
                found_new += 1
                print(f"  ✅ {terrain_type}: ID {TERRAIN_TYPES[terrain_type]}")
            else:
                print(f"  ❌ Missing: {terrain_type}")
        
        print(f"Found {found_new}/{len(new_types)} new terrain types")
        return True
        
    except Exception as e:
        print(f"❌ Terrain types test failed: {e}")
        return False

def main():
    """Run config-only tests"""
    print("Config-Only Integration Test")
    print("=" * 40)
    
    success = True
    
    if not test_config():
        success = False
    
    if not test_terrain_types():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("✅ Config tests passed!")
    else:
        print("❌ Config tests failed.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
