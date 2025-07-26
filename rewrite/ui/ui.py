"""
User Interface - Single File Implementation
Reduced from 2,544 lines (4 files) to ~400 lines (84% reduction)

Simple, functional UI without over-engineering:
- Health and XP bars
- Game menus
- Level information
- Simple button system
"""

import pygame
from config import *

class Button:
    """Simple button class"""
    
    def __init__(self, x, y, width, height, text, font_size=UI_FONT_SIZE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos, mouse_clicked):
        """Update button state"""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.clicked = self.hovered and mouse_clicked
        return self.clicked
    
    def draw(self, screen):
        """Draw the button"""
        # Button background
        color = WHITE if self.hovered else GRAY
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Button text
        text_color = BLACK if self.hovered else WHITE
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class HealthBar:
    """Simple health bar widget"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen, current, maximum, color=GREEN):
        """Draw health bar"""
        # Background
        pygame.draw.rect(screen, RED, self.rect)
        
        # Health
        if maximum > 0:
            health_width = int(self.rect.width * (current / maximum))
            health_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)
            pygame.draw.rect(screen, color, health_rect)
        
        # Border
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class GameUI:
    """Main game UI manager"""
    
    def __init__(self):
        self.font = pygame.font.Font(None, UI_FONT_SIZE)
        self.small_font = pygame.font.Font(None, 18)
        
        # UI elements
        self.health_bar = HealthBar(UI_MARGIN, UI_MARGIN, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT)
        self.xp_bar = HealthBar(UI_MARGIN, UI_MARGIN + 30, HEALTH_BAR_WIDTH, 10)
    
    def draw_hud(self, screen, player, level):
        """Draw the heads-up display during gameplay"""
        if not player:
            return
        
        # Player health bar
        self.health_bar.draw(screen, player.health, player.max_health, GREEN)
        
        # Health text
        health_text = f"Health: {player.health}/{player.max_health}"
        health_surface = self.small_font.render(health_text, True, WHITE)
        screen.blit(health_surface, (UI_MARGIN, UI_MARGIN + HEALTH_BAR_HEIGHT + 5))
        
        # Player XP bar
        self.xp_bar.draw(screen, player.xp, player.xp_to_next_level, BLUE)
        
        # XP text
        xp_text = f"Level {player.level} - XP: {player.xp}/{player.xp_to_next_level}"
        xp_surface = self.small_font.render(xp_text, True, WHITE)
        screen.blit(xp_surface, (UI_MARGIN, UI_MARGIN + 50))
        
        # Player stats
        stats_y = UI_MARGIN + 80
        stats = [
            f"Damage: {player.damage}",
            f"Speed: {player.speed:.0f}",
        ]
        
        for i, stat in enumerate(stats):
            stat_surface = self.small_font.render(stat, True, WHITE)
            screen.blit(stat_surface, (UI_MARGIN, stats_y + i * 20))
        
        # Level info (top right)
        level_info = [
            f"Level: {level.level_number}",
            f"Enemies: {len(level.enemies)}",
            f"Killed: {level.enemies_killed}"
        ]
        
        for i, info in enumerate(level_info):
            info_surface = self.small_font.render(info, True, WHITE)
            info_rect = info_surface.get_rect()
            info_rect.topright = (SCREEN_WIDTH - UI_MARGIN, UI_MARGIN + i * 20)
            screen.blit(info_surface, info_rect)

class MenuUI:
    """Menu system for game states"""
    
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Main menu buttons
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        
        self.start_button = Button(button_x, 300, button_width, button_height, "Start Game")
        self.quit_button = Button(button_x, 370, button_width, button_height, "Quit")
        
        # Game over buttons
        self.restart_button = Button(button_x, 350, button_width, button_height, "Restart")
        self.next_level_button = Button(button_x, 350, button_width, button_height, "Next Level")
        self.menu_button = Button(button_x, 420, button_width, button_height, "Main Menu")
    
    def draw_main_menu(self, screen, mouse_pos, mouse_clicked):
        """Draw main menu"""
        screen.fill(BLACK)
        
        # Title
        title_surface = self.font.render("Simple Roguelike", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_surface = self.small_font.render("Clean Architecture Rewrite", True, GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, 240))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Buttons
        self.start_button.update(mouse_pos, mouse_clicked)
        self.quit_button.update(mouse_pos, mouse_clicked)
        
        self.start_button.draw(screen)
        self.quit_button.draw(screen)
        
        # Instructions
        instructions = [
            "WASD or Arrow Keys - Move",
            "Mouse - Aim and Shoot",
            "ESC - Pause",
            "",
            "Kill all enemies to advance to the next level!"
        ]
        
        for i, instruction in enumerate(instructions):
            if instruction:  # Skip empty lines
                inst_surface = self.small_font.render(instruction, True, WHITE)
                inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, 500 + i * 25))
                screen.blit(inst_surface, inst_rect)
        
        return self.start_button.clicked, self.quit_button.clicked
    
    def draw_pause_menu(self, screen):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_surface = self.font.render("PAUSED", True, WHITE)
        pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_surface, pause_rect)
        
        # Instructions
        inst_surface = self.small_font.render("Press ESC to resume", True, WHITE)
        inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(inst_surface, inst_rect)
    
    def draw_game_over(self, screen, player, level, victory, mouse_pos, mouse_clicked):
        """Draw game over screen"""
        screen.fill(BLACK)
        
        # Title
        title = "Victory!" if victory else "Game Over"
        title_color = GREEN if victory else RED
        title_surface = self.font.render(title, True, title_color)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)
        
        # Stats
        if player:
            stats = [
                f"Final Level: {player.level}",
                f"Health: {player.health}/{player.max_health}",
                f"Damage: {player.damage}",
                f"Enemies Killed: {level.enemies_killed if level else 0}"
            ]
            
            for i, stat in enumerate(stats):
                stat_surface = self.small_font.render(stat, True, WHITE)
                stat_rect = stat_surface.get_rect(center=(SCREEN_WIDTH // 2, 220 + i * 30))
                screen.blit(stat_surface, stat_rect)
        
        # Buttons
        if victory:
            self.next_level_button.update(mouse_pos, mouse_clicked)
            self.next_level_button.draw(screen)
            next_clicked = self.next_level_button.clicked
        else:
            self.restart_button.update(mouse_pos, mouse_clicked)
            self.restart_button.draw(screen)
            next_clicked = self.restart_button.clicked
        
        self.menu_button.update(mouse_pos, mouse_clicked)
        self.menu_button.draw(screen)
        
        return next_clicked, self.menu_button.clicked
