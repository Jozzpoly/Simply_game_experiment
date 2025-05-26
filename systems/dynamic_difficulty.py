"""
Dynamic Difficulty System for Phase 3

This module provides adaptive difficulty that responds to player performance:
- Real-time difficulty assessment and adjustment
- Player skill evaluation across multiple metrics
- Challenge modes and custom modifiers
- Prestige difficulty levels for advanced players
"""

import pygame
import time
import logging
import statistics
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from config import DIFFICULTY_SYSTEM_CONFIG

logger = logging.getLogger(__name__)


@dataclass
class PlayerPerformanceMetrics:
    """Tracks player performance metrics for difficulty assessment"""
    deaths: int = 0
    damage_taken: int = 0
    damage_dealt: int = 0
    enemies_killed: int = 0
    level_completion_times: List[float] = field(default_factory=list)
    accuracy_shots: int = 0
    accuracy_hits: int = 0
    healing_used: int = 0
    items_collected: int = 0
    
    # Time-based tracking
    session_start_time: float = field(default_factory=time.time)
    last_death_time: float = 0
    last_level_start_time: float = field(default_factory=time.time)
    
    def get_death_rate(self, window_seconds: float = 300) -> float:
        """Get deaths per minute in the assessment window"""
        current_time = time.time()
        if current_time - self.session_start_time < window_seconds:
            return 0.0
        return (self.deaths / (window_seconds / 60.0))
    
    def get_accuracy(self) -> float:
        """Get accuracy percentage"""
        if self.accuracy_shots == 0:
            return 1.0
        return self.accuracy_hits / self.accuracy_shots
    
    def get_average_completion_time(self) -> float:
        """Get average level completion time"""
        if not self.level_completion_times:
            return 0.0
        return statistics.mean(self.level_completion_times)
    
    def get_damage_efficiency(self) -> float:
        """Get damage dealt vs damage taken ratio"""
        if self.damage_taken == 0:
            return float('inf')
        return self.damage_dealt / self.damage_taken


@dataclass
class DifficultyModifier:
    """Represents a difficulty modifier"""
    name: str
    description: str
    multipliers: Dict[str, float]
    special_rules: Dict[str, Any]
    enabled: bool = False


