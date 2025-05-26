"""
Modern UI System for Phase 3

This module provides enhanced UI/UX with:
- Responsive design for different screen sizes
- Smooth animations and transitions
- Contextual tooltips and help system
- Accessibility features
- Customizable interface layouts
"""

import pygame
import math
import time
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from config import UI_ENHANCEMENT_CONFIG
from utils.constants import *

# Animation easing functions
def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out animation curve"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2

def ease_out_bounce(t: float) -> float:
    """Bounce ease-out animation curve"""
    n1 = 7.5625
    d1 = 2.75

    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


@dataclass
class Animation:
    """Represents a UI animation"""
    start_time: float
    duration: float
    start_value: float
    end_value: float
    easing_function: Callable[[float], float] = ease_in_out_cubic
    completed: bool = False

    def get_current_value(self) -> float:
        """Get current animated value"""
        if self.completed:
            return self.end_value

        current_time = time.time()
        elapsed = current_time - self.start_time

        if elapsed >= self.duration:
            self.completed = True
            return self.end_value

        progress = elapsed / self.duration
        eased_progress = self.easing_function(progress)

        return self.start_value + (self.end_value - self.start_value) * eased_progress


@dataclass
class Tooltip:
    """Represents a contextual tooltip"""
    text: str
    position: Tuple[int, int]
    max_width: int = 300
    background_color: Tuple[int, int, int] = (40, 40, 40)
    text_color: Tuple[int, int, int] = WHITE
    border_color: Tuple[int, int, int] = (100, 100, 100)
    padding: int = 8
    font_size: int = 14


