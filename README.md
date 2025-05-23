# Simple Roguelike Game

A simple 2D roguelike game with a top-down view, featuring real-time combat with projectile-based attacks similar to Realm of the Mad God.

## Features

- Player character that can move in four directions
- Basic enemies with simple AI behavior
- Combat system where both player and enemies can shoot projectiles
- Simple procedurally generated levels
- Basic collision detection for walls and entities
- Health system for both player and enemies
- Simple pixel art graphics
- Save system to persist game progress between levels and game sessions

## Controls

- **Movement**: WASD or Arrow Keys
- **Shooting**: Left Mouse Button, Space Key (aim with mouse, holding the button fires continuously)

## Requirements

- Python 3.x
- Pygame

## Installation

1. Make sure you have Python installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py`

## Game Structure

- **main.py**: Entry point for the game
- **game.py**: Main game class to handle game loop and states
- **entities/**: Contains all game entities (player, enemies, projectiles)
- **level/**: Level generation and management
- **utils/**: Utility functions and constants
- **ui/**: User interface elements

## How to Play

1. Start the game by clicking the "New Game" button
2. Move around using WASD or arrow keys
3. Aim with your mouse and shoot with left mouse button or spacebar
4. Press U to open the upgrade menu when you have upgrade points
5. Press F11 or Alt+Enter to toggle fullscreen mode
6. Press ESC to exit fullscreen mode
7. Defeat all enemies to win the level
8. Avoid enemy projectiles to stay alive

## Credits

Created as a simple roguelike game project using Python and Pygame.
