"""
Integrated Game Manager for Phase 4

This module coordinates all Phase 3 systems integration into the main game loop:
- Meta-progression system integration
- Dynamic difficulty system integration  
- Advanced level generation integration
- Modern UI system integration
- Performance monitoring integration
"""

import pygame
import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from systems.meta_progression import MetaProgressionManager
from systems.dynamic_difficulty import DynamicDifficultyManager
from systems.advanced_generation import AdvancedLevelGenerator
from ui.modern_ui_system import ModernUISystem
from systems.performance_manager import PerformanceManager
from config import *

logger = logging.getLogger(__name__)


@dataclass
class GameSession:
    """Represents a single game session with integrated systems"""
    session_id: str
    start_time: float
    current_level: int
    player_deaths: int
    enemies_killed: int
    damage_dealt: int
    damage_taken: int
    items_collected: int
    secrets_discovered: int
    architectural_themes_seen: List[str]
    difficulty_zones_encountered: List[str]
    
    def get_session_duration(self) -> float:
        """Get session duration in seconds"""
        return time.time() - self.start_time


class IntegratedGameManager:
    """Main coordinator for all Phase 3 systems integration"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize all Phase 3 systems
        self.meta_progression = MetaProgressionManager()
        self.dynamic_difficulty = DynamicDifficultyManager()
        self.modern_ui = ModernUISystem(screen_width, screen_height)
        self.performance_manager = PerformanceManager()
        
        # Game session tracking
        self.current_session: Optional[GameSession] = None
        self.session_history: List[GameSession] = []
        
        # Integration state
        self.systems_initialized = False
        self.integration_enabled = True
        self.last_save_time = 0
        self.auto_save_interval = 30  # seconds
        
        # Level generation
        self.current_level_generator: Optional[AdvancedLevelGenerator] = None
        self.level_generation_cache: Dict[int, Any] = {}
        
        # UI state
        self.ui_components_created = False
        self.active_tooltips: List[str] = []
        
        logger.info("Integrated Game Manager initialized")
        
    def initialize_systems(self) -> bool:
        """Initialize all integrated systems"""
        try:
            # Load meta-progression data
            self.meta_progression.load_meta_progression()
            
            # Initialize dynamic difficulty with meta-progression bonuses
            self._apply_meta_progression_bonuses()
            
            # Create UI components
            self._create_ui_components()
            
            # Initialize performance monitoring
            self.performance_manager.enabled = True
            
            self.systems_initialized = True
            logger.info("All integrated systems initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize integrated systems: {e}")
            return False
    
    def start_new_session(self, starting_level: int = 1) -> bool:
        """Start a new game session with integrated systems"""
        try:
            # End previous session if exists
            if self.current_session:
                self.end_current_session(successful=False)
            
            # Create new session
            session_id = f"session_{int(time.time())}"
            self.current_session = GameSession(
                session_id=session_id,
                start_time=time.time(),
                current_level=starting_level,
                player_deaths=0,
                enemies_killed=0,
                damage_dealt=0,
                damage_taken=0,
                items_collected=0,
                secrets_discovered=0,
                architectural_themes_seen=[],
                difficulty_zones_encountered=[]
            )
            
            # Notify systems of new session
            self.meta_progression.on_run_start()
            self.dynamic_difficulty.start_new_level()
            
            # Apply inherited items from meta-progression
            inherited_items = self.meta_progression.get_inherited_items()
            
            logger.info(f"New session started: {session_id}, inherited items: {len(inherited_items)}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start new session: {e}")
            return False
    
    def end_current_session(self, successful: bool = False) -> bool:
        """End the current game session and update systems"""
        if not self.current_session:
            return True
            
        try:
            session = self.current_session
            session_duration = session.get_session_duration()
            
            # Update meta-progression
            self.meta_progression.on_run_end(
                successful=successful,
                level_reached=session.current_level,
                playtime=int(session_duration)
            )
            
            # Add mastery experience based on performance
            self._award_mastery_experience(session)
            
            # Add meta currencies based on achievements
            self._award_meta_currencies(session)
            
            # Add legacy items if appropriate
            self._process_legacy_items(session)
            
            # Save meta-progression
            self.meta_progression.save_meta_progression()
            
            # Store session in history
            self.session_history.append(session)
            self.current_session = None
            
            logger.info(f"Session ended: successful={successful}, level={session.current_level}, duration={session_duration:.1f}s")
            return True
            
        except Exception as e:
            logger.error(f"Failed to end session: {e}")
            return False
    
    def generate_level(self, level_number: int, biome_type: str = None) -> Tuple:
        """Generate a level using advanced generation system"""
        try:
            # Check cache first
            cache_key = f"{level_number}_{biome_type}"
            if cache_key in self.level_generation_cache:
                logger.debug(f"Using cached level generation for {cache_key}")
                return self.level_generation_cache[cache_key]
            
            # Create advanced level generator
            self.current_level_generator = AdvancedLevelGenerator(
                current_level=level_number,
                biome_type=biome_type
            )
            
            # Apply difficulty multipliers from dynamic difficulty
            difficulty_multipliers = self.dynamic_difficulty.get_difficulty_multipliers()
            self._apply_difficulty_to_generator(difficulty_multipliers)
            
            # Generate level
            level_data = self.current_level_generator.generate()
            
            # Track architectural theme and difficulty zones
            if self.current_session and len(level_data) >= 10:
                advanced_data = level_data[9]
                if isinstance(advanced_data, dict):
                    theme = advanced_data.get('architectural_theme')
                    if theme and theme not in self.current_session.architectural_themes_seen:
                        self.current_session.architectural_themes_seen.append(theme)
                    
                    difficulty_zones = advanced_data.get('difficulty_zones', [])
                    for zone_type, _, _ in difficulty_zones:
                        if zone_type not in self.current_session.difficulty_zones_encountered:
                            self.current_session.difficulty_zones_encountered.append(zone_type)
            
            # Cache the result
            self.level_generation_cache[cache_key] = level_data
            
            # Limit cache size
            if len(self.level_generation_cache) > 10:
                oldest_key = next(iter(self.level_generation_cache))
                del self.level_generation_cache[oldest_key]
            
            logger.info(f"Advanced level generated: level={level_number}, biome={biome_type}")
            return level_data
            
        except Exception as e:
            logger.error(f"Failed to generate level: {e}")
            # Fallback to basic generation
            from level.level_generator import LevelGenerator
            basic_generator = LevelGenerator(current_level=level_number)
            return basic_generator.generate()
    
    def update_systems(self, delta_time: float, game_events: Dict[str, Any]) -> None:
        """Update all integrated systems"""
        if not self.systems_initialized:
            return
            
        try:
            # Update performance monitoring
            self.performance_manager.update(delta_time)
            
            # Update dynamic difficulty
            self.dynamic_difficulty.update(delta_time)
            
            # Process game events for systems
            self._process_game_events(game_events)
            
            # Update UI system
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            self.modern_ui.update(mouse_pos, mouse_pressed)
            
            # Auto-save meta-progression periodically
            current_time = time.time()
            if current_time - self.last_save_time > self.auto_save_interval:
                self.meta_progression.save_meta_progression()
                self.last_save_time = current_time
                
        except Exception as e:
            logger.error(f"Error updating integrated systems: {e}")
    
    def _apply_meta_progression_bonuses(self) -> None:
        """Apply meta-progression bonuses to game systems"""
        # Get prestige bonuses
        prestige_bonuses = self.meta_progression.get_prestige_bonuses()
        
        # Get mastery bonuses
        weapon_bonuses = self.meta_progression.get_mastery_bonuses('weapon_mastery')
        magic_bonuses = self.meta_progression.get_mastery_bonuses('magic_mastery')
        
        # Apply bonuses to dynamic difficulty (easier start for experienced players)
        if prestige_bonuses.get('all_stats', 0) > 0:
            # Slightly reduce initial difficulty for prestige players
            self.dynamic_difficulty.target_difficulty_multiplier *= 0.95
            
        logger.info(f"Applied meta-progression bonuses: prestige={prestige_bonuses}, weapon={weapon_bonuses}, magic={magic_bonuses}")
    
    def _create_ui_components(self) -> None:
        """Create modern UI components for integrated systems"""
        if self.ui_components_created:
            return
            
        # Create meta-progression UI elements
        self._create_meta_progression_ui()
        
        # Create difficulty UI elements
        self._create_difficulty_ui()
        
        # Create settings UI elements
        self._create_settings_ui()
        
        self.ui_components_created = True
        logger.info("Modern UI components created")
    
    def _create_meta_progression_ui(self) -> None:
        """Create UI elements for meta-progression system"""
        # Currency display panel
        currency_panel = self.modern_ui.create_panel(
            x=10, y=10, width=300, height=120, title="Meta Progression"
        )
        
        # Mastery progress indicators
        mastery_panel = self.modern_ui.create_panel(
            x=10, y=140, width=300, height=100, title="Mastery Progress"
        )
    
    def _create_difficulty_ui(self) -> None:
        """Create UI elements for dynamic difficulty system"""
        # Difficulty indicator
        difficulty_panel = self.modern_ui.create_panel(
            x=self.screen_width - 320, y=10, width=310, height=80, title="Difficulty"
        )
    
    def _create_settings_ui(self) -> None:
        """Create UI elements for settings and configuration"""
        # Settings button
        settings_button = self.modern_ui.create_button(
            x=self.screen_width - 100, y=self.screen_height - 50,
            width=80, height=40, text="Settings",
            callback=self._open_settings_menu, style="secondary"
        )
    
    def _apply_difficulty_to_generator(self, difficulty_multipliers: Dict[str, float]) -> None:
        """Apply dynamic difficulty multipliers to level generator"""
        if not self.current_level_generator:
            return
            
        # Adjust enemy count based on difficulty
        enemy_multiplier = difficulty_multipliers.get('enemy_count', 1.0)
        self.current_level_generator.max_enemies = int(
            self.current_level_generator.max_enemies * enemy_multiplier
        )
        
        # Adjust enemy density
        self.current_level_generator.enemy_density_multiplier *= enemy_multiplier
    
    def _process_game_events(self, game_events: Dict[str, Any]) -> None:
        """Process game events for integrated systems"""
        # Player death
        if game_events.get('player_death'):
            self.dynamic_difficulty.record_player_death()
            if self.current_session:
                self.current_session.player_deaths += 1
        
        # Enemy killed
        if game_events.get('enemy_killed'):
            self.dynamic_difficulty.record_enemy_killed()
            if self.current_session:
                self.current_session.enemies_killed += 1
            
            # Award mastery experience
            self.meta_progression.add_mastery_experience('weapon_mastery', 10)
        
        # Damage dealt
        damage_dealt = game_events.get('damage_dealt', 0)
        if damage_dealt > 0:
            self.dynamic_difficulty.record_damage_dealt(damage_dealt)
            if self.current_session:
                self.current_session.damage_dealt += damage_dealt
        
        # Damage taken
        damage_taken = game_events.get('damage_taken', 0)
        if damage_taken > 0:
            self.dynamic_difficulty.record_damage_taken(damage_taken)
            if self.current_session:
                self.current_session.damage_taken += damage_taken
        
        # Level completed
        if game_events.get('level_completed'):
            completion_time = game_events.get('completion_time', 0)
            self.dynamic_difficulty.record_level_completed(completion_time)
            if self.current_session:
                self.current_session.current_level += 1
        
        # Item collected
        if game_events.get('item_collected'):
            if self.current_session:
                self.current_session.items_collected += 1
        
        # Secret discovered
        if game_events.get('secret_discovered'):
            if self.current_session:
                self.current_session.secrets_discovered += 1
            
            # Award knowledge crystals for discoveries
            self.meta_progression.add_currency('knowledge_crystals', 5, 'secret discovery')
    
    def _award_mastery_experience(self, session: GameSession) -> None:
        """Award mastery experience based on session performance"""
        # Weapon mastery based on enemies killed
        weapon_exp = session.enemies_killed * 5
        self.meta_progression.add_mastery_experience('weapon_mastery', weapon_exp)
        
        # Magic mastery based on damage dealt (assuming some magic use)
        magic_exp = max(1, session.damage_dealt // 100)
        self.meta_progression.add_mastery_experience('magic_mastery', magic_exp)
    
    def _award_meta_currencies(self, session: GameSession) -> None:
        """Award meta currencies based on session achievements"""
        # Soul essence for general progress
        soul_essence = session.current_level * 10 + session.enemies_killed * 2
        self.meta_progression.add_currency('soul_essence', soul_essence, 'session completion')
        
        # Knowledge crystals for exploration
        knowledge_crystals = len(session.architectural_themes_seen) * 5 + session.secrets_discovered * 10
        self.meta_progression.add_currency('knowledge_crystals', knowledge_crystals, 'exploration')
        
        # Fate tokens for exceptional performance
        if session.current_level >= 15 and session.player_deaths <= 2:
            self.meta_progression.add_currency('fate_tokens', 1, 'exceptional performance')
    
    def _process_legacy_items(self, session: GameSession) -> None:
        """Process items for legacy system"""
        # Add items to legacy system based on session performance
        if session.current_level >= 10:
            # Example: Add a legacy item for reaching level 10+
            legacy_item_data = {
                'type': 'weapon',
                'name': f'Veteran Blade (Level {session.current_level})',
                'stats': {'damage': 10 + session.current_level}
            }
            self.meta_progression.add_legacy_item('weapon', legacy_item_data, 0.15)
    
    def _open_settings_menu(self) -> None:
        """Open the settings menu"""
        logger.info("Settings menu requested")
        # This will be implemented in the settings manager
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrated systems"""
        return {
            'systems_initialized': self.systems_initialized,
            'current_session': self.current_session is not None,
            'meta_progression': self.meta_progression.get_meta_progression_summary(),
            'dynamic_difficulty': self.dynamic_difficulty.get_performance_summary(),
            'performance': {
                'fps': self.performance_manager.current_fps,
                'memory_usage': self.performance_manager.memory_usage,
                'performance_level': self.performance_manager.performance_level
            },
            'ui_components': self.ui_components_created
        }
    
    def cleanup(self) -> None:
        """Clean up integrated systems"""
        try:
            # End current session
            if self.current_session:
                self.end_current_session(successful=False)
            
            # Save meta-progression
            self.meta_progression.save_meta_progression()
            
            # Clear UI components
            self.modern_ui.clear_components()
            
            logger.info("Integrated systems cleaned up successfully")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
