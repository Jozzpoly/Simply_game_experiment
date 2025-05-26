"""
Enhanced Enemy System for Phase 2 - New Enemy Types with Advanced AI

This module contains the enhanced enemy classes with new enemy types:
- Mage: Ranged spellcaster with elemental attacks
- Assassin: Stealth-based fast attacker
- Necromancer: Summons minions and uses dark magic
- Golem: Slow but extremely durable tank
- Archer: Long-range precision attacks
- Shaman: Support enemy that buffs others
- Berserker Elite: Enhanced berserker with rage mechanics
- Shadow: Teleporting enemy with hit-and-run tactics
"""

import pygame
import random
import math
import logging
from typing import Dict, List, Optional, Tuple, Any
from entities.enemy import Enemy
from config import *
from utils.constants import *

logger = logging.getLogger(__name__)


class EnhancedEnemy(Enemy):
    """Enhanced enemy class with new types and advanced AI capabilities"""

    def __init__(self, x: int, y: int, difficulty_level: int = 1, enemy_type: str = None):
        # Initialize base enemy first
        super().__init__(x, y, difficulty_level)

        # Override enemy type if specified
        if enemy_type and enemy_type in ENHANCED_ENEMY_TYPES:
            self.enemy_type = enemy_type
        elif enemy_type is None:
            # Choose enemy type based on weights
            self.enemy_type = self._choose_enemy_type()

        # Enhanced properties
        self.enhanced_config = ENHANCED_ENEMY_TYPES.get(self.enemy_type, ENHANCED_ENEMY_TYPES['normal'])
        self.special_abilities = self.enhanced_config.get('special_abilities', [])
        self.ai_complexity = self.enhanced_config.get('ai_complexity', 1.0)

        # Apply enhanced type modifiers
        self._apply_enhanced_type_modifiers(difficulty_level)

        # Special ability properties
        self.ability_cooldowns = {}
        self.active_effects = {}
        self.mana = self.enhanced_config.get('mana', 0)
        self.max_mana = self.mana

        # Initialize ability cooldowns
        for ability in self.special_abilities:
            self.ability_cooldowns[ability] = 0

        # Type-specific initialization
        self._initialize_type_specific_properties()

        # Enhanced visual properties
        self.enhanced_color = self._get_enhanced_enemy_color()
        self.current_color = self.enhanced_color
        self.ability_visual_effects = []

        # Advanced AI properties
        self.tactical_state = "normal"  # normal, aggressive, defensive, support
        self.target_priority = "player"  # player, weakest_ally, strongest_ally
        self.coordination_level = self.ai_complexity

    def _choose_enemy_type(self) -> str:
        """Choose enemy type based on spawn weights"""
        types = list(ENHANCED_ENEMY_TYPES.keys())
        weights = [ENHANCED_ENEMY_TYPES[t]['spawn_weight'] for t in types]
        return random.choices(types, weights=weights)[0]

    def _apply_enhanced_type_modifiers(self, difficulty_level: int) -> None:
        """Apply enhanced stat modifiers based on enemy type"""
        config = self.enhanced_config

        # Apply multipliers
        self.health = int(self.health * config['health_multiplier'])
        self.max_health = self.health
        self.damage = int(self.damage * config['damage_multiplier'])
        self.speed *= config['speed_multiplier']
        self.fire_rate = int(self.fire_rate * config['fire_rate_multiplier'])
        self.detection_radius = config['detection_radius']
        self.preferred_range = config['preferred_range']

        # Calculate XP reward based on difficulty and type
        base_xp = 10 * config.get('spawn_weight', 1.0)  # Base XP value
        xp_multiplier = 1.5 ** (difficulty_level - 1)  # XP scaling
        self.xp_reward = int(base_xp * xp_multiplier)

    def _initialize_type_specific_properties(self) -> None:
        """Initialize properties specific to each enemy type"""
        if self.enemy_type == "mage":
            self.spell_cooldowns = self.enhanced_config.get('spell_cooldowns', {})
            self.current_spell = None
            self.casting_time = 0
            self.is_casting = False

        elif self.enemy_type == "assassin":
            self.stealth_active = False
            self.stealth_timer = 0
            self.stealth_duration = self.enhanced_config.get('stealth_duration', 3000)
            self.backstab_multiplier = self.enhanced_config.get('backstab_multiplier', 3.0)

        elif self.enemy_type == "necromancer":
            self.minions = []
            self.max_minions = self.enhanced_config.get('max_minions', 3)
            self.summon_cooldown = self.enhanced_config.get('summon_cooldown', 4000)
            self.last_summon_time = 0

        elif self.enemy_type == "golem":
            self.slam_radius = self.enhanced_config.get('slam_radius', 120)
            self.regen_rate = self.enhanced_config.get('regen_rate', 2)
            self.last_regen_time = 0
            self.immunity_physical = "immunity_physical" in self.special_abilities

        elif self.enemy_type == "archer":
            self.arrow_types = self.enhanced_config.get('arrow_types', ['normal'])
            self.quiver_size = self.enhanced_config.get('quiver_size', 30)
            self.arrows_remaining = self.quiver_size
            self.current_arrow_type = "normal"

        elif self.enemy_type == "shaman":
            self.support_range = self.enhanced_config.get('support_range', 200)
            self.buff_duration = self.enhanced_config.get('buff_duration', 10000)
            self.active_buffs = {}

        elif self.enemy_type == "berserker_elite":
            self.frenzy_threshold = self.enhanced_config.get('frenzy_threshold', 0.5)
            self.leap_range = self.enhanced_config.get('leap_range', 200)
            self.is_frenzied = False
            self.intimidation_radius = 150

        elif self.enemy_type == "shadow":
            self.teleport_cooldown = self.enhanced_config.get('teleport_cooldown', 2000)
            self.clone_duration = self.enhanced_config.get('clone_duration', 5000)
            self.last_teleport_time = 0
            self.shadow_clones = []
            self.phase_shift_active = False

    def _get_enhanced_enemy_color(self) -> Tuple[int, int, int]:
        """Get color based on enhanced enemy type"""
        color_map = {
            "normal": (255, 0, 0),      # Red
            "fast": (255, 165, 0),      # Orange
            "tank": (128, 128, 128),    # Gray
            "sniper": (0, 128, 0),      # Dark Green
            "berserker": (139, 0, 0),   # Dark Red
            "mage": (75, 0, 130),       # Indigo
            "assassin": (64, 64, 64),   # Dark Gray
            "necromancer": (25, 25, 112), # Midnight Blue
            "golem": (160, 82, 45),     # Saddle Brown
            "archer": (34, 139, 34),    # Forest Green
            "shaman": (218, 165, 32),   # Goldenrod
            "berserker_elite": (220, 20, 60), # Crimson
            "shadow": (72, 61, 139)     # Dark Slate Blue
        }
        return color_map.get(self.enemy_type, (255, 0, 0))

    def update(self, player, walls, projectiles_group, systems_manager=None):
        """Enhanced update with new AI behaviors and abilities"""
        # Update base enemy behavior
        super().update(player, walls, projectiles_group, systems_manager)

        # Update type-specific behaviors
        self._update_type_specific_behavior(player, walls, projectiles_group)

        # Update ability cooldowns
        self._update_ability_cooldowns()

        # Update visual effects
        self._update_visual_effects()

        # Update mana regeneration
        if self.mana < self.max_mana:
            self.mana = min(self.max_mana, self.mana + 0.1)  # Slow mana regen

    def _update_type_specific_behavior(self, player, walls, projectiles_group) -> None:
        """Update behavior specific to each enemy type"""
        current_time = pygame.time.get_ticks()

        if self.enemy_type == "mage":
            self._update_mage_behavior(player, projectiles_group, current_time)
        elif self.enemy_type == "assassin":
            self._update_assassin_behavior(player, walls, current_time)
        elif self.enemy_type == "necromancer":
            self._update_necromancer_behavior(player, projectiles_group, current_time)
        elif self.enemy_type == "golem":
            self._update_golem_behavior(player, current_time)
        elif self.enemy_type == "archer":
            self._update_archer_behavior(player, projectiles_group, current_time)
        elif self.enemy_type == "shaman":
            self._update_shaman_behavior(player, current_time)
        elif self.enemy_type == "berserker_elite":
            self._update_berserker_elite_behavior(player, current_time)
        elif self.enemy_type == "shadow":
            self._update_shadow_behavior(player, walls, current_time)

    def _update_mage_behavior(self, player, projectiles_group, current_time: int) -> None:
        """Update mage-specific behavior"""
        if self.is_casting:
            self.casting_time -= 1
            if self.casting_time <= 0:
                self._cast_spell(player, projectiles_group)
                self.is_casting = False

        # Try to cast spells
        if not self.is_casting and self.state == "attack":
            spell_to_cast = self._choose_spell(player)
            if spell_to_cast and self._can_cast_spell(spell_to_cast):
                self._start_casting(spell_to_cast)

    def _update_assassin_behavior(self, player, walls, current_time: int) -> None:
        """Update assassin-specific behavior"""
        # Handle stealth
        if self.stealth_active:
            self.stealth_timer -= 1
            if self.stealth_timer <= 0:
                self.stealth_active = False

        # Try to activate stealth when low on health
        if (not self.stealth_active and
            self.health / self.max_health < 0.3 and
            self._can_use_ability("stealth")):
            self._activate_stealth()

    def _update_necromancer_behavior(self, player, projectiles_group, current_time: int) -> None:
        """Update necromancer-specific behavior"""
        # Clean up dead minions
        self.minions = [minion for minion in self.minions if hasattr(minion, 'health') and minion.health > 0]

        # Try to summon minions
        if (len(self.minions) < self.max_minions and
            current_time - self.last_summon_time > self.summon_cooldown and
            self._can_use_ability("summon_skeleton")):
            self._summon_minion()
            self.last_summon_time = current_time

    def _update_golem_behavior(self, player, current_time: int) -> None:
        """Update golem-specific behavior"""
        # Regeneration
        if current_time - self.last_regen_time > 2000:  # Every 2 seconds
            if self.health < self.max_health:
                self.health = min(self.max_health, self.health + self.regen_rate)
            self.last_regen_time = current_time

    def _update_archer_behavior(self, player, projectiles_group, current_time: int) -> None:
        """Update archer-specific behavior"""
        # Choose arrow type based on situation
        distance_to_player = pygame.math.Vector2(player.rect.center).distance_to(
            pygame.math.Vector2(self.rect.center))

        if distance_to_player > 300 and "piercing" in self.arrow_types:
            self.current_arrow_type = "piercing"
        elif self.health / self.max_health < 0.5 and "explosive" in self.arrow_types:
            self.current_arrow_type = "explosive"
        else:
            self.current_arrow_type = "normal"

    def _update_shaman_behavior(self, player, current_time: int) -> None:
        """Update shaman-specific behavior"""
        # Buff nearby allies
        if self.group_members:
            for ally in self.group_members:
                if (hasattr(ally, 'rect') and
                    pygame.math.Vector2(ally.rect.center).distance_to(
                        pygame.math.Vector2(self.rect.center)) <= self.support_range):
                    self._buff_ally(ally, current_time)

    def _update_berserker_elite_behavior(self, player, current_time: int) -> None:
        """Update berserker elite-specific behavior"""
        # Check for frenzy activation
        health_percentage = self.health / self.max_health
        if health_percentage <= self.frenzy_threshold and not self.is_frenzied:
            self._activate_frenzy()

    def _update_shadow_behavior(self, player, walls, current_time: int) -> None:
        """Update shadow-specific behavior"""
        # Try to teleport when in danger
        if (self.health / self.max_health < 0.4 and
            current_time - self.last_teleport_time > self.teleport_cooldown and
            self._can_use_ability("shadow_step")):
            self._shadow_step(player, walls)
            self.last_teleport_time = current_time

    def _update_ability_cooldowns(self) -> None:
        """Update ability cooldowns"""
        for ability in self.ability_cooldowns:
            if self.ability_cooldowns[ability] > 0:
                self.ability_cooldowns[ability] -= 1

    def _update_visual_effects(self) -> None:
        """Update visual effects for abilities"""
        # Remove expired visual effects
        self.ability_visual_effects = [
            effect for effect in self.ability_visual_effects
            if effect['duration'] > 0
        ]

        # Update remaining effects
        for effect in self.ability_visual_effects:
            effect['duration'] -= 1

    def _can_use_ability(self, ability: str) -> bool:
        """Check if an ability can be used"""
        return (ability in self.special_abilities and
                self.ability_cooldowns.get(ability, 0) <= 0)

    def _can_cast_spell(self, spell: str) -> bool:
        """Check if a spell can be cast (mage-specific)"""
        if self.enemy_type != "mage":
            return False

        spell_costs = {"fireball": 20, "ice_shard": 15, "lightning_bolt": 30, "teleport": 40}
        mana_cost = spell_costs.get(spell, 10)

        return (self.mana >= mana_cost and
                self.spell_cooldowns.get(spell, 0) <= 0)

    def take_damage(self, damage: int, damage_type: str = "physical") -> None:
        """Enhanced damage taking with elemental resistances and special effects"""
        # Apply type-specific damage modifications
        if self.enemy_type == "golem" and damage_type == "physical" and self.immunity_physical:
            damage = int(damage * 0.2)  # 80% physical resistance
        elif self.enemy_type == "shadow" and self.phase_shift_active:
            damage = int(damage * 0.5)  # 50% damage reduction while phase shifting
        elif self.enemy_type == "assassin" and self.stealth_active:
            damage = int(damage * 1.5)  # Take more damage when hit while stealthed
            self.stealth_active = False  # Break stealth

        # Apply damage
        super().take_damage(damage)

        # Type-specific reactions to taking damage
        if self.enemy_type == "berserker_elite" and not self.is_frenzied:
            # Chance to enter frenzy when taking damage
            if random.random() < 0.1:  # 10% chance
                self._activate_frenzy()

    def _activate_frenzy(self) -> None:
        """Activate berserker frenzy (berserker elite)"""
        if self.enemy_type == "berserker_elite":
            self.is_frenzied = True
            self.speed *= 1.5
            self.damage *= 1.8
            self.fire_rate = int(self.fire_rate * 0.6)
            self.current_color = (255, 0, 0)  # Turn red

    def _activate_stealth(self) -> None:
        """Activate stealth (assassin)"""
        if self.enemy_type == "assassin":
            self.stealth_active = True
            self.stealth_timer = self.stealth_duration
            self.ability_cooldowns["stealth"] = 10000  # 10 second cooldown

    def draw_special_effects(self, surface: pygame.Surface, camera_offset_x: float, camera_offset_y: float) -> None:
        """Draw special visual effects for enhanced enemies"""
        screen_x = self.rect.x - camera_offset_x
        screen_y = self.rect.y - camera_offset_y

        # Draw type-specific effects
        if self.enemy_type == "mage" and self.is_casting:
            # Draw casting circle
            pygame.draw.circle(surface, (138, 43, 226),
                             (int(screen_x + self.rect.width//2), int(screen_y + self.rect.height//2)),
                             30, 3)

        elif self.enemy_type == "assassin" and self.stealth_active:
            # Draw stealth effect (semi-transparent)
            stealth_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            stealth_surface.fill((0, 0, 0, 100))
            surface.blit(stealth_surface, (screen_x, screen_y))

        elif self.enemy_type == "necromancer":
            # Draw dark aura
            pygame.draw.circle(surface, (75, 0, 130),
                             (int(screen_x + self.rect.width//2), int(screen_y + self.rect.height//2)),
                             40, 2)

        elif self.enemy_type == "shaman":
            # Draw support aura
            pygame.draw.circle(surface, (218, 165, 32),
                             (int(screen_x + self.rect.width//2), int(screen_y + self.rect.height//2)),
                             self.support_range//4, 1)

        elif self.enemy_type == "shadow" and self.phase_shift_active:
            # Draw phase shift effect
            phase_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            phase_surface.fill((72, 61, 139, 150))
            surface.blit(phase_surface, (screen_x, screen_y))

    # Placeholder methods for abilities (to be implemented as needed)
    def _choose_spell(self, player):
        """Choose spell for mage to cast"""
        available_spells = [spell for spell in self.special_abilities
                          if self._can_cast_spell(spell)]
        return random.choice(available_spells) if available_spells else None

    def _start_casting(self, spell: str) -> None:
        """Start casting a spell"""
        self.is_casting = True
        self.current_spell = spell
        self.casting_time = 60  # 1 second at 60 FPS

    def _cast_spell(self, player, projectiles_group) -> None:
        """Cast the prepared spell"""
        if not self.current_spell:
            return

        # Placeholder spell casting - would create projectiles/effects
        logger.info(f"{self.enemy_type} casts {self.current_spell}")

        # Consume mana
        spell_costs = {"fireball": 20, "ice_shard": 15, "lightning_bolt": 30, "teleport": 40}
        mana_cost = spell_costs.get(self.current_spell, 10)
        self.mana = max(0, self.mana - mana_cost)

        # Set cooldown
        if hasattr(self, 'spell_cooldowns'):
            self.spell_cooldowns[self.current_spell] = pygame.time.get_ticks() + 2000

        self.current_spell = None

    def _summon_minion(self) -> None:
        """Summon a minion (necromancer)"""
        logger.info(f"{self.enemy_type} summons a minion")
        # Placeholder - would create actual minion entity

    def _buff_ally(self, ally, current_time: int) -> None:
        """Buff an ally (shaman)"""
        if not hasattr(ally, 'buffed_until'):
            ally.buffed_until = current_time + self.buff_duration
            ally.damage *= 1.2  # 20% damage boost
            logger.info(f"{self.enemy_type} buffs ally")

    def _shadow_step(self, player, walls) -> None:
        """Teleport to a new position (shadow)"""
        # Simple teleport - move to random position near player
        player_pos = pygame.math.Vector2(player.rect.center)

        # Try to teleport behind player
        for _ in range(10):  # Try up to 10 positions
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(100, 200)
            new_x = player_pos.x + distance * math.cos(angle)
            new_y = player_pos.y + distance * math.sin(angle)

            # Simple bounds check
            if 50 < new_x < 1000 and 50 < new_y < 1000:
                self.rect.centerx = int(new_x)
                self.rect.centery = int(new_y)
                logger.info(f"{self.enemy_type} shadow steps")
                break
