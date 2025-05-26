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
    """Enhanced screen for upgrading player stats, skills, and equipment"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_tiny = pygame.font.SysFont(None, 18)

        # Player stats reference
        self.player = None

        # Current tab (stats, skills, equipment, achievements)
        self.current_tab = "stats"

        # Scroll offset for skill tree
        self.skill_scroll_y = 0
        self.max_scroll = 0

        # Create tab buttons
        tab_width = 120
        tab_height = 30
        tab_spacing = 10
        tab_start_x = 50

        self.tab_buttons = {
            "stats": Button(tab_start_x, 20, tab_width, tab_height, "Stats", BLUE),
            "skills": Button(tab_start_x + (tab_width + tab_spacing), 20, tab_width, tab_height, "Skills", BLUE),
            "equipment": Button(tab_start_x + 2 * (tab_width + tab_spacing), 20, tab_width, tab_height, "Equipment", BLUE),
            "achievements": Button(tab_start_x + 3 * (tab_width + tab_spacing), 20, tab_width, tab_height, "Achievements", BLUE)
        }

        # Create stat upgrade buttons
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

        # Skill tree layout
        self.skill_tree_area = pygame.Rect(50, 70, width - 100, height - 180)
        self.skill_buttons = {}
        self.skill_connections = []

        # Equipment area
        self.equipment_area = pygame.Rect(50, 70, width - 100, height - 180)

        # Achievement area
        self.achievement_area = pygame.Rect(50, 70, width - 100, height - 180)

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

        # Draw tab buttons
        for tab_name, button in self.tab_buttons.items():
            # Highlight current tab
            if tab_name == self.current_tab:
                button.color = YELLOW
            else:
                button.color = BLUE
            button.draw(surface)

        # Draw title based on current tab
        titles = {
            "stats": "Upgrade Stats",
            "skills": "Skill Tree",
            "equipment": "Equipment",
            "achievements": "Achievements"
        }
        title_text = titles.get(self.current_tab, "Character Progression")
        title_surface = self.font_large.render(title_text, True, YELLOW)
        title_rect = title_surface.get_rect(center=(self.width // 2, 80))
        surface.blit(title_surface, title_rect)

        # Draw content based on current tab
        if self.current_tab == "stats":
            self._draw_stats_tab(surface)
        elif self.current_tab == "skills":
            self._draw_skills_tab(surface)
        elif self.current_tab == "equipment":
            self._draw_equipment_tab(surface)
        elif self.current_tab == "achievements":
            self._draw_achievements_tab(surface)

        # Always draw done button
        self.done_button.draw(surface)

    def _draw_stats_tab(self, surface):
        """Draw the stats upgrade tab"""
        if not self.player:
            return

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

        # Draw stat upgrade buttons
        for button in [self.health_button, self.damage_button, self.speed_button, self.fire_rate_button]:
            button.draw(surface)

    def _draw_skills_tab(self, surface):
        """Draw the skill tree tab"""
        if not self.player:
            return

        skill_tree = self.player.skill_tree

        # Draw skill points
        points_text = f"Skill Points: {skill_tree.skill_points}"
        points_surface = self.font_medium.render(points_text, True, YELLOW)
        points_rect = points_surface.get_rect(center=(self.width // 2, 110))
        surface.blit(points_surface, points_rect)

        # Draw skill categories
        categories = ["combat", "survival", "utility"]
        category_colors = {"combat": RED, "survival": GREEN, "utility": BLUE}

        start_y = 140
        col_width = (self.width - 100) // 3

        for i, category in enumerate(categories):
            x = 50 + i * col_width

            # Category header
            cat_text = category.capitalize()
            cat_surface = self.font_medium.render(cat_text, True, category_colors[category])
            cat_rect = cat_surface.get_rect(center=(x + col_width // 2, start_y))
            surface.blit(cat_surface, cat_rect)

            # Draw skills in this category
            skills = skill_tree.get_skills_by_category(category)
            for j, skill in enumerate(skills):
                skill_y = start_y + 40 + j * 60

                # Skill background
                skill_rect = pygame.Rect(x + 10, skill_y - 15, col_width - 20, 50)

                # Color based on skill state
                if skill.current_level > 0:
                    color = GREEN
                elif skill.unlocked and skill_tree.skill_points > 0:
                    color = YELLOW
                elif skill.unlocked:
                    color = GRAY
                else:
                    color = (50, 50, 50)  # Dark gray for locked

                pygame.draw.rect(surface, color, skill_rect, 2)

                # Skill name
                name_surface = self.font_tiny.render(skill.name, True, WHITE)
                name_rect = name_surface.get_rect(center=(x + col_width // 2, skill_y))
                surface.blit(name_surface, name_rect)

                # Skill level
                level_text = f"{skill.current_level}/{skill.max_level}"
                level_surface = self.font_tiny.render(level_text, True, WHITE)
                level_rect = level_surface.get_rect(center=(x + col_width // 2, skill_y + 15))
                surface.blit(level_surface, level_rect)

                # Store skill button area for clicking
                self.skill_buttons[skill.name] = skill_rect

    def _draw_equipment_tab(self, surface):
        """Draw the equipment tab"""
        if not self.player:
            return

        equipment_manager = self.player.equipment_manager

        # Draw equipped items
        equipped_y = 140
        equipped_text = "Equipped Items:"
        equipped_surface = self.font_medium.render(equipped_text, True, WHITE)
        equipped_rect = equipped_surface.get_rect(center=(self.width // 2, equipped_y))
        surface.blit(equipped_surface, equipped_rect)

        slot_names = {"weapon": "Weapon", "armor": "Armor", "accessory": "Accessory"}
        for i, (slot, name) in enumerate(slot_names.items()):
            y = equipped_y + 40 + i * 40

            # Slot name
            slot_surface = self.font_small.render(f"{name}:", True, WHITE)
            surface.blit(slot_surface, (100, y))

            # Equipped item
            equipped_item = equipment_manager.equipped[slot]
            if equipped_item:
                item_text = equipped_item.get_display_name()
                item_color = equipped_item.get_rarity_color()
            else:
                item_text = "None"
                item_color = GRAY

            item_surface = self.font_small.render(item_text, True, item_color)
            surface.blit(item_surface, (200, y))

        # Draw inventory
        inventory_y = equipped_y + 180
        inventory_text = "Inventory:"
        inventory_surface = self.font_medium.render(inventory_text, True, WHITE)
        inventory_rect = inventory_surface.get_rect(center=(self.width // 2, inventory_y))
        surface.blit(inventory_surface, inventory_rect)

        # Show inventory items (first 10)
        for i, item in enumerate(equipment_manager.inventory[:10]):
            if i >= 10:
                break
            y = inventory_y + 30 + (i % 5) * 25
            x = 100 + (i // 5) * 300

            item_text = item.get_display_name()
            item_color = item.get_rarity_color()
            item_surface = self.font_tiny.render(item_text, True, item_color)
            surface.blit(item_surface, (x, y))

    def _draw_achievements_tab(self, surface):
        """Draw the achievements tab"""
        if not self.player:
            return

        achievement_manager = self.player.achievement_manager

        # Draw achievement progress
        unlocked, total = achievement_manager.get_achievement_progress()
        progress_text = f"Achievements: {unlocked}/{total}"
        progress_surface = self.font_medium.render(progress_text, True, YELLOW)
        progress_rect = progress_surface.get_rect(center=(self.width // 2, 110))
        surface.blit(progress_surface, progress_rect)

        # Draw recent achievements
        if achievement_manager.recently_unlocked:
            recent_text = "Recently Unlocked:"
            recent_surface = self.font_small.render(recent_text, True, GREEN)
            surface.blit(recent_surface, (50, 140))

            for i, achievement in enumerate(achievement_manager.recently_unlocked[:3]):
                y = 160 + i * 25
                ach_text = f"• {achievement.name}"
                ach_surface = self.font_tiny.render(ach_text, True, GREEN)
                surface.blit(ach_surface, (70, y))

        # Draw some unlocked achievements
        unlocked_achievements = achievement_manager.get_unlocked_achievements()
        if unlocked_achievements:
            unlocked_text = "Unlocked Achievements:"
            unlocked_surface = self.font_small.render(unlocked_text, True, WHITE)
            surface.blit(unlocked_surface, (50, 250))

            for i, achievement in enumerate(unlocked_achievements[:8]):
                y = 270 + (i % 4) * 25
                x = 70 + (i // 4) * 300
                ach_text = f"• {achievement.name}"
                ach_surface = self.font_tiny.render(ach_text, True, WHITE)
                surface.blit(ach_surface, (x, y))

    def update(self, mouse_pos):
        """Update UI elements"""
        for button in self.buttons:
            button.update(mouse_pos)

        # Update tab buttons
        for button in self.tab_buttons.values():
            button.update(mouse_pos)

    def handle_click(self, event, player):
        """Handle button clicks and apply upgrades"""
        # Check tab buttons first
        for tab_name, button in self.tab_buttons.items():
            if button.is_clicked(event):
                self.current_tab = tab_name
                return f"tab_{tab_name}"

        # Handle done button
        if self.done_button.is_clicked(event):
            return "done"

        # Handle tab-specific clicks
        if self.current_tab == "stats":
            return self._handle_stats_click(event, player)
        elif self.current_tab == "skills":
            return self._handle_skills_click(event, player)
        elif self.current_tab == "equipment":
            return self._handle_equipment_click(event, player)

        return None

    def _handle_stats_click(self, event, player):
        """Handle clicks in the stats tab"""
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

        return None

    def _handle_skills_click(self, event, player):
        """Handle clicks in the skills tab"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check if any skill was clicked
            for skill_name, skill_rect in self.skill_buttons.items():
                if skill_rect.collidepoint(mouse_pos):
                    if player.skill_tree.upgrade_skill(skill_name):
                        return f"skill_{skill_name}"

        return None

    def _handle_equipment_click(self, event, player):
        """Handle clicks in the equipment tab"""
        # For now, just return None - equipment management could be added later
        # This could include equipping/unequipping items, upgrading equipment, etc.
        return None


