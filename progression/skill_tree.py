"""
Skill tree system for character progression.

This module implements a comprehensive skill tree system with branching paths
and specializations for combat, survival, and utility skills.
"""

import pygame
from typing import Dict, List, Optional, Any, Tuple
from utils.constants import *


class Skill:
    """Represents a single skill in the skill tree"""

    def __init__(self, name: str, category: str, max_level: int,
                 description: str, prerequisites: Optional[List[str]] = None,
                 stats: Optional[Dict[str, Any]] = None):
        self.name = name
        self.category = category
        self.max_level = max_level
        self.current_level = 0
        self.description = description
        self.prerequisites = prerequisites or []
        self.stats = stats or {}
        self.unlocked = len(self.prerequisites) == 0  # Unlock if no prerequisites

    def can_upgrade(self, skill_points: int, learned_skills: Dict[str, int]) -> bool:
        """Check if this skill can be upgraded"""
        if self.current_level >= self.max_level:
            return False
        if skill_points < 1:
            return False

        # Check prerequisites
        for prereq in self.prerequisites:
            if prereq not in learned_skills or learned_skills[prereq] < 1:
                return False

        return True

    def upgrade(self) -> bool:
        """Upgrade the skill by one level"""
        if self.current_level < self.max_level:
            self.current_level += 1
            return True
        return False

    def get_current_bonus(self, stat_name: str) -> float:
        """Get the current bonus for a specific stat"""
        if stat_name not in self.stats:
            return 0.0

        base_value = self.stats[stat_name]
        if isinstance(base_value, dict):
            # Handle complex stat structures
            if "per_level" in base_value:
                return base_value["per_level"] * self.current_level
            elif "base_value" in base_value:
                return base_value["base_value"] + (base_value.get("per_level", 0) * self.current_level)
        else:
            # Simple per-level bonus
            return base_value * self.current_level

    def get_description_with_level(self) -> str:
        """Get description with current level information"""
        if self.current_level == 0:
            return f"{self.description} (Not learned)"
        elif self.current_level >= self.max_level:
            return f"{self.description} (MAX: {self.current_level}/{self.max_level})"
        else:
            return f"{self.description} (Level {self.current_level}/{self.max_level})"


