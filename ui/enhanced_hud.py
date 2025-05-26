import pygame
import os
from typing import Optional, Dict
from utils.constants import *
from config import HUD_BACKGROUND_ALPHA
from ui.enhanced_ui_elements import ProgressBar
import logging

logger = logging.getLogger(__name__)

class ModernHUD:
    """Enhanced HUD with modern styling and visual effects"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Load UI icons if available
        self.icons = self._load_ui_icons()

        # Fonts
        self.font_large = pygame.font.SysFont(None, 28)
        self.font_medium = pygame.font.SysFont(None, 24)
        self.font_small = pygame.font.SysFont(None, 20)

        # Progress bars
        self.health_bar = ProgressBar(15, 15, 250, 25, color=GREEN)
        self.xp_bar = ProgressBar(15, 50, 250, 20, color=CYAN)

        # HUD panel background
        self.hud_panel = self._create_hud_panel()

        # Animation properties
        self.pulse_timer = 0
        self.warning_flash = False

    def _load_ui_icons(self) -> Dict[str, Optional[pygame.Surface]]:
        """Load UI icons from files if available"""
        icons = {}
        icon_names = ["health", "mana", "xp"]

        for icon_name in icon_names:
            icon_path = f"assets/images/ui/icons/{icon_name}.png"
            if os.path.exists(icon_path):
                try:
                    icons[icon_name] = pygame.image.load(icon_path).convert_alpha()
                except pygame.error as e:
                    logger.warning(f"Failed to load icon {icon_path}: {e}")
                    icons[icon_name] = None
            else:
                icons[icon_name] = None

        return icons

    def _create_hud_panel(self) -> pygame.Surface:
        """Create a modern HUD panel background"""
        panel_width = 400  # Increased width to accommodate text
        panel_height = 120
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)

        # Semi-transparent dark background with gradient (configurable transparency)
        for y in range(panel_height):
            alpha = int(HUD_BACKGROUND_ALPHA * (1.0 - y / panel_height * 0.3))  # Use configurable alpha
            color = (15, 15, 25, alpha)
            pygame.draw.line(panel, color[:3], (0, y), (panel_width, y))

        # Modern border
        border_color = (80, 120, 160)
        pygame.draw.rect(panel, border_color, (0, 0, panel_width, panel_height), 2)

        # Corner accents
        accent_color = (120, 160, 200)
        corner_size = 15
        pygame.draw.rect(panel, accent_color, (0, 0, corner_size, corner_size))
        pygame.draw.rect(panel, accent_color, (panel_width - corner_size, 0, corner_size, corner_size))

        # Inner glow effect
        pygame.draw.rect(panel, (100, 140, 180, 50), (1, 1, panel_width - 2, panel_height - 2), 1)

        return panel

    def update(self, dt: float = 1.0):
        """Update HUD animations and effects"""
        self.pulse_timer += dt * 2.0

        # Update progress bars
        self.health_bar.update(0, dt)  # Will be set in draw method
        self.xp_bar.update(0, dt)      # Will be set in draw method

    def draw(self, surface: pygame.Surface, player, score: int = 0, current_level: int = 1):
        """Draw the enhanced HUD"""
        if not player:
            return

        # Draw HUD panel background
        surface.blit(self.hud_panel, (5, 5))

        # Update and draw health bar
        max_health = player.get_effective_max_health()
        if max_health > 0:
            # Pass the actual health value, not percentage - ProgressBar will calculate the ratio
            health_value = player.health
            # Set the max value for the progress bar to match max health
            self.health_bar.max_value = max_health
            health_percentage = (player.health / max_health) * 100  # For color calculation only
        else:
            health_value = 0
            self.health_bar.max_value = 100
            health_percentage = 0

        self.health_bar.update(health_value)

        # Health bar color changes based on health level
        if health_percentage < 25:
            self.health_bar.color = RED
            self.warning_flash = True
        elif health_percentage < 50:
            self.health_bar.color = ORANGE
        else:
            self.health_bar.color = GREEN
            self.warning_flash = False

        self.health_bar.draw(surface)

        # Draw health icon and text
        if self.icons["health"]:
            surface.blit(self.icons["health"], (270, 12))

        health_text = f"{player.health}/{player.get_effective_max_health()}"
        health_surface = self.font_medium.render(health_text, True, WHITE)
        surface.blit(health_surface, (305, 18))

        # Update and draw XP bar
        if hasattr(player, 'xp_to_next_level') and player.xp_to_next_level > 0:
            # Pass the actual XP value, not percentage - ProgressBar will calculate the ratio
            xp_value = player.xp
            # Set the max value for the progress bar to match XP needed for next level
            self.xp_bar.max_value = player.xp_to_next_level
        else:
            xp_value = 100
            self.xp_bar.max_value = 100

        self.xp_bar.update(xp_value)
        self.xp_bar.draw(surface)

        # Draw XP icon and text
        if self.icons["xp"]:
            surface.blit(self.icons["xp"], (270, 47))

        xp_text = f"Lv.{player.level} ({player.xp}/{player.xp_to_next_level})"
        xp_surface = self.font_small.render(xp_text, True, CYAN)
        surface.blit(xp_surface, (305, 52))

        # Draw upgrade points notification
        if player.upgrade_points > 0:
            self._draw_upgrade_notification(surface, player.upgrade_points)

        # Draw score and level info (top right)
        self._draw_score_info(surface, score, current_level)

        # Draw special effects indicators
        self._draw_special_effects(surface, player)

        # Draw minimap frame (if needed)
        self._draw_minimap_frame(surface)

    def _draw_upgrade_notification(self, surface: pygame.Surface, upgrade_points: int):
        """Draw upgrade points notification with pulsing effect"""
        # Pulsing effect
        pulse_alpha = int(200 + 55 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 180).x))

        # Notification background
        notif_width = 200
        notif_height = 30
        notif_x = self.screen_width // 2 - notif_width // 2
        notif_y = 20

        notif_surface = pygame.Surface((notif_width, notif_height), pygame.SRCALPHA)
        notif_surface.fill((255, 215, 0, pulse_alpha))

        # Border
        pygame.draw.rect(notif_surface, (255, 215, 0), (0, 0, notif_width, notif_height), 2)

        surface.blit(notif_surface, (notif_x, notif_y))

        # Text
        text = f"Upgrade Points: {upgrade_points} (Press U)"
        text_surface = self.font_medium.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(notif_x + notif_width // 2, notif_y + notif_height // 2))
        surface.blit(text_surface, text_rect)

    def _draw_score_info(self, surface: pygame.Surface, score: int, current_level: int):
        """Draw score and level information in top right"""
        # Score
        score_text = f"Score: {score:,}"
        score_surface = self.font_medium.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topright = (self.screen_width - 15, 15)

        # Background for score
        score_bg = pygame.Surface((score_rect.width + 10, score_rect.height + 6), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 150))
        pygame.draw.rect(score_bg, (100, 100, 100), (0, 0, score_rect.width + 10, score_rect.height + 6), 1)

        surface.blit(score_bg, (score_rect.x - 5, score_rect.y - 3))
        surface.blit(score_surface, score_rect)

        # Level
        level_text = f"Level: {current_level}"
        level_surface = self.font_medium.render(level_text, True, WHITE)
        level_rect = level_surface.get_rect()
        level_rect.topright = (self.screen_width - 15, score_rect.bottom + 10)

        # Background for level
        level_bg = pygame.Surface((level_rect.width + 10, level_rect.height + 6), pygame.SRCALPHA)
        level_bg.fill((0, 0, 0, 150))
        pygame.draw.rect(level_bg, (100, 100, 100), (0, 0, level_rect.width + 10, level_rect.height + 6), 1)

        surface.blit(level_bg, (level_rect.x - 5, level_rect.y - 3))
        surface.blit(level_surface, level_rect)

    def _draw_special_effects(self, surface: pygame.Surface, player):
        """Draw special effect indicators"""
        effect_y = 85

        # Shield indicator
        if hasattr(player, 'shield_health') and player.shield_health > 0:
            shield_text = f"Shield: {player.shield_health}"
            shield_surface = self.font_small.render(shield_text, True, CYAN)

            # Background
            shield_bg = pygame.Surface((shield_surface.get_width() + 8, shield_surface.get_height() + 4), pygame.SRCALPHA)
            shield_bg.fill((0, 255, 255, 100))
            pygame.draw.rect(shield_bg, CYAN, (0, 0, shield_bg.get_width(), shield_bg.get_height()), 1)

            surface.blit(shield_bg, (15, effect_y))
            surface.blit(shield_surface, (19, effect_y + 2))
            effect_y += 25

        # Multi-shot indicator
        if hasattr(player, 'multi_shot_duration') and player.multi_shot_duration > 0:
            multi_text = f"Multi-Shot: {player.multi_shot_duration // 60}s"
            multi_surface = self.font_small.render(multi_text, True, ORANGE)

            # Background
            multi_bg = pygame.Surface((multi_surface.get_width() + 8, multi_surface.get_height() + 4), pygame.SRCALPHA)
            multi_bg.fill((255, 165, 0, 100))
            pygame.draw.rect(multi_bg, ORANGE, (0, 0, multi_bg.get_width(), multi_bg.get_height()), 1)

            surface.blit(multi_bg, (15, effect_y))
            surface.blit(multi_surface, (19, effect_y + 2))
            effect_y += 25

        # Invincibility indicator
        if hasattr(player, 'invincibility_duration') and player.invincibility_duration > 0:
            invincible_text = f"Invincible: {player.invincibility_duration // 60}s"
            invincible_surface = self.font_small.render(invincible_text, True, YELLOW)

            # Background with pulsing effect
            pulse_alpha = int(150 + 105 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer * 360).x))
            invincible_bg = pygame.Surface((invincible_surface.get_width() + 8, invincible_surface.get_height() + 4), pygame.SRCALPHA)
            invincible_bg.fill((255, 255, 0, pulse_alpha))
            pygame.draw.rect(invincible_bg, YELLOW, (0, 0, invincible_bg.get_width(), invincible_bg.get_height()), 1)

            surface.blit(invincible_bg, (15, effect_y))
            surface.blit(invincible_surface, (19, effect_y + 2))

    def _draw_minimap_frame(self, surface: pygame.Surface):
        """Draw a modern frame around the minimap area"""
        # Minimap is drawn in bottom right, so we add a frame there
        frame_size = 150
        frame_x = self.screen_width - frame_size - 10
        frame_y = self.screen_height - frame_size - 10

        # Modern frame
        frame_surface = pygame.Surface((frame_size + 10, frame_size + 10), pygame.SRCALPHA)
        pygame.draw.rect(frame_surface, (80, 120, 160), (0, 0, frame_size + 10, frame_size + 10), 2)
        pygame.draw.rect(frame_surface, (120, 160, 200, 50), (1, 1, frame_size + 8, frame_size + 8), 1)

        surface.blit(frame_surface, (frame_x - 5, frame_y - 5))