class XPProgressBar:
    """XP progress bar for the main game UI"""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, surface, player):
        """Draw the XP progress bar"""
        if not player:
            return

        # Calculate XP progress
        current_xp = player.xp
        xp_needed = player.xp_to_next_level
        progress = current_xp / xp_needed if xp_needed > 0 else 1.0

        # Draw background
        pygame.draw.rect(surface, GRAY, self.rect)

        # Draw progress bar
        progress_width = int(self.rect.width * progress)
        progress_rect = pygame.Rect(self.rect.x, self.rect.y, progress_width, self.rect.height)
        pygame.draw.rect(surface, YELLOW, progress_rect)

        # Draw border
        pygame.draw.rect(surface, WHITE, self.rect, 2)

        # Draw text
        xp_text = f"Level {player.level} - XP: {current_xp}/{xp_needed}"
        text_surface = self.font.render(xp_text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class SkillNotification:
    """Notification for skill upgrades and achievements"""

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont(None, 24)
        self.notifications = []
        self.max_notifications = 3

    def add_notification(self, text, color=WHITE, duration=180):  # 3 seconds at 60 FPS
        """Add a notification to display"""
        self.notifications.append({
            "text": text,
            "color": color,
            "timer": duration,
            "max_timer": duration
        })

        # Keep only the most recent notifications
        if len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)

    def update(self):
        """Update notification timers"""
        self.notifications = [
            notif for notif in self.notifications
            if notif["timer"] > 0
        ]

        for notif in self.notifications:
            notif["timer"] -= 1

    def draw(self, surface):
        """Draw all active notifications"""
        for i, notif in enumerate(self.notifications):
            y = self.rect.y + i * 30

            # Calculate alpha based on remaining time
            alpha = min(255, int(255 * (notif["timer"] / notif["max_timer"])))

            # Create surface with alpha
            text_surface = self.font.render(notif["text"], True, notif["color"])
            text_surface.set_alpha(alpha)

            surface.blit(text_surface, (self.rect.x, y))