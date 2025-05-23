import pygame
import sys
from level.level import Level
from ui.ui_elements import GameOverScreen, StartScreen, UpgradeScreen
from utils.constants import *
from utils.save_manager import SaveManager
from utils.audio_manager import AudioManager

class Game:
    """Main game class with improved features"""

    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Explicitly initialize font module
        if not pygame.font.get_init():
            pygame.font.init()

        # Display settings
        self.is_fullscreen = False
        self.windowed_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create screen
        self.screen = pygame.display.set_mode(self.windowed_size)
        pygame.display.set_caption(TITLE)

        # Clock for controlling frame rate
        self.clock = pygame.time.Clock()

        # Game state
        self.running = True
        self.state = "start"  # start, playing, game_over, upgrade, paused
        self.paused = False

        # Level (will be initialized after audio manager)
        self.level = None
        self.current_level = 1

        # UI screens
        self.start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game_over_screen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.upgrade_screen = UpgradeScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Victory condition
        self.victory = False

        # Score tracking
        self.score = 0
        self.high_score = 0

        # Continuous shooting
        self.continuous_shooting = False
        self.last_auto_shot_time = 0

        # Player reference for upgrades
        self.player = None

        # Save manager
        self.save_manager = SaveManager()

        # Audio manager
        self.audio_manager = AudioManager()

        # Initialize level with audio manager
        self.level = Level(self.audio_manager)

        # Check for existing save and update start screen
        if self.save_manager.save_exists():
            self.start_screen.set_continue_available(True)

    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        self.is_fullscreen = not self.is_fullscreen

        if self.is_fullscreen:
            # Switch to fullscreen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # Switch to windowed mode
            self.screen = pygame.display.set_mode(self.windowed_size)

        # Recreate UI screens with new screen dimensions
        screen_width, screen_height = self.screen.get_size()
        self.start_screen = StartScreen(screen_width, screen_height)
        self.game_over_screen = GameOverScreen(screen_width, screen_height)
        self.upgrade_screen = UpgradeScreen(screen_width, screen_height)

        # Update continue button availability if needed
        if self.save_manager.save_exists():
            self.start_screen.set_continue_available(True)

    def toggle_pause(self):
        """Toggle pause state"""
        if self.state == "playing":
            self.state = "paused"
            self.paused = True
            # Pause music
            if hasattr(self, 'audio_manager'):
                self.audio_manager.pause_music()
        elif self.state == "paused":
            self.state = "playing"
            self.paused = False
            # Resume music
            if hasattr(self, 'audio_manager'):
                self.audio_manager.resume_music()

    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle mouse clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.state == "playing":
                            # Player shooting - start continuous shooting
                            self.continuous_shooting = True
                            mouse_x, mouse_y = pygame.mouse.get_pos()
                            self.level.handle_player_shoot(mouse_x, mouse_y)
                        elif self.state == "start":
                            # Check for play button click (new game)
                            if self.start_screen.check_play(event):
                                self.start_new_game()
                            # Check for continue button click
                            elif self.start_screen.check_continue(event):
                                self.continue_game()
                        elif self.state == "game_over":
                            # Check for restart button click
                            if self.game_over_screen.check_restart(event):
                                self.start_new_game()
                            # Check for next level button click
                            elif self.victory and self.game_over_screen.check_next_level(event):
                                self.next_level()
                        elif self.state == "upgrade":
                            # Handle upgrade button clicks
                            upgrade_result = self.upgrade_screen.handle_click(event, self.level.player)
                            if upgrade_result == "done":
                                # Return to game after upgrades
                                self.state = "playing"

                # Handle mouse button release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        # Stop continuous shooting
                        self.continuous_shooting = False

                # Handle keyboard input
                elif event.type == pygame.KEYDOWN:
                    # Handle fullscreen toggle keys
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                        # Alt+Enter for fullscreen toggle
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        # ESC key - exit fullscreen if in fullscreen mode, or pause/unpause game
                        if self.is_fullscreen:
                            self.toggle_fullscreen()
                        elif self.state == "playing":
                            self.toggle_pause()
                        elif self.state == "paused":
                            self.toggle_pause()
                    elif event.key == pygame.K_SPACE:
                        if self.state == "playing":
                            # Start continuous shooting with spacebar
                            self.continuous_shooting = True
                    elif event.key == pygame.K_u:
                        if self.state == "playing" and self.level.player.upgrade_points > 0:
                            # Open upgrade screen
                            self.state = "upgrade"
                            self.upgrade_screen.update_stats(self.level.player)
                    elif event.key == pygame.K_p:
                        # P key to pause/unpause
                        if self.state == "playing":
                            self.toggle_pause()
                        elif self.state == "paused":
                            self.toggle_pause()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        # Stop continuous shooting
                        self.continuous_shooting = False

            # Update
            self.update()

            # Draw
            self.draw()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Clean up
        self.audio_manager.cleanup()
        pygame.quit()
        sys.exit()

    def update(self):
        """Update game state"""
        if self.state == "playing" and not self.paused:
            # Handle continuous shooting
            if self.continuous_shooting:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_auto_shot_time > self.level.player.fire_rate:
                    self.last_auto_shot_time = current_time
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.level.handle_player_shoot(mouse_x, mouse_y)

            # Update level with game reference for scoring and screen dimensions
            screen_width, screen_height = self.screen.get_size()
            self.level.update(self, screen_width, screen_height)

            # Store player reference for upgrades
            self.player = self.level.player

            # Check for player death
            if self.level.player.health <= 0:
                self.state = "game_over"
                self.victory = False

            # Check for victory (all enemies defeated)
            if len(self.level.enemies) == 0:
                self.state = "game_over"
                self.victory = True
                # Add bonus score for completing the level
                self.score += LEVEL_COMPLETE_SCORE
                # Add XP for completing the level
                self.level.player.add_xp(XP_PER_LEVEL)
                # Save the game state when completing a level
                self.save_game()

            # Check if player leveled up and has upgrade points
            if self.level.player_level_up and self.level.player.upgrade_points > 0:
                self.state = "upgrade"
                self.upgrade_screen.update_stats(self.level.player)
                self.level.player_level_up = False  # Reset the flag

        elif self.state == "start":
            # Update start screen
            mouse_pos = pygame.mouse.get_pos()
            self.start_screen.update(mouse_pos)

        elif self.state == "game_over":
            # Update game over screen
            mouse_pos = pygame.mouse.get_pos()
            self.game_over_screen.update(mouse_pos)

        elif self.state == "upgrade":
            # Update upgrade screen
            mouse_pos = pygame.mouse.get_pos()
            self.upgrade_screen.update(mouse_pos)

        elif self.state == "paused":
            # Don't update anything when paused
            pass

    def draw(self):
        """Draw the current game state"""
        if self.state == "playing" or self.state == "paused":
            # Level handles its own drawing now
            self.level.draw(self.screen, self.score, self.current_level)

            # Draw pause overlay if paused
            if self.state == "paused":
                self._draw_pause_overlay()

        elif self.state == "start":
            # Draw start screen
            self.start_screen.draw(self.screen)

        elif self.state == "game_over":
            # Update high score if needed
            if self.score > self.high_score:
                self.high_score = self.score

            # Draw game over screen
            self.game_over_screen.draw(self.screen, self.victory, self.score, self.high_score, self.current_level)

        elif self.state == "upgrade":
            # Draw upgrade screen
            self.upgrade_screen.draw(self.screen)

        # Update display
        pygame.display.flip()

    def _draw_pause_overlay(self):
        """Draw pause overlay"""
        # Create semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Draw pause text
        font = pygame.font.SysFont(None, 72)
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(pause_text, pause_rect)

        # Draw instructions
        font_small = pygame.font.SysFont(None, 36)
        instructions = [
            "Press P or ESC to resume",
            "Press F11 for fullscreen",
            "Press U for upgrades (if available)"
        ]

        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20 + i * 40))
            self.screen.blit(text, text_rect)

    def start_new_game(self):
        """Start a completely new game"""
        self.state = "playing"
        self.current_level = 1
        self.level.generate_level(self.current_level)
        self.victory = False
        self.score = 0
        self.continuous_shooting = False

        # Delete any existing save
        self.save_manager.delete_save()

        # Start background music
        self.audio_manager.play_music(BACKGROUND_MUSIC)

    def continue_game(self):
        """Continue from a saved game"""
        # Load saved game data
        saved_data = self.save_manager.load_game()

        if saved_data:
            self.state = "playing"
            self.current_level = saved_data.get("current_level", 1)
            self.score = saved_data.get("score", 0)
            self.high_score = saved_data.get("high_score", 0)

            # Load player data if available
            player_data = saved_data.get("player_data", None)

            # Generate the level for the current level
            if player_data:
                # Create a temporary player to load data into
                temp_player = self.level.player if self.level.player else None
                if temp_player:
                    # Load player stats
                    temp_player.health = player_data.get("health", PLAYER_HEALTH)
                    temp_player.max_health = player_data.get("max_health", PLAYER_HEALTH)
                    temp_player.damage = player_data.get("damage", PLAYER_DAMAGE)
                    temp_player.speed = player_data.get("speed", PLAYER_SPEED)
                    temp_player.fire_rate = player_data.get("fire_rate", PLAYER_FIRE_RATE)
                    temp_player.level = player_data.get("level", 1)  # This is the player level (integer)
                    temp_player.xp = player_data.get("xp", 0)
                    temp_player.xp_to_next_level = player_data.get("xp_to_next_level", 100)
                    temp_player.upgrade_points = player_data.get("upgrade_points", 0)

                    # Generate level with the loaded player
                    self.level.generate_level(self.current_level, temp_player)
                else:
                    # No existing player, generate new level
                    self.level.generate_level(self.current_level)
            else:
                # No player data, generate new level
                self.level.generate_level(self.current_level)

            self.victory = False
            self.continuous_shooting = False

            # Start background music
            self.audio_manager.play_music(BACKGROUND_MUSIC)
        else:
            # If no save data found, start a new game
            self.start_new_game()

    def next_level(self):
        """Advance to the next level"""
        self.state = "playing"
        self.current_level += 1

        # Keep the player object when generating the next level
        self.level.generate_level(self.current_level, self.level.player)
        self.victory = False
        self.continuous_shooting = False

        # Save the game state
        self.save_game()

    def save_game(self):
        """Save the current game state with player data"""
        # Create player data dictionary
        player_data = {
            "health": self.level.player.health,
            "max_health": self.level.player.max_health,
            "damage": self.level.player.damage,
            "speed": self.level.player.speed,
            "fire_rate": self.level.player.fire_rate,
            "level": self.level.player.level,
            "xp": self.level.player.xp,
            "xp_to_next_level": self.level.player.xp_to_next_level,
            "upgrade_points": self.level.player.upgrade_points
        }

        game_data = {
            "current_level": self.current_level,
            "score": self.score,
            "high_score": self.high_score,
            "player_data": player_data
        }

        # Save the game data
        self.save_manager.save_game(game_data)

        # Update start screen to show continue button
        self.start_screen.set_continue_available(True)
