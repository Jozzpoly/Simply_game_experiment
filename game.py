import pygame
import sys
import logging
from typing import Optional, Tuple, TYPE_CHECKING
from level.level import Level
from ui.ui_elements import GameOverScreen, StartScreen, UpgradeScreen, XPProgressBar, SkillNotification
from utils.constants import *
from utils.save_manager import SaveManager
from utils.audio_manager import AudioManager

# Import for type checking only to avoid circular imports
if TYPE_CHECKING:
    from entities.player import Player

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Game:
    """Main game class with improved features and type safety"""

    def __init__(self) -> None:
        """Initialize the game with proper error handling and type safety"""
        # Initialize pygame
        pygame.init()
        logger.info("Pygame initialized successfully")

        # Explicitly initialize font module
        if not pygame.font.get_init():
            pygame.font.init()
            logger.info("Pygame font module initialized")

        # Display settings
        self.is_fullscreen: bool = False
        self.windowed_size: Tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create screen
        self.screen: pygame.Surface = pygame.display.set_mode(self.windowed_size)
        pygame.display.set_caption(TITLE)

        # Clock for controlling frame rate
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Game state - using enum for type safety
        self.running: bool = True
        self.state: GameState = GameState.START
        self.paused: bool = False

        # Level (will be initialized after audio manager)
        self.level: Optional[Level] = None
        self.current_level: int = 1

        # UI screens
        self.start_screen: StartScreen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game_over_screen: GameOverScreen = GameOverScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.upgrade_screen: UpgradeScreen = UpgradeScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Enhanced UI elements - position XP bar below health bar
        self.xp_progress_bar: XPProgressBar = XPProgressBar(10, 35, 300, 25)
        self.skill_notifications: SkillNotification = SkillNotification(SCREEN_WIDTH - 300, 50, 280, 100)

        # Victory condition
        self.victory: bool = False

        # Score tracking
        self.score: int = 0
        self.high_score: int = 0

        # Continuous shooting
        self.continuous_shooting: bool = False
        self.last_auto_shot_time: int = 0

        # Player reference for upgrades
        self.player: Optional['Player'] = None

        # Save manager
        self.save_manager: SaveManager = SaveManager()

        # Audio manager with proper error handling
        self.audio_manager: AudioManager
        try:
            self.audio_manager = AudioManager()
            logger.info("Audio manager initialized successfully")
        except (ImportError, pygame.error) as e:
            logger.warning(f"Could not initialize audio manager: {e}")
            logger.info("Running game in silent mode...")
            # Import disabled audio manager as fallback
            from utils.audio_manager_disabled import AudioManager as DisabledAudioManager
            self.audio_manager = DisabledAudioManager()
        except Exception as e:
            logger.error(f"Unexpected error initializing audio: {e}")
            # Fallback to disabled audio manager
            from utils.audio_manager_disabled import AudioManager as DisabledAudioManager
            self.audio_manager = DisabledAudioManager()

        # Initialize level with audio manager
        self.level = Level(self.audio_manager)
        logger.info("Level initialized successfully")

        # Check for existing save and update start screen
        if self.save_manager.save_exists():
            self.start_screen.set_continue_available(True)
            logger.info("Existing save file found, continue option enabled")

    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode with proper error handling"""
        try:
            self.is_fullscreen = not self.is_fullscreen
            logger.info(f"Toggling fullscreen mode: {self.is_fullscreen}")

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

            # Initialize enhanced UI elements - position XP bar below health bar
            self.xp_progress_bar = XPProgressBar(10, 35, 300, 25)
            self.skill_notifications = SkillNotification(screen_width - 300, 50, 280, 100)

            # Update continue button availability if needed
            if self.save_manager.save_exists():
                self.start_screen.set_continue_available(True)

        except pygame.error as e:
            logger.error(f"Failed to toggle fullscreen: {e}")
            # Revert fullscreen state if toggle failed
            self.is_fullscreen = not self.is_fullscreen

    def toggle_pause(self) -> None:
        """Toggle pause state using GameState enum"""
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSE
            self.paused = True
            logger.info("Game paused")
            # Pause music
            if hasattr(self, 'audio_manager'):
                self.audio_manager.pause_music()
        elif self.state == GameState.PAUSE:
            self.state = GameState.PLAYING
            self.paused = False
            logger.info("Game resumed")
            # Resume music
            if hasattr(self, 'audio_manager'):
                self.audio_manager.resume_music()

    def run(self) -> None:
        """Main game loop with improved error handling and type safety"""
        logger.info("Starting main game loop")

        while self.running:
            try:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        logger.info("Quit event received")

                    # Handle mouse clicks
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            self._handle_left_click(event)

                    # Handle mouse button release
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:  # Left mouse button
                            # Stop continuous shooting
                            self.continuous_shooting = False

                    # Handle keyboard input
                    elif event.type == pygame.KEYDOWN:
                        self._handle_keydown(event)

                    elif event.type == pygame.KEYUP:
                        self._handle_keyup(event)

                # Update
                self.update()

                # Draw
                self.draw()

                # Cap the frame rate
                self.clock.tick(FPS)

            except Exception as e:
                logger.error(f"Error in main game loop: {e}")
                # Continue running but log the error
                continue

        # Clean up
        logger.info("Cleaning up and exiting")
        self.audio_manager.cleanup()
        pygame.quit()
        sys.exit()

    def _handle_left_click(self, event: pygame.event.Event) -> None:
        """Handle left mouse button clicks based on current game state"""
        if self.state == GameState.PLAYING:
            # Player shooting - start continuous shooting
            self.continuous_shooting = True
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.level:
                self.level.handle_player_shoot(mouse_x, mouse_y)
        elif self.state == GameState.START:
            # Check for play button click (new game)
            if self.start_screen.check_play(event):
                self.start_new_game()
            # Check for continue button click
            elif self.start_screen.check_continue(event):
                self.continue_game()
        elif self.state == GameState.GAME_OVER:
            # Check for restart button click
            if self.game_over_screen.check_restart(event):
                self.start_new_game()
            # Check for next level button click
            elif self.victory and self.game_over_screen.check_next_level(event):
                self.next_level()
        elif self.state == GameState.UPGRADE:
            # Handle upgrade button clicks
            if self.level and self.level.player:
                upgrade_result = self.upgrade_screen.handle_click(event, self.level.player)
                if upgrade_result == "done":
                    # Return to game after upgrades
                    self.state = GameState.PLAYING
                elif upgrade_result and upgrade_result.startswith("skill_"):
                    # Skill was upgraded
                    skill_name = upgrade_result[6:]  # Remove "skill_" prefix
                    self.skill_notifications.add_notification(f"Skill Upgraded: {skill_name}", BLUE)
                elif upgrade_result and upgrade_result.startswith("tab_"):
                    # Tab was switched - no action needed, just update display
                    pass
                elif upgrade_result == "inventory_full":
                    # Inventory is full, cannot equip new item
                    self.skill_notifications.add_notification("Inventory full! Cannot equip item.", RED)
                elif upgrade_result and upgrade_result.startswith("equipped_"):
                    # Item was equipped successfully
                    item_type = upgrade_result[9:]  # Remove "equipped_" prefix
                    self.skill_notifications.add_notification(f"{item_type.capitalize()} equipped!", GREEN)
                elif upgrade_result and upgrade_result.startswith("unequipped_"):
                    # Item was unequipped successfully
                    item_type = upgrade_result[11:]  # Remove "unequipped_" prefix
                    self.skill_notifications.add_notification(f"{item_type.capitalize()} unequipped!", YELLOW)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle keyboard key press events"""
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
            elif self.state == GameState.PLAYING:
                self.toggle_pause()
            elif self.state == GameState.PAUSE:
                self.toggle_pause()
        elif event.key == pygame.K_SPACE:
            if self.state == GameState.PLAYING:
                # Start continuous shooting with spacebar
                self.continuous_shooting = True
        elif event.key == pygame.K_u:
            if (self.state == GameState.PLAYING and self.level and
                self.level.player and self.level.player.upgrade_points > 0):
                # Open upgrade screen
                self.state = GameState.UPGRADE
                self.upgrade_screen.update_stats(self.level.player)
        elif event.key == pygame.K_p:
            # P key to pause/unpause
            if self.state == GameState.PLAYING:
                self.toggle_pause()
            elif self.state == GameState.PAUSE:
                self.toggle_pause()

    def _handle_keyup(self, event: pygame.event.Event) -> None:
        """Handle keyboard key release events"""
        if event.key == pygame.K_SPACE:
            # Stop continuous shooting
            self.continuous_shooting = False

    def update(self) -> None:
        """Update game state based on current GameState"""
        if self.state == GameState.PLAYING and not self.paused and self.level:
            # Handle continuous shooting
            if self.continuous_shooting and self.level.player:
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
            if self.level.player and self.level.player.health <= 0:
                self.state = GameState.GAME_OVER
                self.victory = False
                logger.info("Player died - game over")

            # Check for victory (all enemies defeated)
            if len(self.level.enemies) == 0:
                self.state = GameState.GAME_OVER
                self.victory = True
                # Add bonus score for completing the level
                self.score += LEVEL_COMPLETE_SCORE
                # Add XP for completing the level
                if self.level.player:
                    self.level.player.add_xp(XP_PER_LEVEL)
                # Save the game state when completing a level
                self.save_game()
                logger.info(f"Level {self.current_level} completed!")

            # Check if player leveled up and has upgrade points or skill points
            if (self.level.player and self.level.player_level_up and
                (self.level.player.upgrade_points > 0 or self.level.player.skill_tree.skill_points > 0)):
                self.state = GameState.UPGRADE
                self.upgrade_screen.update_stats(self.level.player)
                self.level.player_level_up = False  # Reset the flag

                # Add level up notification
                self.skill_notifications.add_notification(f"Level Up! Now Level {self.level.player.level}", YELLOW)

            # Update skill notifications
            self.skill_notifications.update()

            # Check for new achievements
            if (self.level.player and hasattr(self.level.player, 'achievement_manager')):
                recent_achievements = self.level.player.achievement_manager.recently_unlocked
                for achievement in recent_achievements:
                    self.skill_notifications.add_notification(f"Achievement: {achievement.name}", GREEN)
                # Clear recent achievements after showing notifications
                self.level.player.achievement_manager.clear_recent_notifications()

        elif self.state == GameState.START:
            # Update start screen
            mouse_pos = pygame.mouse.get_pos()
            self.start_screen.update(mouse_pos)

        elif self.state == GameState.GAME_OVER:
            # Update game over screen
            mouse_pos = pygame.mouse.get_pos()
            self.game_over_screen.update(mouse_pos)

        elif self.state == GameState.UPGRADE:
            # Update upgrade screen
            mouse_pos = pygame.mouse.get_pos()
            self.upgrade_screen.update(mouse_pos)

        elif self.state == GameState.PAUSE:
            # Don't update anything when paused
            pass

    def draw(self) -> None:
        """Draw the current game state based on GameState"""
        if self.state in (GameState.PLAYING, GameState.PAUSE):
            # Level handles its own drawing now
            if self.level:
                self.level.draw(self.screen, self.score, self.current_level)

                # Draw enhanced UI elements
                if self.level.player:
                    self.xp_progress_bar.draw(self.screen, self.level.player)
                    self.skill_notifications.draw(self.screen)

            # Draw pause overlay if paused
            if self.state == GameState.PAUSE:
                self._draw_pause_overlay()

        elif self.state == GameState.START:
            # Draw start screen
            self.start_screen.draw(self.screen)

        elif self.state == GameState.GAME_OVER:
            # Update high score if needed
            if self.score > self.high_score:
                self.high_score = self.score

            # Draw game over screen
            self.game_over_screen.draw(self.screen, self.victory, self.score, self.high_score, self.current_level)

        elif self.state == GameState.UPGRADE:
            # Draw upgrade screen
            self.upgrade_screen.draw(self.screen)

        # Update display
        pygame.display.flip()

    def _draw_pause_overlay(self) -> None:
        """Draw pause overlay with instructions"""
        # Create semi-transparent overlay
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(PAUSE_OVERLAY_ALPHA)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        # Draw pause text
        font = pygame.font.SysFont(None, PAUSE_TITLE_FONT_SIZE)
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(pause_text, pause_rect)

        # Draw instructions
        font_small = pygame.font.SysFont(None, PAUSE_INSTRUCTION_FONT_SIZE)
        instructions = [
            "Press P or ESC to resume",
            "Press F11 for fullscreen",
            "Press U for upgrades (if available)"
        ]

        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20 + i * 40))
            self.screen.blit(text, text_rect)

    def start_new_game(self) -> None:
        """Start a completely new game with proper error handling"""
        try:
            self.state = GameState.PLAYING
            self.current_level = 1
            if self.level:
                self.level.generate_level(self.current_level)
            self.victory = False
            self.score = 0
            self.continuous_shooting = False

            # Delete any existing save
            self.save_manager.delete_save()

            # Start background music
            self.audio_manager.play_music(BACKGROUND_MUSIC)
            logger.info("New game started successfully")

        except Exception as e:
            logger.error(f"Failed to start new game: {e}")
            # Fallback to start screen
            self.state = GameState.START

    def continue_game(self) -> None:
        """Continue from a saved game with proper error handling"""
        try:
            # Load saved game data
            saved_data = self.save_manager.load_game()

            if saved_data and self.level:
                self.state = GameState.PLAYING
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

                        # Load progression data if available
                        progression_data = player_data.get("progression_data", None)
                        if progression_data:
                            temp_player.load_progression_data(progression_data)

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
                logger.info(f"Game continued from level {self.current_level}")
            else:
                # If no save data found, start a new game
                logger.warning("No save data found, starting new game")
                self.start_new_game()

        except Exception as e:
            logger.error(f"Failed to continue game: {e}")
            # Fallback to new game
            self.start_new_game()

    def next_level(self) -> None:
        """Advance to the next level with proper error handling"""
        try:
            self.state = GameState.PLAYING
            self.current_level += 1

            # Keep the player object when generating the next level
            if self.level and self.level.player:
                self.level.generate_level(self.current_level, self.level.player)
            self.victory = False
            self.continuous_shooting = False

            # Save the game state
            self.save_game()
            logger.info(f"Advanced to level {self.current_level}")

        except Exception as e:
            logger.error(f"Failed to advance to next level: {e}")
            # Stay on current level
            self.state = GameState.PLAYING

    def save_game(self) -> None:
        """Save the current game state with player data and error handling"""
        try:
            if not self.level or not self.level.player:
                logger.warning("Cannot save game: no level or player data")
                return

            # Create player data dictionary with enhanced progression
            player_data = {
                "health": self.level.player.health,
                "max_health": self.level.player.max_health,
                "damage": self.level.player.damage,
                "speed": self.level.player.speed,
                "fire_rate": self.level.player.fire_rate,
                "level": self.level.player.level,
                "xp": self.level.player.xp,
                "xp_to_next_level": self.level.player.xp_to_next_level,
                "upgrade_points": self.level.player.upgrade_points,
                "progression_data": self.level.player.get_progression_data()
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
            logger.info("Game saved successfully")

        except Exception as e:
            logger.error(f"Failed to save game: {e}")
