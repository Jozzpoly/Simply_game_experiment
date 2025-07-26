#!/usr/bin/env python3
"""
Simple Roguelike Game - Clean Architecture Rewrite
Entry point for the simplified rouge-like game.

This rewrite focuses on core gameplay mechanics with minimal complexity:
- Basic player movement and combat
- Simple enemy AI
- Procedural level generation
- Essential progression system
- Clean, maintainable code under 3,500 lines total
"""

import pygame
import sys
import logging
from game import Game

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Initialize and run the game"""
    try:
        # Initialize pygame
        pygame.init()
        logger.info("Starting Simple Roguelike Game")
        
        # Create and run the game
        game = Game()
        game.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        logger.info("Game shutdown complete")

if __name__ == "__main__":
    main()
