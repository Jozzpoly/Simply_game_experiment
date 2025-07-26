"""
Save Manager - Simple Implementation
Basic save/load functionality without over-engineering.
Saves essential game state only.
"""

import json
import os
import logging
from config import SAVE_FILE

logger = logging.getLogger(__name__)

class SaveManager:
    """Simple save/load manager"""
    
    def __init__(self, save_file=SAVE_FILE):
        self.save_file = save_file
    
    def save_game(self, player, level_number):
        """Save current game state"""
        try:
            # Create save data
            save_data = {
                'player': {
                    'level': player.level,
                    'health': player.health,
                    'max_health': player.max_health,
                    'damage': player.damage,
                    'speed': player.speed,
                    'xp': player.xp,
                    'xp_to_next_level': player.xp_to_next_level
                },
                'game': {
                    'current_level': level_number
                }
            }
            
            # Write to file
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            logger.info(f"Game saved to {self.save_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save game: {e}")
            return False
    
    def load_game(self):
        """Load saved game state"""
        try:
            if not os.path.exists(self.save_file):
                logger.info("No save file found")
                return None
            
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            logger.info(f"Game loaded from {self.save_file}")
            return save_data
            
        except Exception as e:
            logger.error(f"Failed to load game: {e}")
            return None
    
    def delete_save(self):
        """Delete save file"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
                logger.info(f"Save file {self.save_file} deleted")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete save file: {e}")
            return False
    
    def has_save(self):
        """Check if save file exists"""
        return os.path.exists(self.save_file)
    
    def apply_save_to_player(self, player, save_data):
        """Apply saved data to player object"""
        try:
            player_data = save_data.get('player', {})
            
            player.level = player_data.get('level', 1)
            player.health = player_data.get('health', player.max_health)
            player.max_health = player_data.get('max_health', player.max_health)
            player.damage = player_data.get('damage', player.damage)
            player.speed = player_data.get('speed', player.speed)
            player.xp = player_data.get('xp', 0)
            player.xp_to_next_level = player_data.get('xp_to_next_level', 100)
            
            logger.info(f"Applied save data to player (Level {player.level})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply save data: {e}")
            return False