class SkillTree:
    """Manages the player's skill tree progression"""

    def __init__(self):
        self.skill_points = 0
        self.skills: Dict[str, Skill] = {}
        self.learned_skills: Dict[str, int] = {}
        self._initialize_skills()
        # Update skill availability after initialization
        self._update_skill_availability()

    def _initialize_skills(self) -> None:
        """Initialize all available skills"""
        # Combat Skills
        self.skills["critical_strike"] = Skill(
            "Critical Strike",
            "combat",
            COMBAT_SKILLS["critical_strike"]["max_level"],
            "Increases critical hit chance",
            stats={"critical_chance": COMBAT_SKILLS["critical_strike"]["chance_per_level"]}
        )

        self.skills["multi_shot"] = Skill(
            "Multi Shot",
            "combat",
            COMBAT_SKILLS["multi_shot"]["max_level"],
            "Fire additional projectiles",
            prerequisites=["critical_strike"],
            stats={"extra_projectiles": COMBAT_SKILLS["multi_shot"]["projectiles_per_level"]}
        )

        self.skills["piercing_shots"] = Skill(
            "Piercing Shots",
            "combat",
            COMBAT_SKILLS["piercing_shots"]["max_level"],
            "Projectiles pierce through enemies",
            prerequisites=["critical_strike"],
            stats={"pierce_count": COMBAT_SKILLS["piercing_shots"]["pierce_count_per_level"]}
        )

        self.skills["explosive_shots"] = Skill(
            "Explosive Shots",
            "combat",
            COMBAT_SKILLS["explosive_shots"]["max_level"],
            "Projectiles explode on impact",
            prerequisites=["multi_shot", "piercing_shots"],
            stats={"explosion_radius": COMBAT_SKILLS["explosive_shots"]["explosion_radius_per_level"]}
        )

        self.skills["weapon_mastery"] = Skill(
            "Weapon Mastery",
            "combat",
            COMBAT_SKILLS["weapon_mastery"]["max_level"],
            "Increases weapon damage",
            stats={"damage_bonus": COMBAT_SKILLS["weapon_mastery"]["damage_bonus_per_level"]}
        )

        # Survival Skills
        self.skills["armor_mastery"] = Skill(
            "Armor Mastery",
            "survival",
            SURVIVAL_SKILLS["armor_mastery"]["max_level"],
            "Reduces incoming damage",
            stats={"damage_reduction": SURVIVAL_SKILLS["armor_mastery"]["damage_reduction_per_level"]}
        )

        self.skills["health_regeneration"] = Skill(
            "Health Regeneration",
            "survival",
            SURVIVAL_SKILLS["health_regeneration"]["max_level"],
            "Slowly regenerates health over time",
            stats={
                "regen_amount": SURVIVAL_SKILLS["health_regeneration"]["regen_per_level"],
                "regen_interval": SURVIVAL_SKILLS["health_regeneration"]["regen_interval"]
            }
        )

        self.skills["shield_mastery"] = Skill(
            "Shield Mastery",
            "survival",
            SURVIVAL_SKILLS["shield_mastery"]["max_level"],
            "Improves shield effectiveness",
            prerequisites=["armor_mastery"],
            stats={"shield_bonus": SURVIVAL_SKILLS["shield_mastery"]["shield_bonus_per_level"]}
        )

        self.skills["damage_resistance"] = Skill(
            "Damage Resistance",
            "survival",
            SURVIVAL_SKILLS["damage_resistance"]["max_level"],
            "Reduces all damage taken",
            prerequisites=["health_regeneration"],
            stats={"resistance": SURVIVAL_SKILLS["damage_resistance"]["resistance_per_level"]}
        )

        self.skills["second_wind"] = Skill(
            "Second Wind",
            "survival",
            SURVIVAL_SKILLS["second_wind"]["max_level"],
            "Heal when health drops below 25%",
            prerequisites=["shield_mastery", "damage_resistance"],
            stats={
                "health_threshold": SURVIVAL_SKILLS["second_wind"]["health_threshold"],
                "heal_amount": SURVIVAL_SKILLS["second_wind"]["heal_amount"]
            }
        )

        # Utility Skills
        self.skills["movement_mastery"] = Skill(
            "Movement Mastery",
            "utility",
            UTILITY_SKILLS["movement_mastery"]["max_level"],
            "Increases movement speed",
            stats={"speed_bonus": UTILITY_SKILLS["movement_mastery"]["speed_bonus_per_level"]}
        )

        self.skills["resource_efficiency"] = Skill(
            "Resource Efficiency",
            "utility",
            UTILITY_SKILLS["resource_efficiency"]["max_level"],
            "Gain bonus experience points",
            stats={"xp_bonus": UTILITY_SKILLS["resource_efficiency"]["xp_bonus_per_level"]}
        )

        self.skills["item_magnetism"] = Skill(
            "Item Magnetism",
            "utility",
            UTILITY_SKILLS["item_magnetism"]["max_level"],
            "Items are attracted from further away",
            prerequisites=["movement_mastery"],
            stats={"magnet_range": UTILITY_SKILLS["item_magnetism"]["range_per_level"]}
        )

        self.skills["detection"] = Skill(
            "Detection",
            "utility",
            UTILITY_SKILLS["detection"]["max_level"],
            "Increases detection range for enemies and items",
            prerequisites=["resource_efficiency"],
            stats={"detection_range": UTILITY_SKILLS["detection"]["range_bonus_per_level"]}
        )

        self.skills["lucky_find"] = Skill(
            "Lucky Find",
            "utility",
            UTILITY_SKILLS["lucky_find"]["max_level"],
            "Increases item drop rates",
            prerequisites=["item_magnetism", "detection"],
            stats={"drop_bonus": UTILITY_SKILLS["lucky_find"]["drop_chance_bonus_per_level"]}
        )

    def add_skill_points(self, points: int) -> None:
        """Add skill points to spend"""
        self.skill_points += points

    def can_upgrade_skill(self, skill_name: str) -> bool:
        """Check if a skill can be upgraded"""
        if skill_name not in self.skills:
            return False
        return self.skills[skill_name].can_upgrade(self.skill_points, self.learned_skills)

    def upgrade_skill(self, skill_name: str) -> bool:
        """Upgrade a skill if possible"""
        if not self.can_upgrade_skill(skill_name):
            return False

        skill = self.skills[skill_name]
        if skill.upgrade():
            self.skill_points -= 1
            self.learned_skills[skill_name] = skill.current_level

            # Unlock skills that have this as a prerequisite
            self._update_skill_availability()
            return True
        return False

    def _update_skill_availability(self) -> None:
        """Update which skills are available based on learned skills"""
        for skill in self.skills.values():
            if not skill.unlocked:
                # Check if all prerequisites are met
                prerequisites_met = True
                for prereq in skill.prerequisites:
                    if prereq not in self.learned_skills or self.learned_skills[prereq] < 1:
                        prerequisites_met = False
                        break
                skill.unlocked = prerequisites_met

    def get_skill_bonus(self, skill_name: str, stat_name: str) -> float:
        """Get the current bonus from a skill for a specific stat"""
        if skill_name not in self.skills:
            return 0.0
        return self.skills[skill_name].get_current_bonus(stat_name)

    def get_total_bonus(self, stat_name: str) -> float:
        """Get the total bonus for a stat from all skills including synergies"""
        total = 0.0

        # Add individual skill bonuses
        for skill in self.skills.values():
            total += skill.get_current_bonus(stat_name)

        # Add synergy bonuses
        synergy_bonuses = self.calculate_synergy_bonuses()
        total += synergy_bonuses.get(stat_name, 0.0)

        return total

    def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get all skills in a specific category"""
        return [skill for skill in self.skills.values() if skill.category == category]

    def calculate_synergy_bonuses(self) -> Dict[str, float]:
        """Calculate bonuses from skill synergies"""
        synergy_bonuses = {}

        for synergy_name, synergy_data in SKILL_SYNERGIES.items():
            if self._check_synergy_requirements(synergy_data):
                # Apply synergy bonuses
                for bonus_stat, bonus_value in synergy_data["bonus"].items():
                    if isinstance(bonus_value, (int, float)):
                        synergy_bonuses[bonus_stat] = synergy_bonuses.get(bonus_stat, 0.0) + bonus_value
                    # Handle boolean bonuses (special effects)
                    elif isinstance(bonus_value, bool) and bonus_value:
                        synergy_bonuses[bonus_stat] = True

        return synergy_bonuses

    def _check_synergy_requirements(self, synergy_data: Dict[str, Any]) -> bool:
        """Check if synergy requirements are met"""
        required_skills = synergy_data["skills"]
        min_levels = synergy_data["min_levels"]

        if len(required_skills) != len(min_levels):
            return False

        for skill_name, min_level in zip(required_skills, min_levels):
            if skill_name not in self.skills:
                return False
            if self.skills[skill_name].current_level < min_level:
                return False

        return True

    def get_active_synergies(self) -> Dict[str, Dict[str, Any]]:
        """Get information about currently active synergies"""
        active_synergies = {}

        for synergy_name, synergy_data in SKILL_SYNERGIES.items():
            if self._check_synergy_requirements(synergy_data):
                active_synergies[synergy_name] = {
                    "name": synergy_name.replace("_", " ").title(),
                    "skills": synergy_data["skills"],
                    "bonuses": synergy_data["bonus"]
                }

        return active_synergies

    def get_potential_synergies(self) -> Dict[str, Dict[str, Any]]:
        """Get synergies that could be unlocked with current skills"""
        potential_synergies = {}

        for synergy_name, synergy_data in SKILL_SYNERGIES.items():
            if not self._check_synergy_requirements(synergy_data):
                # Check how close we are to unlocking this synergy
                required_skills = synergy_data["skills"]
                min_levels = synergy_data["min_levels"]
                progress = []

                for skill_name, min_level in zip(required_skills, min_levels):
                    if skill_name in self.skills:
                        current_level = self.skills[skill_name].current_level
                        progress.append({
                            "skill": skill_name,
                            "current": current_level,
                            "required": min_level,
                            "met": current_level >= min_level
                        })
                    else:
                        progress.append({
                            "skill": skill_name,
                            "current": 0,
                            "required": min_level,
                            "met": False
                        })

                # Only include if at least one requirement is partially met
                if any(p["current"] > 0 for p in progress):
                    potential_synergies[synergy_name] = {
                        "name": synergy_name.replace("_", " ").title(),
                        "progress": progress,
                        "bonuses": synergy_data["bonus"]
                    }

        return potential_synergies

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill tree to dictionary for saving"""
        return {
            "skill_points": self.skill_points,
            "learned_skills": self.learned_skills.copy(),
            "active_synergies": list(self.get_active_synergies().keys())
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load skill tree from dictionary"""
        self.skill_points = data.get("skill_points", 0)
        self.learned_skills = data.get("learned_skills", {})

        # Update skill levels and unlock skills that have been learned
        for skill_name, level in self.learned_skills.items():
            if skill_name in self.skills:
                self.skills[skill_name].current_level = level
                if level > 0:
                    self.skills[skill_name].unlocked = True

        # Update availability for skills that depend on loaded skills
        self._update_skill_availability()
