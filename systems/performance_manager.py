"""
Performance Management System for optimizing game performance with large numbers of entities.
Handles enemy AI optimization, level-of-detail systems, and adaptive performance adjustments.
"""

import pygame
import time
import logging
from typing import List, Dict, Any, Optional, Tuple
from config import *

# Try to import psutil for memory monitoring, fallback if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

logger = logging.getLogger(__name__)

class PerformanceManager:
    """Manages game performance optimization and monitoring"""

    def __init__(self):
        self.enabled = PERFORMANCE_MONITORING_ENABLED
        self.fps_samples: List[float] = []
        self.frame_count = 0
        self.last_log_time = 0
        self.current_fps = 60.0
        self.average_fps = 60.0

        # Performance state
        self.performance_level = "high"  # high, medium, low
        self.last_adjustment_time = 0
        self.adjustment_cooldown = 5000  # ms between adjustments

        # Memory monitoring
        self.process = None
        if MEMORY_MONITORING_ENABLED and PSUTIL_AVAILABLE:
            try:
                self.process = psutil.Process()
            except:
                self.process = None
        self.memory_usage = 0

        # Enemy optimization state
        self.active_enemies_count = 0
        self.sleeping_enemies_count = 0
        self.culled_enemies_count = 0

    def update(self, dt: float) -> None:
        """Update performance monitoring and optimization"""
        if not self.enabled:
            return

        self.frame_count += 1
        current_time = pygame.time.get_ticks()

        # Calculate FPS
        if dt > 0:
            current_fps = 1.0 / dt
            self.fps_samples.append(current_fps)

            # Keep only recent samples
            if len(self.fps_samples) > 60:  # Keep 1 second of samples at 60 FPS
                self.fps_samples.pop(0)

            self.current_fps = current_fps
            self.average_fps = sum(self.fps_samples) / len(self.fps_samples)

        # Update memory usage
        if self.process and self.frame_count % 60 == 0:  # Check every second
            try:
                self.memory_usage = self.process.memory_info().rss / 1024 / 1024  # MB
            except:
                self.memory_usage = 0

        # Log performance periodically
        if current_time - self.last_log_time > PERFORMANCE_LOG_INTERVAL * (1000 / 60):  # Convert frames to ms
            self._log_performance()
            self.last_log_time = current_time

        # Check for performance adjustments
        if (ADAPTIVE_PERFORMANCE_ENABLED and
            current_time - self.last_adjustment_time > self.adjustment_cooldown):
            self._check_performance_adjustments()
            self.last_adjustment_time = current_time

    def _log_performance(self) -> None:
        """Log current performance metrics"""
        logger.info(f"Performance - FPS: {self.average_fps:.1f}, "
                   f"Memory: {self.memory_usage:.1f}MB, "
                   f"Active Enemies: {self.active_enemies_count}, "
                   f"Sleeping: {self.sleeping_enemies_count}, "
                   f"Culled: {self.culled_enemies_count}")

        # Warn about low performance
        if self.average_fps < FPS_WARNING_THRESHOLD:
            logger.warning(f"Low FPS detected: {self.average_fps:.1f}")

        if self.memory_usage > MEMORY_WARNING_THRESHOLD:
            logger.warning(f"High memory usage: {self.memory_usage:.1f}MB")

    def _check_performance_adjustments(self) -> None:
        """Check if performance adjustments are needed"""
        if self.average_fps < PERFORMANCE_ADJUSTMENT_THRESHOLD:
            if self.performance_level == "high":
                self.performance_level = "medium"
                logger.info("Reducing performance level to medium")
            elif self.performance_level == "medium":
                self.performance_level = "low"
                logger.info("Reducing performance level to low")
        elif self.average_fps > FPS_TARGET * 0.9:  # 90% of target
            if self.performance_level == "low":
                self.performance_level = "medium"
                logger.info("Increasing performance level to medium")
            elif self.performance_level == "medium":
                self.performance_level = "high"
                logger.info("Increasing performance level to high")

    def get_enemy_update_frequency(self, distance_to_player: float) -> int:
        """Get the update frequency for an enemy based on distance and performance"""
        if not ENEMY_AI_OPTIMIZATION_ENABLED:
            return 1

        base_frequency = ENEMY_AI_UPDATE_FREQUENCY_CLOSE

        if distance_to_player > ENEMY_AI_UPDATE_DISTANCE:
            base_frequency = ENEMY_AI_UPDATE_FREQUENCY_DISTANT

        # Adjust based on performance level
        if self.performance_level == "low":
            base_frequency *= 2
        elif self.performance_level == "medium":
            base_frequency = max(1, int(base_frequency * 1.5))

        return base_frequency

    def should_enemy_sleep(self, distance_to_player: float) -> bool:
        """Determine if an enemy should sleep based on distance and performance"""
        if not ENEMY_AI_OPTIMIZATION_ENABLED:
            return False

        sleep_distance = ENEMY_AI_SLEEP_DISTANCE

        # Adjust sleep distance based on performance
        if self.performance_level == "low":
            sleep_distance *= 0.7
        elif self.performance_level == "medium":
            sleep_distance *= 0.85

        return distance_to_player > sleep_distance

    def should_enemy_be_culled(self, distance_to_player: float) -> bool:
        """Determine if an enemy should be completely culled"""
        if not ENEMY_CULLING_ENABLED:
            return False

        cull_distance = ENEMY_CULLING_DISTANCE

        # Adjust cull distance based on performance
        if self.performance_level == "low":
            cull_distance *= 0.6
        elif self.performance_level == "medium":
            cull_distance *= 0.8

        return distance_to_player > cull_distance

    def update_enemy_counts(self, active: int, sleeping: int, culled: int) -> None:
        """Update enemy count statistics"""
        self.active_enemies_count = active
        self.sleeping_enemies_count = sleeping
        self.culled_enemies_count = culled

    def get_max_active_enemies(self) -> int:
        """Get the maximum number of active enemies based on performance"""
        base_max = MAX_ACTIVE_ENEMIES

        if self.performance_level == "low":
            return int(base_max * 0.6)
        elif self.performance_level == "medium":
            return int(base_max * 0.8)

        return base_max

    def should_reduce_effects(self) -> bool:
        """Check if visual effects should be reduced"""
        return (AUTO_REDUCE_EFFECTS_ON_LAG and
                self.performance_level in ["low", "medium"])

    def should_reduce_particles(self) -> bool:
        """Check if particle count should be reduced"""
        return (AUTO_REDUCE_PARTICLES_ON_LAG and
                self.performance_level == "low")

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        return {
            "fps": self.current_fps,
            "average_fps": self.average_fps,
            "memory_mb": self.memory_usage,
            "performance_level": self.performance_level,
            "active_enemies": self.active_enemies_count,
            "sleeping_enemies": self.sleeping_enemies_count,
            "culled_enemies": self.culled_enemies_count
        }


