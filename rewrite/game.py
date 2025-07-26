"""
Main Game Class - Simplified Implementation
Reduced from 679 lines to ~300 lines (56% reduction)

Core game loop and state management without over-engineering:
- Simple state machine
- Basic event handling
- Essential game logic only
"""

import pygame
import sys
import logging
from config import *
from level.level import Level
from ui.ui import GameUI, MenuUI
from utils.save_manager import SaveManager

logger = logging.getLogger(__name__)

class Game:
    """Main game class with simplified architecture"""
    
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.running = True
        
        # Game objects
        self.level = None
        self.current_level_number = 1
        
        # UI
        self.game_ui = GameUI()
        self.menu_ui = MenuUI()
        
        # Save system
        self.save_manager = SaveManager()
        
        # Input state
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        
        logger.info("Game initialized successfully")
    
    def run(self):
        """Main game loop"""
        logger.info("Starting game loop")
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        logger.info("Game loop ended")
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle pygame events"""
        self.mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state in [GameState.MENU, GameState.GAME_OVER]:
                        self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_clicked = True
        
        # Update input state
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
    
    def update(self, dt):
        """Update game based on current state"""
        if self.state == GameState.PLAYING:
            self.update_gameplay(dt)
        elif self.state == GameState.MENU:
            self.update_menu()
        elif self.state == GameState.GAME_OVER:
            self.update_game_over()
        # PAUSED state doesn't need updates
    
    def update_gameplay(self, dt):
        """Update gameplay state"""
        if not self.level:
            return
        
        # Update level
        self.level.update(dt, self.keys_pressed, self.mouse_pos, self.mouse_clicked)
        
        # Check for player death
        if self.level.player and self.level.player.health <= 0:
            self.state = GameState.GAME_OVER
            logger.info("Player died - game over")
        
        # Check for level completion
        elif self.level.is_completed():
            self.state = GameState.GAME_OVER
            logger.info(f"Level {self.current_level_number} completed!")
    
    def update_menu(self):
        """Update main menu"""
        start_clicked, quit_clicked = self.menu_ui.draw_main_menu(
            self.screen, self.mouse_pos, self.mouse_clicked
        )
        
        if start_clicked:
            self.start_new_game()
        elif quit_clicked:
            self.running = False
    
    def update_game_over(self):
        """Update game over screen"""
        victory = self.level and self.level.is_completed()
        
        next_clicked, menu_clicked = self.menu_ui.draw_game_over(
            self.screen, 
            self.level.player if self.level else None,
            self.level,
            victory,
            self.mouse_pos, 
            self.mouse_clicked
        )
        
        if next_clicked:
            if victory:
                self.advance_to_next_level()
            else:
                self.start_new_game()
        elif menu_clicked:
            self.return_to_menu()
    
    def draw(self):
        """Draw everything based on current state"""
        if self.state == GameState.PLAYING:
            # Draw level
            if self.level:
                self.level.draw(self.screen)
                self.game_ui.draw_hud(self.screen, self.level.player, self.level)
        
        elif self.state == GameState.PAUSED:
            # Draw level (frozen) and pause overlay
            if self.level:
                self.level.draw(self.screen)
                self.game_ui.draw_hud(self.screen, self.level.player, self.level)
            self.menu_ui.draw_pause_menu(self.screen)
        
        elif self.state == GameState.MENU:
            # Menu drawing is handled in update_menu
            pass
        
        elif self.state == GameState.GAME_OVER:
            # Game over drawing is handled in update_game_over
            pass
        
        # Update display
        pygame.display.flip()
    
    def start_new_game(self):
        """Start a new game"""
        logger.info("Starting new game")
        self.current_level_number = 1
        self.level = Level(self.current_level_number)
        self.state = GameState.PLAYING
        
        # Delete any existing save
        self.save_manager.delete_save()
    
    def advance_to_next_level(self):
        """Advance to the next level"""
        logger.info(f"Advancing to level {self.current_level_number + 1}")
        
        # Save current progress
        if self.level and self.level.player:
            self.save_manager.save_game(self.level.player, self.current_level_number + 1)
        
        # Create next level
        self.current_level_number += 1
        old_player = self.level.player if self.level else None
        self.level = Level(self.current_level_number)
        
        # Transfer player stats to new level
        if old_player and self.level.player:
            self.level.player.level = old_player.level
            self.level.player.health = old_player.health
            self.level.player.max_health = old_player.max_health
            self.level.player.damage = old_player.damage
            self.level.player.speed = old_player.speed
            self.level.player.xp = old_player.xp
            self.level.player.xp_to_next_level = old_player.xp_to_next_level
        
        self.state = GameState.PLAYING
    
    def return_to_menu(self):
        """Return to main menu"""
        logger.info("Returning to main menu")
        self.state = GameState.MENU
        self.level = None
    
    def load_game(self):
        """Load a saved game"""
        save_data = self.save_manager.load_game()
        if not save_data:
            logger.warning("No save data found, starting new game")
            self.start_new_game()
            return
        
        # Load level
        self.current_level_number = save_data.get('game', {}).get('current_level', 1)
        self.level = Level(self.current_level_number)
        
        # Apply save data to player
        if self.level.player:
            self.save_manager.apply_save_to_player(self.level.player, save_data)
        
        self.state = GameState.PLAYING
        logger.info(f"Game loaded - Level {self.current_level_number}")