class DynamicDifficultyManager:
    """Manages dynamic difficulty adjustment and challenge modes"""
    
    def __init__(self):
        self.config = DIFFICULTY_SYSTEM_CONFIG
        self.adaptive_config = self.config.get('adaptive_difficulty', {})
        
        # Performance tracking
        self.metrics = PlayerPerformanceMetrics()
        self.performance_history: List[Dict[str, float]] = []
        
        # Difficulty state
        self.current_difficulty_multiplier = 1.0
        self.target_difficulty_multiplier = 1.0
        self.last_adjustment_time = time.time()
        
        # Challenge modes
        self.active_modifiers: List[DifficultyModifier] = []
        self.available_modifiers = self._initialize_modifiers()
        
        # Assessment
        self.assessment_window = self.adaptive_config.get('assessment_window', 300)
        self.adjustment_frequency = self.adaptive_config.get('adjustment_frequency', 60)
        self.max_adjustment = self.adaptive_config.get('max_adjustment_per_cycle', 0.1)
        self.difficulty_range = self.adaptive_config.get('difficulty_range', [0.5, 2.0])
        
    def _initialize_modifiers(self) -> Dict[str, DifficultyModifier]:
        """Initialize available difficulty modifiers"""
        modifiers = {}
        
        modifier_configs = self.config.get('challenge_modes', {}).get('custom_modifiers', {})
        
        for name, config in modifier_configs.items():
            modifier = DifficultyModifier(
                name=name,
                description=f"{name.replace('_', ' ').title()} mode",
                multipliers=config,
                special_rules=config
            )
            modifiers[name] = modifier
            
        return modifiers
    
    def update(self, delta_time: float) -> None:
        """Update difficulty system"""
        current_time = time.time()
        
        # Check if it's time for difficulty assessment
        if (self.adaptive_config.get('enabled', True) and 
            current_time - self.last_adjustment_time >= self.adjustment_frequency):
            
            self._assess_and_adjust_difficulty()
            self.last_adjustment_time = current_time
            
        # Gradually adjust current difficulty toward target
        if abs(self.current_difficulty_multiplier - self.target_difficulty_multiplier) > 0.01:
            adjustment_speed = 0.02  # 2% per frame toward target
            if self.current_difficulty_multiplier < self.target_difficulty_multiplier:
                self.current_difficulty_multiplier = min(
                    self.target_difficulty_multiplier,
                    self.current_difficulty_multiplier + adjustment_speed
                )
            else:
                self.current_difficulty_multiplier = max(
                    self.target_difficulty_multiplier,
                    self.current_difficulty_multiplier - adjustment_speed
                )
    
    def _assess_and_adjust_difficulty(self) -> None:
        """Assess player performance and adjust difficulty"""
        # Calculate performance scores
        performance_scores = self._calculate_performance_scores()
        
        # Determine target difficulty based on performance
        target_difficulty = self._calculate_target_difficulty(performance_scores)
        
        # Apply adjustment limits
        max_change = self.max_adjustment
        current_diff = self.target_difficulty_multiplier
        
        if target_difficulty > current_diff:
            self.target_difficulty_multiplier = min(
                target_difficulty,
                current_diff + max_change,
                self.difficulty_range[1]
            )
        else:
            self.target_difficulty_multiplier = max(
                target_difficulty,
                current_diff - max_change,
                self.difficulty_range[0]
            )
        
        # Log adjustment
        if abs(self.target_difficulty_multiplier - current_diff) > 0.01:
            logger.info(f"Difficulty adjusted: {current_diff:.2f} -> {self.target_difficulty_multiplier:.2f}")
            logger.debug(f"Performance scores: {performance_scores}")
        
        # Store performance history
        self.performance_history.append({
            'timestamp': time.time(),
            'difficulty': self.current_difficulty_multiplier,
            'performance_scores': performance_scores.copy()
        })
        
        # Limit history size
        if len(self.performance_history) > 100:
            self.performance_history = self.performance_history[-50:]
    
    def _calculate_performance_scores(self) -> Dict[str, float]:
        """Calculate normalized performance scores (0.0 = struggling, 1.0 = excelling)"""
        scores = {}
        
        # Death rate score (lower is better)
        death_rate = self.metrics.get_death_rate(self.assessment_window)
        scores['death_rate'] = max(0.0, 1.0 - (death_rate / 2.0))  # 2+ deaths/min = 0 score
        
        # Accuracy score
        accuracy = self.metrics.get_accuracy()
        scores['accuracy'] = accuracy
        
        # Completion time score (faster is better, but not too fast)
        avg_completion = self.metrics.get_average_completion_time()
        if avg_completion > 0:
            # Target completion time: 2-5 minutes per level
            target_time = 180  # 3 minutes
            if avg_completion < target_time * 0.5:
                scores['completion_time'] = 0.8  # Too fast, increase difficulty
            elif avg_completion > target_time * 2:
                scores['completion_time'] = 0.2  # Too slow, decrease difficulty
            else:
                # Optimal range
                scores['completion_time'] = 0.6
        else:
            scores['completion_time'] = 0.5  # No data
        
        # Damage efficiency score
        damage_efficiency = self.metrics.get_damage_efficiency()
        if damage_efficiency == float('inf'):
            scores['damage_efficiency'] = 1.0  # Perfect (no damage taken)
        else:
            # Good efficiency is 3:1 damage dealt to taken ratio
            scores['damage_efficiency'] = min(1.0, damage_efficiency / 3.0)
        
        return scores
    
    def _calculate_target_difficulty(self, performance_scores: Dict[str, float]) -> float:
        """Calculate target difficulty based on performance scores"""
        # Weight different factors
        factor_weights = {
            'death_rate': 0.4,
            'completion_time': 0.3,
            'damage_efficiency': 0.2,
            'accuracy': 0.1
        }
        
        # Calculate weighted average performance
        weighted_performance = 0.0
        total_weight = 0.0
        
        for factor, weight in factor_weights.items():
            if factor in performance_scores:
                weighted_performance += performance_scores[factor] * weight
                total_weight += weight
        
        if total_weight > 0:
            weighted_performance /= total_weight
        else:
            weighted_performance = 0.5  # Default to neutral
        
        # Convert performance to difficulty target
        # Performance 0.0-0.4: Decrease difficulty
        # Performance 0.4-0.6: Maintain difficulty
        # Performance 0.6-1.0: Increase difficulty
        
        if weighted_performance < 0.4:
            # Player struggling, decrease difficulty
            target_multiplier = 0.7 + (weighted_performance / 0.4) * 0.3
        elif weighted_performance > 0.6:
            # Player excelling, increase difficulty
            excess_performance = weighted_performance - 0.6
            target_multiplier = 1.0 + (excess_performance / 0.4) * 0.5
        else:
            # Player in optimal range, maintain current difficulty
            target_multiplier = self.target_difficulty_multiplier
        
        return target_multiplier
    
    def record_player_death(self) -> None:
        """Record a player death"""
        self.metrics.deaths += 1
        self.metrics.last_death_time = time.time()
        
    def record_damage_taken(self, damage: int) -> None:
        """Record damage taken by player"""
        self.metrics.damage_taken += damage
        
    def record_damage_dealt(self, damage: int) -> None:
        """Record damage dealt by player"""
        self.metrics.damage_dealt += damage
        
    def record_enemy_killed(self) -> None:
        """Record enemy killed by player"""
        self.metrics.enemies_killed += 1
        
    def record_shot_fired(self, hit: bool = False) -> None:
        """Record a shot fired and whether it hit"""
        self.metrics.accuracy_shots += 1
        if hit:
            self.metrics.accuracy_hits += 1
            
    def record_level_completed(self, completion_time: float) -> None:
        """Record level completion"""
        self.metrics.level_completion_times.append(completion_time)
        
        # Limit history size
        if len(self.metrics.level_completion_times) > 20:
            self.metrics.level_completion_times = self.metrics.level_completion_times[-10:]
    
    def start_new_level(self) -> None:
        """Called when starting a new level"""
        self.metrics.last_level_start_time = time.time()
    
    def get_difficulty_multipliers(self) -> Dict[str, float]:
        """Get current difficulty multipliers for game systems"""
        base_multipliers = {
            'enemy_health': self.current_difficulty_multiplier,
            'enemy_damage': self.current_difficulty_multiplier * 0.8,  # Less aggressive damage scaling
            'enemy_speed': 1.0 + (self.current_difficulty_multiplier - 1.0) * 0.5,  # Moderate speed scaling
            'enemy_count': 1.0 + (self.current_difficulty_multiplier - 1.0) * 0.3,  # Conservative count scaling
            'item_rarity': 1.0 / self.current_difficulty_multiplier,  # Better items when harder
            'xp_gain': self.current_difficulty_multiplier  # More XP for harder difficulty
        }
        
        # Apply active modifiers
        for modifier in self.active_modifiers:
            if modifier.enabled:
                for stat, multiplier in modifier.multipliers.items():
                    if stat in base_multipliers:
                        base_multipliers[stat] *= multiplier
                    else:
                        base_multipliers[stat] = multiplier
        
        return base_multipliers
    
    def activate_modifier(self, modifier_name: str) -> bool:
        """Activate a difficulty modifier"""
        if modifier_name in self.available_modifiers:
            modifier = self.available_modifiers[modifier_name]
            modifier.enabled = True
            
            if modifier not in self.active_modifiers:
                self.active_modifiers.append(modifier)
            
            logger.info(f"Activated difficulty modifier: {modifier_name}")
            return True
        return False
    
    def deactivate_modifier(self, modifier_name: str) -> bool:
        """Deactivate a difficulty modifier"""
        if modifier_name in self.available_modifiers:
            modifier = self.available_modifiers[modifier_name]
            modifier.enabled = False
            
            if modifier in self.active_modifiers:
                self.active_modifiers.remove(modifier)
            
            logger.info(f"Deactivated difficulty modifier: {modifier_name}")
            return True
        return False
    
    def get_active_modifiers(self) -> List[str]:
        """Get list of active modifier names"""
        return [mod.name for mod in self.active_modifiers if mod.enabled]
    
    def get_difficulty_description(self) -> str:
        """Get human-readable difficulty description"""
        difficulty = self.current_difficulty_multiplier
        
        if difficulty < 0.7:
            return "Very Easy"
        elif difficulty < 0.9:
            return "Easy"
        elif difficulty < 1.1:
            return "Normal"
        elif difficulty < 1.3:
            return "Hard"
        elif difficulty < 1.6:
            return "Very Hard"
        else:
            return "Extreme"
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of player performance"""
        return {
            'difficulty_multiplier': self.current_difficulty_multiplier,
            'difficulty_description': self.get_difficulty_description(),
            'deaths': self.metrics.deaths,
            'enemies_killed': self.metrics.enemies_killed,
            'accuracy': self.metrics.get_accuracy() * 100,
            'average_completion_time': self.metrics.get_average_completion_time(),
            'damage_efficiency': self.metrics.get_damage_efficiency(),
            'active_modifiers': self.get_active_modifiers(),
            'session_duration': time.time() - self.metrics.session_start_time
        }
    
    def reset_session(self) -> None:
        """Reset session metrics"""
        self.metrics = PlayerPerformanceMetrics()
        self.performance_history.clear()
        self.current_difficulty_multiplier = 1.0
        self.target_difficulty_multiplier = 1.0
        logger.info("Dynamic difficulty session reset")
