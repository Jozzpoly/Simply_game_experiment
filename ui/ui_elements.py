import pygame
from utils.constants import *

class Button:
    """A clickable button for UI"""

    def __init__(self, x, y, width, height, text, color=BLUE, hover_color=PURPLE, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.enabled = True

        # Font
        self.font = pygame.font.SysFont(None, 32)

    def draw(self, surface):
        """Draw the button on the given surface"""
        # Draw button background
        if self.enabled:
            color = self.hover_color if self.is_hovered else self.color
        else:
            # Disabled button appears grayed out
            color = GRAY

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        # Draw text
        text_color = self.text_color if self.enabled else (200, 200, 200)  # Lighter text for disabled
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.is_hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        """Check if button was clicked"""
        if self.enabled and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

    def set_enabled(self, enabled):
        """Enable or disable the button"""
        self.enabled = enabled
        if not enabled:
            self.is_hovered = False

class GameOverScreen:
    """Game over screen with restart button and next level button"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_small = pygame.font.SysFont(None, 32)

        # Create buttons
        button_width = 200
        button_height = 50

        # Restart button (positioned on the left when victory)
        restart_x = (width - button_width) // 2
        restart_y = height // 2 + 50
        self.restart_button = Button(restart_x, restart_y, button_width, button_height, "Restart Game")

        # Next level button (only shown on victory)
        next_level_x = (width - button_width) // 2
        next_level_y = height // 2 + 120
        self.next_level_button = Button(next_level_x, next_level_y, button_width, button_height, "Next Level", GREEN)

    def draw(self, surface, victory=False, score=0, high_score=0, current_level=1):
        """Draw the game over screen"""
        # Fill background
        surface.fill(BLACK)

        # Draw game over text
        if victory:
            text = "Level Complete!"
            text_color = GREEN
        else:
            text = "Game Over"
            text_color = RED

        text_surface = self.font_large.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 80))
        surface.blit(text_surface, text_rect)

        # Draw score
        score_text = f"Score: {score}"
        score_surface = self.font_small.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(center=(self.width // 2, self.height // 2 - 30))
        surface.blit(score_surface, score_rect)

        # Draw high score
        high_score_text = f"High Score: {high_score}"
        high_score_surface = self.font_small.render(high_score_text, True, YELLOW)
        high_score_rect = high_score_surface.get_rect(center=(self.width // 2, self.height // 2))
        surface.blit(high_score_surface, high_score_rect)

        # Draw level info if victorious
        if victory:
            level_text = f"Current Level: {current_level}"
            level_surface = self.font_small.render(level_text, True, WHITE)
            level_rect = level_surface.get_rect(center=(self.width // 2, self.height // 2 + 30))
            surface.blit(level_surface, level_rect)

            # Draw both buttons
            self.restart_button.draw(surface)
            self.next_level_button.draw(surface)
        else:
            # Only draw restart button
            self.restart_button.draw(surface)

    def update(self, mouse_pos):
        """Update UI elements"""
        self.restart_button.update(mouse_pos)
        self.next_level_button.update(mouse_pos)

    def check_restart(self, event):
        """Check if restart button was clicked"""
        return self.restart_button.is_clicked(event)

    def check_next_level(self, event):
        """Check if next level button was clicked"""
        return self.next_level_button.is_clicked(event)

class StartScreen:
    """Start screen with play and continue buttons"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_small = pygame.font.SysFont(None, 32)

        # Create buttons
        button_width = 200
        button_height = 50

        # New game button
        button_x = (width - button_width) // 2
        button_y = height // 2 + 50
        self.play_button = Button(button_x, button_y, button_width, button_height, "New Game")

        # Continue button
        continue_x = (width - button_width) // 2
        continue_y = height // 2 + 120
        self.continue_button = Button(continue_x, continue_y, button_width, button_height, "Continue Game", GREEN)

        # Flag to track if continue is available
        self.continue_available = False

    def draw(self, surface):
        """Draw the start screen"""
        # Fill background
        surface.fill(BLACK)

        # Draw title
        title_surface = self.font_large.render("Simple Roguelike", True, WHITE)
        title_rect = title_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
        surface.blit(title_surface, title_rect)

        # Draw instructions
        instructions = [
            "WASD or Arrow Keys to move",
            "Mouse or Space to shoot",
            "U key to open upgrade menu",
            "F11 or Alt+Enter for fullscreen",
            "ESC to exit fullscreen",
            "Defeat all enemies to win!"
        ]

        for i, instruction in enumerate(instructions):
            text_surface = self.font_small.render(instruction, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 30 + i * 30))
            surface.blit(text_surface, text_rect)

        # Draw play button
        self.play_button.draw(surface)

        # Draw continue button if available
        if self.continue_available:
            self.continue_button.draw(surface)

    def update(self, mouse_pos):
        """Update UI elements"""
        self.play_button.update(mouse_pos)
        if self.continue_available:
            self.continue_button.update(mouse_pos)

    def check_play(self, event):
        """Check if play button was clicked"""
        return self.play_button.is_clicked(event)

    def check_continue(self, event):
        """Check if continue button was clicked"""
        if self.continue_available:
            return self.continue_button.is_clicked(event)
        return False

    def set_continue_available(self, available):
        """Set whether the continue button should be available"""
        self.continue_available = available

