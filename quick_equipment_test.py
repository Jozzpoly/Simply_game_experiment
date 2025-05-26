#!/usr/bin/env python3
"""
Quick test to generate equipment and verify no +0 stats in actual game context
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from progression.equipment import EquipmentManager

def test_equipment_in_game_context():
    """Test equipment generation exactly as it happens in the game"""
    print("🔧 Testing Equipment Generation in Game Context...")
    
    # Create equipment manager exactly like in the game
    equipment_manager = EquipmentManager()
    
    # Test equipment generation for different scenarios
    test_scenarios = [
        ("weapon", 1, "Early game weapon"),
        ("armor", 1, "Early game armor"), 
        ("accessory", 1, "Early game accessory"),
        ("weapon", 5, "Mid game weapon"),
        ("armor", 5, "Mid game armor"),
        ("accessory", 5, "Mid game accessory"),
        ("weapon", 10, "Late game weapon"),
        ("armor", 10, "Late game armor"),
        ("accessory", 10, "Late game accessory"),
    ]
    
    all_good = True
    
    for equipment_type, player_level, description in test_scenarios:
        print(f"\n  Testing {description} (Level {player_level}):")
        
        # Generate 5 items of each type to test variety
        for i in range(5):
            equipment = equipment_manager.generate_random_equipment(equipment_type, player_level)
            
            print(f"    {i+1}. {equipment.get_display_name()}")
            
            # Check each stat
            has_zero_stats = False
            for stat_name, base_value in equipment.stats.items():
                effective_value = equipment.get_stat_bonus(stat_name)
                
                if effective_value <= 0:
                    print(f"      ❌ PROBLEM: {stat_name} = +{effective_value}")
                    has_zero_stats = True
                    all_good = False
                else:
                    print(f"      ✅ {stat_name}: +{effective_value}")
            
            if has_zero_stats:
                print(f"      💥 ITEM HAS ZERO STATS!")
    
    print(f"\n📊 Final Result:")
    if all_good:
        print("✅ ALL EQUIPMENT GENERATION WORKING PERFECTLY!")
        print("🎉 NO items with +0 stats found!")
        print("🔧 Fix is working in game context!")
    else:
        print("❌ STILL PROBLEMS WITH EQUIPMENT GENERATION!")
        print("💥 Some items still have +0 stats!")
    
    return all_good

if __name__ == "__main__":
    test_equipment_in_game_context()
