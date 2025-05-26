#!/usr/bin/env python3
"""
Asset verification script to ensure all visual assets are properly created and accessible.
"""

import os
import pygame

def verify_assets():
    """Verify that all expected assets exist and can be loaded"""
    print("🎨 Visual Asset Verification Report")
    print("=" * 50)
    
    # Initialize pygame for image loading
    pygame.init()
    
    missing_assets = []
    corrupted_assets = []
    verified_assets = []
    
    # Define expected assets
    expected_assets = {
        "Equipment Weapons": [
            "assets/images/equipment/weapons/sword.png",
            "assets/images/equipment/weapons/rifle.png",
            "assets/images/equipment/weapons/cannon.png",
            "assets/images/equipment/weapons/blaster.png",
            "assets/images/equipment/weapons/launcher.png"
        ],
        "Equipment Armor": [
            "assets/images/equipment/armor/vest.png",
            "assets/images/equipment/armor/plate.png",
            "assets/images/equipment/armor/mail.png",
            "assets/images/equipment/armor/shield.png",
            "assets/images/equipment/armor/barrier.png"
        ],
        "Equipment Accessories": [
            "assets/images/equipment/accessories/ring.png",
            "assets/images/equipment/accessories/amulet.png",
            "assets/images/equipment/accessories/charm.png",
            "assets/images/equipment/accessories/orb.png",
            "assets/images/equipment/accessories/crystal.png"
        ],
        "Rarity Borders": [
            "assets/images/equipment/borders/common_border.png",
            "assets/images/equipment/borders/uncommon_border.png",
            "assets/images/equipment/borders/rare_border.png",
            "assets/images/equipment/borders/epic_border.png"
        ],
        "Special Items": [
            "assets/images/shield_boost.png",
            "assets/images/xp_boost.png",
            "assets/images/multi_shot_boost.png",
            "assets/images/invincibility_boost.png"
        ],
        "Enemy Type Variants": []
    }
    
    # Add enemy type animation files
    enemy_types = ["normal", "fast", "tank", "sniper", "berserker"]
    animation_types = ["idle", "walk", "attack"]
    frame_counts = {"idle": 4, "walk": 8, "attack": 6}
    
    for enemy_type in enemy_types:
        for anim_type in animation_types:
            for frame in range(frame_counts[anim_type]):
                path = f"assets/images/entities/enemy_{enemy_type}/{anim_type}_{frame}.png"
                expected_assets["Enemy Type Variants"].append(path)
    
    # Verify each category
    total_expected = 0
    total_verified = 0
    
    for category, asset_list in expected_assets.items():
        print(f"\n📁 {category}:")
        category_verified = 0
        
        for asset_path in asset_list:
            total_expected += 1
            
            if not os.path.exists(asset_path):
                missing_assets.append(asset_path)
                print(f"  ❌ MISSING: {asset_path}")
            else:
                try:
                    # Try to load the image to verify it's not corrupted
                    test_surface = pygame.image.load(asset_path)
                    verified_assets.append(asset_path)
                    category_verified += 1
                    total_verified += 1
                    print(f"  ✅ {os.path.basename(asset_path)}")
                except pygame.error as e:
                    corrupted_assets.append((asset_path, str(e)))
                    print(f"  🔥 CORRUPTED: {asset_path} - {e}")
        
        print(f"  📊 Category Status: {category_verified}/{len(asset_list)} verified")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Total Expected Assets: {total_expected}")
    print(f"Successfully Verified: {total_verified}")
    print(f"Missing Assets: {len(missing_assets)}")
    print(f"Corrupted Assets: {len(corrupted_assets)}")
    
    if missing_assets:
        print(f"\n❌ Missing Assets ({len(missing_assets)}):")
        for asset in missing_assets:
            print(f"  - {asset}")
    
    if corrupted_assets:
        print(f"\n🔥 Corrupted Assets ({len(corrupted_assets)}):")
        for asset, error in corrupted_assets:
            print(f"  - {asset}: {error}")
    
    # Calculate success rate
    success_rate = (total_verified / total_expected) * 100 if total_expected > 0 else 0
    
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 ALL ASSETS VERIFIED SUCCESSFULLY!")
        print("✨ The visual asset creation was completed without issues.")
    elif success_rate >= 90:
        print("✅ Asset creation mostly successful with minor issues.")
    else:
        print("⚠️  Significant issues found. Review missing/corrupted assets.")
    
    # Additional checks
    print("\n🔍 Additional Checks:")
    
    # Check directory structure
    required_dirs = [
        "assets/images/equipment",
        "assets/images/equipment/weapons",
        "assets/images/equipment/armor", 
        "assets/images/equipment/accessories",
        "assets/images/equipment/borders"
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ Directory exists: {directory}")
        else:
            print(f"  ❌ Missing directory: {directory}")
    
    # Check file sizes (should be reasonable for 32x32 PNG files)
    large_files = []
    for asset in verified_assets:
        try:
            size = os.path.getsize(asset)
            if size > 10000:  # 10KB threshold for 32x32 PNG
                large_files.append((asset, size))
        except OSError:
            pass
    
    if large_files:
        print(f"\n📏 Large Files (>10KB) - May need optimization:")
        for asset, size in large_files:
            print(f"  - {os.path.basename(asset)}: {size:,} bytes")
    else:
        print("  ✅ All file sizes are reasonable")
    
    pygame.quit()
    return success_rate == 100

if __name__ == "__main__":
    success = verify_assets()
    exit(0 if success else 1)