class ModernButton:
    """Enhanced button with modern styling and animations"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 callback: Optional[Callable] = None, style: str = "primary"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.style = style

        # State
        self.is_hovered = False
        self.is_pressed = False
        self.is_enabled = True

        # Animations
        self.hover_animation = Animation(0, 0.2, 0, 1)
        self.press_animation = Animation(0, 0.1, 0, 1)

        # Style configuration
        self.styles = {
            "primary": {
                "bg_color": (70, 130, 180),
                "hover_color": (100, 149, 237),
                "press_color": (65, 105, 225),
                "text_color": WHITE,
                "border_radius": 8
            },
            "secondary": {
                "bg_color": (105, 105, 105),
                "hover_color": (128, 128, 128),
                "press_color": (169, 169, 169),
                "text_color": WHITE,
                "border_radius": 8
            },
            "danger": {
                "bg_color": (220, 20, 60),
                "hover_color": (255, 69, 0),
                "press_color": (178, 34, 34),
                "text_color": WHITE,
                "border_radius": 8
            }
        }

    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> None:
        """Update button state and animations"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos) and self.is_enabled

        # Start hover animation
        if self.is_hovered and not was_hovered:
            self.hover_animation = Animation(time.time(), 0.2, 0, 1)
        elif not self.is_hovered and was_hovered:
            self.hover_animation = Animation(time.time(), 0.2, 1, 0)

        # Handle press state
        was_pressed = self.is_pressed
        self.is_pressed = self.is_hovered and mouse_pressed

        if self.is_pressed and not was_pressed:
            self.press_animation = Animation(time.time(), 0.1, 0, 1)
        elif not self.is_pressed and was_pressed:
            self.press_animation = Animation(time.time(), 0.1, 1, 0)

    def handle_click(self) -> bool:
        """Handle button click"""
        if self.is_hovered and self.is_enabled and self.callback:
            self.callback()
            return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw button with modern styling"""
        if not self.is_enabled:
            return

        style = self.styles.get(self.style, self.styles["primary"])

        # Calculate current colors based on animations
        hover_factor = self.hover_animation.get_current_value()
        press_factor = self.press_animation.get_current_value()

        base_color = style["bg_color"]
        hover_color = style["hover_color"]
        press_color = style["press_color"]

        # Interpolate colors
        if press_factor > 0:
            current_color = self._interpolate_color(base_color, press_color, press_factor)
        else:
            current_color = self._interpolate_color(base_color, hover_color, hover_factor)

        # Draw button background with rounded corners
        self._draw_rounded_rect(surface, self.rect, current_color, style["border_radius"])

        # Draw text
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, style["text_color"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def _interpolate_color(self, color1: Tuple[int, int, int],
                          color2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Interpolate between two colors"""
        return (
            int(color1[0] + (color2[0] - color1[0]) * factor),
            int(color1[1] + (color2[1] - color1[1]) * factor),
            int(color1[2] + (color2[2] - color1[2]) * factor)
        )

    def _draw_rounded_rect(self, surface: pygame.Surface, rect: pygame.Rect,
                          color: Tuple[int, int, int], radius: int) -> None:
        """Draw a rounded rectangle"""
        if radius <= 0:
            pygame.draw.rect(surface, color, rect)
            return

        # Draw main rectangle
        pygame.draw.rect(surface, color,
                        pygame.Rect(rect.x + radius, rect.y, rect.width - 2 * radius, rect.height))
        pygame.draw.rect(surface, color,
                        pygame.Rect(rect.x, rect.y + radius, rect.width, rect.height - 2 * radius))

        # Draw corners
        pygame.draw.circle(surface, color, (rect.x + radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.y + radius), radius)
        pygame.draw.circle(surface, color, (rect.x + radius, rect.bottom - radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)


class ModernPanel:
    """Modern panel with glass-morphism effect"""

    def __init__(self, x: int, y: int, width: int, height: int, title: str = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title

        # Appearance
        self.background_alpha = 180
        self.border_color = (255, 255, 255, 100)
        self.title_color = WHITE

        # Animation
        self.slide_animation = Animation(0, 0.3, -height, 0, ease_out_bounce)

    def show(self) -> None:
        """Show panel with animation"""
        self.slide_animation = Animation(time.time(), 0.3, -self.rect.height, 0, ease_out_bounce)

    def hide(self) -> None:
        """Hide panel with animation"""
        self.slide_animation = Animation(time.time(), 0.3, 0, -self.rect.height)

    def is_visible(self) -> bool:
        """Check if panel is visible"""
        return self.slide_animation.get_current_value() > -self.rect.height + 10

    def draw(self, surface: pygame.Surface) -> None:
        """Draw panel with modern styling"""
        if not self.is_visible():
            return

        # Apply slide animation
        offset_y = self.slide_animation.get_current_value()
        draw_rect = pygame.Rect(self.rect.x, self.rect.y + offset_y,
                               self.rect.width, self.rect.height)

        # Create surface for glass effect
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Draw background with transparency
        pygame.draw.rect(panel_surface, (20, 20, 20, self.background_alpha),
                        pygame.Rect(0, 0, self.rect.width, self.rect.height), border_radius=12)

        # Draw border
        pygame.draw.rect(panel_surface, self.border_color[:3],
                        pygame.Rect(0, 0, self.rect.width, self.rect.height),
                        width=2, border_radius=12)

        # Blit panel to main surface
        surface.blit(panel_surface, draw_rect.topleft)

        # Draw title
        if self.title:
            font = pygame.font.Font(None, 28)
            title_surface = font.render(self.title, True, self.title_color)
            title_rect = title_surface.get_rect(centerx=draw_rect.centerx, y=draw_rect.y + 15)
            surface.blit(title_surface, title_rect)


class TooltipManager:
    """Manages contextual tooltips"""

    def __init__(self):
        self.active_tooltip: Optional[Tooltip] = None
        self.show_delay = 0.5  # seconds
        self.hover_start_time = 0
        self.last_mouse_pos = (0, 0)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update tooltip system"""
        # Check if mouse moved
        if mouse_pos != self.last_mouse_pos:
            self.hover_start_time = time.time()
            self.last_mouse_pos = mouse_pos
            self.active_tooltip = None

    def show_tooltip(self, text: str, position: Tuple[int, int]) -> None:
        """Show tooltip at position"""
        if time.time() - self.hover_start_time >= self.show_delay:
            self.active_tooltip = Tooltip(text, position)

    def hide_tooltip(self) -> None:
        """Hide active tooltip"""
        self.active_tooltip = None

    def draw(self, surface: pygame.Surface) -> None:
        """Draw active tooltip"""
        if not self.active_tooltip:
            return

        tooltip = self.active_tooltip

        # Create tooltip surface
        font = pygame.font.Font(None, tooltip.font_size)

        # Word wrap text
        words = tooltip.text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= tooltip.max_width - 2 * tooltip.padding:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        # Calculate tooltip size
        line_height = font.get_height()
        tooltip_width = max(font.size(line)[0] for line in lines) + 2 * tooltip.padding
        tooltip_height = len(lines) * line_height + 2 * tooltip.padding

        # Adjust position to keep tooltip on screen
        screen_width, screen_height = surface.get_size()
        x, y = tooltip.position

        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width
        if y + tooltip_height > screen_height:
            y = screen_height - tooltip_height

        # Draw tooltip background
        tooltip_rect = pygame.Rect(x, y, tooltip_width, tooltip_height)

        # Background with transparency
        tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        pygame.draw.rect(tooltip_surface, (*tooltip.background_color, 220),
                        pygame.Rect(0, 0, tooltip_width, tooltip_height), border_radius=6)
        pygame.draw.rect(tooltip_surface, tooltip.border_color,
                        pygame.Rect(0, 0, tooltip_width, tooltip_height),
                        width=1, border_radius=6)

        surface.blit(tooltip_surface, (x, y))

        # Draw text lines
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, tooltip.text_color)
            text_y = y + tooltip.padding + i * line_height
            surface.blit(text_surface, (x + tooltip.padding, text_y))


class ModernUISystem:
    """Main modern UI system coordinator"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.config = UI_ENHANCEMENT_CONFIG

        # UI scaling
        self.ui_scale = self.config.get('customization', {}).get('ui_scaling', 1.0)

        # Components
        self.tooltip_manager = TooltipManager()
        self.buttons: List[ModernButton] = []
        self.panels: List[ModernPanel] = []

        # Responsive breakpoints
        self.breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1920
        }

    def get_device_type(self) -> str:
        """Get current device type based on screen width"""
        if self.screen_width < self.breakpoints['mobile']:
            return 'mobile'
        elif self.screen_width < self.breakpoints['tablet']:
            return 'tablet'
        else:
            return 'desktop'

    def scale_value(self, value: int) -> int:
        """Scale a value based on UI scaling"""
        return int(value * self.ui_scale)

    def create_button(self, x: int, y: int, width: int, height: int,
                     text: str, callback: Optional[Callable] = None,
                     style: str = "primary") -> ModernButton:
        """Create a modern button"""
        button = ModernButton(
            self.scale_value(x), self.scale_value(y),
            self.scale_value(width), self.scale_value(height),
            text, callback, style
        )
        self.buttons.append(button)
        return button

    def create_panel(self, x: int, y: int, width: int, height: int,
                    title: str = "") -> ModernPanel:
        """Create a modern panel"""
        panel = ModernPanel(
            self.scale_value(x), self.scale_value(y),
            self.scale_value(width), self.scale_value(height),
            title
        )
        self.panels.append(panel)
        return panel

    def update(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> None:
        """Update all UI components"""
        # Update tooltip manager
        self.tooltip_manager.update(mouse_pos)

        # Update buttons
        for button in self.buttons:
            button.update(mouse_pos, mouse_pressed)

    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Handle mouse clicks on UI elements"""
        for button in self.buttons:
            if button.handle_click():
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw all UI components"""
        # Draw panels
        for panel in self.panels:
            panel.draw(surface)

        # Draw buttons
        for button in self.buttons:
            button.draw(surface)

        # Draw tooltips last (on top)
        self.tooltip_manager.draw(surface)

    def show_tooltip(self, text: str, position: Tuple[int, int]) -> None:
        """Show a tooltip"""
        self.tooltip_manager.show_tooltip(text, position)

    def hide_tooltip(self) -> None:
        """Hide active tooltip"""
        self.tooltip_manager.hide_tooltip()

    def clear_components(self) -> None:
        """Clear all UI components"""
        self.buttons.clear()
        self.panels.clear()
        self.tooltip_manager.hide_tooltip()
