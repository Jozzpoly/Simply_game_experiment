#!/usr/bin/env python3
"""
Test script to verify all visual improvements are working correctly.
"""

import pygame
import os
import sys
from utils.constants import *
from entities.enemy import Enemy
from entities.item import EquipmentItem
from progression.equipment import Equipment

def test_visual_improvements():
    """Test all visual improvements"""
    print("🎨 Testing Visual Improvements")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Enemy Type Animation Loading
    print("\n1. Testing Enemy Type Animation Loading...")
    total_tests += 1
    
    try:
        enemy_types = ["normal", "fast", "tank", "sniper", "berserker"]
        loaded_types = []
        
        for enemy_type in enemy_types:
            # Check if animation files exist
            base_path = f"assets/images/entities/enemy_{enemy_type}"
            if os.path.exists(base_path):
                # Check for required animation files
                required_files = [
                    "idle_0.png", "idle_1.png", "idle_2.png", "idle_3.png",
                    "walk_0.png", "walk_1.png", "walk_2.png", "walk_3.png",
                    "attack_0.png", "attack_1.png", "attack_2.png", "attack_3.png"
                ]
                
                all_files_exist = all(
                    os.path.exists(os.path.join(base_path, file)) 
                    for file in required_files
                )
                
                if all_files_exist:
                    loaded_types.append(enemy_type)
                    print(f"  ✅ {enemy_type.title()} enemy animations: FOUND")
                else:
                    print(f"  ❌ {enemy_type.title()} enemy animations: INCOMPLETE")
            else:
                print(f"  ❌ {enemy_type.title()} enemy animations: MISSING")
        
        if len(loaded_types) == len(enemy_types):
            print("  🎉 All enemy type animations loaded successfully!")
            success_count += 1
        else:
            print(f"  ⚠️  Only {len(loaded_types)}/{len(enemy_types)} enemy types have complete animations")
    
    except Exception as e:
        print(f"  ❌ Error testing enemy animations: {e}")
    
    # Test 2: Equipment Icon Loading
    print("\n2. Testing Equipment Icon Loading...")
    total_tests += 1
    
    try:
        loaded_icons = 0
        total_icons = len(EQUIPMENT_ICON_MAPPING)
        
        for equipment_name, icon_path in EQUIPMENT_ICON_MAPPING.items():
            if os.path.exists(icon_path):
                try:
                    # Try to load the icon
                    icon = pygame.image.load(icon_path)
                    loaded_icons += 1
                    print(f"  ✅ {equipment_name}: {icon_path}")
                except pygame.error:
                    print(f"  ❌ {equipment_name}: CORRUPTED - {icon_path}")
            else:
                print(f"  ❌ {equipment_name}: MISSING - {icon_path}")
        
        if loaded_icons == total_icons:
            print(f"  🎉 All {total_icons} equipment icons loaded successfully!")
            success_count += 1
        else:
            print(f"  ⚠️  Only {loaded_icons}/{total_icons} equipment icons loaded")
    
    except Exception as e:
        print(f"  ❌ Error testing equipment icons: {e}")
    
    # Test 3: Rarity Border Loading
    print("\n3. Testing Rarity Border Loading...")
    total_tests += 1
    
    try:
        rarity_borders = ["common", "uncommon", "rare", "epic"]
        loaded_borders = 0
        
        for rarity in rarity_borders:
            border_path = f"assets/images/equipment/borders/{rarity}_border.png"
            if os.path.exists(border_path):
                try:
                    border = pygame.image.load(border_path)
                    loaded_borders += 1
                    print(f"  ✅ {rarity.title()} border: {border_path}")
                except pygame.error:
                    print(f"  ❌ {rarity.title()} border: CORRUPTED - {border_path}")
            else:
                print(f"  ❌ {rarity.title()} border: MISSING - {border_path}")
        
        if loaded_borders == len(rarity_borders):
            print(f"  🎉 All {len(rarity_borders)} rarity borders loaded successfully!")
            success_count += 1
        else:
            print(f"  ⚠️  Only {loaded_borders}/{len(rarity_borders)} rarity borders loaded")
    
    except Exception as e:
        print(f"  ❌ Error testing rarity borders: {e}")
    
    # Test 4: Special Item Icons
    print("\n4. Testing Special Item Icons...")
    total_tests += 1
    
    try:
        special_items = {
            "Shield Boost": SHIELD_BOOST_IMG,
            "XP Boost": XP_BOOST_IMG,
            "Multi-Shot": MULTI_SHOT_BOOST_IMG,
            "Invincibility": INVINCIBILITY_BOOST_IMG
        }
        
        loaded_special = 0
        
        for item_name, icon_path in special_items.items():
            if os.path.exists(icon_path):
                try:
                    icon = pygame.image.load(icon_path)
                    loaded_special += 1
                    print(f"  ✅ {item_name}: {icon_path}")
                except pygame.error:
                    print(f"  ❌ {item_name}: CORRUPTED - {icon_path}")
            else:
                print(f"  ❌ {item_name}: MISSING - {icon_path}")
        
        if loaded_special == len(special_items):
            print(f"  🎉 All {len(special_items)} special item icons loaded successfully!")
            success_count += 1
        else:
            print(f"  ⚠️  Only {loaded_special}/{len(special_items)} special item icons loaded")
    
    except Exception as e:
        print(f"  ❌ Error testing special item icons: {e}")
    
    # Test 5: Equipment Item Creation
    print("\n5. Testing Equipment Item Creation...")
    total_tests += 1
    
    try:
        # Test creating equipment items with icons
        test_equipment = Equipment("weapon", "Sword", "Common", 1, {"damage_bonus": 10})
        equipment_item = EquipmentItem(100, 100, test_equipment)
        
        # Check if the equipment item was created successfully
        if hasattr(equipment_item, 'equipment') and equipment_item.equipment.name == "Sword":
            print("  ✅ Equipment item creation: SUCCESS")
            print(f"  ✅ Equipment name: {equipment_item.equipment.name}")
            print(f"  ✅ Equipment type: {equipment_item.equipment.equipment_type}")
            print(f"  ✅ Equipment rarity: {equipment_item.equipment.rarity}")
            success_count += 1
        else:
            print("  ❌ Equipment item creation: FAILED")
    
    except Exception as e:
        print(f"  ❌ Error testing equipment item creation: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VISUAL IMPROVEMENTS TEST SUMMARY")
    print("=" * 50)
    print(f"Tests Passed: {success_count}/{total_tests}")
    print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("🎉 ALL VISUAL IMPROVEMENTS WORKING PERFECTLY!")
        print("✨ The game is ready with enhanced visual assets!")
    elif success_count >= total_tests * 0.8:
        print("✅ Most visual improvements working correctly!")
        print("⚠️  Minor issues detected - check failed tests above")
    else:
        print("⚠️  Significant issues detected with visual improvements")
        print("🔧 Review failed tests and fix missing/corrupted assets")
    
    # Additional Info
    print(f"\n📊 Asset Statistics:")
    print(f"  • Enemy Type Variants: 5 types × 18 animations = 90 files")
    print(f"  • Equipment Icons: {len(EQUIPMENT_ICON_MAPPING)} unique icons")
    print(f"  • Rarity Borders: 4 border overlays")
    print(f"  • Special Items: 4 themed icons")
    print(f"  • Total New Assets: ~113 files")
    
    pygame.quit()
    return success_count == total_tests

if __name__ == "__main__":
    success = test_visual_improvements()
    sys.exit(0 if success else 1)