class EnemyOptimizationManager:
    """Manages enemy AI optimization and level-of-detail systems"""

    def __init__(self, performance_manager: PerformanceManager):
        self.performance_manager = performance_manager
        self.enemy_states: Dict[int, Dict[str, Any]] = {}
        self.frame_count = 0

    def update_enemy_optimization(self, enemies: pygame.sprite.Group, player_pos: Tuple[float, float]) -> None:
        """Update optimization state for all enemies"""
        if not ENEMY_AI_OPTIMIZATION_ENABLED:
            return

        self.frame_count += 1
        active_count = 0
        sleeping_count = 0
        culled_count = 0

        max_active = self.performance_manager.get_max_active_enemies()
        active_enemies = []

        # Calculate distances and sort by priority
        enemy_distances = []
        for enemy in enemies:
            if hasattr(enemy, 'rect'):
                enemy_pos = (enemy.rect.centerx, enemy.rect.centery)
                distance = ((player_pos[0] - enemy_pos[0]) ** 2 +
                           (player_pos[1] - enemy_pos[1]) ** 2) ** 0.5
                enemy_distances.append((enemy, distance))

        # Sort by distance (closest first)
        enemy_distances.sort(key=lambda x: x[1])

        # Apply optimization based on distance and performance
        for enemy, distance in enemy_distances:
            enemy_id = id(enemy)

            # Initialize enemy state if needed
            if enemy_id not in self.enemy_states:
                self.enemy_states[enemy_id] = {
                    "last_update_frame": 0,
                    "state": "active",
                    "simplified_ai": False
                }

            enemy_state = self.enemy_states[enemy_id]

            # Determine enemy optimization state
            if self.performance_manager.should_enemy_be_culled(distance):
                enemy_state["state"] = "culled"
                enemy.ai_enabled = False
                enemy.visible = False
                culled_count += 1
            elif self.performance_manager.should_enemy_sleep(distance):
                enemy_state["state"] = "sleeping"
                enemy.ai_enabled = False
                enemy.visible = True
                sleeping_count += 1
            elif active_count < max_active:
                enemy_state["state"] = "active"
                enemy.ai_enabled = True
                enemy.visible = True
                active_count += 1
                active_enemies.append(enemy)

                # Determine if enemy should use simplified AI
                update_freq = self.performance_manager.get_enemy_update_frequency(distance)
                enemy_state["simplified_ai"] = update_freq > 1

                # Check if enemy should update this frame
                if self.frame_count - enemy_state["last_update_frame"] >= update_freq:
                    enemy_state["should_update"] = True
                    enemy_state["last_update_frame"] = self.frame_count
                else:
                    enemy_state["should_update"] = False
            else:
                # Too many active enemies, put this one to sleep
                enemy_state["state"] = "sleeping"
                enemy.ai_enabled = False
                enemy.visible = True
                sleeping_count += 1

        # Update performance manager with counts
        self.performance_manager.update_enemy_counts(active_count, sleeping_count, culled_count)

    def should_enemy_update(self, enemy) -> bool:
        """Check if an enemy should update this frame"""
        enemy_id = id(enemy)
        if enemy_id not in self.enemy_states:
            return True

        return self.enemy_states[enemy_id].get("should_update", True)

    def is_enemy_using_simplified_ai(self, enemy) -> bool:
        """Check if an enemy should use simplified AI"""
        enemy_id = id(enemy)
        if enemy_id not in self.enemy_states:
            return False

        return self.enemy_states[enemy_id].get("simplified_ai", False)

    def cleanup_dead_enemies(self, alive_enemies: pygame.sprite.Group) -> None:
        """Clean up optimization state for dead enemies"""
        alive_ids = {id(enemy) for enemy in alive_enemies}
        dead_ids = set(self.enemy_states.keys()) - alive_ids

        for dead_id in dead_ids:
            del self.enemy_states[dead_id]
