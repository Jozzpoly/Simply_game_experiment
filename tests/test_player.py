import unittest
import pygame
import sys
import os

# Add the parent directory to the path so we can import the game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.player import Player
from utils.constants import *

class TestPlayer(unittest.TestCase):
    """Test cases for the Player class"""

    def setUp(self):
        """Set up the test environment"""
        # Initialize pygame
        pygame.init()

        # Create a player instance for testing
        self.player = Player(100, 100)

        # Mock the current_level_ref attribute to avoid None reference issues
        class MockLevel:
            def add_floating_text(self, text, x, y, color, duration=60):
                pass

            class MockAnimationManager:
                def add_damage_text(self, amount, x, y):
                    pass

            class MockVisualEffects:
                class MockScreenEffects:
                    def add_screen_shake(self, intensity, duration):
                        pass
                    def add_screen_flash(self, color, intensity, duration):
                        pass

                class MockParticleSystem:
                    def add_impact_effect(self, x, y, dx, dy, color, particle_count):
                        pass
                    def add_healing_effect(self, x, y, particle_count):
                        pass

                def __init__(self):
                    self.screen_effects = self.MockScreenEffects()
                    self.particle_system = self.MockParticleSystem()

            def __init__(self):
                self.animation_manager = self.MockAnimationManager()
                self.visual_effects = self.MockVisualEffects()

        self.player.current_level_ref = MockLevel()

    def tearDown(self):
        """Clean up after each test"""
        pygame.quit()

    def test_init(self):
        """Test player initialization"""
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.xp, 0)
        self.assertEqual(self.player.xp_to_next_level, 100)
        self.assertEqual(self.player.upgrade_points, 0)
        self.assertEqual(self.player.health, PLAYER_HEALTH)
        self.assertEqual(self.player.max_health, PLAYER_HEALTH)
        self.assertEqual(self.player.damage, PLAYER_DAMAGE)
        self.assertEqual(self.player.speed, PLAYER_SPEED)
        self.assertEqual(self.player.fire_rate, PLAYER_FIRE_RATE)

    def test_add_xp_no_level_up(self):
        """Test adding XP without leveling up"""
        # Add XP but not enough to level up
        result = self.player.add_xp(50)

        # Check that XP was added but no level up occurred
        self.assertEqual(self.player.xp, 50)
        self.assertEqual(self.player.level, 1)
        self.assertFalse(result)

    def test_add_xp_with_level_up(self):
        """Test adding XP with level up"""
        # Add enough XP to level up
        result = self.player.add_xp(100)

        # Check that level up occurred
        self.assertEqual(self.player.level, 2)
        self.assertEqual(self.player.xp, 0)  # XP should be reset
        self.assertEqual(self.player.xp_to_next_level, 150)  # Next level requires more XP
        self.assertEqual(self.player.upgrade_points, UPGRADE_POINTS_PER_LEVEL)
        self.assertTrue(result)

    def test_add_xp_multiple_levels(self):
        """Test adding enough XP to gain multiple levels"""
        # Add enough XP for multiple level ups
        # First level up requires 100 XP, second level up requires 150 XP
        # So we need at least 250 XP to reach level 3
        self.player.add_xp(100)  # Level up to level 2
        self.player.add_xp(150)  # Level up to level 3

        # Check that multiple level ups occurred
        self.assertEqual(self.player.level, 3)  # Should have gained 2 levels
        self.assertEqual(self.player.upgrade_points, 2 * UPGRADE_POINTS_PER_LEVEL)

    def test_level_up(self):
        """Test the level_up method directly"""
        initial_level = self.player.level
        initial_xp_to_next = self.player.xp_to_next_level

        # Call level_up directly
        self.player.level_up()

        # Check that level increased
        self.assertEqual(self.player.level, initial_level + 1)
        # Check that XP requirement increased
        self.assertEqual(self.player.xp_to_next_level, int(initial_xp_to_next * 1.5))
        # Check that upgrade points were awarded
        self.assertEqual(self.player.upgrade_points, UPGRADE_POINTS_PER_LEVEL)

    def test_upgrade_health(self):
        """Test upgrading health"""
        # Give the player upgrade points
        self.player.upgrade_points = 1
        initial_health = self.player.max_health

        # Upgrade health
        result = self.player.upgrade_health()

        # Check that health was upgraded
        self.assertTrue(result)
        self.assertTrue(self.player.max_health > initial_health)
        self.assertEqual(self.player.upgrade_points, 0)
        self.assertEqual(self.player.health_upgrades, 1)

    def test_upgrade_damage(self):
        """Test upgrading damage"""
        # Give the player upgrade points
        self.player.upgrade_points = 1
        initial_damage = self.player.damage

        # Upgrade damage
        result = self.player.upgrade_damage()

        # Check that damage was upgraded
        self.assertTrue(result)
        self.assertTrue(self.player.damage > initial_damage)
        self.assertEqual(self.player.upgrade_points, 0)
        self.assertEqual(self.player.damage_upgrades, 1)

    def test_upgrade_speed(self):
        """Test upgrading speed"""
        # Give the player upgrade points
        self.player.upgrade_points = 1
        initial_speed = self.player.speed

        # Upgrade speed
        result = self.player.upgrade_speed()

        # Check that speed was upgraded
        self.assertTrue(result)
        self.assertTrue(self.player.speed > initial_speed)
        self.assertEqual(self.player.upgrade_points, 0)
        self.assertEqual(self.player.speed_upgrades, 1)

    def test_upgrade_fire_rate(self):
        """Test upgrading fire rate"""
        # Give the player upgrade points
        self.player.upgrade_points = 1
        initial_fire_rate = self.player.fire_rate

        # Upgrade fire rate
        result = self.player.upgrade_fire_rate()

        # Check that fire rate was upgraded (lower is better)
        self.assertTrue(result)
        self.assertTrue(self.player.fire_rate < initial_fire_rate)
        self.assertEqual(self.player.upgrade_points, 0)
        self.assertEqual(self.player.fire_rate_upgrades, 1)

    def test_upgrade_without_points(self):
        """Test attempting to upgrade without upgrade points"""
        # Ensure player has no upgrade points
        self.player.upgrade_points = 0

        # Try to upgrade
        result = self.player.upgrade_health()

        # Check that upgrade failed
        self.assertFalse(result)
        self.assertEqual(self.player.health_upgrades, 0)

    def test_take_damage(self):
        """Test taking damage"""
        initial_health = self.player.health
        damage_amount = 10

        # Take damage
        result = self.player.take_damage(damage_amount)

        # Check that health was reduced
        self.assertEqual(self.player.health, initial_health - damage_amount)
        self.assertFalse(result)  # Player should not have died

        # Test fatal damage
        self.player.health = 5
        result = self.player.take_damage(10)
        self.assertTrue(result)  # Player should have died

if __name__ == '__main__':
    unittest.main()
