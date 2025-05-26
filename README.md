# Simple Roguelike Game

A simple 2D roguelike game with a top-down view, featuring real-time combat with projectile-based attacks similar to Realm of the Mad God.

## Features

### Core Gameplay
- Player character that can move in four directions
- Basic enemies with simple AI behavior
- Combat system where both player and enemies can shoot projectiles
- Simple procedurally generated levels
- Basic collision detection for walls and entities
- Health system for both player and enemies
- Simple pixel art graphics
- Save system to persist game progress between levels and game sessions

### Enhanced Progression System
- **Skill Tree System**: Three specialization paths (Combat, Survival, Utility) with 15+ unique skills
- **Equipment System**: Weapons, armor, and accessories with rarity levels and upgrade mechanics
- **Achievement System**: 20+ achievements with rewards and progress tracking
- **Enhanced XP System**: Variable XP rewards based on enemy types and difficulty scaling
- **Visual Feedback**: Real-time XP progress bar and skill notifications

## Controls

- **Movement**: WASD or Arrow Keys
- **Shooting**: Left Mouse Button, Space Key (aim with mouse, holding the button fires continuously)

## Requirements

- Python 3.7 or higher
- Pygame 2.0 or higher

## Installation

### Quick Setup (Windows PowerShell)
```powershell
# Clone or download the project, then navigate to the directory
cd "path\to\simple_rouge_like"

# Set up development environment (installs dependencies)
.\dev_utils.ps1 setup

# Run the game
.\run_game.ps1
```

### Manual Installation
1. Make sure you have Python 3.7+ installed
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game using one of these methods:

   **Windows PowerShell (Recommended):**
   ```powershell
   .\run_game_simple.ps1
   ```

   **Command Line:**
   ```bash
   python main.py
   ```

### Development Setup
For development and testing, use the provided PowerShell scripts:

```powershell
# Check system requirements
.\dev_utils.ps1 check

# Install all dependencies
.\dev_utils.ps1 install

# Run all tests
.\run_tests_simple.ps1

# Run specific tests
.\run_tests_simple.ps1 -TestFile progression

# Clean up cache files
.\dev_utils.ps1 clean
```

## Game Structure

### Core Files
- **main.py**: Entry point for the game
- **game.py**: Main game class to handle game loop and states
- **run_game.ps1**: PowerShell script to run the game (Windows)
- **run_tests.ps1**: PowerShell script to run all tests (Windows)
- **dev_utils.ps1**: Development utilities script (Windows)

### Game Modules
- **entities/**: Contains all game entities (player, enemies, projectiles, items)
- **level/**: Level generation and management
- **progression/**: Character progression systems (skills, equipment, achievements)
- **ui/**: User interface elements and screens
- **utils/**: Utility functions, constants, and managers
- **tests/**: Comprehensive test suite for all systems

### Key Features
- **Skill Tree System** (`progression/skill_tree.py`): Three specialization paths with prerequisite-based progression
- **Equipment System** (`progression/equipment.py`): Weapons, armor, and accessories with rarity and upgrade mechanics
- **Achievement System** (`progression/achievements.py`): Goal tracking and reward system
- **Enhanced UI** (`ui/ui_elements.py`): Tabbed upgrade interface with visual skill tree
- **Save System** (`utils/save_manager.py`): Persistent progression data storage

## How to Play

### Basic Controls
1. **Start the game** by clicking the "New Game" button or "Continue" to resume
2. **Move around** using WASD or arrow keys
3. **Aim and shoot** with your mouse and left mouse button or spacebar
4. **Defeat all enemies** to complete the level
5. **Avoid enemy projectiles** to stay alive

### Progression System
6. **Gain XP** by defeating enemies (different enemy types give different XP amounts)
7. **Level up** to earn upgrade points and skill points
8. **Open upgrade menu** by pressing U or when you level up
9. **Navigate tabs** in the upgrade screen:
   - **Stats Tab**: Upgrade basic stats (health, damage, speed, fire rate)
   - **Skills Tab**: Learn and upgrade skills in three specialization trees
   - **Equipment Tab**: Manage weapons, armor, and accessories
   - **Achievements Tab**: View unlocked achievements and progress

### Advanced Features
10. **Collect equipment** dropped by enemies (15% chance, higher for bosses)
11. **Upgrade equipment** to improve their stat bonuses
12. **Unlock achievements** for various accomplishments
13. **Build your character** by choosing skills that complement your playstyle

### Keyboard Shortcuts
- **U**: Open upgrade menu (when points available)
- **F11 / Alt+Enter**: Toggle fullscreen mode
- **ESC**: Exit fullscreen mode or pause game
- **P**: Pause/unpause game
- **Space**: Alternative shooting key

## Troubleshooting

### PowerShell Execution Issues
If you encounter PowerShell execution policy errors:

```powershell
# Check current execution policy
Get-ExecutionPolicy

# Set execution policy for current user (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Common Issues
- **"Python is not recognized"**: Ensure Python is installed and added to your PATH
- **"Pygame not found"**: Install pygame with `pip install pygame`
- **PowerShell ampersand (&) errors**: Use the provided `.ps1` scripts instead of manual commands
- **Permission denied**: Run PowerShell as administrator or adjust execution policy

### Getting Help
- Run `.\run_game_simple.ps1 -Help` for game launcher options
- Run `.\run_tests_simple.ps1 -Help` for testing options
- Run `.\dev_utils.ps1 help` for development utilities
- Check `PROGRESSION_FEATURES.md` for detailed progression system documentation

## Credits

Created as a simple roguelike game project using Python and Pygame.

Enhanced with comprehensive character progression system including:
- Skill tree system with three specialization paths
- Equipment system with rarity levels and upgrades
- Achievement system with rewards and progress tracking
- Enhanced UI with tabbed interface and visual feedback
