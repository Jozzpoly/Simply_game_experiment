import pygame
import random
import math
import os
from typing import Optional
from entities.enemy import Enemy
from entities.projectile import Projectile
from utils.constants import *

class BossEnemy(Enemy):
    """Boss enemy with enhanced abilities and multiple attack patterns"""

    def __init__(self, x: int, y: int, difficulty_level: int = 1, boss_type: str = "standard"):
        # Initialize with enhanced stats
        super().__init__(x, y, difficulty_level)

        # Boss-specific properties
        self.boss_type = boss_type
        self.is_boss = True

        # Scale boss stats
        self.max_health = int(self.health * BOSS_HEALTH_MULTIPLIER)
        self.health = self.max_health
        self.damage = int(self.damage * BOSS_DAMAGE_MULTIPLIER)

        # Boss XP reward (much higher than regular enemies)
        self.xp_reward = int(XP_PER_BOSS * (XP_DIFFICULTY_MULTIPLIER ** (difficulty_level - 1)))

        # Boss visual properties - load 64x64 boss sprite
        self.original_size = self.rect.size
        self.scale_factor = BOSS_SIZE_MULTIPLIER
        self._load_boss_sprite()
        self._scale_sprite()

        # Boss behavior properties
        self.attack_pattern = 0  # Current attack pattern
        self.pattern_timer = 0
        self.pattern_duration = 180  # frames per pattern
        self.special_attack_cooldown = 0
        self.special_attack_delay = 300  # frames between special attacks

        # Movement patterns
        self.movement_pattern = "circle"  # circle, figure8, aggressive
        self.movement_timer = 0
        self.movement_center = pygame.math.Vector2(x, y)
        self.movement_radius = 100
        self.movement_angle = 0

        # Multi-shot properties
        self.burst_count = 0
        self.burst_delay = 10  # frames between burst shots
        self.burst_timer = 0

        # Boss phases based on health
        self.phase = 1
        self.max_phases = 3

    def _load_boss_sprite(self) -> None:
        """Load the 64x64 boss sprite"""
        try:
            # Try to load boss idle frame 0 as the base sprite
            boss_sprite_path = "assets/images/entities/boss/idle_0.png"
            if os.path.exists(boss_sprite_path):
                self.image = pygame.image.load(boss_sprite_path).convert_alpha()
                self.rect = self.image.get_rect()
                self.rect.center = (self.rect.centerx, self.rect.centery)
            else:
                # Fallback to regular enemy sprite if boss sprite not found
                pass
        except pygame.error:
            # Fallback to regular enemy sprite if loading fails
            pass

    def _scale_sprite(self) -> None:
        """Scale the boss sprite to be larger"""
        new_width = int(self.original_size[0] * self.scale_factor)
        new_height = int(self.original_size[1] * self.scale_factor)

        # Scale the image
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

        # Update rect but keep center position
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # Update collision rect
        self.collision_rect = self.rect.inflate(-8, -8)

    def update(self, player, walls, projectiles_group) -> None:
        """Enhanced boss update with multiple attack patterns"""
        # Update phase based on health
        health_percentage = self.health / self.max_health
        if health_percentage > 0.66:
            self.phase = 1
        elif health_percentage > 0.33:
            self.phase = 2
        else:
            self.phase = 3

        # Update timers
        self.pattern_timer += 1
        self.movement_timer += 1
        self.special_attack_cooldown = max(0, self.special_attack_cooldown - 1)
        self.burst_timer = max(0, self.burst_timer - 1)

        # Switch attack patterns periodically
        if self.pattern_timer >= self.pattern_duration:
            self.pattern_timer = 0
            self.attack_pattern = (self.attack_pattern + 1) % 3

        # Calculate distance to player
        player_pos = pygame.math.Vector2(player.rect.center)
        boss_pos = pygame.math.Vector2(self.rect.center)
        distance_to_player = player_pos.distance_to(boss_pos)

        # Boss movement patterns
        self._update_movement_pattern(player_pos, boss_pos)

        # Boss attack patterns
        if distance_to_player <= self.detection_radius * 2:  # Larger detection radius
            self._execute_attack_pattern(player, projectiles_group)

        # Move the boss
        self.move(self.velocity.x, self.velocity.y, walls)

        # Update collision rectangle
        if hasattr(self, 'collision_rect'):
            self.collision_rect.center = self.rect.center

    def _update_movement_pattern(self, player_pos: pygame.math.Vector2, boss_pos: pygame.math.Vector2) -> None:
        """Update boss movement based on current pattern and phase"""
        if self.phase == 1:
            # Phase 1: Circular movement around player
            self.movement_center = player_pos
            self.movement_angle += 0.02

            target_x = self.movement_center.x + math.cos(self.movement_angle) * self.movement_radius
            target_y = self.movement_center.y + math.sin(self.movement_angle) * self.movement_radius

            direction = pygame.math.Vector2(target_x - boss_pos.x, target_y - boss_pos.y)
            if direction.length() > 0:
                direction.normalize_ip()
                self.velocity = direction * (self.speed * 0.7)

        elif self.phase == 2:
            # Phase 2: Figure-8 movement with occasional charges
            if self.movement_timer % 240 < 120:  # First half of cycle
                self.movement_angle += 0.03
                offset_x = math.cos(self.movement_angle) * self.movement_radius
                offset_y = math.sin(self.movement_angle * 2) * (self.movement_radius * 0.5)
            else:  # Charge at player
                direction = player_pos - boss_pos
                if direction.length() > 0:
                    direction.normalize_ip()
                    self.velocity = direction * (self.speed * 1.2)
                return

            target_pos = self.movement_center + pygame.math.Vector2(offset_x, offset_y)
            direction = target_pos - boss_pos
            if direction.length() > 0:
                direction.normalize_ip()
                self.velocity = direction * self.speed

        else:  # Phase 3: Aggressive pursuit
            direction = player_pos - boss_pos
            if direction.length() > 0:
                direction.normalize_ip()
                self.velocity = direction * (self.speed * 1.5)

    def _execute_attack_pattern(self, player, projectiles_group) -> None:
        """Execute different attack patterns based on phase and pattern"""
        if not self.can_shoot():
            return

        if self.phase == 1:
            if self.attack_pattern == 0:
                self._single_shot_attack(player, projectiles_group)
            elif self.attack_pattern == 1:
                self._burst_attack(player, projectiles_group)
            else:
                self._spread_attack(player, projectiles_group)

        elif self.phase == 2:
            if self.attack_pattern == 0:
                self._burst_attack(player, projectiles_group)
            elif self.attack_pattern == 1:
                self._spiral_attack(player, projectiles_group)
            else:
                self._rapid_fire_attack(player, projectiles_group)

        else:  # Phase 3
            if self.attack_pattern == 0:
                self._rapid_fire_attack(player, projectiles_group)
            elif self.attack_pattern == 1:
                self._shotgun_attack(player, projectiles_group)
            else:
                self._homing_attack(player, projectiles_group)

    def _single_shot_attack(self, player, projectiles_group) -> None:
        """Standard single shot attack"""
        self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)

    def _burst_attack(self, player, projectiles_group) -> None:
        """Burst fire attack - multiple shots in quick succession"""
        if self.burst_count == 0:
            self.burst_count = 3
            self.burst_timer = self.burst_delay

        if self.burst_timer == 0 and self.burst_count > 0:
            self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)
            self.burst_count -= 1
            self.burst_timer = self.burst_delay

    def _spread_attack(self, player, projectiles_group) -> None:
        """Spread shot attack - multiple projectiles in a fan pattern"""
        center_direction = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )
        if center_direction.length() > 0:
            center_direction.normalize_ip()

        # Create 3 projectiles with slight angle variations
        angles = [-0.3, 0, 0.3]  # radians
        for angle in angles:
            rotated_direction = center_direction.rotate(math.degrees(angle))
            self._create_projectile(rotated_direction, projectiles_group)

    def _spiral_attack(self, player, projectiles_group) -> None:
        """Spiral attack pattern"""
        if self.movement_timer % 15 == 0:  # Shoot every 15 frames
            angle = (self.movement_timer * 0.2) % (2 * math.pi)
            direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
            self._create_projectile(direction, projectiles_group)

    def _rapid_fire_attack(self, player, projectiles_group) -> None:
        """Rapid fire at player"""
        if self.movement_timer % 8 == 0:  # Faster shooting
            self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)

    def _shotgun_attack(self, player, projectiles_group) -> None:
        """Shotgun-style attack with many projectiles"""
        center_direction = pygame.math.Vector2(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )
        if center_direction.length() > 0:
            center_direction.normalize_ip()

        # Create 5 projectiles with wider spread
        angles = [-0.6, -0.3, 0, 0.3, 0.6]
        for angle in angles:
            rotated_direction = center_direction.rotate(math.degrees(angle))
            self._create_projectile(rotated_direction, projectiles_group)

    def _homing_attack(self, player, projectiles_group) -> None:
        """Create homing projectiles (simplified - just aimed at player)"""
        if self.movement_timer % 20 == 0:
            self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)

    def _create_projectile(self, direction: pygame.math.Vector2, projectiles_group) -> None:
        """Create a boss projectile with enhanced properties"""
        projectile = Projectile(
            self.rect.centerx,
            self.rect.centery,
            direction,
            ENEMY_PROJECTILE_IMG,
            PROJECTILE_SPEED * 1.2,  # Faster projectiles
            self.damage,
            is_player_projectile=False
        )
        projectiles_group.add(projectile)

        # Play boss shooting sound
        if hasattr(self, 'audio_manager') and self.audio_manager:
            self.audio_manager.play_sound('enemy_shoot', volume_modifier=1.2)

    def draw_health_bar(self, screen: pygame.Surface, camera_offset_x: int, camera_offset_y: int) -> None:
        """Draw enhanced boss health bar"""
        # Draw larger health bar for boss
        bar_width = 80
        bar_height = 8
        bar_x = self.rect.centerx - camera_offset_x - bar_width // 2
        bar_y = self.rect.y - camera_offset_y - 15

        # Background
        pygame.draw.rect(screen, BLACK, (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))

        # Health
        health_width = int(bar_width * (self.health / self.max_health))

        # Color based on phase
        if self.phase == 1:
            health_color = GREEN
        elif self.phase == 2:
            health_color = YELLOW
        else:
            health_color = RED

        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))

        # Boss indicator
        font = pygame.font.SysFont(None, 16)
        boss_text = font.render("BOSS", True, WHITE)
        text_rect = boss_text.get_rect(center=(bar_x + bar_width // 2, bar_y - 10))
        screen.blit(boss_text, text_rect)
