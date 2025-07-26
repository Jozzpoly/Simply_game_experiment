"""
Level Generator - Simplified Implementation
Reduced from 991 lines to ~200 lines (80% reduction)

Basic room-based procedural generation without complex biomes or themes.
Focus on playable, fun levels with simple algorithms.
"""

import random
import math
from config import *

class Room:
    """Simple room representation"""
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + width // 2
        self.center_y = y + height // 2
    
    def intersects(self, other):
        """Check if this room intersects with another room"""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

class LevelGenerator:
    """Simple level generator using room-based algorithm"""
    
    def __init__(self, level_number=1):
        self.level_number = level_number
        self.width = LEVEL_WIDTH
        self.height = LEVEL_HEIGHT
        self.rooms = []
        self.tiles = []
        
        # Initialize empty level (all walls)
        self.tiles = [[1 for _ in range(self.width)] for _ in range(self.height)]
    
    def generate(self):
        """Generate a complete level"""
        # Clear previous generation
        self.rooms = []
        self.tiles = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Generate rooms
        self.generate_rooms()
        
        # Connect rooms with corridors
        self.connect_rooms()
        
        # Place player in first room
        player_pos = self.get_player_spawn_position()
        
        # Place enemies in rooms
        enemy_positions = self.place_enemies()
        
        return self.tiles, player_pos, enemy_positions
    
    def generate_rooms(self):
        """Generate random rooms that don't overlap"""
        attempts = 0
        max_attempts = 100
        
        while len(self.rooms) < MAX_ROOMS and attempts < max_attempts:
            attempts += 1
            
            # Random room size and position
            room_width = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            room_height = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            
            # Ensure room fits in level with border
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            
            new_room = Room(x, y, room_width, room_height)
            
            # Check if room overlaps with existing rooms
            overlaps = False
            for existing_room in self.rooms:
                if new_room.intersects(existing_room):
                    overlaps = True
                    break
            
            if not overlaps:
                self.rooms.append(new_room)
                self.carve_room(new_room)
    
    def carve_room(self, room):
        """Carve out a room in the tile grid"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x] = 0  # Floor tile
    
    def connect_rooms(self):
        """Connect all rooms with corridors"""
        if len(self.rooms) < 2:
            return
        
        # Connect each room to the next one
        for i in range(len(self.rooms) - 1):
            room1 = self.rooms[i]
            room2 = self.rooms[i + 1]
            self.create_corridor(room1, room2)
        
        # Optionally add some extra connections for more interesting layouts
        if len(self.rooms) > 3:
            # Connect first and last room
            self.create_corridor(self.rooms[0], self.rooms[-1])
    
    def create_corridor(self, room1, room2):
        """Create a corridor between two rooms"""
        # Start from center of room1
        x1, y1 = room1.center_x, room1.center_y
        x2, y2 = room2.center_x, room2.center_y
        
        # Create L-shaped corridor
        if random.choice([True, False]):
            # Horizontal first, then vertical
            self.carve_horizontal_corridor(x1, x2, y1)
            self.carve_vertical_corridor(y1, y2, x2)
        else:
            # Vertical first, then horizontal
            self.carve_vertical_corridor(y1, y2, x1)
            self.carve_horizontal_corridor(x1, x2, y2)
    
    def carve_horizontal_corridor(self, x1, x2, y):
        """Carve a horizontal corridor"""
        start_x = min(x1, x2)
        end_x = max(x1, x2)
        
        for x in range(start_x, end_x + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = 0  # Floor tile
    
    def carve_vertical_corridor(self, y1, y2, x):
        """Carve a vertical corridor"""
        start_y = min(y1, y2)
        end_y = max(y1, y2)
        
        for y in range(start_y, end_y + 1):
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = 0  # Floor tile
    
    def get_player_spawn_position(self):
        """Get player spawn position (center of first room)"""
        if self.rooms:
            room = self.rooms[0]
            return (room.center_x * TILE_SIZE, room.center_y * TILE_SIZE)
        else:
            # Fallback to center of level
            return (self.width * TILE_SIZE // 2, self.height * TILE_SIZE // 2)
    
    def place_enemies(self):
        """Place enemies in rooms (excluding first room where player spawns)"""
        enemy_positions = []
        
        # Skip first room (player spawn)
        for room in self.rooms[1:]:
            # Number of enemies based on room size and level
            room_area = room.width * room.height
            base_enemies = random.randint(MIN_ENEMIES_PER_ROOM, MAX_ENEMIES_PER_ROOM)
            level_bonus = self.level_number // 3  # Extra enemies every 3 levels
            num_enemies = min(base_enemies + level_bonus, room_area // 4)
            
            # Place enemies randomly in room
            for _ in range(num_enemies):
                # Random position within room (avoid edges)
                enemy_x = random.randint(room.x + 1, room.x + room.width - 2)
                enemy_y = random.randint(room.y + 1, room.y + room.height - 2)
                
                # Convert to pixel coordinates
                pixel_x = enemy_x * TILE_SIZE + TILE_SIZE // 2
                pixel_y = enemy_y * TILE_SIZE + TILE_SIZE // 2
                
                enemy_positions.append((pixel_x, pixel_y))
        
        return enemy_positions
    
    def is_valid_position(self, x, y):
        """Check if a tile position is valid (floor, not wall)"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x] == 0  # Floor tile
        return False
