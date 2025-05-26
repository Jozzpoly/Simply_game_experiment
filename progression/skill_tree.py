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
        """Get the total bonus for a stat from all skills"""
        total = 0.0
        for skill in self.skills.values():
            total += skill.get_current_bonus(stat_name)
        return total
    
    def get_skills_by_category(self, category: str) -> List[Skill]:
        """Get all skills in a specific category"""
        return [skill for skill in self.skills.values() if skill.category == category]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert skill tree to dictionary for saving"""
        return {
            "skill_points": self.skill_points,
            "learned_skills": self.learned_skills.copy()
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load skill tree from dictionary"""
        self.skill_points = data.get("skill_points", 0)
        self.learned_skills = data.get("learned_skills", {})
        
        # Update skill levels
        for skill_name, level in self.learned_skills.items():
            if skill_name in self.skills:
                self.skills[skill_name].current_level = level
        
        # Update availability
        self._update_skill_availability()
