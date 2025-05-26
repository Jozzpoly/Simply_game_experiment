import json
import os
from utils.constants import *
from config import PLAYER_BASE_SPEED

class SaveManager:
    """Handles saving and loading game state with enhanced security"""

    def __init__(self, save_file="game_save.json"):
        """Initialize the save manager with the save file path"""
        self.save_file = save_file

        # Define required fields for validation
        self.required_fields = ["current_level", "score", "high_score"]

        # Define valid ranges for numeric fields
        self.valid_ranges = {
            "current_level": (1, 100),  # Level 1 to 100
            "score": (0, 1000000),      # 0 to 1,000,000
            "high_score": (0, 1000000), # 0 to 1,000,000
        }

        # Define valid ranges for player stats
        self.player_valid_ranges = {
            "health": (1, PLAYER_HEALTH * 10),
            "max_health": (PLAYER_HEALTH, PLAYER_HEALTH * 10),
            "damage": (PLAYER_DAMAGE, PLAYER_DAMAGE * 10),
            "speed": (1, PLAYER_BASE_SPEED * 5),
            "fire_rate": (100, PLAYER_FIRE_RATE * 2),
            "level": (1, 100),
            "xp": (0, 100000),
            "xp_to_next_level": (100, 1000000),
            "upgrade_points": (0, 100)
        }

        # Define required fields for progression data
        self.progression_fields = ["skill_tree", "equipment_manager", "achievement_manager", "stats"]

    def save_game(self, game_data):
        """
        Save game data to a file with validation

        Args:
            game_data (dict): Dictionary containing game state to save

        Returns:
            bool: True if save was successful, False otherwise
        """
        # Validate data before saving
        if not self._validate_game_data(game_data):
            print("Error: Invalid game data format")
            return False

        try:
            with open(self.save_file, 'w') as f:
                json.dump(game_data, f)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self):
        """
        Load game data from file with validation

        Returns:
            dict: Game data if load was successful, None otherwise
        """
        if not os.path.exists(self.save_file):
            return None

        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)

            # Validate and sanitize loaded data
            if not self._validate_game_data(data):
                print("Warning: Save file contains invalid data, using defaults")
                return self._create_default_save()

            return data
        except json.JSONDecodeError:
            print("Error: Save file is corrupted (invalid JSON)")
            return None
        except IOError as e:
            print(f"Error reading save file: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error loading game: {e}")
            return None

    def save_exists(self):
        """Check if a save file exists"""
        return os.path.exists(self.save_file)

    def delete_save(self):
        """Delete the save file if it exists"""
        if self.save_exists():
            try:
                os.remove(self.save_file)
                return True
            except Exception as e:
                print(f"Error deleting save file: {e}")
                return False
        return True  # No save to delete is still a success

    def _validate_game_data(self, data):
        """
        Validate game data structure and values

        Args:
            data (dict): Game data to validate

        Returns:
            bool: True if data is valid, False otherwise
        """
        # Check if data is a dictionary
        if not isinstance(data, dict):
            return False

        # Check for required fields
        for field in self.required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return False

        # Validate numeric fields
        for field, (min_val, max_val) in self.valid_ranges.items():
            if field in data:
                # Ensure field is numeric
                if not isinstance(data[field], (int, float)):
                    data[field] = min_val
                # Ensure field is within valid range
                data[field] = max(min_val, min(data[field], max_val))

        # Validate player data if present
        if "player_data" in data and isinstance(data["player_data"], dict):
            player_data = data["player_data"]

            for field, (min_val, max_val) in self.player_valid_ranges.items():
                if field in player_data:
                    # Ensure field is numeric
                    if not isinstance(player_data[field], (int, float)):
                        player_data[field] = min_val
                    # Ensure field is within valid range
                    player_data[field] = max(min_val, min(player_data[field], max_val))

            # Validate progression data if present
            if "progression_data" in player_data and isinstance(player_data["progression_data"], dict):
                progression_data = player_data["progression_data"]

                # Validate that progression data has expected structure
                for field in self.progression_fields:
                    if field not in progression_data:
                        print(f"Missing progression field: {field}")
                        # Don't fail validation, just warn - progression data is optional

                # Validate stats dictionary
                if "stats" in progression_data and isinstance(progression_data["stats"], dict):
                    stats = progression_data["stats"]
                    # Ensure all stat values are non-negative integers
                    for stat_name, value in stats.items():
                        if not isinstance(value, (int, float)) or value < 0:
                            stats[stat_name] = 0

        return True

    def _create_default_save(self):
        """
        Create a default save data structure

        Returns:
            dict: Default save data
        """
        return {
            "current_level": 1,
            "score": 0,
            "high_score": 0,
            "player_data": {
                "health": PLAYER_HEALTH,
                "max_health": PLAYER_HEALTH,
                "damage": PLAYER_DAMAGE,
                "speed": PLAYER_BASE_SPEED,
                "fire_rate": PLAYER_FIRE_RATE,
                "level": 1,
                "xp": 0,
                "xp_to_next_level": 100,
                "upgrade_points": 0
            }
        }
