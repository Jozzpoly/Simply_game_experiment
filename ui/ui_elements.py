import pygame
from utils.constants import *
from progression.achievements import Achievement

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
            "detailed": Button(tab_start_x + (tab_width + tab_spacing), 20, tab_width, tab_height, "Detailed", BLUE),
            "skills": Button(tab_start_x + 2 * (tab_width + tab_spacing), 20, tab_width, tab_height, "Skills", BLUE),
            "equipment": Button(tab_start_x + 3 * (tab_width + tab_spacing), 20, tab_width, tab_height, "Equipment", BLUE),
            "achievements": Button(tab_start_x + 4 * (tab_width + tab_spacing), 20, tab_width, tab_height, "Achievements", BLUE)
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

        # Done button - positioned at the very bottom of the screen
        done_button_y = height - button_height - 10  # 10px margin from bottom
        self.done_button = Button(width // 2 - button_width // 2,
                                 done_button_y,
                                 button_width, button_height, "Done", YELLOW)

        # Group all buttons for easier updating
        self.buttons = [self.health_button, self.damage_button,
                        self.speed_button, self.fire_rate_button,
                        self.done_button]

        # Skill tree layout
        self.skill_tree_area = pygame.Rect(50, 70, width - 100, height - 180)
        self.skill_buttons = {}  # Initialize skill buttons dictionary
        self.skill_connections = []

        # Tooltip system for skills
        self.tooltip_skill = None
        self.tooltip_timer = 0
        self.tooltip_delay = 30  # frames to wait before showing tooltip

        # Equipment and inventory UI elements
        self.equipment_slots = {}
        self.inventory_items = {}

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
            "detailed": "Detailed Statistics",
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
        elif self.current_tab == "detailed":
            self._draw_detailed_stats_tab(surface)
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

        # Draw each stat (showing effective stats with equipment bonuses)
        effective_max_health = self.player.get_effective_max_health()
        effective_damage = self.player.get_effective_damage()
        effective_speed = self.player.get_effective_speed()
        effective_fire_rate = self.player.get_effective_fire_rate()

        stats = [
            f"Level: {self.player.level}",
            f"Health: {self.player.health}/{effective_max_health}",
            f"Damage: {effective_damage:.1f}",
            f"Speed: {effective_speed:.1f}",
            f"Fire Rate: {effective_fire_rate}ms"
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

    def _draw_detailed_stats_tab(self, surface):
        """Draw comprehensive player statistics with breakdowns"""
        if not self.player:
            return

        # Helper function to format stats properly
        def format_stat(value, stat_type="number"):
            if stat_type == "percentage":
                return f"{value * 100:.2f}%"
            elif stat_type == "integer":
                return f"{int(value)}"
            elif stat_type == "decimal":
                return f"{value:.2f}"
            elif stat_type == "time":
                return f"{int(value)}ms"
            else:
                return f"{value:.1f}"

        # Start drawing stats in columns
        left_col_x = 50
        right_col_x = 400
        start_y = 120
        line_height = 20

        # Left Column - Combat Stats
        current_y = start_y

        # Combat Stats Header
        combat_header = self.font_medium.render("Combat Statistics", True, RED)
        surface.blit(combat_header, (left_col_x, current_y))
        current_y += 30

        # Base stats
        base_damage = self.player.damage
        equipment_damage = self.player.equipment_manager.get_total_stat_bonus("damage_bonus")
        skill_damage_multiplier = self.player.skill_tree.get_total_bonus("damage_bonus")
        effective_damage = self.player.get_effective_damage()

        combat_stats = [
            ("Base Damage:", format_stat(base_damage, "decimal")),
            ("Equipment Bonus:", f"+{format_stat(equipment_damage, 'decimal')}"),
            ("Skill Multiplier:", format_stat(skill_damage_multiplier, "percentage")),
            ("Total Damage:", format_stat(effective_damage, "decimal")),
            ("", ""),  # Spacer
            ("Base Fire Rate:", format_stat(self.player.fire_rate, "time")),
            ("Equipment Bonus:", f"-{format_stat(self.player.equipment_manager.get_total_stat_bonus('fire_rate_bonus'), 'time')}"),
            ("Effective Fire Rate:", format_stat(self.player.get_effective_fire_rate(), "time")),
            ("", ""),  # Spacer
            ("Critical Chance:", format_stat(self.player.get_critical_chance(), "percentage")),
            ("Critical Multiplier:", format_stat(self.player.get_critical_multiplier(), "decimal")),
        ]

        for stat_name, stat_value in combat_stats:
            if stat_name:  # Skip spacers
                stat_text = f"{stat_name} {stat_value}"
                color = WHITE if not stat_name.startswith("Total") else YELLOW
                stat_surface = self.font_small.render(stat_text, True, color)
                surface.blit(stat_surface, (left_col_x + 10, current_y))
            current_y += line_height

        # Right Column - Defensive & Utility Stats
        current_y = start_y

        # Defensive Stats Header
        defense_header = self.font_medium.render("Defensive & Utility", True, GREEN)
        surface.blit(defense_header, (right_col_x, current_y))
        current_y += 30

        # Health and defense
        base_health = self.player.max_health
        equipment_health = self.player.equipment_manager.get_total_stat_bonus("health_bonus")
        effective_max_health = self.player.get_effective_max_health()

        defensive_stats = [
            ("Base Max Health:", format_stat(base_health, "integer")),
            ("Equipment Bonus:", f"+{format_stat(equipment_health, 'integer')}"),
            ("Total Max Health:", format_stat(effective_max_health, "integer")),
            ("Current Health:", format_stat(self.player.health, "integer")),
            ("", ""),  # Spacer
            ("Base Speed:", format_stat(self.player.speed, "decimal")),
            ("Equipment Bonus:", f"+{format_stat(self.player.equipment_manager.get_total_stat_bonus('speed_bonus'), 'decimal')}"),
            ("Effective Speed:", format_stat(self.player.get_effective_speed(), "decimal")),
            ("", ""),  # Spacer
            ("Damage Reduction:", format_stat(self.player.equipment_manager.get_total_stat_bonus("damage_reduction"), "percentage")),
            ("XP Bonus:", format_stat(self.player.get_xp_bonus(), "percentage")),
        ]

        for stat_name, stat_value in defensive_stats:
            if stat_name:  # Skip spacers
                stat_text = f"{stat_name} {stat_value}"
                color = WHITE if not stat_name.startswith("Total") and not stat_name.startswith("Effective") else YELLOW
                stat_surface = self.font_small.render(stat_text, True, color)
                surface.blit(stat_surface, (right_col_x + 10, current_y))
            current_y += line_height

        # Skill Bonuses Section (bottom)
        skill_y = start_y + 300
        skill_header = self.font_medium.render("Active Skill Bonuses", True, BLUE)
        surface.blit(skill_header, (left_col_x, skill_y))
        skill_y += 25

        # Get all active skill bonuses
        skill_bonuses = []
        for skill_name, skill in self.player.skill_tree.skills.items():
            if skill.current_level > 0:
                for stat_name, bonus_per_level in skill.stats.items():
                    total_bonus = bonus_per_level * skill.current_level
                    if total_bonus > 0:
                        formatted_bonus = format_stat(total_bonus, "percentage" if "chance" in stat_name or "bonus" in stat_name else "number")
                        skill_bonuses.append(f"{skill.name}: +{formatted_bonus} {stat_name.replace('_', ' ')}")

        # Display skill bonuses in two columns
        for i, bonus_text in enumerate(skill_bonuses[:8]):  # Limit to 8 bonuses
            x = left_col_x + 10 if i % 2 == 0 else right_col_x + 10
            y = skill_y + (i // 2) * line_height
            bonus_surface = self.font_tiny.render(bonus_text, True, CYAN)
            surface.blit(bonus_surface, (x, y))

    def _draw_skills_tab(self, surface):
        """Draw the enhanced skill tree tab with synergies"""
        if not self.player:
            return

        skill_tree = self.player.skill_tree

        # Draw skill points
        points_text = f"Skill Points: {skill_tree.skill_points}"
        points_surface = self.font_medium.render(points_text, True, YELLOW)
        points_rect = points_surface.get_rect(center=(self.width // 2, 110))
        surface.blit(points_surface, points_rect)

        # Draw active synergies
        active_synergies = skill_tree.get_active_synergies()
        if active_synergies:
            synergy_text = f"Active Synergies: {len(active_synergies)}"
            synergy_surface = self.font_small.render(synergy_text, True, PURPLE)
            surface.blit(synergy_surface, (50, 130))

        # Draw skill categories
        categories = ["combat", "survival", "utility"]
        category_colors = {"combat": RED, "survival": GREEN, "utility": BLUE}

        start_y = 160
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
                    # Check if skill is part of active synergy
                    is_synergy_skill = any(skill.name in synergy_data["skills"]
                                         for synergy_data in active_synergies.values())
                    color = PURPLE if is_synergy_skill else GREEN
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

        # Draw synergy information at the bottom
        synergy_y = start_y + 350
        if active_synergies:
            synergy_title = "Active Synergies:"
            synergy_title_surface = self.font_small.render(synergy_title, True, PURPLE)
            surface.blit(synergy_title_surface, (50, synergy_y))

            synergy_y += 25
            for i, (_, synergy_data) in enumerate(list(active_synergies.items())[:3]):
                synergy_display = synergy_data["name"]
                synergy_surface = self.font_tiny.render(f"• {synergy_display}", True, WHITE)
                surface.blit(synergy_surface, (70, synergy_y + i * 20))

        # Show potential synergies
        potential_synergies = skill_tree.get_potential_synergies()
        if potential_synergies and synergy_y + 80 < self.height - 50:
            potential_title = "Potential Synergies:"
            potential_title_surface = self.font_tiny.render(potential_title, True, CYAN)
            surface.blit(potential_title_surface, (300, synergy_y))

            pot_y = synergy_y + 20
            for i, (_, synergy_data) in enumerate(list(potential_synergies.items())[:2]):
                synergy_display = synergy_data["name"]
                progress_text = f"• {synergy_display} (In Progress)"
                progress_surface = self.font_tiny.render(progress_text, True, CYAN)
                surface.blit(progress_surface, (320, pot_y + i * 20))

        # Draw skill tooltip if hovering
        self._draw_skill_tooltip(surface)

    def _draw_equipment_tab(self, surface):
        """Draw the enhanced equipment tab with interactive elements"""
        if not self.player:
            return

        equipment_manager = self.player.equipment_manager

        # Draw equipped items section
        equipped_y = 140
        equipped_text = "Equipped Items:"
        equipped_surface = self.font_medium.render(equipped_text, True, WHITE)
        equipped_rect = equipped_surface.get_rect(center=(self.width // 2, equipped_y))
        surface.blit(equipped_surface, equipped_rect)

        # Store equipment slot rectangles for clicking
        self.equipment_slots = {}
        slot_names = {"weapon": "Weapon", "armor": "Armor", "accessory": "Accessory"}

        for i, (slot, name) in enumerate(slot_names.items()):
            y = equipped_y + 40 + i * 50
            slot_rect = pygame.Rect(80, y - 5, 400, 40)

            # Draw slot background
            pygame.draw.rect(surface, (40, 40, 40), slot_rect)
            pygame.draw.rect(surface, WHITE, slot_rect, 2)

            # Store for click detection
            self.equipment_slots[slot] = slot_rect

            # Slot name
            slot_surface = self.font_small.render(f"{name}:", True, WHITE)
            surface.blit(slot_surface, (90, y))

            # Equipped item
            equipped_item = equipment_manager.equipped[slot]
            if equipped_item:
                item_text = equipped_item.get_display_name()
                item_color = equipped_item.get_rarity_color()

                # Show stats preview
                stats_text = self._get_equipment_stats_text(equipped_item)
                stats_surface = self.font_tiny.render(stats_text, True, CYAN)
                surface.blit(stats_surface, (90, y + 20))
            else:
                item_text = "None (Click to equip)"
                item_color = GRAY

            item_surface = self.font_small.render(item_text, True, item_color)
            surface.blit(item_surface, (200, y))

        # Draw set bonuses
        set_bonuses = equipment_manager.get_active_set_bonuses()
        if set_bonuses:
            set_y = equipped_y + 200
            set_text = "Active Set Bonuses:"
            set_surface = self.font_medium.render(set_text, True, YELLOW)
            surface.blit(set_surface, (100, set_y))

            bonus_y = set_y + 30
            for rarity, bonus_info in set_bonuses.items():
                count = bonus_info["count"]
                bonuses = bonus_info["bonuses"]

                # Set name and count
                set_name = f"{rarity} Set ({count} items):"
                set_name_surface = self.font_small.render(set_name, True, EQUIPMENT_RARITY_COLORS[rarity])
                surface.blit(set_name_surface, (120, bonus_y))

                # Bonus details
                bonus_text = ", ".join([f"+{v} {k.replace('_', ' ')}" for k, v in bonuses.items()])
                bonus_surface = self.font_tiny.render(bonus_text, True, WHITE)
                surface.blit(bonus_surface, (140, bonus_y + 20))

                bonus_y += 45

        # Draw inventory section - adjust position to avoid Done button overlap
        inventory_y = equipped_y + 280  # Moved up to avoid Done button
        inventory_text = "Inventory (Click to equip):"
        inventory_surface = self.font_medium.render(inventory_text, True, WHITE)
        surface.blit(inventory_surface, (100, inventory_y))

        # Store inventory item rectangles for clicking
        self.inventory_items = {}
        items_per_row = 3
        item_height = 30  # Reduced height to fit more items

        # Calculate max rows that fit above Done button (y=550)
        max_y = self.height - 60  # Leave space for Done button
        available_height = max_y - (inventory_y + 30)
        max_rows = max(1, available_height // item_height)
        max_items = min(12, max_rows * items_per_row)

        for i, item in enumerate(equipment_manager.inventory[:max_items]):
            row = i // items_per_row
            col = i % items_per_row
            x = 100 + col * 250
            y = inventory_y + 30 + row * item_height

            item_rect = pygame.Rect(x, y, 240, item_height - 5)

            # Draw item background
            item_color = item.get_rarity_color()
            pygame.draw.rect(surface, (20, 20, 20), item_rect)
            pygame.draw.rect(surface, item_color, item_rect, 2)

            # Store for click detection
            self.inventory_items[i] = {"item": item, "rect": item_rect}

            # Item name and level
            item_text = item.get_display_name()
            item_surface = self.font_tiny.render(item_text, True, item_color)
            surface.blit(item_surface, (x + 5, y + 5))

            # Item stats preview
            stats_text = self._get_equipment_stats_text(item)
            stats_surface = self.font_tiny.render(stats_text, True, CYAN)
            surface.blit(stats_surface, (x + 5, y + 18))

    def _get_equipment_stats_text(self, equipment) -> str:
        """Get a short text representation of equipment stats with proper formatting"""
        stats = []
        for stat_name, value in equipment.stats.items():
            if value > 0:
                # Use the new formatted display method
                formatted_bonus = equipment.get_formatted_stat_bonus(stat_name)
                stat_display = stat_name.replace("_", " ").title()
                stats.append(f"{stat_display}: {formatted_bonus}")
        return ", ".join(stats[:2])  # Show first 2 stats

    def _draw_achievements_tab(self, surface):
        """Draw the enhanced achievements tab with progress and chains"""
        if not self.player:
            return

        achievement_manager = self.player.achievement_manager

        # Draw achievement progress
        unlocked, total = achievement_manager.get_achievement_progress()
        progress_text = f"Achievements: {unlocked}/{total}"
        progress_surface = self.font_medium.render(progress_text, True, YELLOW)
        progress_rect = progress_surface.get_rect(center=(self.width // 2, 110))
        surface.blit(progress_surface, progress_rect)

        # Draw completed chains
        completed_chains = len(achievement_manager.completed_chains)
        total_chains = len(achievement_manager.achievement_chains)
        chains_text = f"Completed Chains: {completed_chains}/{total_chains}"
        chains_surface = self.font_small.render(chains_text, True, PURPLE)
        surface.blit(chains_surface, (50, 130))

        # Draw recent achievements
        if achievement_manager.recently_unlocked:
            recent_text = "Recently Unlocked:"
            recent_surface = self.font_small.render(recent_text, True, GREEN)
            surface.blit(recent_surface, (50, 160))

            for i, achievement in enumerate(achievement_manager.recently_unlocked[:3]):
                y = 180 + i * 25
                ach_text = f"• {achievement.name}"
                ach_surface = self.font_tiny.render(ach_text, True, GREEN)
                surface.blit(ach_surface, (70, y))

        # Draw progressive achievements in progress
        progressive_achievements = [ach for ach in achievement_manager.achievements.values()
                                  if ach.achievement_type == "progressive" and not ach.unlocked and ach.progress > 0]
        if progressive_achievements:
            progress_text = "In Progress:"
            progress_surface = self.font_small.render(progress_text, True, CYAN)
            surface.blit(progress_surface, (400, 160))

            for i, achievement in enumerate(progressive_achievements[:4]):
                y = 180 + i * 30
                # Achievement name
                ach_text = f"• {achievement.name}"
                ach_surface = self.font_tiny.render(ach_text, True, WHITE)
                surface.blit(ach_surface, (420, y))

                # Progress bar
                progress_width = 150
                progress_height = 8
                progress_rect = pygame.Rect(420, y + 15, progress_width, progress_height)

                # Background
                pygame.draw.rect(surface, GRAY, progress_rect)

                # Progress fill
                fill_width = int(progress_width * (achievement.progress / achievement.max_progress))
                fill_rect = pygame.Rect(420, y + 15, fill_width, progress_height)
                pygame.draw.rect(surface, CYAN, fill_rect)

                # Progress text
                progress_text = f"{achievement.progress}/{achievement.max_progress}"
                progress_surface = self.font_tiny.render(progress_text, True, WHITE)
                surface.blit(progress_surface, (580, y + 12))

        # Draw unlocked achievements
        unlocked_achievements = achievement_manager.get_unlocked_achievements()
        if unlocked_achievements:
            unlocked_text = "Unlocked Achievements:"
            unlocked_surface = self.font_small.render(unlocked_text, True, WHITE)
            surface.blit(unlocked_surface, (50, 300))

            for i, achievement in enumerate(unlocked_achievements[:8]):
                y = 320 + (i % 4) * 25
                x = 70 + (i // 4) * 300

                # Color code by achievement type
                if achievement.achievement_type == "chain":
                    color = PURPLE
                elif achievement.achievement_type == "progressive":
                    color = CYAN
                elif achievement.hidden:
                    color = YELLOW
                else:
                    color = WHITE

                ach_text = f"• {achievement.name}"
                ach_surface = self.font_tiny.render(ach_text, True, color)
                surface.blit(ach_surface, (x, y))

        # Draw achievement chains status
        if achievement_manager.achievement_chains:
            chains_title = "Achievement Chains:"
            chains_title_surface = self.font_small.render(chains_title, True, PURPLE)
            surface.blit(chains_title_surface, (50, 450))

            chain_y = 470
            for i, (chain_name, chain_data) in enumerate(list(achievement_manager.achievement_chains.items())[:3]):
                chain_display = chain_data["name"]

                # Check completion status
                required_achievements = chain_data["achievements"]
                completed_count = sum(1 for ach_name in required_achievements
                                    if achievement_manager.achievements.get(ach_name, Achievement("", "")).unlocked)
                total_count = len(required_achievements)

                is_completed = chain_name in achievement_manager.completed_chains
                color = GREEN if is_completed else WHITE

                chain_text = f"• {chain_display} ({completed_count}/{total_count})"
                chain_surface = self.font_tiny.render(chain_text, True, color)
                surface.blit(chain_surface, (70, chain_y + i * 20))

    def update(self, mouse_pos):
        """Update UI elements"""
        for button in self.buttons:
            button.update(mouse_pos)

        # Update tab buttons
        for button in self.tab_buttons.values():
            button.update(mouse_pos)

        # Update skill tooltip system
        if self.current_tab == "skills":
            self._update_skill_tooltip(mouse_pos)

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button only
            mouse_pos = event.pos  # Use event position, not current mouse position

            # Check if any skill was clicked
            for skill_display_name, skill_rect in self.skill_buttons.items():
                if skill_rect.collidepoint(mouse_pos):
                    # Convert display name to internal key
                    skill_internal_key = self._get_skill_internal_key(skill_display_name, player.skill_tree)

                    if skill_internal_key:
                        # Check if skill can be upgraded using internal key
                        if player.skill_tree.can_upgrade_skill(skill_internal_key):
                            if player.skill_tree.upgrade_skill(skill_internal_key):
                                return f"skill_{skill_display_name}"

        return None

    def _get_skill_internal_key(self, display_name: str, skill_tree) -> str:
        """Convert skill display name to internal key"""
        for internal_key, skill in skill_tree.skills.items():
            if skill.name == display_name:
                return internal_key
        return None

    def _handle_equipment_click(self, event, player):
        """Handle clicks in the equipment tab with interactive management"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos  # Use event position, not current mouse position
            equipment_manager = player.equipment_manager

            # Check if clicking on equipped item slots (to unequip)
            if hasattr(self, 'equipment_slots'):
                for slot_type, slot_rect in self.equipment_slots.items():
                    if slot_rect.collidepoint(mouse_pos):
                        equipped_item = equipment_manager.equipped[slot_type]
                        if equipped_item:
                            # Unequip item
                            unequipped = equipment_manager.unequip_item(slot_type)
                            if unequipped:
                                return f"unequipped_{slot_type}"
                        else:
                            # Try to auto-equip best item of this type from inventory
                            best_item = self._find_best_item_for_slot(equipment_manager, slot_type)
                            if best_item:
                                equipment_manager.equip_item(best_item)
                                return f"equipped_{slot_type}"

            # Check if clicking on inventory items (to equip)
            if hasattr(self, 'inventory_items'):
                for item_index, item_data in self.inventory_items.items():
                    if item_data["rect"].collidepoint(mouse_pos):
                        item = item_data["item"]
                        # Equip the clicked item and handle old item
                        old_item = equipment_manager.equip_item(item)

                        # If there was an old item equipped, add it to inventory
                        if old_item and not equipment_manager.add_to_inventory(old_item):
                            # If inventory is full, we need to handle this case
                            # For now, we'll just not equip the new item and show a message
                            # The old item stays equipped
                            equipment_manager.equipped[item.equipment_type] = old_item
                            equipment_manager.inventory.append(item)  # Put the new item back
                            return "inventory_full"

                        return f"equipped_{item.equipment_type}"

        return None

    def _find_best_item_for_slot(self, equipment_manager, slot_type):
        """Find the best item in inventory for a specific equipment slot"""
        best_item = None
        best_score = 0

        for item in equipment_manager.inventory:
            if item.equipment_type == slot_type:
                # Calculate item score based on level and rarity
                rarity_bonus = EQUIPMENT_RARITIES.index(item.rarity) + 1
                score = item.level * rarity_bonus

                if score > best_score:
                    best_score = score
                    best_item = item

        return best_item

    def _update_skill_tooltip(self, mouse_pos):
        """Update skill tooltip based on mouse position"""
        if not self.player or not hasattr(self, 'skill_buttons'):
            return

        # Check if mouse is over any skill button
        hovered_skill = None
        for skill_name, skill_rect in self.skill_buttons.items():
            if skill_rect.collidepoint(mouse_pos):
                hovered_skill = skill_name
                break

        # Update tooltip state
        if hovered_skill != self.tooltip_skill:
            self.tooltip_skill = hovered_skill
            self.tooltip_timer = 0
        elif self.tooltip_skill:
            self.tooltip_timer += 1

    def _draw_skill_tooltip(self, surface):
        """Draw detailed skill tooltip"""
        if not self.tooltip_skill or self.tooltip_timer < self.tooltip_delay or not self.player:
            return

        # Find the skill object
        skill = None
        for skill_obj in self.player.skill_tree.skills.values():
            if skill_obj.name == self.tooltip_skill:
                skill = skill_obj
                break

        if not skill:
            return

        # Get mouse position for tooltip placement
        mouse_pos = pygame.mouse.get_pos()
        tooltip_x = mouse_pos[0] + 15
        tooltip_y = mouse_pos[1] - 10

        # Create tooltip content
        tooltip_lines = []

        # Skill name and level
        tooltip_lines.append(f"{skill.name} ({skill.current_level}/{skill.max_level})")
        tooltip_lines.append("")  # Spacer

        # Description
        tooltip_lines.append(skill.description)
        tooltip_lines.append("")  # Spacer

        # Current bonuses
        if skill.current_level > 0:
            tooltip_lines.append("Current Bonuses:")
            for stat_name, bonus_per_level in skill.stats.items():
                current_bonus = bonus_per_level * skill.current_level
                if "chance" in stat_name or "bonus" in stat_name:
                    tooltip_lines.append(f"  +{current_bonus * 100:.1f}% {stat_name.replace('_', ' ')}")
                else:
                    tooltip_lines.append(f"  +{current_bonus:.1f} {stat_name.replace('_', ' ')}")
            tooltip_lines.append("")  # Spacer

        # Next level preview
        if skill.current_level < skill.max_level:
            tooltip_lines.append("Next Level:")
            for stat_name, bonus_per_level in skill.stats.items():
                next_bonus = bonus_per_level * (skill.current_level + 1)
                if "chance" in stat_name or "bonus" in stat_name:
                    tooltip_lines.append(f"  +{next_bonus * 100:.1f}% {stat_name.replace('_', ' ')}")
                else:
                    tooltip_lines.append(f"  +{next_bonus:.1f} {stat_name.replace('_', ' ')}")

        # Prerequisites
        if skill.prerequisites:
            tooltip_lines.append("")  # Spacer
            tooltip_lines.append("Prerequisites:")
            for prereq in skill.prerequisites:
                prereq_skill = self.player.skill_tree.skills.get(prereq)
                if prereq_skill:
                    status = "✓" if prereq_skill.current_level > 0 else "✗"
                    tooltip_lines.append(f"  {status} {prereq_skill.name}")

        # Calculate tooltip size
        max_width = 0
        line_height = 16
        for line in tooltip_lines:
            if line:  # Skip empty lines for width calculation
                text_surface = self.font_tiny.render(line, True, WHITE)
                max_width = max(max_width, text_surface.get_width())

        tooltip_width = max_width + 20
        tooltip_height = len(tooltip_lines) * line_height + 10

        # Adjust position if tooltip would go off screen
        if tooltip_x + tooltip_width > self.width:
            tooltip_x = mouse_pos[0] - tooltip_width - 15
        if tooltip_y + tooltip_height > self.height:
            tooltip_y = mouse_pos[1] - tooltip_height + 10

        # Draw tooltip background
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        pygame.draw.rect(surface, (40, 40, 40), tooltip_rect)
        pygame.draw.rect(surface, WHITE, tooltip_rect, 2)

        # Draw tooltip text
        for i, line in enumerate(tooltip_lines):
            if line:  # Skip empty lines
                color = YELLOW if i == 0 else WHITE  # Highlight skill name
                if line.startswith("Current Bonuses:") or line.startswith("Next Level:") or line.startswith("Prerequisites:"):
                    color = CYAN
                elif line.startswith("  ✓"):
                    color = GREEN
                elif line.startswith("  ✗"):
                    color = RED

                text_surface = self.font_tiny.render(line, True, color)
                surface.blit(text_surface, (tooltip_x + 10, tooltip_y + 5 + i * line_height))


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