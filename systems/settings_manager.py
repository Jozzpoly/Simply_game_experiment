"""
Settings Manager for Phase 4

This module provides comprehensive settings and configuration management:
- Graphics and performance settings
- Audio and accessibility options
- Gameplay difficulty preferences
- UI customization options
- Control scheme configuration
- Real-time settings application
"""

import pygame
import logging
import json
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from config import *

logger = logging.getLogger(__name__)


class SettingType(Enum):
    """Types of settings"""
    BOOLEAN = "boolean"
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    CHOICE = "choice"
    KEYBIND = "keybind"
    RESOLUTION = "resolution"


@dataclass
class SettingDefinition:
    """Definition of a setting"""
    key: str
    name: str
    description: str
    setting_type: SettingType
    default_value: Any
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    choices: Optional[List[Any]] = None
    requires_restart: bool = False
    category: str = "general"
    on_change: Optional[Callable] = None


class SettingsManager:
    """Comprehensive settings and configuration manager"""
    
    def __init__(self):
        self.settings: Dict[str, Any] = {}
        self.setting_definitions: Dict[str, SettingDefinition] = {}
        self.categories: Dict[str, List[str]] = {}
        self.change_callbacks: Dict[str, List[Callable]] = {}
        self.pending_restart_changes: List[str] = []
        
        # Initialize setting definitions
        self._initialize_setting_definitions()
        
        # Load default values
        self._load_default_settings()
        
        logger.info("Settings Manager initialized")
    
    def _initialize_setting_definitions(self) -> None:
        """Initialize all setting definitions"""
        
        # Graphics Settings
        graphics_settings = [
            SettingDefinition(
                key="graphics.fullscreen",
                name="Fullscreen",
                description="Enable fullscreen mode",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                requires_restart=True,
                category="graphics"
            ),
            SettingDefinition(
                key="graphics.resolution",
                name="Resolution",
                description="Screen resolution",
                setting_type=SettingType.RESOLUTION,
                default_value=[1920, 1080],
                choices=[[1280, 720], [1920, 1080], [2560, 1440], [3840, 2160]],
                requires_restart=True,
                category="graphics"
            ),
            SettingDefinition(
                key="graphics.vsync",
                name="V-Sync",
                description="Enable vertical synchronization",
                setting_type=SettingType.BOOLEAN,
                default_value=True,
                category="graphics"
            ),
            SettingDefinition(
                key="graphics.ui_scale",
                name="UI Scale",
                description="User interface scaling factor",
                setting_type=SettingType.FLOAT,
                default_value=1.0,
                min_value=0.5,
                max_value=2.0,
                category="graphics"
            ),
            SettingDefinition(
                key="graphics.particle_quality",
                name="Particle Quality",
                description="Quality of particle effects",
                setting_type=SettingType.CHOICE,
                default_value="high",
                choices=["low", "medium", "high", "ultra"],
                category="graphics"
            ),
            SettingDefinition(
                key="graphics.shadow_quality",
                name="Shadow Quality",
                description="Quality of shadow effects",
                setting_type=SettingType.CHOICE,
                default_value="medium",
                choices=["off", "low", "medium", "high"],
                category="graphics"
            )
        ]
        
        # Audio Settings
        audio_settings = [
            SettingDefinition(
                key="audio.master_volume",
                name="Master Volume",
                description="Overall audio volume",
                setting_type=SettingType.FLOAT,
                default_value=0.8,
                min_value=0.0,
                max_value=1.0,
                category="audio"
            ),
            SettingDefinition(
                key="audio.music_volume",
                name="Music Volume",
                description="Background music volume",
                setting_type=SettingType.FLOAT,
                default_value=0.7,
                min_value=0.0,
                max_value=1.0,
                category="audio"
            ),
            SettingDefinition(
                key="audio.sfx_volume",
                name="Sound Effects Volume",
                description="Sound effects volume",
                setting_type=SettingType.FLOAT,
                default_value=0.8,
                min_value=0.0,
                max_value=1.0,
                category="audio"
            ),
            SettingDefinition(
                key="audio.mute",
                name="Mute All Audio",
                description="Disable all audio",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="audio"
            )
        ]
        
        # Gameplay Settings
        gameplay_settings = [
            SettingDefinition(
                key="gameplay.difficulty_mode",
                name="Difficulty Mode",
                description="How difficulty is managed",
                setting_type=SettingType.CHOICE,
                default_value="adaptive",
                choices=["fixed_easy", "fixed_normal", "fixed_hard", "adaptive", "custom"],
                category="gameplay"
            ),
            SettingDefinition(
                key="gameplay.auto_save",
                name="Auto Save",
                description="Automatically save progress",
                setting_type=SettingType.BOOLEAN,
                default_value=True,
                category="gameplay"
            ),
            SettingDefinition(
                key="gameplay.show_fps",
                name="Show FPS",
                description="Display frame rate counter",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="gameplay"
            ),
            SettingDefinition(
                key="gameplay.show_tooltips",
                name="Show Tooltips",
                description="Display helpful tooltips",
                setting_type=SettingType.BOOLEAN,
                default_value=True,
                category="gameplay"
            ),
            SettingDefinition(
                key="gameplay.pause_on_focus_loss",
                name="Pause on Focus Loss",
                description="Pause game when window loses focus",
                setting_type=SettingType.BOOLEAN,
                default_value=True,
                category="gameplay"
            )
        ]
        
        # Accessibility Settings
        accessibility_settings = [
            SettingDefinition(
                key="accessibility.colorblind_mode",
                name="Colorblind Support",
                description="Enable colorblind-friendly colors",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="accessibility"
            ),
            SettingDefinition(
                key="accessibility.high_contrast",
                name="High Contrast Mode",
                description="Increase visual contrast",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="accessibility"
            ),
            SettingDefinition(
                key="accessibility.large_text",
                name="Large Text",
                description="Use larger text size",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="accessibility"
            ),
            SettingDefinition(
                key="accessibility.screen_reader",
                name="Screen Reader Support",
                description="Enable screen reader compatibility",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="accessibility"
            ),
            SettingDefinition(
                key="accessibility.reduced_motion",
                name="Reduced Motion",
                description="Reduce animations and effects",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="accessibility"
            )
        ]
        
        # Controls Settings
        controls_settings = [
            SettingDefinition(
                key="controls.mouse_sensitivity",
                name="Mouse Sensitivity",
                description="Mouse movement sensitivity",
                setting_type=SettingType.FLOAT,
                default_value=1.0,
                min_value=0.1,
                max_value=3.0,
                category="controls"
            ),
            SettingDefinition(
                key="controls.keyboard_layout",
                name="Keyboard Layout",
                description="Keyboard layout preference",
                setting_type=SettingType.CHOICE,
                default_value="qwerty",
                choices=["qwerty", "azerty", "dvorak", "custom"],
                category="controls"
            )
        ]
        
        # Advanced Settings
        advanced_settings = [
            SettingDefinition(
                key="advanced.debug_mode",
                name="Debug Mode",
                description="Enable debug features",
                setting_type=SettingType.BOOLEAN,
                default_value=False,
                category="advanced"
            ),
            SettingDefinition(
                key="advanced.performance_monitoring",
                name="Performance Monitoring",
                description="Enable performance monitoring",
                setting_type=SettingType.BOOLEAN,
                default_value=True,
                category="advanced"
            ),
            SettingDefinition(
                key="advanced.log_level",
                name="Log Level",
                description="Logging verbosity level",
                setting_type=SettingType.CHOICE,
                default_value="INFO",
                choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                category="advanced"
            )
        ]
        
        # Register all settings
        all_settings = (graphics_settings + audio_settings + gameplay_settings + 
                       accessibility_settings + controls_settings + advanced_settings)
        
        for setting in all_settings:
            self.setting_definitions[setting.key] = setting
            
            # Organize by category
            if setting.category not in self.categories:
                self.categories[setting.category] = []
            self.categories[setting.category].append(setting.key)
    
    def _load_default_settings(self) -> None:
        """Load default values for all settings"""
        for key, definition in self.setting_definitions.items():
            self.settings[key] = definition.default_value
    
    def get_setting(self, key: str) -> Any:
        """Get a setting value"""
        return self.settings.get(key, None)
    
    def set_setting(self, key: str, value: Any, apply_immediately: bool = True) -> bool:
        """Set a setting value"""
        try:
            if key not in self.setting_definitions:
                logger.warning(f"Unknown setting key: {key}")
                return False
            
            definition = self.setting_definitions[key]
            
            # Validate value
            if not self._validate_setting_value(definition, value):
                logger.warning(f"Invalid value for setting {key}: {value}")
                return False
            
            # Store old value
            old_value = self.settings.get(key)
            
            # Set new value
            self.settings[key] = value
            
            # Handle restart requirement
            if definition.requires_restart:
                if key not in self.pending_restart_changes:
                    self.pending_restart_changes.append(key)
                logger.info(f"Setting {key} changed, restart required")
            
            # Apply immediately if requested and possible
            if apply_immediately and not definition.requires_restart:
                self._apply_setting_change(key, value, old_value)
            
            # Call change callbacks
            self._call_change_callbacks(key, value, old_value)
            
            logger.debug(f"Setting {key} changed from {old_value} to {value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set setting {key}: {e}")
            return False
    
    def _validate_setting_value(self, definition: SettingDefinition, value: Any) -> bool:
        """Validate a setting value against its definition"""
        try:
            if definition.setting_type == SettingType.BOOLEAN:
                return isinstance(value, bool)
            
            elif definition.setting_type == SettingType.INTEGER:
                if not isinstance(value, int):
                    return False
                if definition.min_value is not None and value < definition.min_value:
                    return False
                if definition.max_value is not None and value > definition.max_value:
                    return False
                return True
            
            elif definition.setting_type == SettingType.FLOAT:
                if not isinstance(value, (int, float)):
                    return False
                if definition.min_value is not None and value < definition.min_value:
                    return False
                if definition.max_value is not None and value > definition.max_value:
                    return False
                return True
            
            elif definition.setting_type == SettingType.STRING:
                return isinstance(value, str)
            
            elif definition.setting_type == SettingType.CHOICE:
                return value in definition.choices
            
            elif definition.setting_type == SettingType.RESOLUTION:
                return (isinstance(value, list) and len(value) == 2 and
                       all(isinstance(x, int) and x > 0 for x in value))
            
            elif definition.setting_type == SettingType.KEYBIND:
                # Validate keybind format
                return isinstance(value, (int, str))
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating setting value: {e}")
            return False
    
    def _apply_setting_change(self, key: str, new_value: Any, old_value: Any) -> None:
        """Apply a setting change immediately"""
        try:
            # Audio settings
            if key.startswith("audio."):
                self._apply_audio_setting(key, new_value)
            
            # Graphics settings
            elif key.startswith("graphics."):
                self._apply_graphics_setting(key, new_value)
            
            # Gameplay settings
            elif key.startswith("gameplay."):
                self._apply_gameplay_setting(key, new_value)
            
            # Accessibility settings
            elif key.startswith("accessibility."):
                self._apply_accessibility_setting(key, new_value)
            
            # Controls settings
            elif key.startswith("controls."):
                self._apply_controls_setting(key, new_value)
            
        except Exception as e:
            logger.error(f"Failed to apply setting change {key}: {e}")
    
    def _apply_audio_setting(self, key: str, value: Any) -> None:
        """Apply audio setting changes"""
        # This would integrate with the audio manager
        logger.debug(f"Applied audio setting: {key} = {value}")
    
    def _apply_graphics_setting(self, key: str, value: Any) -> None:
        """Apply graphics setting changes"""
        # This would integrate with the graphics/rendering system
        logger.debug(f"Applied graphics setting: {key} = {value}")
    
    def _apply_gameplay_setting(self, key: str, value: Any) -> None:
        """Apply gameplay setting changes"""
        # This would integrate with the game manager
        logger.debug(f"Applied gameplay setting: {key} = {value}")
    
    def _apply_accessibility_setting(self, key: str, value: Any) -> None:
        """Apply accessibility setting changes"""
        # This would integrate with the UI system
        logger.debug(f"Applied accessibility setting: {key} = {value}")
    
    def _apply_controls_setting(self, key: str, value: Any) -> None:
        """Apply controls setting changes"""
        # This would integrate with the input system
        logger.debug(f"Applied controls setting: {key} = {value}")
    
    def _call_change_callbacks(self, key: str, new_value: Any, old_value: Any) -> None:
        """Call registered change callbacks"""
        if key in self.change_callbacks:
            for callback in self.change_callbacks[key]:
                try:
                    callback(key, new_value, old_value)
                except Exception as e:
                    logger.error(f"Error in setting change callback: {e}")
    
    def register_change_callback(self, key: str, callback: Callable) -> None:
        """Register a callback for setting changes"""
        if key not in self.change_callbacks:
            self.change_callbacks[key] = []
        self.change_callbacks[key].append(callback)
    
    def get_category_settings(self, category: str) -> Dict[str, Any]:
        """Get all settings in a category"""
        if category not in self.categories:
            return {}
        
        return {key: self.settings[key] for key in self.categories[category]}
    
    def get_all_categories(self) -> List[str]:
        """Get list of all setting categories"""
        return list(self.categories.keys())
    
    def get_setting_definition(self, key: str) -> Optional[SettingDefinition]:
        """Get setting definition"""
        return self.setting_definitions.get(key)
    
    def reset_to_defaults(self, category: Optional[str] = None) -> None:
        """Reset settings to default values"""
        if category:
            # Reset specific category
            if category in self.categories:
                for key in self.categories[category]:
                    definition = self.setting_definitions[key]
                    self.set_setting(key, definition.default_value)
        else:
            # Reset all settings
            for key, definition in self.setting_definitions.items():
                self.set_setting(key, definition.default_value)
        
        logger.info(f"Settings reset to defaults: {category or 'all'}")
    
    def export_settings(self) -> Dict[str, Any]:
        """Export current settings"""
        return self.settings.copy()
    
    def import_settings(self, settings_data: Dict[str, Any]) -> bool:
        """Import settings from data"""
        try:
            success_count = 0
            total_count = len(settings_data)
            
            for key, value in settings_data.items():
                if self.set_setting(key, value, apply_immediately=False):
                    success_count += 1
            
            # Apply all changes at once
            self._apply_all_settings()
            
            logger.info(f"Imported {success_count}/{total_count} settings")
            return success_count == total_count
            
        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False
    
    def _apply_all_settings(self) -> None:
        """Apply all current settings"""
        for key, value in self.settings.items():
            definition = self.setting_definitions.get(key)
            if definition and not definition.requires_restart:
                self._apply_setting_change(key, value, None)
    
    def has_pending_restart_changes(self) -> bool:
        """Check if there are settings that require restart"""
        return len(self.pending_restart_changes) > 0
    
    def get_pending_restart_changes(self) -> List[str]:
        """Get list of settings that require restart"""
        return self.pending_restart_changes.copy()
    
    def clear_pending_restart_changes(self) -> None:
        """Clear pending restart changes (call after restart)"""
        self.pending_restart_changes.clear()
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Get summary of current settings"""
        return {
            'total_settings': len(self.settings),
            'categories': list(self.categories.keys()),
            'pending_restart_changes': len(self.pending_restart_changes),
            'settings_by_category': {
                category: len(keys) for category, keys in self.categories.items()
            }
        }
