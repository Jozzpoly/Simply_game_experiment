"""
Systems Manager - Coordinates all game systems for optimal performance and modularity.
Handles initialization, updates, and communication between different systems.
"""

import pygame
import logging
from typing import Dict, Any, Optional, Tuple
from .performance_manager import PerformanceManager, EnemyOptimizationManager
from .terrain_system import TerrainManager
from config import *

logger = logging.getLogger(__name__)

class SystemsManager:
    """Central coordinator for all game systems"""
    
    def __init__(self, seed: int = None):
        """Initialize all game systems"""
        logger.info("Initializing game systems...")
        
        # Core systems
        self.performance_manager = PerformanceManager()
        self.enemy_optimization_manager = EnemyOptimizationManager(self.performance_manager)
        self.terrain_manager = TerrainManager(seed) if DYNAMIC_TERRAIN_ENABLED else None
        
        # System state
        self.initialized = True
        self.last_update_time = 0
        self.frame_count = 0
        
        # Performance tracking
        self.system_update_times: Dict[str, float] = {}
        
        logger.info("Game systems initialized successfully")
    
    def update(self, dt: float, game_state: Dict[str, Any]) -> None:
        """Update all systems with current game state"""
        if not self.initialized:
            return
        
        self.frame_count += 1
        current_time = pygame.time.get_ticks()
        
        # Update performance manager first
        start_time = pygame.time.get_ticks()
        self.performance_manager.update(dt)
        self.system_update_times['performance'] = pygame.time.get_ticks() - start_time
        
        # Extract common data from game state
        player_pos = game_state.get('player_position', (0, 0))
        camera_pos = game_state.get('camera_position', (0, 0))
        screen_size = game_state.get('screen_size', (SCREEN_WIDTH, SCREEN_HEIGHT))
        enemies = game_state.get('enemies', pygame.sprite.Group())
        
        # Update enemy optimization
        if enemies and hasattr(enemies, '__iter__'):
            start_time = pygame.time.get_ticks()
            self.enemy_optimization_manager.update_enemy_optimization(enemies, player_pos)
            self.system_update_times['enemy_optimization'] = pygame.time.get_ticks() - start_time
        
        # Update terrain system
        if self.terrain_manager:
            start_time = pygame.time.get_ticks()
            self.terrain_manager.update(camera_pos[0], camera_pos[1], screen_size[0], screen_size[1])
            self.system_update_times['terrain'] = pygame.time.get_ticks() - start_time
        
        self.last_update_time = current_time
    
    def should_enemy_update(self, enemy) -> bool:
        """Check if an enemy should update this frame"""
        return self.enemy_optimization_manager.should_enemy_update(enemy)
    
    def is_enemy_using_simplified_ai(self, enemy) -> bool:
        """Check if an enemy should use simplified AI"""
        return self.enemy_optimization_manager.is_enemy_using_simplified_ai(enemy)
    
    def get_tile_at_position(self, world_x: int, world_y: int) -> int:
        """Get terrain tile type at world position"""
        if self.terrain_manager:
            return self.terrain_manager.get_tile_at_position(world_x, world_y)
        return TERRAIN_TYPES['floor']  # Default fallback
    
    def render_terrain(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """Render terrain if terrain system is enabled"""
        if self.terrain_manager:
            self.terrain_manager.render_visible_terrain(surface, camera_x, camera_y)
    
    def cleanup_dead_enemies(self, alive_enemies: pygame.sprite.Group) -> None:
        """Clean up optimization data for dead enemies"""
        self.enemy_optimization_manager.cleanup_dead_enemies(alive_enemies)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics from all systems"""
        stats = {
            'frame_count': self.frame_count,
            'systems_initialized': self.initialized,
            'system_update_times': self.system_update_times.copy()
        }
        
        # Add performance manager stats
        if self.performance_manager:
            stats.update(self.performance_manager.get_performance_stats())
        
        # Add terrain system stats
        if self.terrain_manager:
            terrain_stats = self.terrain_manager.get_performance_stats()
            stats['terrain'] = terrain_stats
        
        return stats
    
    def get_max_active_enemies(self) -> int:
        """Get maximum number of active enemies based on performance"""
        return self.performance_manager.get_max_active_enemies()
    
    def should_reduce_effects(self) -> bool:
        """Check if visual effects should be reduced for performance"""
        return self.performance_manager.should_reduce_effects()
    
    def should_reduce_particles(self) -> bool:
        """Check if particle count should be reduced for performance"""
        return self.performance_manager.should_reduce_particles()
    
    def get_enemy_update_frequency(self, distance_to_player: float) -> int:
        """Get update frequency for an enemy based on distance and performance"""
        return self.performance_manager.get_enemy_update_frequency(distance_to_player)
    
    def log_performance_summary(self) -> None:
        """Log a comprehensive performance summary"""
        if not PERFORMANCE_MONITORING_ENABLED:
            return
        
        stats = self.get_performance_stats()
        
        logger.info("=== SYSTEMS PERFORMANCE SUMMARY ===")
        logger.info(f"Frame: {stats['frame_count']}")
        logger.info(f"FPS: {stats.get('fps', 0):.1f} (avg: {stats.get('average_fps', 0):.1f})")
        logger.info(f"Memory: {stats.get('memory_mb', 0):.1f}MB")
        logger.info(f"Performance Level: {stats.get('performance_level', 'unknown')}")
        
        # Enemy stats
        logger.info(f"Enemies - Active: {stats.get('active_enemies', 0)}, "
                   f"Sleeping: {stats.get('sleeping_enemies', 0)}, "
                   f"Culled: {stats.get('culled_enemies', 0)}")
        
        # Terrain stats
        if 'terrain' in stats:
            terrain = stats['terrain']
            logger.info(f"Terrain - Loaded Chunks: {terrain.get('loaded_chunks', 0)}, "
                       f"Loaded This Frame: {terrain.get('chunks_loaded_this_frame', 0)}, "
                       f"Unloaded This Frame: {terrain.get('chunks_unloaded_this_frame', 0)}")
        
        # System update times
        if 'system_update_times' in stats:
            times = stats['system_update_times']
            logger.info("System Update Times (ms):")
            for system, time_ms in times.items():
                logger.info(f"  {system}: {time_ms:.2f}")
        
        logger.info("=====================================")
    
    def shutdown(self) -> None:
        """Shutdown all systems gracefully"""
        logger.info("Shutting down game systems...")
        
        # Log final performance summary
        self.log_performance_summary()
        
        # Clean up systems
        self.initialized = False
        
        logger.info("Game systems shutdown complete")


class SystemsIntegration:
    """Helper class for integrating systems with existing game code"""
    
    @staticmethod
    def create_game_state_dict(level, player, camera_offset_x: float, camera_offset_y: float, 
                              screen_width: int, screen_height: int) -> Dict[str, Any]:
        """Create a game state dictionary for systems manager"""
        game_state = {
            'screen_size': (screen_width, screen_height),
            'camera_position': (camera_offset_x, camera_offset_y)
        }
        
        if player and hasattr(player, 'rect'):
            game_state['player_position'] = (player.rect.centerx, player.rect.centery)
        else:
            game_state['player_position'] = (0, 0)
        
        if level and hasattr(level, 'enemies'):
            game_state['enemies'] = level.enemies
        else:
            game_state['enemies'] = pygame.sprite.Group()
        
        return game_state
    
    @staticmethod
    def apply_enemy_optimizations(enemy, systems_manager: SystemsManager) -> None:
        """Apply optimization settings to an enemy based on systems manager state"""
        if not hasattr(enemy, 'ai_enabled'):
            enemy.ai_enabled = True
        if not hasattr(enemy, 'visible'):
            enemy.visible = True
        if not hasattr(enemy, 'simplified_ai'):
            enemy.simplified_ai = False
        
        # Apply optimizations based on systems manager recommendations
        enemy.simplified_ai = systems_manager.is_enemy_using_simplified_ai(enemy)
    
    @staticmethod
    def should_skip_enemy_update(enemy, systems_manager: SystemsManager) -> bool:
        """Check if an enemy update should be skipped for performance"""
        if not hasattr(enemy, 'ai_enabled') or not enemy.ai_enabled:
            return True
        
        return not systems_manager.should_enemy_update(enemy)
    
    @staticmethod
    def get_optimized_particle_count(base_count: int, systems_manager: SystemsManager) -> int:
        """Get optimized particle count based on performance"""
        if systems_manager.should_reduce_particles():
            return max(1, base_count // 3)
        elif systems_manager.should_reduce_effects():
            return max(1, base_count // 2)
        return base_count
    
    @staticmethod
    def should_skip_visual_effect(systems_manager: SystemsManager) -> bool:
        """Check if visual effects should be skipped for performance"""
        return systems_manager.should_reduce_effects()
