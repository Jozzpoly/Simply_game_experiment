import pygame
import random
from utils.constants import *

class Projectile(pygame.sprite.Sprite):
    """Projectile class for combat with visual effects"""

    def __init__(self, x, y, direction, image_path, speed, damage, is_player_projectile=True):
        super().__init__()

        # Load image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Movement
        self.direction = direction
        self.speed = speed

        # Combat
        self.damage = damage
        self.is_player_projectile = is_player_projectile
        self.killed_enemy = False  # Flag to track if this projectile killed an enemy

        # Lifetime
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 5000  # milliseconds

        # Visual effects
        self.original_image = self.image.copy()
        self.rotation = 0
        self.rotation_speed = random.randint(5, 15) if is_player_projectile else 0

        # Trail effect (for player projectiles)
        self.trail = []
        self.trail_length = 5 if is_player_projectile else 0
        self.trail_timer = 0
        self.trail_update_rate = 2  # frames between trail updates

    def update(self, walls, enemies=None, player=None, game=None):
        """Update projectile position and check for collisions"""
        # Move the projectile
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Update visual effects
        self._update_visual_effects()

        # Check if projectile has exceeded its lifetime
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifetime:
            self.kill()
            return

        # Check for wall collisions
        if pygame.sprite.spritecollideany(self, walls):
            # Add impact effect on wall collision
            if game and hasattr(game, 'level') and hasattr(game.level, 'visual_effects'):
                game.level.visual_effects.particle_system.add_impact_effect(
                    self.rect.centerx, self.rect.centery,
                    -self.direction.x, -self.direction.y,
                    GRAY, particle_count=4
                )
            self.kill()
            return

        # Check for entity collisions
        if self.is_player_projectile and enemies:
            # Player projectile hitting enemies
            hit_enemy = pygame.sprite.spritecollideany(self, enemies)
            if hit_enemy:
                # Add impact visual effects
                if game and hasattr(game, 'level') and hasattr(game.level, 'visual_effects'):
                    # Impact particles
                    game.level.visual_effects.particle_system.add_impact_effect(
                        self.rect.centerx, self.rect.centery,
                        self.direction.x, self.direction.y,
                        RED, particle_count=6
                    )

                    # Screen shake for enemy hits
                    game.level.visual_effects.screen_effects.add_screen_shake(intensity=2.0, duration=5)

                # If enemy is killed, add score and set flag
                enemy_died = hit_enemy.take_damage(self.damage)
                if enemy_died and game:
                    game.score += ENEMY_KILL_SCORE
                    self.killed_enemy = True  # Set flag for XP gain
                    self.killed_enemy_ref = hit_enemy  # Store reference to killed enemy

                    # Add explosion effect for enemy death
                    if hasattr(game, 'level') and hasattr(game.level, 'visual_effects'):
                        game.level.visual_effects.particle_system.add_explosion(
                            hit_enemy.rect.centerx, hit_enemy.rect.centery,
                            ORANGE, particle_count=12, intensity=6.0
                        )
                        # Bigger screen shake for enemy death
                        game.level.visual_effects.screen_effects.add_screen_shake(intensity=4.0, duration=8)

                self.kill()
                return

        elif not self.is_player_projectile and player:
            # Enemy projectile hitting player - check against player's collision rect if available
            if hasattr(player, 'collision_rect'):
                # Use the player's collision rectangle for more accurate hit detection
                if self.rect.colliderect(player.collision_rect):
                    player.take_damage(self.damage)
                    self.kill()
                    return
            else:
                # Fallback to sprite collision if no collision_rect is available
                temp_player_group = pygame.sprite.Group()
                temp_player_group.add(player)
                if pygame.sprite.spritecollideany(self, temp_player_group):
                    player.take_damage(self.damage)
                    self.kill()
                    return

    def _update_visual_effects(self):
        """Update visual effects for the projectile"""
        # Rotate the projectile
        if self.rotation_speed != 0:
            self.rotation = (self.rotation + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.original_image, self.rotation)
            # Keep the same center position
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        # Update trail - always increment timer regardless of trail length
        self.trail_timer += 1

        # Only add to trail if we have a trail length > 0 and timer threshold is reached
        if self.trail_length > 0 and self.trail_timer >= self.trail_update_rate:
            self.trail_timer = 0
            # Add current position to trail
            self.trail.append((self.rect.centerx, self.rect.centery))

            # Always limit trail length to prevent memory leaks
            while len(self.trail) > self.trail_length:
                self.trail.pop(0)

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Draw the projectile with its trail"""
        # Draw trail
        if self.trail:
            # Draw trail segments with decreasing size and alpha
            for i, pos in enumerate(self.trail):
                # Calculate size and alpha based on position in trail
                size = int(self.rect.width * (i + 1) / len(self.trail) * 0.8)
                alpha = int(255 * (i + 1) / len(self.trail) * 0.6)

                # Create a surface for this trail segment
                trail_surf = pygame.Surface((size, size), pygame.SRCALPHA)

                # Choose color based on projectile type
                if self.is_player_projectile:
                    color = (0, 255, 255, alpha)  # Cyan for player
                else:
                    color = (255, 0, 0, alpha)  # Red for enemies

                # Draw the trail segment
                pygame.draw.circle(trail_surf, color, (size // 2, size // 2), size // 2)

                # Draw on the main surface with camera offset
                trail_rect = trail_surf.get_rect(center=(pos[0] - camera_offset_x, pos[1] - camera_offset_y))
                surface.blit(trail_surf, trail_rect)

        # Draw the projectile itself
        surface.blit(self.image, (self.rect.x - camera_offset_x, self.rect.y - camera_offset_y))
