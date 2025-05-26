import pygame
import os
from typing import Optional, Tuple, Dict, Any
from utils.constants import *
import logging

logger = logging.getLogger(__name__)

class ModernButton:
    """Enhanced button with modern styling and animations"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 style: str = "primary", font_size: int = 24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.style = style
        self.font_size = font_size
        self.enabled = True

        # Button states
        self.is_hovered = False
        self.is_pressed = False
        self.animation_progress = 0.0

        # Load button graphics if available
        self.button_graphics = self._load_button_graphics()

        # Font
        self.font = pygame.font.SysFont(None, font_size)

        # Colors based on style
        self.colors = self._get_style_colors()

    def _load_button_graphics(self) -> Dict[str, Optional[pygame.Surface]]:
        """Load button graphics from files if available"""
        graphics = {}
        button_path = f"assets/images/ui/buttons/button_{self.rect.width}x{self.rect.height}"

        for state in ["normal", "hover", "pressed", "disabled"]:
            file_path = f"{button_path}_{state}.png"
            if os.path.exists(file_path):
                try:
                    graphics[state] = pygame.image.load(file_path).convert_alpha()
                except pygame.error as e:
                    logger.warning(f"Failed to load button graphic {file_path}: {e}")
                    graphics[state] = None
            else:
                graphics[state] = None

        return graphics

    def _get_style_colors(self) -> Dict[str, Tuple[int, int, int]]:
        """Get colors based on button style"""
        if self.style == "primary":
            return {
                "normal": (70, 130, 180),
                "hover": (90, 150, 200),
                "pressed": (50, 100, 140),
                "disabled": (80, 80, 80),
                "text": WHITE,
                "border": (50, 100, 150)
            }
        elif self.style == "success":
            return {
                "normal": (60, 150, 60),
                "hover": (80, 170, 80),
                "pressed": (40, 120, 40),
                "disabled": (80, 80, 80),
                "text": WHITE,
                "border": (40, 120, 40)
            }
        elif self.style == "danger":
            return {
                "normal": (180, 60, 60),
                "hover": (200, 80, 80),
                "pressed": (140, 40, 40),
                "disabled": (80, 80, 80),
                "text": WHITE,
                "border": (140, 40, 40)
            }
        else:  # default
            return {
                "normal": (100, 100, 100),
                "hover": (120, 120, 120),
                "pressed": (80, 80, 80),
                "disabled": (60, 60, 60),
                "text": WHITE,
                "border": (80, 80, 80)
            }

    def update(self, mouse_pos: Tuple[int, int], dt: float = 1.0):
        """Update button state and animations"""
        was_hovered = self.is_hovered
        self.is_hovered = self.enabled and self.rect.collidepoint(mouse_pos)

        # Smooth animation for hover effect
        target_progress = 1.0 if self.is_hovered else 0.0
        animation_speed = 8.0 * dt

        if self.animation_progress < target_progress:
            self.animation_progress = min(target_progress, self.animation_progress + animation_speed)
        elif self.animation_progress > target_progress:
            self.animation_progress = max(target_progress, self.animation_progress - animation_speed)

    def draw(self, surface: pygame.Surface):
        """Draw the button with modern styling"""
        # Determine current state
        if not self.enabled:
            state = "disabled"
        elif self.is_pressed:
            state = "pressed"
        elif self.is_hovered:
            state = "hover"
        else:
            state = "normal"

        # Use graphics if available, otherwise draw programmatically
        if self.button_graphics.get(state):
            surface.blit(self.button_graphics[state], self.rect.topleft)
        else:
            self._draw_programmatic_button(surface, state)

        # Draw text
        self._draw_text(surface)

    def _draw_programmatic_button(self, surface: pygame.Surface, state: str):
        """Draw button programmatically if graphics aren't available"""
        color = self.colors[state]

        # Draw gradient background
        for y in range(self.rect.height):
            alpha = 1.0 - (y / self.rect.height) * 0.3
            line_color = (int(color[0] * alpha), int(color[1] * alpha), int(color[2] * alpha))
            pygame.draw.line(surface, line_color,
                           (self.rect.x + 2, self.rect.y + y),
                           (self.rect.x + self.rect.width - 3, self.rect.y + y))

        # Draw border
        border_color = self.colors["border"]
        if self.is_hovered:
            # Glowing border effect
            glow_intensity = int(50 * self.animation_progress)
            border_color = (
                min(255, border_color[0] + glow_intensity),
                min(255, border_color[1] + glow_intensity),
                min(255, border_color[2] + glow_intensity)
            )

        pygame.draw.rect(surface, border_color, self.rect, 2)

        # Inner highlight
        if state != "pressed":
            pygame.draw.line(surface, (255, 255, 255, 50),
                           (self.rect.x + 2, self.rect.y + 2),
                           (self.rect.x + self.rect.width - 3, self.rect.y + 2))

    def _draw_text(self, surface: pygame.Surface):
        """Draw button text"""
        text_color = self.colors["text"]
        if not self.enabled:
            text_color = (150, 150, 150)

        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Slight offset when pressed
        if self.is_pressed:
            text_rect.y += 1

        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events. Returns True if button was clicked."""
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True
            self.is_pressed = False

        return False

    def set_enabled(self, enabled: bool):
        """Enable or disable the button"""
        self.enabled = enabled
        if not enabled:
            self.is_hovered = False
            self.is_pressed = False

class ModernPanel:
    """Enhanced panel with modern styling"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.alpha = 220  # Semi-transparent

        # Load panel graphics if available
        self.panel_graphic = self._load_panel_graphic()

        # Title font
        self.title_font = pygame.font.SysFont(None, 32)

    def _load_panel_graphic(self) -> Optional[pygame.Surface]:
        """Load panel graphic from file if available"""
        panel_path = f"assets/images/ui/panels/panel_{self.rect.width}x{self.rect.height}.png"
        if os.path.exists(panel_path):
            try:
                return pygame.image.load(panel_path).convert_alpha()
            except pygame.error as e:
                logger.warning(f"Failed to load panel graphic {panel_path}: {e}")
        return None

    def draw(self, surface: pygame.Surface):
        """Draw the panel"""
        if self.panel_graphic:
            surface.blit(self.panel_graphic, self.rect.topleft)
        else:
            self._draw_programmatic_panel(surface)

        # Draw title if provided
        if self.title:
            self._draw_title(surface)

    def _draw_programmatic_panel(self, surface: pygame.Surface):
        """Draw panel programmatically if graphic isn't available"""
        # Semi-transparent background
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        panel_surface.fill((20, 20, 30, self.alpha))

        # Modern border
        border_color = (100, 150, 200)
        pygame.draw.rect(panel_surface, border_color, (0, 0, self.rect.width, self.rect.height), 3)

        # Inner highlight
        pygame.draw.rect(panel_surface, (150, 200, 255, 100),
                        (2, 2, self.rect.width - 4, self.rect.height - 4), 1)

        # Corner accents
        corner_size = 20
        accent_color = (150, 200, 255)
        pygame.draw.rect(panel_surface, accent_color, (0, 0, corner_size, corner_size))
        pygame.draw.rect(panel_surface, accent_color,
                        (self.rect.width - corner_size, 0, corner_size, corner_size))
        pygame.draw.rect(panel_surface, accent_color,
                        (0, self.rect.height - corner_size, corner_size, corner_size))
        pygame.draw.rect(panel_surface, accent_color,
                        (self.rect.width - corner_size, self.rect.height - corner_size, corner_size, corner_size))

        surface.blit(panel_surface, self.rect.topleft)

    def _draw_title(self, surface: pygame.Surface):
        """Draw panel title"""
        title_surface = self.title_font.render(self.title, True, WHITE)
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.rect.centerx
        title_rect.y = self.rect.y + 10
        surface.blit(title_surface, title_rect)

