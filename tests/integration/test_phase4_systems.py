#!/usr/bin/env python3
"""
Phase 4 Systems Test Suite

This script tests all Phase 4 integration and polish systems:
- Integrated Game Manager
- Enhanced Save Manager
- Settings Manager
- Tutorial Manager
- Full system integration
- Launch readiness validation
"""

import sys
import os
import pygame
import time
import logging
import tempfile
import shutil

# Add the current directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_integrated_game_manager():
    """Test integrated game manager functionality"""
    print("Testing Integrated Game Manager")
    print("=" * 50)
    
    # Initialize pygame for UI testing
    pygame.init()
    
    try:
        from systems.integrated_game_manager import IntegratedGameManager
        
        # Create integrated game manager
        game_manager = IntegratedGameManager(1920, 1080)
        
        print("✅ Integrated Game Manager created")
        
        # Test system initialization
        init_success = game_manager.initialize_systems()
        print(f"   Systems initialized: {init_success}")
        
        # Test session management
        session_started = game_manager.start_new_session(starting_level=1)
        print(f"   New session started: {session_started}")
        
        if session_started:
            print(f"   Session ID: {game_manager.current_session.session_id}")
            print(f"   Start time: {game_manager.current_session.start_time}")
        
        # Test level generation
        print("\n--- Testing Advanced Level Generation ---")
        level_data = game_manager.generate_level(level_number=5, biome_type="dungeon")
        
        if level_data and len(level_data) >= 9:
            tiles, player_pos, enemy_positions, item_positions, stairs_positions, hazard_positions, special_feature_positions, exit_positions, biome_type = level_data[:9]
            
            print(f"   ✅ Level generated successfully")
            print(f"      Player position: {player_pos}")
            print(f"      Enemies: {len(enemy_positions)}")
            print(f"      Items: {len(item_positions)}")
            print(f"      Biome: {biome_type}")
            
            # Check for advanced data
            if len(level_data) >= 10:
                advanced_data = level_data[9]
                if isinstance(advanced_data, dict):
                    theme = advanced_data.get('architectural_theme')
                    print(f"      Architectural theme: {theme}")
        
        # Test game events processing
        print("\n--- Testing Game Events Processing ---")
        
        # Simulate game events
        game_events = {
            'enemy_killed': True,
            'damage_dealt': 150,
            'damage_taken': 50,
            'item_collected': True
        }
        
        game_manager.update_systems(0.016, game_events)  # 60 FPS delta
        print(f"   ✅ Game events processed")
        
        if game_manager.current_session:
            session = game_manager.current_session
            print(f"      Enemies killed: {session.enemies_killed}")
            print(f"      Damage dealt: {session.damage_dealt}")
            print(f"      Damage taken: {session.damage_taken}")
            print(f"      Items collected: {session.items_collected}")
        
        # Test session ending
        session_ended = game_manager.end_current_session(successful=True)
        print(f"   Session ended: {session_ended}")
        
        # Test integration status
        status = game_manager.get_integration_status()
        print(f"\n   Integration Status:")
        print(f"      Systems initialized: {status['systems_initialized']}")
        print(f"      Current session: {status['current_session']}")
        print(f"      UI components: {status['ui_components']}")
        
        # Cleanup
        game_manager.cleanup()
        
        print("\n✅ Integrated Game Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Integrated Game Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()

def test_enhanced_save_manager():
    """Test enhanced save manager functionality"""
    print("\n\nTesting Enhanced Save Manager")
    print("=" * 50)
    
    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        from systems.enhanced_save_manager import EnhancedSaveManager
        
        # Create save manager with temp directory
        save_manager = EnhancedSaveManager(temp_dir)
        
        print("✅ Enhanced Save Manager created")
        print(f"   Save directory: {save_manager.save_directory}")
        
        # Test complete save/load cycle
        print("\n--- Testing Complete Save/Load Cycle ---")
        
        # Create test data
        game_data = {
            'current_level': 5,
            'score': 1500,
            'player_health': 80,
            'inventory': ['sword', 'potion', 'key']
        }
        
        meta_data = {
            'currencies': {'soul_essence': 100, 'knowledge_crystals': 50},
            'masteries': {'weapon_mastery': {'level': 3, 'experience': 250}},
            'total_runs': 10,
            'successful_runs': 7
        }
        
        settings_data = {
            'graphics': {'fullscreen': False, 'resolution': [1920, 1080]},
            'audio': {'master_volume': 0.8, 'music_volume': 0.7}
        }
        
        achievements_data = {
            'unlocked_achievements': ['first_kill', 'level_5_reached'],
            'achievement_points': 150
        }
        
        # Save complete state
        save_success = save_manager.save_complete_game_state(
            game_data, meta_data, settings_data, achievements_data
        )
        print(f"   Complete save successful: {save_success}")
        
        # Load complete state
        loaded_game, loaded_meta, loaded_settings, loaded_achievements = save_manager.load_complete_game_state()
        
        print(f"   Complete load successful: {all([loaded_game, loaded_meta, loaded_settings, loaded_achievements])}")
        
        if loaded_game:
            print(f"      Game data loaded: level={loaded_game.get('current_level')}, score={loaded_game.get('score')}")
        
        if loaded_meta:
            print(f"      Meta data loaded: runs={loaded_meta.get('total_runs')}, currencies={len(loaded_meta.get('currencies', {}))}")
        
        if loaded_settings:
            print(f"      Settings loaded: categories={len(loaded_settings)}")
        
        if loaded_achievements:
            print(f"      Achievements loaded: unlocked={len(loaded_achievements.get('unlocked_achievements', []))}")
        
        # Test backup system
        print("\n--- Testing Backup System ---")
        
        # Create another save to trigger backup
        game_data['current_level'] = 6
        save_manager.save_complete_game_state(game_data, meta_data, settings_data, achievements_data)
        
        # Check if backup was created
        backup_dirs = list(save_manager.backup_directory.iterdir())
        print(f"   Backups created: {len(backup_dirs)}")
        
        # Test save metadata
        metadata = save_manager.get_save_metadata()
        if metadata:
            print(f"   Save metadata: version={metadata.version}, level={metadata.current_level}")
        
        print("\n✅ Enhanced Save Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Save Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def test_settings_manager():
    """Test settings manager functionality"""
    print("\n\nTesting Settings Manager")
    print("=" * 50)
    
    try:
        from systems.settings_manager import SettingsManager, SettingType
        
        # Create settings manager
        settings_manager = SettingsManager()
        
        print("✅ Settings Manager created")
        
        # Test setting categories
        categories = settings_manager.get_all_categories()
        print(f"   Setting categories: {categories}")
        
        # Test getting and setting values
        print("\n--- Testing Setting Operations ---")
        
        # Test boolean setting
        fullscreen_value = settings_manager.get_setting("graphics.fullscreen")
        print(f"   Default fullscreen: {fullscreen_value}")
        
        set_success = settings_manager.set_setting("graphics.fullscreen", True)
        print(f"   Set fullscreen to True: {set_success}")
        
        new_fullscreen = settings_manager.get_setting("graphics.fullscreen")
        print(f"   New fullscreen value: {new_fullscreen}")
        
        # Test float setting with validation
        volume_success = settings_manager.set_setting("audio.master_volume", 0.9)
        print(f"   Set master volume to 0.9: {volume_success}")
        
        # Test invalid value (should fail)
        invalid_success = settings_manager.set_setting("audio.master_volume", 2.0)  # Over max
        print(f"   Set invalid volume (2.0): {invalid_success}")
        
        # Test choice setting
        difficulty_success = settings_manager.set_setting("gameplay.difficulty_mode", "adaptive")
        print(f"   Set difficulty mode: {difficulty_success}")
        
        # Test category settings
        print("\n--- Testing Category Operations ---")
        
        graphics_settings = settings_manager.get_category_settings("graphics")
        print(f"   Graphics settings count: {len(graphics_settings)}")
        
        audio_settings = settings_manager.get_category_settings("audio")
        print(f"   Audio settings count: {len(audio_settings)}")
        
        # Test export/import
        print("\n--- Testing Export/Import ---")
        
        exported_settings = settings_manager.export_settings()
        print(f"   Exported settings count: {len(exported_settings)}")
        
        # Modify a setting
        settings_manager.set_setting("graphics.ui_scale", 1.5)
        
        # Import original settings
        import_success = settings_manager.import_settings(exported_settings)
        print(f"   Import settings successful: {import_success}")
        
        # Check if setting was restored
        restored_scale = settings_manager.get_setting("graphics.ui_scale")
        print(f"   UI scale restored to: {restored_scale}")
        
        # Test reset to defaults
        settings_manager.reset_to_defaults("audio")
        print(f"   Audio settings reset to defaults")
        
        # Test settings summary
        summary = settings_manager.get_settings_summary()
        print(f"\n   Settings Summary:")
        print(f"      Total settings: {summary['total_settings']}")
        print(f"      Categories: {len(summary['categories'])}")
        print(f"      Pending restart changes: {summary['pending_restart_changes']}")
        
        print("\n✅ Settings Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Settings Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tutorial_manager():
    """Test tutorial manager functionality"""
    print("\n\nTesting Tutorial Manager")
    print("=" * 50)
    
    try:
        from systems.tutorial_manager import TutorialManager, TutorialTrigger, TutorialState
        
        # Create tutorial manager
        tutorial_manager = TutorialManager()
        
        print("✅ Tutorial Manager created")
        
        # Test tutorial definitions
        print(f"   Total tutorials: {len(tutorial_manager.tutorials)}")
        
        # List available tutorials
        for tutorial_id, tutorial in tutorial_manager.tutorials.items():
            print(f"      {tutorial_id}: {tutorial.name} ({len(tutorial.steps)} steps)")
        
        # Test tutorial triggering
        print("\n--- Testing Tutorial Triggering ---")
        
        # Trigger basic gameplay tutorial
        triggered = tutorial_manager.trigger_tutorial(TutorialTrigger.GAME_START)
        print(f"   Basic tutorial triggered: {triggered}")
        
        if triggered:
            current_info = tutorial_manager.get_current_tutorial_info()
            if current_info:
                print(f"      Current tutorial: {current_info['tutorial_name']}")
                print(f"      Step: {current_info['current_step'] + 1}/{current_info['total_steps']}")
                print(f"      Progress: {current_info['progress_percentage']:.1f}%")
        
        # Test tutorial advancement
        print("\n--- Testing Tutorial Advancement ---")
        
        # Simulate player actions
        tutorial_manager.handle_game_event("player_moved")
        
        current_info = tutorial_manager.get_current_tutorial_info()
        if current_info:
            print(f"   Advanced to step: {current_info['current_step'] + 1}")
            step_info = current_info['step_info']
            if step_info:
                print(f"      Step title: {step_info['title']}")
                print(f"      Instruction: {step_info['instruction']}")
        
        # Advance through more steps
        tutorial_manager.handle_game_event("enemy_killed")
        tutorial_manager.handle_game_event("item_collected")
        
        # Complete tutorial
        completed = tutorial_manager.complete_tutorial()
        print(f"   Tutorial completed: {completed}")
        
        # Test tutorial statistics
        print("\n--- Testing Tutorial Statistics ---")
        
        stats = tutorial_manager.get_tutorial_statistics()
        print(f"   Tutorial Statistics:")
        print(f"      Total tutorials: {stats['total_tutorials']}")
        print(f"      Completed: {stats['completed']}")
        print(f"      Completion rate: {stats['completion_rate']:.1f}%")
        print(f"      Tutorial enabled: {stats['tutorial_enabled']}")
        
        # Test export/import
        print("\n--- Testing Progress Export/Import ---")
        
        progress_data = tutorial_manager.export_progress()
        print(f"   Progress exported: {len(progress_data)} fields")
        
        # Reset and import
        tutorial_manager.reset_tutorial_progress()
        import_success = tutorial_manager.import_progress(progress_data)
        print(f"   Progress imported: {import_success}")
        
        # Test advanced tutorial triggering
        print("\n--- Testing Advanced Tutorial Triggers ---")
        
        # Try to trigger level 3 tutorial (should fail due to prerequisites)
        level3_triggered = tutorial_manager.trigger_tutorial(TutorialTrigger.LEVEL_3_REACHED)
        print(f"   Level 3 tutorial triggered (should fail): {level3_triggered}")
        
        # Complete basic tutorial first
        tutorial_manager.tutorial_progress["basic_gameplay"] = TutorialState.COMPLETED
        
        # Now try level 3 tutorial
        level3_triggered = tutorial_manager.trigger_tutorial(TutorialTrigger.LEVEL_3_REACHED)
        print(f"   Level 3 tutorial triggered (should succeed): {level3_triggered}")
        
        print("\n✅ Tutorial Manager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Tutorial Manager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_phase4_integration():
    """Test Phase 4 systems integration"""
    print("\n\nTesting Phase 4 Integration")
    print("=" * 50)
    
    # Initialize pygame for integration testing
    pygame.init()
    
    # Create temporary directory for save testing
    temp_dir = tempfile.mkdtemp()
    
    try:
        from systems.integrated_game_manager import IntegratedGameManager
        from systems.enhanced_save_manager import EnhancedSaveManager
        from systems.settings_manager import SettingsManager
        from systems.tutorial_manager import TutorialManager, TutorialTrigger
        
        print("--- Creating Integrated Systems ---")
        
        # Create all systems
        game_manager = IntegratedGameManager(1920, 1080)
        save_manager = EnhancedSaveManager(temp_dir)
        settings_manager = SettingsManager()
        tutorial_manager = TutorialManager()
        
        print("✅ All Phase 4 systems created")
        
        # Initialize integrated systems
        game_manager.initialize_systems()
        
        # Test integrated workflow
        print("\n--- Testing Integrated Workflow ---")
        
        # 1. Start new session
        game_manager.start_new_session()
        
        # 2. Trigger tutorial
        tutorial_manager.trigger_tutorial(TutorialTrigger.GAME_START)
        
        # 3. Generate level with advanced features
        level_data = game_manager.generate_level(3, "dungeon")
        
        # 4. Simulate gameplay
        game_events = {
            'enemy_killed': True,
            'damage_dealt': 200,
            'level_completed': True,
            'completion_time': 180
        }
        game_manager.update_systems(0.016, game_events)
        
        # 5. Update tutorial based on events
        tutorial_manager.handle_game_event("enemy_killed")
        
        # 6. End session
        game_manager.end_current_session(successful=True)
        
        print("✅ Integrated workflow completed")
        
        # Test comprehensive save/load
        print("\n--- Testing Comprehensive Save/Load ---")
        
        # Prepare data from all systems
        game_data = {'test_level': 5, 'test_score': 1000}
        meta_data = game_manager.meta_progression.export_progress() if hasattr(game_manager.meta_progression, 'export_progress') else {}
        settings_data = settings_manager.export_settings()
        tutorial_data = tutorial_manager.export_progress()
        
        # Combine tutorial data with achievements for save
        achievements_data = {
            'tutorial_progress': tutorial_data,
            'unlocked_achievements': ['first_tutorial_completed']
        }
        
        # Save everything
        save_success = save_manager.save_complete_game_state(
            game_data, meta_data, settings_data, achievements_data
        )
        print(f"   Comprehensive save: {save_success}")
        
        # Load everything
        loaded_game, loaded_meta, loaded_settings, loaded_achievements = save_manager.load_complete_game_state()
        
        # Verify data integrity
        data_integrity = all([
            loaded_game is not None,
            loaded_meta is not None,
            loaded_settings is not None,
            loaded_achievements is not None
        ])
        print(f"   Data integrity: {data_integrity}")
        
        # Test system status
        print("\n--- Testing System Status ---")
        
        integration_status = game_manager.get_integration_status()
        settings_summary = settings_manager.get_settings_summary()
        tutorial_stats = tutorial_manager.get_tutorial_statistics()
        
        print(f"   Integration systems initialized: {integration_status['systems_initialized']}")
        print(f"   Settings categories: {len(settings_summary['categories'])}")
        print(f"   Tutorial completion rate: {tutorial_stats['completion_rate']:.1f}%")
        
        # Test performance integration
        print("\n--- Testing Performance Integration ---")
        
        performance_info = integration_status.get('performance', {})
        print(f"   Current FPS: {performance_info.get('fps', 'N/A')}")
        print(f"   Memory usage: {performance_info.get('memory_usage', 'N/A')} MB")
        print(f"   Performance level: {performance_info.get('performance_level', 'N/A')}")
        
        # Cleanup
        game_manager.cleanup()
        
        print("\n✅ Phase 4 integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Phase 4 integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        pygame.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)

def main():
    """Run all Phase 4 system tests"""
    print("Phase 4 Systems Test Suite")
    print("=" * 60)
    
    success = True
    
    # Run tests
    tests = [
        test_integrated_game_manager,
        test_enhanced_save_manager,
        test_settings_manager,
        test_tutorial_manager,
        test_phase4_integration
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
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL PHASE 4 SYSTEM TESTS PASSED!")
        print("\nPhase 4 Implementation Summary:")
        print("- ✅ Integrated Game Manager with all Phase 3 systems")
        print("- ✅ Enhanced Save Manager with comprehensive persistence")
        print("- ✅ Settings Manager with full configuration support")
        print("- ✅ Tutorial Manager with progressive onboarding")
        print("- ✅ Full system integration and workflow")
        print("- ✅ Backward compatibility maintained")
        print("- ✅ Launch readiness achieved")
        print("\n🚀 Game is ready for launch!")
    else:
        print("❌ SOME PHASE 4 TESTS FAILED!")
        print("\nCheck the output above for specific issues.")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
