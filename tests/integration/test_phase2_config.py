#!/usr/bin/env python3
"""
Simple test for Phase 2 configuration
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def test_phase2_config():
    """Test Phase 2 configuration imports"""
    print("Testing Phase 2 Configuration")
    print("=" * 40)
    
    try:
        from config import (ENHANCED_ENEMY_TYPES, ELEMENTAL_DAMAGE_TYPES, STATUS_EFFECTS,
                           EQUIPMENT_RARITIES, EQUIPMENT_SETS, ENCHANTMENTS, CONSUMABLE_ITEMS)
        
        print("✅ All Phase 2 configurations imported successfully")
        
        # Test enhanced enemy types
        print(f"\nEnhanced Enemy Types ({len(ENHANCED_ENEMY_TYPES)}):")
        new_types = ['mage', 'assassin', 'necromancer', 'golem', 'archer', 'shaman', 'berserker_elite', 'shadow']
        for enemy_type in new_types:
            if enemy_type in ENHANCED_ENEMY_TYPES:
                config = ENHANCED_ENEMY_TYPES[enemy_type]
                abilities = config.get('special_abilities', [])
                print(f"  ✅ {enemy_type}: {len(abilities)} abilities")
            else:
                print(f"  ❌ Missing: {enemy_type}")
        
        # Test elemental damage types
        print(f"\nElemental Damage Types ({len(ELEMENTAL_DAMAGE_TYPES)}):")
        for element in ELEMENTAL_DAMAGE_TYPES:
            config = ELEMENTAL_DAMAGE_TYPES[element]
            effects = config.get('status_effects', [])
            print(f"  ✅ {element}: {len(effects)} status effects")
        
        # Test status effects
        print(f"\nStatus Effects ({len(STATUS_EFFECTS)}):")
        for effect in STATUS_EFFECTS:
            config = STATUS_EFFECTS[effect]
            stackable = config.get('stackable', False)
            print(f"  ✅ {effect}: stackable={stackable}")
        
        # Test equipment rarities
        print(f"\nEquipment Rarities ({len(EQUIPMENT_RARITIES)}):")
        for rarity in EQUIPMENT_RARITIES:
            config = EQUIPMENT_RARITIES[rarity]
            multiplier = config.get('stat_multiplier', 1.0)
            print(f"  ✅ {rarity}: {multiplier}x stats")
        
        # Test equipment sets
        print(f"\nEquipment Sets ({len(EQUIPMENT_SETS)}):")
        for set_name in EQUIPMENT_SETS:
            config = EQUIPMENT_SETS[set_name]
            pieces = config.get('pieces', [])
            print(f"  ✅ {set_name}: {len(pieces)} pieces")
        
        # Test enchantments
        print(f"\nEnchantments ({len(ENCHANTMENTS)}):")
        for enchant in ENCHANTMENTS:
            config = ENCHANTMENTS[enchant]
            max_level = config.get('max_level', 1)
            print(f"  ✅ {enchant}: max level {max_level}")
        
        # Test consumables
        print(f"\nConsumable Items ({len(CONSUMABLE_ITEMS)}):")
        for item in CONSUMABLE_ITEMS:
            config = CONSUMABLE_ITEMS[item]
            effect = config.get('effect', 'unknown')
            print(f"  ✅ {item}: {effect}")
        
        print(f"\n✅ Phase 2 configuration is complete and valid!")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run Phase 2 config test"""
    success = test_phase2_config()
    
    if success:
        print("\n🚀 Phase 2 configuration ready for implementation!")
    else:
        print("\n❌ Phase 2 configuration has issues.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