class UpgradeScreen:
    """Screen for upgrading player stats"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)

        # Player stats reference
        self.player = None

        # Create buttons
        button_width = 180
        button_height = 40
        button_spacing = 20

        # Position buttons in a grid
        start_x = (width - (button_width * 2 + button_spacing)) // 2
        start_y = height // 2 - 20

        # Upgrade buttons
        self.health_button = Button(start_x, start_y, button_width, button_height,
                                   "Upgrade Health", GREEN)
        self.damage_button = Button(start_x + button_width + button_spacing, start_y,
                                   button_width, button_height, "Upgrade Damage", RED)
        self.speed_button = Button(start_x, start_y + button_height + button_spacing,
                                  button_width, button_height, "Upgrade Speed", BLUE)
        self.fire_rate_button = Button(start_x + button_width + button_spacing,
                                      start_y + button_height + button_spacing,
                                      button_width, button_height, "Upgrade Fire Rate", PURPLE)

        # Done button
        self.done_button = Button(width // 2 - button_width // 2,
                                 start_y + (button_height + button_spacing) * 2 + 20,
                                 button_width, button_height, "Done", YELLOW)

        # Group all buttons for easier updating
        self.buttons = [self.health_button, self.damage_button,
                        self.speed_button, self.fire_rate_button,
                        self.done_button]

    def update_stats(self, player):
        """Update the player reference and button states"""
        self.player = player

        # Enable/disable buttons based on upgrade points
        has_points = player.upgrade_points > 0
        self.health_button.set_enabled(has_points)
        self.damage_button.set_enabled(has_points)
        self.speed_button.set_enabled(has_points)
        # Only enable fire rate if it's not already at minimum
        self.fire_rate_button.set_enabled(has_points and player.fire_rate > 100)

    def draw(self, surface):
        """Draw the upgrade screen"""
        # Fill background
        surface.fill(BLACK)

        # Draw title
        title_text = "Upgrade Your Character"
        title_surface = self.font_large.render(title_text, True, YELLOW)
        title_rect = title_surface.get_rect(center=(self.width // 2, 80))
        surface.blit(title_surface, title_rect)

        # Draw player stats
        if self.player:
            # Current stats section
            stats_y = 150
            stats_text = "Current Stats:"
            stats_surface = self.font_medium.render(stats_text, True, WHITE)
            stats_rect = stats_surface.get_rect(center=(self.width // 2, stats_y))
            surface.blit(stats_surface, stats_rect)

            # Draw each stat
            stats = [
                f"Level: {self.player.level}",
                f"Health: {self.player.health}/{self.player.max_health}",
                f"Damage: {self.player.damage}",
                f"Speed: {self.player.speed}",
                f"Fire Rate: {self.player.fire_rate}ms"
            ]

            for i, stat in enumerate(stats):
                stat_surface = self.font_small.render(stat, True, WHITE)
                stat_rect = stat_surface.get_rect(center=(self.width // 2, stats_y + 30 + i * 25))
                surface.blit(stat_surface, stat_rect)

            # Draw upgrade points
            points_text = f"Upgrade Points: {self.player.upgrade_points}"
            points_surface = self.font_medium.render(points_text, True, YELLOW)
            points_rect = points_surface.get_rect(center=(self.width // 2, stats_y + 30 + len(stats) * 25 + 10))
            surface.blit(points_surface, points_rect)

            # Draw upgrade descriptions
            descriptions = [
                f"Health: +{MAX_HEALTH_UPGRADE} max health",
                f"Damage: +{MAX_DAMAGE_UPGRADE} damage",
                f"Speed: +{MAX_SPEED_UPGRADE} speed",
                f"Fire Rate: -{FIRE_RATE_UPGRADE}ms cooldown"
            ]

            desc_y = self.height - 120
            for i, desc in enumerate(descriptions):
                desc_surface = self.font_small.render(desc, True, CYAN)
                desc_rect = desc_surface.get_rect(center=(self.width // 2, desc_y + i * 25))
                surface.blit(desc_surface, desc_rect)

        # Draw all buttons
        for button in self.buttons:
            button.draw(surface)

    def update(self, mouse_pos):
        """Update UI elements"""
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_click(self, event, player):
        """Handle button clicks and apply upgrades"""
        if self.health_button.is_clicked(event):
            if player.upgrade_health():
                self.update_stats(player)
                return "health"

        elif self.damage_button.is_clicked(event):
            if player.upgrade_damage():
                self.update_stats(player)
                return "damage"

        elif self.speed_button.is_clicked(event):
            if player.upgrade_speed():
                self.update_stats(player)
                return "speed"

        elif self.fire_rate_button.is_clicked(event):
            if player.upgrade_fire_rate():
                self.update_stats(player)
                return "fire_rate"

        elif self.done_button.is_clicked(event):
            return "done"

        return None
