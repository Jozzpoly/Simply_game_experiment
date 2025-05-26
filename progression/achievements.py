"""
Achievement system for tracking player progress and milestones.

This module implements achievements that reward players for various
accomplishments and provide additional progression goals.
"""

import pygame
from typing import Dict, List, Optional, Any, Callable, Tuple
from utils.constants import *


class Achievement:
    """Represents a single achievement"""

    def __init__(self, name: str, description: str, reward_xp: int = 0,
                 reward_skill_points: int = 0, condition: Optional[Callable] = None,
                 hidden: bool = False):
        self.name = name
        self.description = description
        self.reward_xp = reward_xp
        self.reward_skill_points = reward_skill_points
        self.condition = condition
        self.hidden = hidden
        self.unlocked = False
        self.progress = 0
        self.max_progress = 1

    def check_condition(self, player_stats: Dict[str, Any]) -> bool:
        """Check if the achievement condition is met"""
        if self.condition:
            return self.condition(player_stats)
        return False

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
            "progress": self.progress
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load achievement from dictionary"""
        self.unlocked = data.get("unlocked", False)
        self.progress = data.get("progress", 0)


class AchievementManager:
    """Manages all achievements and tracks progress"""

    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.recently_unlocked: List[Achievement] = []
        self._initialize_achievements()

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
        self.achievements["secret_path"] = Achievement(
            "Secret Path",
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

    def check_achievements(self, player_stats: Dict[str, Any]) -> List[Achievement]:
        """Check all achievements and return newly unlocked ones"""
        newly_unlocked = []

        for achievement in self.achievements.values():
            if not achievement.unlocked and achievement.check_condition(player_stats):
                newly_unlocked.append(achievement)
                achievement.unlock()

        self.recently_unlocked.extend(newly_unlocked)
        return newly_unlocked

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
            }
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load achievement manager from dictionary"""
        achievements_data = data.get("achievements", {})
        for name, ach_data in achievements_data.items():
            if name in self.achievements:
                self.achievements[name].from_dict(ach_data)
