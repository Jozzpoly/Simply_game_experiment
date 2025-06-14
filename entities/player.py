import pygame
import random
from typing import Optional, Union, List, Dict, Tuple, Any, cast, TYPE_CHECKING
from pygame.sprite import Group
from entities.entity import Entity
from entities.projectile import Projectile
from utils.constants import *
from config import PLAYER_BASE_SPEED
from utils.animation_system import EnhancedSpriteAnimator
from progression.skill_tree import SkillTree
from progression.equipment import EquipmentManager
from progression.achievements import AchievementManager

# Import Level for type checking only to avoid circular imports
if TYPE_CHECKING:
    from level.level import Level

class Player(Entity):
    """Player character class with upgrade system"""

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, PLAYER_IMG, PLAYER_HEALTH)
        self.speed: float = PLAYER_BASE_SPEED
        self.fire_rate: int = PLAYER_FIRE_RATE
        self.damage: int = PLAYER_DAMAGE

        # Create a smaller collision rectangle for better movement through corridors
        # Keep the visual sprite the same size but make the collision box smaller
        self.collision_rect: pygame.Rect = self.rect.inflate(-8, -8)  # Reduce width and height by 8 pixels each

        # Upgrade system
        # Player's experience level (integer) - not to be confused with the level/map reference
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next_level: int = 100
        self.upgrade_points: int = 0

        # Stats for tracking upgrades
        self.health_upgrades: int = 0
        self.damage_upgrades: int = 0
        self.speed_upgrades: int = 0
        self.fire_rate_upgrades: int = 0

        # Enhanced progression systems
        self.skill_tree = SkillTree()
        self.equipment_manager = EquipmentManager()
        self.achievement_manager = AchievementManager()

        # Player statistics for achievements
        self.stats = {
            "enemies_killed": 0,
            "bosses_killed": 0,
            "levels_completed": 0,
            "perfect_levels": 0,
            "near_death_survivals": 0,
            "skills_learned": 0,
            "maxed_skills": 0,
            "maxed_combat_skills": 0,
            "equipment_equipped": 0,
            "full_equipment_sets": 0,
            "items_collected": 0,
            "secrets_found": 0,
            "max_crit_streak": 0,
            "current_crit_streak": 0,
            "fastest_level_time": float('inf'),
            "player_level": 1,
            "total_damage_dealt": 0
        }

        # Regeneration timer for health regen skill
        self.regen_timer = 0

        # Critical hit system
        self.last_shot_was_critical = False

        # Visual feedback effects
        self.flash_red: bool = False
        self.flash_timer: int = 0
        self.flash_duration: int = 10  # frames
        self.original_image: pygame.Surface = self.image.copy()
        self.flash_image: pygame.Surface = self._create_flash_image(self.original_image, RED)

        # Enhanced animation system
        self.animator = EnhancedSpriteAnimator(self.original_image, "player")
        self.is_moving = False
        self.is_attacking = False
        self.attack_timer = 0

        # Reference to the Level object (not to be confused with self.level which is the player's experience level)
        # This is used for adding visual effects and interacting with the current game level/map
        self.current_level_ref: Optional['Level'] = None

        # Audio manager reference for sound effects
        self.audio_manager = None

        # Special item effects
        self.shield_health: int = 0
        self.shield_duration: int = 0
        self.multi_shot_duration: int = 0
        self.invincibility_duration: int = 0

        # Environmental effects
        self.slow_effect: float = 1.0  # Speed multiplier (1.0 = normal, 0.5 = half speed)
        self.slow_duration: int = 0
        self.damage_boost_multiplier: float = 1.0
        self.damage_boost_duration: int = 0
        self.status_effects: Dict[str, Dict[str, Any]] = {}  # For poison, etc.

    def _create_flash_image(self, original: pygame.Surface, color: Tuple[int, int, int]) -> pygame.Surface:
        """Create a flashed version of the image for damage feedback"""
        flash_img = original.copy()

        # Create a colored overlay
        overlay = pygame.Surface(flash_img.get_size(), pygame.SRCALPHA)
        overlay.fill((color[0], color[1], color[2], 128))  # Semi-transparent color

        # Apply the overlay
        flash_img.blit(overlay, (0, 0))

        return flash_img

    def update(self, walls: Group) -> None:
        """Update player position based on keyboard input"""
        keys = pygame.key.get_pressed()

        # Reset velocity
        self.velocity.x = 0
        self.velocity.y = 0

        # Handle movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = self.speed

        # Normalize diagonal movement
        self.is_moving = self.velocity.length() > 0
        if self.is_moving:
            self.velocity.normalize_ip()
            self.velocity *= self.get_effective_speed()

        # Move the player
        self.move(self.velocity.x, self.velocity.y, walls)

        # Update collision rectangle position to match the sprite
        self.collision_rect.center = self.rect.center

        # Update attack timer
        if self.is_attacking:
            self.attack_timer += 1
            if self.attack_timer >= 18:  # Attack animation duration (6 frames * 3 duration each)
                self.is_attacking = False
                self.attack_timer = 0

        # Update animation system
        self.animator.update(self.is_moving, self.is_attacking)

        # Update sprite image from animation (unless flashing)
        if not self.flash_red:
            self.image = self.animator.get_current_surface()

        # Handle visual effects
        if self.flash_red:
            self.flash_timer -= 1
            if self.flash_timer <= 0:
                self.flash_red = False
                self.image = self.animator.get_current_surface()
            else:
                self.image = self.flash_image

        # Update special item effects
        self._update_special_effects()

        # Apply skill effects
        self.apply_skill_effects()

    def shoot(self, target_x: int, target_y: int, projectiles_group: Group) -> bool:
        """Shoot a projectile towards the target position"""
        if self.can_shoot():
            # Trigger attack animation
            self.is_attacking = True

            # Calculate direction vector
            start_x = self.rect.centerx
            start_y = self.rect.centery

            # Create direction vector
            direction = pygame.math.Vector2(target_x - start_x, target_y - start_y)
            if direction.length() > 0:
                direction.normalize_ip()

            # Calculate effective damage with critical hits
            base_damage = self.get_effective_damage()
            final_damage, is_critical = self.calculate_critical_hit(base_damage)

            # Get skill-based bonuses
            pierce_count = int(self.skill_tree.get_total_bonus("pierce_count"))
            explosion_radius = self.skill_tree.get_total_bonus("explosion_radius")
            extra_projectiles = int(self.skill_tree.get_total_bonus("extra_projectiles"))

            # Create main projectile
            projectile = Projectile(
                start_x,
                start_y,
                direction,
                PLAYER_PROJECTILE_IMG,
                PROJECTILE_SPEED,
                final_damage,
                is_player_projectile=True
            )

            # Apply skill effects to projectile
            if is_critical:
                projectile.is_critical = True
            if pierce_count > 0:
                projectile.pierce_count = pierce_count
            if explosion_radius > 0:
                projectile.explosion_radius = explosion_radius

            # Add to group
            projectiles_group.add(projectile)

            # Play shooting sound
            if hasattr(self, 'audio_manager') and self.audio_manager:
                self.audio_manager.play_sound('player_shoot')

            # Calculate total extra projectiles from all sources
            total_extra_projectiles = extra_projectiles

            # Add item-based multi-shot projectiles - they stack with skill multishot
            if self.multi_shot_duration > 0:
                total_extra_projectiles += 2  # Item always gives 2 extra projectiles

            if total_extra_projectiles > 0:
                import math
                # Calculate spread angles for additional projectiles
                angle_step = 0.3  # Base angle between projectiles
                start_angle = -(total_extra_projectiles * angle_step) / 2

                for i in range(total_extra_projectiles):
                    angle = start_angle + (i * angle_step)

                    # Calculate rotated direction
                    cos_a = math.cos(angle)
                    sin_a = math.sin(angle)
                    rotated_x = direction.x * cos_a - direction.y * sin_a
                    rotated_y = direction.x * sin_a + direction.y * cos_a
                    rotated_direction = pygame.math.Vector2(rotated_x, rotated_y)

                    # Create additional projectile with same properties as main projectile
                    multi_projectile = Projectile(
                        start_x,
                        start_y,
                        rotated_direction,
                        PLAYER_PROJECTILE_IMG,
                        PROJECTILE_SPEED,
                        final_damage,
                        is_player_projectile=True
                    )

                    # Apply same skill effects
                    if is_critical:
                        multi_projectile.is_critical = True
                    if pierce_count > 0:
                        multi_projectile.pierce_count = pierce_count
                    if explosion_radius > 0:
                        multi_projectile.explosion_radius = explosion_radius

                    projectiles_group.add(multi_projectile)

            return True
        return False

    def can_shoot(self) -> bool:
        """Check if enough time has passed to shoot again (using effective fire rate)"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.get_effective_fire_rate():
            self.last_shot_time = current_time
            return True
        return False

    def _update_special_effects(self) -> None:
        """Update special item effects"""
        # Update shield duration
        if self.shield_duration > 0:
            self.shield_duration -= 1
            if self.shield_duration <= 0:
                self.shield_health = 0

        # Update multi-shot duration
        if self.multi_shot_duration > 0:
            self.multi_shot_duration -= 1

        # Update invincibility duration
        if self.invincibility_duration > 0:
            self.invincibility_duration -= 1

        # Update environmental effects
        self._update_environmental_effects()

    def add_xp(self, amount: int) -> bool:
        """Add experience points and check for level up"""
        self.xp += amount

        # Check for level up
        if self.xp >= self.xp_to_next_level:
            self.level_up()
            return True
        return False

    def level_up(self) -> None:
        """Level up the player and award upgrade points"""
        # Increment the player's experience level (integer)
        self.level += 1
        self.xp -= self.xp_to_next_level

        # Increase XP required for next level (scaling difficulty)
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)

        # Award upgrade points and skill points
        self.upgrade_points += UPGRADE_POINTS_PER_LEVEL
        self.skill_tree.add_skill_points(SKILL_POINTS_PER_LEVEL)

        # Update player level stat for achievements
        self.stats["player_level"] = self.level

        # Check for achievements
        self.achievement_manager.check_achievements(self.stats)

        # Play level up sound
        if hasattr(self, 'audio_manager') and self.audio_manager:
            self.audio_manager.play_sound('level_up')

    def upgrade_health(self) -> bool:
        """Upgrade player's maximum health with diminishing returns"""
        if self.upgrade_points > 0:
            # Health has the least diminishing returns
            health_increase = MAX_HEALTH_UPGRADE / (1 + 0.1 * self.health_upgrades)
            health_increase = max(5, int(health_increase))  # Ensure minimum increase of 5

            self.max_health += health_increase
            self.health += health_increase  # Also heal the player
            self.health_upgrades += 1
            self.upgrade_points -= 1
            return True
        return False

    def upgrade_damage(self) -> bool:
        """Upgrade player's damage with diminishing returns"""
        if self.upgrade_points > 0:
            # Calculate diminishing returns
            damage_increase = MAX_DAMAGE_UPGRADE / (1 + 0.15 * self.damage_upgrades)
            damage_increase = max(1, int(damage_increase))  # Ensure minimum increase of 1

            self.damage += damage_increase
            self.damage_upgrades += 1
            self.upgrade_points -= 1
            return True
        return False

    def upgrade_speed(self) -> bool:
        """Upgrade player's movement speed with diminishing returns"""
        if self.upgrade_points > 0:
            # Speed has the most aggressive diminishing returns to prevent becoming too fast
            speed_increase = MAX_SPEED_UPGRADE / (1 + 0.25 * self.speed_upgrades)
            speed_increase = max(0.1, round(speed_increase, 1))  # Ensure minimum increase of 0.1

            self.speed += speed_increase
            self.speed_upgrades += 1
            self.upgrade_points -= 1
            return True
        return False

    def upgrade_fire_rate(self) -> bool:
        """Upgrade player's fire rate (reduce cooldown) with diminishing returns"""
        if self.upgrade_points > 0 and self.fire_rate > 100:  # Ensure fire rate doesn't go too low
            # Calculate diminishing returns based on number of previous upgrades
            reduction = FIRE_RATE_UPGRADE / (1 + 0.2 * self.fire_rate_upgrades)

            # Apply the reduction (rounded to nearest integer)
            self.fire_rate -= int(reduction)

            # Ensure fire rate doesn't go below minimum
            self.fire_rate = max(100, self.fire_rate)

            self.fire_rate_upgrades += 1
            self.upgrade_points -= 1
            return True
        return False

    def take_damage(self, amount: int) -> bool:
        """Take damage with visual feedback"""
        # Check for invincibility
        if self.invincibility_duration > 0:
            return False  # No damage taken

        # Apply damage reduction from skills and equipment
        damage_reduction = self.get_damage_reduction()
        amount = int(amount * (1.0 - damage_reduction))

        # Ensure minimum damage of 1 (unless fully blocked)
        if amount > 0:
            amount = max(1, amount)

        # Check for shield
        if self.shield_health > 0:
            shield_damage = min(amount, self.shield_health)
            self.shield_health -= shield_damage
            amount -= shield_damage

            # If shield absorbed all damage, no health damage
            if amount <= 0:
                return False

        # Flash the player red
        self.flash_red = True
        self.flash_timer = self.flash_duration
        self.image = self.flash_image

        # Play hurt sound
        if hasattr(self, 'audio_manager') and self.audio_manager:
            self.audio_manager.play_sound('player_hurt')

        # Apply damage using parent method
        result = super().take_damage(amount)

        # Add floating damage text and visual effects if we have a reference to the level
        if hasattr(self, 'current_level_ref') and self.current_level_ref is not None:
            # Add floating damage text using new animation system
            self.current_level_ref.animation_manager.add_damage_text(amount, self.rect.centerx, self.rect.centery)

            # Add screen shake and flash effects
            self.current_level_ref.visual_effects.screen_effects.add_screen_shake(intensity=3.0, duration=8)
            self.current_level_ref.visual_effects.screen_effects.add_screen_flash(color=RED, intensity=80, duration=3)

            # Add impact particles
            self.current_level_ref.visual_effects.particle_system.add_impact_effect(
                self.rect.centerx, self.rect.centery, 0, -1, RED, particle_count=6
            )

        return result

    def heal(self, amount: int) -> int:
        """Heal the player by the given amount with visual effects"""
        old_health = self.health
        effective_max_health = self.get_effective_max_health()
        self.health = min(effective_max_health, self.health + amount)
        actual_heal = self.health - old_health

        # Add healing visual effects if we have a reference to the level
        if actual_heal > 0 and hasattr(self, 'current_level_ref') and self.current_level_ref is not None:
            # Add floating heal text using new animation system
            self.current_level_ref.animation_manager.add_heal_text(actual_heal, self.rect.centerx, self.rect.centery)

            # Add healing particles
            self.current_level_ref.visual_effects.particle_system.add_healing_effect(
                self.rect.centerx, self.rect.centery, particle_count=8
            )

        return actual_heal

    def get_effective_damage(self) -> float:
        """Get effective damage including all bonuses"""
        base_damage = self.damage

        # Equipment bonuses
        equipment_bonus = self.equipment_manager.get_total_stat_bonus("damage_bonus")

        # Skill bonuses
        weapon_mastery_bonus = self.skill_tree.get_total_bonus("damage_bonus")

        # Calculate total damage
        total_damage = base_damage + equipment_bonus
        total_damage *= (1.0 + weapon_mastery_bonus)

        # Apply environmental damage boost
        total_damage *= self.damage_boost_multiplier

        # Cap damage at reasonable maximum (10000)
        return min(10000.0, total_damage)

    def get_effective_speed(self) -> float:
        """Get effective speed including all bonuses"""
        base_speed = self.speed

        # Equipment bonuses
        equipment_bonus = self.equipment_manager.get_total_stat_bonus("speed_bonus")

        # Skill bonuses
        movement_bonus = self.skill_tree.get_total_bonus("speed_bonus")

        # Calculate total speed
        total_speed = base_speed + equipment_bonus
        total_speed *= (1.0 + movement_bonus)

        # Apply environmental slow effects
        total_speed *= self.slow_effect

        return total_speed

    def get_effective_fire_rate(self) -> int:
        """Get effective fire rate including all bonuses"""
        base_fire_rate = self.fire_rate

        # Equipment bonuses (negative values reduce fire rate)
        equipment_bonus = self.equipment_manager.get_total_stat_bonus("fire_rate_bonus")

        # Calculate total fire rate (ensure minimum)
        total_fire_rate = max(100, int(base_fire_rate - equipment_bonus))

        return total_fire_rate

    def get_critical_chance(self) -> float:
        """Get critical hit chance from skills and equipment"""
        # Base critical chance from skills
        skill_crit = self.skill_tree.get_total_bonus("critical_chance")

        # Equipment critical chance
        equipment_crit = self.equipment_manager.get_total_stat_bonus("critical_chance")

        # Cap critical chance at 95% (0.95)
        return min(0.95, skill_crit + equipment_crit)

    def get_critical_multiplier(self) -> float:
        """Get critical hit damage multiplier"""
        base_multiplier = 2.0  # 200% damage on critical hits

        # Check for synergy bonuses that affect critical damage
        synergy_bonuses = self.skill_tree.calculate_synergy_bonuses()
        crit_damage_bonus = synergy_bonuses.get("critical_damage_multiplier", 0.0)

        return base_multiplier + crit_damage_bonus

    def get_damage_reduction(self) -> float:
        """Get damage reduction from skills and equipment"""
        # Skill-based damage reduction
        armor_mastery = self.skill_tree.get_total_bonus("damage_reduction")
        damage_resistance = self.skill_tree.get_total_bonus("resistance")

        # Equipment damage reduction
        equipment_reduction = self.equipment_manager.get_total_stat_bonus("damage_reduction")

        # Combine all sources (cap at 90% reduction)
        total_reduction = armor_mastery + damage_resistance + equipment_reduction
        return min(0.9, total_reduction)

    def get_effective_max_health(self) -> int:
        """Get effective max health including equipment bonuses"""
        base_max_health = self.max_health

        # Equipment health bonus
        equipment_bonus = self.equipment_manager.get_total_stat_bonus("health_bonus")

        # Calculate total max health
        total_max_health = int(base_max_health + equipment_bonus)

        # Cap max health at reasonable maximum (50000)
        return min(50000, total_max_health)

    def get_xp_bonus(self) -> float:
        """Get XP bonus from skills and equipment"""
        # Skill XP bonus
        skill_bonus = self.skill_tree.get_total_bonus("xp_bonus")

        # Equipment XP bonus
        equipment_bonus = self.equipment_manager.get_total_stat_bonus("xp_bonus")

        return skill_bonus + equipment_bonus

    def get_projectile_speed_bonus(self) -> float:
        """Get projectile speed bonus from equipment"""
        return self.equipment_manager.get_total_stat_bonus("projectile_speed")

    def get_item_find_bonus(self) -> float:
        """Get item find bonus from equipment"""
        return self.equipment_manager.get_total_stat_bonus("item_find")

    def get_skill_cooldown_reduction(self) -> float:
        """Get skill cooldown reduction from equipment"""
        return self.equipment_manager.get_total_stat_bonus("skill_cooldown")

    def get_resource_bonus(self) -> float:
        """Get resource bonus from equipment"""
        return self.equipment_manager.get_total_stat_bonus("resource_bonus")

    def update_progression_stats(self, stat_name: str, value: int = 1) -> None:
        """Update a progression statistic and check achievements"""
        if stat_name in self.stats:
            self.stats[stat_name] += value
            # Check for new achievements
            newly_unlocked = self.achievement_manager.check_achievements(self.stats)

            # Award XP and skill points for achievements
            for achievement in newly_unlocked:
                rewards = achievement.unlock()
                if rewards["xp"] > 0:
                    self.add_xp(rewards["xp"])
                if rewards["skill_points"] > 0:
                    self.skill_tree.add_skill_points(rewards["skill_points"])

    def apply_skill_effects(self) -> None:
        """Apply passive skill effects like health regeneration"""
        # Health regeneration from skills
        skill_regen_amount = self.skill_tree.get_total_bonus("regen_amount")

        # Health regeneration from equipment
        equipment_regen_amount = self.equipment_manager.get_total_stat_bonus("regeneration")

        # Total regeneration amount
        total_regen_amount = skill_regen_amount + equipment_regen_amount

        if total_regen_amount > 0:
            # Use skill regen interval if available, otherwise default to 60 frames (1 second at 60 FPS)
            regen_interval = self.skill_tree.get_skill_bonus("health_regeneration", "regen_interval")
            if regen_interval <= 0:
                regen_interval = 60  # Default interval for equipment regeneration

            self.regen_timer += 1
            if self.regen_timer >= regen_interval:
                self.regen_timer = 0
                effective_max_health = self.get_effective_max_health()
                if self.health < effective_max_health:
                    self.heal(int(total_regen_amount))

        # Second Wind effect
        second_wind_level = self.skill_tree.skills["second_wind"].current_level
        if second_wind_level > 0:
            effective_max_health = self.get_effective_max_health()
            health_threshold = self.skill_tree.get_skill_bonus("second_wind", "health_threshold")
            if self.health / effective_max_health <= health_threshold:
                # Trigger second wind (once per near-death experience)
                if not hasattr(self, '_second_wind_triggered'):
                    self._second_wind_triggered = True
                    heal_amount = self.skill_tree.get_skill_bonus("second_wind", "heal_amount")
                    heal_value = int(effective_max_health * heal_amount)
                    self.heal(heal_value)
                    self.update_progression_stats("near_death_survivals")
            else:
                # Reset second wind when health is above threshold
                if hasattr(self, '_second_wind_triggered'):
                    delattr(self, '_second_wind_triggered')

    def calculate_critical_hit(self, base_damage: float) -> Tuple[float, bool]:
        """Calculate if an attack is a critical hit and return damage and crit status"""
        crit_chance = self.get_critical_chance()
        is_critical = random.random() < crit_chance

        if is_critical:
            # Critical hit multiplier (2x damage)
            damage = base_damage * 2.0
            self.last_shot_was_critical = True
            self.stats["current_crit_streak"] += 1
            self.stats["max_crit_streak"] = max(self.stats["max_crit_streak"],
                                               self.stats["current_crit_streak"])
        else:
            damage = base_damage
            self.last_shot_was_critical = False
            self.stats["current_crit_streak"] = 0

        return damage, is_critical

    def get_progression_data(self) -> Dict[str, Any]:
        """Get all progression data for saving"""
        return {
            "skill_tree": self.skill_tree.to_dict(),
            "equipment_manager": self.equipment_manager.to_dict(),
            "achievement_manager": self.achievement_manager.to_dict(),
            "stats": self.stats.copy(),
            "regen_timer": self.regen_timer
        }

    def load_progression_data(self, data: Dict[str, Any]) -> None:
        """Load progression data from save"""
        if "skill_tree" in data:
            self.skill_tree.from_dict(data["skill_tree"])
        if "equipment_manager" in data:
            self.equipment_manager.from_dict(data["equipment_manager"])
        if "achievement_manager" in data:
            self.achievement_manager.from_dict(data["achievement_manager"])
        if "stats" in data:
            self.stats.update(data["stats"])
        if "regen_timer" in data:
            self.regen_timer = data["regen_timer"]

    def _update_environmental_effects(self) -> None:
        """Update environmental effects like slow, poison, etc."""
        # Update slow effect
        if self.slow_duration > 0:
            self.slow_duration -= 1
            if self.slow_duration <= 0:
                self.slow_effect = 1.0  # Reset to normal speed

        # Update damage boost
        if self.damage_boost_duration > 0:
            self.damage_boost_duration -= 1
            if self.damage_boost_duration <= 0:
                self.damage_boost_multiplier = 1.0  # Reset to normal damage

        # Update status effects
        effects_to_remove = []
        for effect_name, effect_data in self.status_effects.items():
            effect_data['duration'] -= 1

            # Apply effect
            if effect_name == 'poison':
                if effect_data['duration'] % effect_data.get('interval', 60) == 0:  # Every second at 60 FPS
                    self.take_damage(effect_data['damage'])

            # Remove expired effects
            if effect_data['duration'] <= 0:
                effects_to_remove.append(effect_name)

        # Clean up expired effects
        for effect_name in effects_to_remove:
            del self.status_effects[effect_name]

    def apply_slow(self, slow_factor: float, duration: int) -> None:
        """Apply slow effect to player"""
        self.slow_effect = min(self.slow_effect, slow_factor)  # Take the strongest slow
        self.slow_duration = max(self.slow_duration, duration)  # Take the longest duration

    def apply_damage_boost(self, boost_multiplier: float, duration: int) -> None:
        """Apply damage boost effect to player"""
        self.damage_boost_multiplier = max(self.damage_boost_multiplier, boost_multiplier)
        self.damage_boost_duration = max(self.damage_boost_duration, duration)

    def apply_status_effect(self, effect_type: str, damage: int, duration: int) -> None:
        """Apply status effect like poison"""
        if effect_type == 'poison':
            self.status_effects['poison'] = {
                'damage': damage,
                'duration': duration,
                'interval': 60  # Damage every second
            }

    def apply_knockback(self, force: float) -> None:
        """Apply knockback effect (simple implementation)"""
        # For now, just add a brief invincibility to prevent spam
        self.invincibility_duration = max(self.invincibility_duration, 30)  # 0.5 seconds at 60 FPS

    def drain_mana(self, amount: int) -> None:
        """Drain mana (if player has mana system)"""
        # Placeholder for future mana system
        pass

    def boost_mana(self, amount: int) -> None:
        """Boost mana (if player has mana system)"""
        # Placeholder for future mana system
        pass