class ProgressBar:
    """Modern progress bar with smooth animations"""

    def __init__(self, x: int, y: int, width: int, height: int,
                 max_value: float = 100.0, color: Tuple[int, int, int] = GREEN):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = 0.0
        self.display_value = 0.0  # For smooth animation
        self.color = color
        self.background_color = (40, 40, 40)
        self.border_color = (100, 100, 100)

    def update(self, value: float, dt: float = 1.0):
        """Update progress bar value with smooth animation"""
        # Ensure values are valid numbers
        if not isinstance(value, (int, float)) or value != value:  # Check for NaN
            value = 0
        if not isinstance(self.max_value, (int, float)) or self.max_value != self.max_value:
            self.max_value = 100.0
        if self.max_value <= 0:
            self.max_value = 100.0

        self.current_value = max(0, min(self.max_value, value))

        # Smooth animation towards target value
        diff = self.current_value - self.display_value
        animation_speed = 5.0 * dt

        if abs(diff) > 0.1:
            self.display_value += diff * animation_speed
        else:
            self.display_value = self.current_value

    def draw(self, surface: pygame.Surface):
        """Draw the progress bar"""
        # Background
        pygame.draw.rect(surface, self.background_color, self.rect)

        # Progress fill
        if self.display_value > 0 and self.max_value > 0:
            # Ensure we don't get infinity or invalid values
            fill_ratio = min(1.0, max(0.0, self.display_value / self.max_value))
            fill_width = max(0, min(self.rect.width - 4, int(fill_ratio * (self.rect.width - 4))))

            if fill_width > 0:
                fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                                      fill_width, self.rect.height - 4)
                pygame.draw.rect(surface, self.color, fill_rect)

                # Highlight effect
                if fill_width > 2:
                    highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2,
                                               fill_width, 2)
                    highlight_color = (min(255, self.color[0] + 50),
                                     min(255, self.color[1] + 50),
                                     min(255, self.color[2] + 50))
                    pygame.draw.rect(surface, highlight_color, highlight_rect)

        # Border
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
