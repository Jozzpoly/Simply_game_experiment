"""
Enhanced Save Manager for Phase 4

This module provides comprehensive save/load functionality for all game systems:
- Core game state (levels, score, player data)
- Meta-progression data (currencies, mastery, prestige)
- Dynamic difficulty state and history
- Player preferences and settings
- Achievement and unlock tracking
- Version migration and compatibility
"""

import json
import os
import shutil
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SaveFileMetadata:
    """Metadata for save files"""
    version: str
    created_time: float
    last_modified: float
    game_version: str
    player_name: str
    total_playtime: int
    current_level: int
    achievements_unlocked: int
    
    
class EnhancedSaveManager:
    """Enhanced save manager with comprehensive game state persistence"""
    
    def __init__(self, save_directory: str = "saves"):
        self.save_directory = Path(save_directory)
        self.save_directory.mkdir(exist_ok=True)
        
        # Save file paths
        self.game_save_file = self.save_directory / "game_state.json"
        self.meta_save_file = self.save_directory / "meta_progression.json"
        self.settings_save_file = self.save_directory / "settings.json"
        self.achievements_save_file = self.save_directory / "achievements.json"
        
        # Backup system
        self.backup_directory = self.save_directory / "backups"
        self.backup_directory.mkdir(exist_ok=True)
        self.max_backups = 5
        
        # Version management
        self.current_version = "4.0"
        self.supported_versions = ["1.0", "2.0", "3.0", "4.0"]
        
        logger.info(f"Enhanced Save Manager initialized: {self.save_directory}")
    
    def save_complete_game_state(self, game_data: Dict[str, Any], 
                                meta_progression_data: Dict[str, Any],
                                settings_data: Dict[str, Any],
                                achievements_data: Dict[str, Any]) -> bool:
        """Save complete game state including all systems"""
        try:
            # Create backup before saving
            self._create_backup()
            
            # Save core game state
            game_success = self._save_game_state(game_data)
            
            # Save meta-progression data
            meta_success = self._save_meta_progression(meta_progression_data)
            
            # Save settings
            settings_success = self._save_settings(settings_data)
            
            # Save achievements
            achievements_success = self._save_achievements(achievements_data)
            
            success = all([game_success, meta_success, settings_success, achievements_success])
            
            if success:
                logger.info("Complete game state saved successfully")
            else:
                logger.error("Failed to save some components of game state")
                
            return success
            
        except Exception as e:
            logger.error(f"Failed to save complete game state: {e}")
            return False
    
    def load_complete_game_state(self) -> Tuple[Optional[Dict], Optional[Dict], Optional[Dict], Optional[Dict]]:
        """Load complete game state including all systems"""
        try:
            # Load core game state
            game_data = self._load_game_state()
            
            # Load meta-progression data
            meta_data = self._load_meta_progression()
            
            # Load settings
            settings_data = self._load_settings()
            
            # Load achievements
            achievements_data = self._load_achievements()
            
            # Validate and migrate if necessary
            game_data = self._validate_and_migrate_game_data(game_data)
            meta_data = self._validate_and_migrate_meta_data(meta_data)
            settings_data = self._validate_and_migrate_settings_data(settings_data)
            achievements_data = self._validate_and_migrate_achievements_data(achievements_data)
            
            logger.info("Complete game state loaded successfully")
            return game_data, meta_data, settings_data, achievements_data
            
        except Exception as e:
            logger.error(f"Failed to load complete game state: {e}")
            return None, None, None, None
    
    def _save_game_state(self, game_data: Dict[str, Any]) -> bool:
        """Save core game state"""
        try:
            # Add metadata
            enhanced_data = {
                'metadata': {
                    'version': self.current_version,
                    'saved_time': time.time(),
                    'game_version': '4.0'
                },
                'game_state': game_data
            }
            
            with open(self.game_save_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to save game state: {e}")
            return False
    
    def _load_game_state(self) -> Optional[Dict[str, Any]]:
        """Load core game state"""
        try:
            if not self.game_save_file.exists():
                return None
                
            with open(self.game_save_file, 'r') as f:
                data = json.load(f)
                
            # Extract game state from enhanced format
            if 'game_state' in data:
                return data['game_state']
            else:
                # Legacy format
                return data
                
        except Exception as e:
            logger.error(f"Failed to load game state: {e}")
            return None
    
    def _save_meta_progression(self, meta_data: Dict[str, Any]) -> bool:
        """Save meta-progression data"""
        try:
            # Add metadata
            enhanced_data = {
                'metadata': {
                    'version': self.current_version,
                    'saved_time': time.time(),
                    'data_type': 'meta_progression'
                },
                'meta_progression': meta_data
            }
            
            with open(self.meta_save_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to save meta-progression: {e}")
            return False
    
    def _load_meta_progression(self) -> Optional[Dict[str, Any]]:
        """Load meta-progression data"""
        try:
            if not self.meta_save_file.exists():
                return None
                
            with open(self.meta_save_file, 'r') as f:
                data = json.load(f)
                
            # Extract meta-progression from enhanced format
            if 'meta_progression' in data:
                return data['meta_progression']
            else:
                # Legacy format
                return data
                
        except Exception as e:
            logger.error(f"Failed to load meta-progression: {e}")
            return None
    
    def _save_settings(self, settings_data: Dict[str, Any]) -> bool:
        """Save player settings and preferences"""
        try:
            # Add metadata
            enhanced_data = {
                'metadata': {
                    'version': self.current_version,
                    'saved_time': time.time(),
                    'data_type': 'settings'
                },
                'settings': settings_data
            }
            
            with open(self.settings_save_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
    
    def _load_settings(self) -> Optional[Dict[str, Any]]:
        """Load player settings and preferences"""
        try:
            if not self.settings_save_file.exists():
                return self._get_default_settings()
                
            with open(self.settings_save_file, 'r') as f:
                data = json.load(f)
                
            # Extract settings from enhanced format
            if 'settings' in data:
                return data['settings']
            else:
                # Legacy format or direct settings
                return data
                
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return self._get_default_settings()
    
    def _save_achievements(self, achievements_data: Dict[str, Any]) -> bool:
        """Save achievement and unlock data"""
        try:
            # Add metadata
            enhanced_data = {
                'metadata': {
                    'version': self.current_version,
                    'saved_time': time.time(),
                    'data_type': 'achievements'
                },
                'achievements': achievements_data
            }
            
            with open(self.achievements_save_file, 'w') as f:
                json.dump(enhanced_data, f, indent=2)
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to save achievements: {e}")
            return False
    
    def _load_achievements(self) -> Optional[Dict[str, Any]]:
        """Load achievement and unlock data"""
        try:
            if not self.achievements_save_file.exists():
                return self._get_default_achievements()
                
            with open(self.achievements_save_file, 'r') as f:
                data = json.load(f)
                
            # Extract achievements from enhanced format
            if 'achievements' in data:
                return data['achievements']
            else:
                # Legacy format
                return data
                
        except Exception as e:
            logger.error(f"Failed to load achievements: {e}")
            return self._get_default_achievements()
    
    def _create_backup(self) -> bool:
        """Create backup of current save files"""
        try:
            timestamp = int(time.time())
            backup_dir = self.backup_directory / f"backup_{timestamp}"
            backup_dir.mkdir(exist_ok=True)
            
            # Backup all save files
            save_files = [
                self.game_save_file,
                self.meta_save_file,
                self.settings_save_file,
                self.achievements_save_file
            ]
            
            for save_file in save_files:
                if save_file.exists():
                    backup_file = backup_dir / save_file.name
                    shutil.copy2(save_file, backup_file)
            
            # Clean up old backups
            self._cleanup_old_backups()
            
            logger.info(f"Backup created: {backup_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return False
    
    def _cleanup_old_backups(self) -> None:
        """Remove old backup directories"""
        try:
            backup_dirs = sorted([d for d in self.backup_directory.iterdir() if d.is_dir()],
                                key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Keep only the most recent backups
            for old_backup in backup_dirs[self.max_backups:]:
                shutil.rmtree(old_backup)
                logger.debug(f"Removed old backup: {old_backup}")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")
    
    def _validate_and_migrate_game_data(self, data: Optional[Dict]) -> Optional[Dict]:
        """Validate and migrate game data if necessary"""
        if not data:
            return None
            
        # Check version and migrate if necessary
        version = data.get('version', '1.0')
        
        if version not in self.supported_versions:
            logger.warning(f"Unsupported save version: {version}")
            return None
        
        # Perform migrations
        if version == '1.0':
            data = self._migrate_game_data_1_to_2(data)
            version = '2.0'
        
        if version == '2.0':
            data = self._migrate_game_data_2_to_3(data)
            version = '3.0'
            
        if version == '3.0':
            data = self._migrate_game_data_3_to_4(data)
            version = '4.0'
        
        data['version'] = self.current_version
        return data
    
    def _validate_and_migrate_meta_data(self, data: Optional[Dict]) -> Optional[Dict]:
        """Validate and migrate meta-progression data"""
        if not data:
            return self._get_default_meta_progression()
            
        # Ensure all required fields exist
        required_fields = ['currencies', 'masteries', 'prestige_level', 'total_runs']
        for field in required_fields:
            if field not in data:
                data[field] = self._get_default_meta_progression()[field]
        
        return data
    
    def _validate_and_migrate_settings_data(self, data: Optional[Dict]) -> Dict[str, Any]:
        """Validate and migrate settings data"""
        if not data:
            return self._get_default_settings()
            
        # Merge with defaults to ensure all settings exist
        default_settings = self._get_default_settings()
        
        # Update defaults with loaded settings
        for key, value in data.items():
            if key in default_settings:
                default_settings[key] = value
        
        return default_settings
    
    def _validate_and_migrate_achievements_data(self, data: Optional[Dict]) -> Dict[str, Any]:
        """Validate and migrate achievements data"""
        if not data:
            return self._get_default_achievements()
            
        # Ensure all required fields exist
        default_achievements = self._get_default_achievements()
        
        for key, value in default_achievements.items():
            if key not in data:
                data[key] = value
        
        return data
    
    def _migrate_game_data_1_to_2(self, data: Dict) -> Dict:
        """Migrate game data from version 1.0 to 2.0"""
        # Add Phase 2 fields
        if 'equipment_sets' not in data:
            data['equipment_sets'] = {}
        if 'status_effects' not in data:
            data['status_effects'] = []
        return data
    
    def _migrate_game_data_2_to_3(self, data: Dict) -> Dict:
        """Migrate game data from version 2.0 to 3.0"""
        # Add Phase 3 fields
        if 'architectural_themes_seen' not in data:
            data['architectural_themes_seen'] = []
        if 'difficulty_zones_encountered' not in data:
            data['difficulty_zones_encountered'] = []
        return data
    
    def _migrate_game_data_3_to_4(self, data: Dict) -> Dict:
        """Migrate game data from version 3.0 to 4.0"""
        # Add Phase 4 integration fields
        if 'ui_preferences' not in data:
            data['ui_preferences'] = {}
        if 'tutorial_progress' not in data:
            data['tutorial_progress'] = {}
        return data
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings configuration"""
        return {
            'graphics': {
                'fullscreen': False,
                'resolution': [1920, 1080],
                'vsync': True,
                'ui_scale': 1.0
            },
            'audio': {
                'master_volume': 0.8,
                'music_volume': 0.7,
                'sfx_volume': 0.8,
                'mute': False
            },
            'gameplay': {
                'difficulty_mode': 'adaptive',
                'auto_save': True,
                'show_fps': False,
                'show_tooltips': True
            },
            'accessibility': {
                'colorblind_mode': False,
                'high_contrast': False,
                'large_text': False,
                'screen_reader': False
            },
            'controls': {
                'mouse_sensitivity': 1.0,
                'keyboard_layout': 'qwerty',
                'custom_keybinds': {}
            }
        }
    
    def _get_default_meta_progression(self) -> Dict[str, Any]:
        """Get default meta-progression data"""
        return {
            'currencies': {
                'soul_essence': {'name': 'soul_essence', 'amount': 0, 'lifetime_earned': 0},
                'knowledge_crystals': {'name': 'knowledge_crystals', 'amount': 0, 'lifetime_earned': 0},
                'fate_tokens': {'name': 'fate_tokens', 'amount': 0, 'lifetime_earned': 0}
            },
            'masteries': {
                'weapon_mastery': {'mastery_type': 'weapon_mastery', 'level': 0, 'experience': 0, 'unlocked_abilities': []},
                'magic_mastery': {'mastery_type': 'magic_mastery', 'level': 0, 'experience': 0, 'unlocked_abilities': []}
            },
            'prestige_level': 0,
            'prestige_experience': 0,
            'total_runs': 0,
            'successful_runs': 0,
            'total_playtime': 0,
            'deepest_level_reached': 0,
            'unlocked_biomes': [],
            'unlocked_enemies': [],
            'unlocked_features': [],
            'legacy_items': [],
            'memory_fragments': []
        }
    
    def _get_default_achievements(self) -> Dict[str, Any]:
        """Get default achievements data"""
        return {
            'unlocked_achievements': [],
            'achievement_progress': {},
            'hidden_achievements_discovered': [],
            'achievement_points': 0,
            'last_achievement_time': 0
        }
    
    def save_exists(self) -> bool:
        """Check if any save files exist"""
        return any([
            self.game_save_file.exists(),
            self.meta_save_file.exists(),
            self.settings_save_file.exists(),
            self.achievements_save_file.exists()
        ])
    
    def delete_all_saves(self) -> bool:
        """Delete all save files"""
        try:
            save_files = [
                self.game_save_file,
                self.meta_save_file,
                self.settings_save_file,
                self.achievements_save_file
            ]
            
            for save_file in save_files:
                if save_file.exists():
                    save_file.unlink()
            
            logger.info("All save files deleted")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete save files: {e}")
            return False
    
    def get_save_metadata(self) -> Optional[SaveFileMetadata]:
        """Get metadata about the current save"""
        try:
            if not self.game_save_file.exists():
                return None
                
            with open(self.game_save_file, 'r') as f:
                data = json.load(f)
                
            metadata = data.get('metadata', {})
            game_state = data.get('game_state', data)
            
            return SaveFileMetadata(
                version=metadata.get('version', '1.0'),
                created_time=metadata.get('saved_time', 0),
                last_modified=self.game_save_file.stat().st_mtime,
                game_version=metadata.get('game_version', '1.0'),
                player_name=game_state.get('player_name', 'Unknown'),
                total_playtime=game_state.get('total_playtime', 0),
                current_level=game_state.get('current_level', 1),
                achievements_unlocked=len(game_state.get('achievements', []))
            )
            
        except Exception as e:
            logger.error(f"Failed to get save metadata: {e}")
            return None
