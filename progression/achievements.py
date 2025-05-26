"""
Achievement system for tracking player progress and milestones.

This module implements achievements that reward players for various
accomplishments and provide additional progression goals.
"""

import pygame
from typing import Dict, List, Optional, Any, Callable, Tuple
from utils.constants import *


class Achievement:
    """Represents a single achievement with support for progressive and chain types"""

    def __init__(self, name: str, description: str, reward_xp: int = 0,
                 reward_skill_points: int = 0, condition: Optional[Callable] = None,
                 hidden: bool = False, achievement_type: str = "simple",
                 max_progress: int = 1, prerequisites: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.reward_xp = reward_xp
        self.reward_skill_points = reward_skill_points
        self.condition = condition
        self.hidden = hidden
        self.achievement_type = achievement_type
        self.unlocked = False
        self.progress = 0
        self.max_progress = max_progress
        self.prerequisites = prerequisites or []

    def check_condition(self, player_stats: Dict[str, Any]) -> bool:
        """Check if the achievement condition is met"""
        if self.condition:
            if self.achievement_type == "progressive":
                # For progressive achievements, update progress
                new_progress = self.condition(player_stats)
                if isinstance(new_progress, (int, float)):
                    self.progress = min(new_progress, self.max_progress)
                    return self.progress >= self.max_progress
                else:
                    return new_progress
            else:
                return self.condition(player_stats)
        return False

    def update_progress(self, amount: int = 1) -> bool:
        """Update progress for progressive achievements"""
        if self.achievement_type == "progressive" and not self.unlocked:
            self.progress = min(self.progress + amount, self.max_progress)
            return self.progress >= self.max_progress
        return False

    def get_progress_percentage(self) -> float:
        """Get progress as a percentage"""
        if self.max_progress <= 0:
            return 100.0 if self.unlocked else 0.0
        return min(100.0, (self.progress / self.max_progress) * 100.0)

    def is_available(self, unlocked_achievements: List[str]) -> bool:
        """Check if achievement is available based on prerequisites"""
        if not self.prerequisites:
            return True
        return all(prereq in unlocked_achievements for prereq in self.prerequisites)

    def unlock(self) -> Dict[str, int]:
        """Unlock the achievement and return rewards"""
        if not self.unlocked:
            self.unlocked = True
            return {
                "xp": self.reward_xp,
                "skill_points": self.reward_skill_points
            }
        return {"xp": 0, "skill_points": 0}

    def to_dict(self) -> Dict[str, Any]:
        """Convert achievement to dictionary for saving"""
        return {
            "name": self.name,
            "unlocked": self.unlocked,
            "progress": self.progress,
            "achievement_type": self.achievement_type,
            "max_progress": self.max_progress
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load achievement from dictionary"""
        self.unlocked = data.get("unlocked", False)
        self.progress = data.get("progress", 0)
        # achievement_type and max_progress are set during initialization


class AchievementManager:
    """Manages all achievements and tracks progress"""

    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.recently_unlocked: List[Achievement] = []
        self.achievement_chains: Dict[str, Dict[str, Any]] = {}
        self.completed_chains: List[str] = []
        self._initialize_achievements()
        self._initialize_achievement_chains()

    def _initialize_achievements(self) -> None:
        """Initialize all available achievements"""

        # Level-based achievements
        self.achievements["first_steps"] = Achievement(
            "First Steps",
            "Reach level 2",
            reward_xp=25,
            reward_skill_points=1,
            condition=lambda stats: stats.get("player_level", 1) >= 2
        )

        self.achievements["experienced"] = Achievement(
            "Experienced",
            "Reach level 5",
            reward_xp=50,
            reward_skill_points=1,
            condition=lambda stats: stats.get("player_level", 1) >= 5
        )

        self.achievements["veteran"] = Achievement(
            "Veteran",
            "Reach level 10",
            reward_xp=100,
            reward_skill_points=2,
            condition=lambda stats: stats.get("player_level", 1) >= 10
        )

        self.achievements["master"] = Achievement(
            "Master",
            "Reach level 20",
            reward_xp=200,
            reward_skill_points=3,
            condition=lambda stats: stats.get("player_level", 1) >= 20
        )

        # Combat achievements
        self.achievements["first_blood"] = Achievement(
            "First Blood",
            "Defeat your first enemy",
            reward_xp=10,
            condition=lambda stats: stats.get("enemies_killed", 0) >= 1
        )

        self.achievements["slayer"] = Achievement(
            "Slayer",
            "Defeat 50 enemies",
            reward_xp=75,
            reward_skill_points=1,
            condition=lambda stats: stats.get("enemies_killed", 0) >= 50
        )

        self.achievements["destroyer"] = Achievement(
            "Destroyer",
            "Defeat 200 enemies",
            reward_xp=150,
            reward_skill_points=2,
            condition=lambda stats: stats.get("enemies_killed", 0) >= 200
        )

        self.achievements["boss_hunter"] = Achievement(
            "Boss Hunter",
            "Defeat your first boss",
            reward_xp=100,
            reward_skill_points=1,
            condition=lambda stats: stats.get("bosses_killed", 0) >= 1
        )

        self.achievements["boss_slayer"] = Achievement(
            "Boss Slayer",
            "Defeat 10 bosses",
            reward_xp=250,
            reward_skill_points=2,
            condition=lambda stats: stats.get("bosses_killed", 0) >= 10
        )

        # Survival achievements
        self.achievements["survivor"] = Achievement(
            "Survivor",
            "Complete 5 levels without dying",
            reward_xp=100,
            reward_skill_points=1,
            condition=lambda stats: stats.get("levels_completed", 0) >= 5
        )

        self.achievements["untouchable"] = Achievement(
            "Untouchable",
            "Complete a level without taking damage",
            reward_xp=75,
            reward_skill_points=1,
            condition=lambda stats: stats.get("perfect_levels", 0) >= 1
        )

        self.achievements["iron_will"] = Achievement(
            "Iron Will",
            "Survive with 1 HP",
            reward_xp=50,
            condition=lambda stats: stats.get("near_death_survivals", 0) >= 1
        )

        # Progression achievements
        self.achievements["skill_student"] = Achievement(
            "Skill Student",
            "Learn your first skill",
            reward_xp=25,
            condition=lambda stats: stats.get("skills_learned", 0) >= 1
        )

        self.achievements["skill_master"] = Achievement(
            "Skill Master",
            "Max out a skill",
            reward_xp=100,
            reward_skill_points=1,
            condition=lambda stats: stats.get("maxed_skills", 0) >= 1
        )

        self.achievements["well_equipped"] = Achievement(
            "Well Equipped",
            "Equip your first piece of equipment",
            reward_xp=25,
            condition=lambda stats: stats.get("equipment_equipped", 0) >= 1
        )

        self.achievements["fully_equipped"] = Achievement(
            "Fully Equipped",
            "Have equipment in all slots",
            reward_xp=75,
            reward_skill_points=1,
            condition=lambda stats: stats.get("full_equipment_sets", 0) >= 1
        )

        # Collection achievements
        self.achievements["collector"] = Achievement(
            "Collector",
            "Collect 100 items",
            reward_xp=50,
            condition=lambda stats: stats.get("items_collected", 0) >= 100
        )

        self.achievements["hoarder"] = Achievement(
            "Hoarder",
            "Collect 500 items",
            reward_xp=150,
            reward_skill_points=1,
            condition=lambda stats: stats.get("items_collected", 0) >= 500
        )

        # Special achievements
        self.achievements["speed_runner"] = Achievement(
            "Speed Runner",
            "Complete a level in under 2 minutes",
            reward_xp=100,
            reward_skill_points=1,
            condition=lambda stats: stats.get("fastest_level_time", float('inf')) < 120
        )

        self.achievements["perfectionist"] = Achievement(
            "Perfectionist",
            "Complete 10 perfect levels (no damage taken)",
            reward_xp=200,
            reward_skill_points=2,
            condition=lambda stats: stats.get("perfect_levels", 0) >= 10
        )

        # Hidden achievements
        self.achievements["secret_finder"] = Achievement(
            "Secret Finder",
            "Discover a hidden area",
            reward_xp=50,
            reward_skill_points=1,
            condition=lambda stats: stats.get("secrets_found", 0) >= 1,
            hidden=True
        )

        self.achievements["lucky_shot"] = Achievement(
            "Lucky Shot",
            "Get 10 critical hits in a row",
            reward_xp=75,
            condition=lambda stats: stats.get("max_crit_streak", 0) >= 10,
            hidden=True
        )

        # Progressive achievements
        self.achievements["enemy_slayer"] = Achievement(
            "Enemy Slayer",
            "Defeat 100 enemies",
            reward_xp=150,
            reward_skill_points=2,
            condition=lambda stats: stats.get("enemies_killed", 0),
            achievement_type="progressive",
            max_progress=100
        )

        self.achievements["damage_dealer"] = Achievement(
            "Damage Dealer",
            "Deal 10,000 total damage",
            reward_xp=200,
            reward_skill_points=2,
            condition=lambda stats: stats.get("total_damage_dealt", 0),
            achievement_type="progressive",
            max_progress=10000
        )

        self.achievements["treasure_hunter"] = Achievement(
            "Treasure Hunter",
            "Collect 50 items",
            reward_xp=100,
            reward_skill_points=1,
            condition=lambda stats: stats.get("items_collected", 0),
            achievement_type="progressive",
            max_progress=50
        )

        # Chain achievements
        self.achievements["combat_master"] = Achievement(
            "Combat Master",
            "Master all combat skills",
            reward_xp=300,
            reward_skill_points=3,
            condition=lambda stats: stats.get("maxed_combat_skills", 0) >= 5,
            achievement_type="chain",
            prerequisites=["boss_hunter", "enemy_slayer"]
        )

        self.achievements["immortal"] = Achievement(
            "Immortal",
            "Complete 20 perfect levels",
            reward_xp=400,
            reward_skill_points=4,
            condition=lambda stats: stats.get("perfect_levels", 0) >= 20,
            achievement_type="chain",
            prerequisites=["perfectionist", "damage_dealer"]
        )

        self.achievements["master_explorer"] = Achievement(
            "Master Explorer",
            "Find all secrets and collect all treasures",
            reward_xp=250,
            reward_skill_points=3,
            condition=lambda stats: (stats.get("secrets_found", 0) >= 10 and
                                   stats.get("items_collected", 0) >= 100),
            achievement_type="chain",
            prerequisites=["treasure_hunter", "secret_finder"]
        )

    def _initialize_achievement_chains(self) -> None:
        """Initialize achievement chains from constants"""
        self.achievement_chains = ACHIEVEMENT_CHAINS.copy()

    def check_achievements(self, player_stats: Dict[str, Any]) -> List[Achievement]:
        """Check all achievements and return newly unlocked ones"""
        newly_unlocked = []
        unlocked_names = [name for name, ach in self.achievements.items() if ach.unlocked]

        for achievement in self.achievements.values():
            if not achievement.unlocked:
                # Check if prerequisites are met for chain achievements
                if achievement.achievement_type == "chain":
                    if not achievement.is_available(unlocked_names):
                        continue

                # Check achievement condition
                if achievement.check_condition(player_stats):
                    newly_unlocked.append(achievement)
                    achievement.unlock()

        # Check for completed chains
        self._check_achievement_chains(newly_unlocked)

        self.recently_unlocked.extend(newly_unlocked)
        return newly_unlocked

    def _check_achievement_chains(self, newly_unlocked: List[Achievement]) -> None:
        """Check if any achievement chains have been completed"""
        for chain_name, chain_data in self.achievement_chains.items():
            if chain_name not in self.completed_chains:
                required_achievements = chain_data["achievements"]
                if all(self.achievements.get(ach_name, Achievement("", "")).unlocked
                       for ach_name in required_achievements):
                    # Chain completed! Award chain rewards
                    self.completed_chains.append(chain_name)
                    # Could add chain completion notification here

    def get_unlocked_achievements(self) -> List[Achievement]:
        """Get all unlocked achievements"""
        return [ach for ach in self.achievements.values() if ach.unlocked]

    def get_locked_achievements(self, include_hidden: bool = False) -> List[Achievement]:
        """Get all locked achievements"""
        locked = [ach for ach in self.achievements.values() if not ach.unlocked]
        if not include_hidden:
            locked = [ach for ach in locked if not ach.hidden]
        return locked

    def get_achievement_progress(self) -> Tuple[int, int]:
        """Get achievement progress (unlocked, total)"""
        unlocked = len(self.get_unlocked_achievements())
        total = len([ach for ach in self.achievements.values() if not ach.hidden])
        return unlocked, total

    def clear_recent_notifications(self) -> None:
        """Clear the list of recently unlocked achievements"""
        self.recently_unlocked.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Convert achievement manager to dictionary for saving"""
        return {
            "achievements": {
                name: achievement.to_dict()
                for name, achievement in self.achievements.items()
            },
            "completed_chains": self.completed_chains.copy()
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load achievement manager from dictionary"""
        achievements_data = data.get("achievements", {})
        for name, ach_data in achievements_data.items():
            if name in self.achievements:
                self.achievements[name].from_dict(ach_data)

        # Load completed chains
        self.completed_chains = data.get("completed_chains", [])
