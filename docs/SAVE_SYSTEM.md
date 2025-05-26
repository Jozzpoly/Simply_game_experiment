# Save System Documentation

## Overview
The save system allows players to save their progress between levels and game sessions. It preserves:
- Current level progression
- Accumulated score
- High score

## Implementation Details

### SaveManager Class
Located in `utils/save_manager.py`, this class handles all file operations for saving and loading game state.

#### Methods:
- `save_game(game_data)`: Saves the provided game data to a JSON file
- `load_game()`: Loads game data from the save file
- `save_exists()`: Checks if a save file exists
- `delete_save()`: Deletes the save file if it exists

### Game Class Changes
The Game class has been updated to include:

#### New Properties:
- `current_level`: Tracks the player's current level
- `save_manager`: Instance of SaveManager for handling save operations

#### New Methods:
- `start_new_game()`: Starts a completely new game (level 1, score 0)
- `continue_game()`: Loads a saved game and continues from that point
- `next_level()`: Advances to the next level after completing the current one
- `save_game()`: Saves the current game state

### UI Changes

#### StartScreen:
- Added "Continue Game" button that appears when a save file exists
- "Start Game" renamed to "New Game" for clarity

#### GameOverScreen:
- Added "Next Level" button that appears when a level is completed
- Victory message changed to "Level Complete!" instead of "Victory!"
- Added display of current level number

### Save File Format
The save file is stored as JSON with the following structure:
```json
{
  "current_level": 2,
  "score": 750,
  "high_score": 1500
}
```

## When Saves Occur
The game automatically saves:
1. When a player completes a level
2. When a player advances to the next level

## How to Use

### As a Player:
- **New Game**: Starts a fresh game from level 1
- **Continue Game**: Resumes from your last saved point
- **Next Level**: After completing a level, advances to the next level
- **Restart Game**: Starts a new game from level 1, discarding progress

### For Developers:
To save additional data in the future:
1. Add the new data to the `game_data` dictionary in the `save_game()` method
2. Update the `continue_game()` method to load the new data
3. Ensure any new game elements properly use the loaded data

## Error Handling
The save system includes error handling for:
- File not found (when no save exists)
- File read/write errors
- Invalid JSON data

If errors occur during loading, the game will default to starting a new game.
