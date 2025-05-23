import random
from utils.constants import *

class Room:
    """A rectangular room in the dungeon"""

    def __init__(self, x, y, width, height, room_type="normal"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center_x = x + width // 2
        self.center_y = y + height // 2
        self.room_type = room_type  # normal, treasure, challenge, boss

    def intersects(self, other):
        """Check if this room intersects with another room"""
        # Add a buffer of 1 tile to avoid rooms being too close
        return (
            self.x - 1 <= other.x + other.width + 1 and
            self.x + self.width + 1 >= other.x - 1 and
            self.y - 1 <= other.y + other.height + 1 and
            self.y + self.height + 1 >= other.y - 1
        )

    def get_center(self):
        """Get the center coordinates of the room"""
        return (self.center_x, self.center_y)

    def get_random_position(self):
        """Get a random position inside the room"""
        x = random.randint(self.x + 1, self.x + self.width - 2)
        y = random.randint(self.y + 1, self.y + self.height - 2)
        return (x, y)

    def get_multiple_random_positions(self, count):
        """Get multiple random positions inside the room"""
        positions = []
        for _ in range(count):
            positions.append(self.get_random_position())
        return positions

class LevelGenerator:
    """Procedural level generator with improved level design"""

    def __init__(self, width=LEVEL_WIDTH, height=LEVEL_HEIGHT, current_level=1):
        self.width = width
        self.height = height
        self.current_level_number = current_level  # Renamed for clarity
        self.tiles = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = floor
        self.rooms = []
        self.enemy_positions = []
        self.item_positions = []
        self.player_start_pos = None

        # Scale difficulty based on current level number
        self.max_rooms = min(MAX_ROOMS + current_level, 50)  # Cap at 50 rooms for larger levels
        self.max_enemies = min(MAX_ENEMIES_BASE + (current_level * ENEMY_SCALING_FACTOR), MAX_ENEMIES_CAP)
        self.items_per_level = min(ITEMS_PER_LEVEL + current_level // 2, 10)  # Cap at 10 items

    def generate(self):
        """Generate a new level with improved design"""
        # Reset
        self.tiles = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []
        self.enemy_positions = []
        self.item_positions = []

        # Create rooms
        for _ in range(self.max_rooms):
            # Random room size with occasional larger rooms
            if random.random() < 0.2:  # 20% chance for a larger room
                w = random.randint(ROOM_MAX_SIZE - 2, ROOM_MAX_SIZE + 2)
                h = random.randint(ROOM_MAX_SIZE - 2, ROOM_MAX_SIZE + 2)
                room_type = random.choice(["treasure", "challenge"])
            else:
                w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                room_type = "normal"

            # Random room position
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            # Create new room
            new_room = Room(x, y, w, h, room_type)

            # Check if it intersects with existing rooms
            failed = False
            for other_room in self.rooms:
                if new_room.intersects(other_room):
                    failed = True
                    break

            if not failed:
                # Room is valid, carve it out
                self._create_room(new_room)

                # Connect to previous room
                if len(self.rooms) > 0:
                    prev_room = self.rooms[-1]
                    self._create_corridor(prev_room.get_center(), new_room.get_center())

                    # Occasionally add a second corridor to create loops (better level design)
                    if len(self.rooms) > 2 and random.random() < 0.3:  # 30% chance
                        random_prev_room = random.choice(self.rooms[:-1])  # Choose a random previous room
                        self._create_corridor(random_prev_room.get_center(), new_room.get_center())

                # Add room to list
                self.rooms.append(new_room)

        # Add a boss room if we're at level 5 or a multiple of 5
        if self.current_level_number % 5 == 0 and len(self.rooms) > 3:
            self._add_boss_room()

        # Set player start position to the center of the first room
        if self.rooms:
            self.player_start_pos = self.rooms[0].get_center()

            # Generate enemy positions based on room types
            self._generate_enemies()

            # Generate item positions based on room types
            self._generate_items()

        return self.tiles, self.player_start_pos, self.enemy_positions, self.item_positions

    def _add_boss_room(self):
        """Add a special boss room connected to the last room"""
        if not self.rooms:
            return

        last_room = self.rooms[-1]

        # Boss room is larger
        w = ROOM_MAX_SIZE + 4
        h = ROOM_MAX_SIZE + 4

        # Try to place the boss room in different directions from the last room
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for direction in directions:
            # Calculate position for boss room
            x = last_room.center_x + direction[0] * (last_room.width + w) // 2
            y = last_room.center_y + direction[1] * (last_room.height + h) // 2

            # Adjust to ensure room is within bounds
            x = max(1, min(x - w // 2, self.width - w - 1))
            y = max(1, min(y - h // 2, self.height - h - 1))

            boss_room = Room(x, y, w, h, "boss")

            # Check if it intersects with existing rooms
            failed = False
            for other_room in self.rooms:
                if boss_room.intersects(other_room):
                    failed = True
                    break

            if not failed:
                # Room is valid, carve it out
                self._create_room(boss_room)

                # Connect to the last room
                self._create_corridor(last_room.get_center(), boss_room.get_center())

                # Add room to list
                self.rooms.append(boss_room)
                return

    def _generate_enemies(self):
        """Generate enemy positions based on room types and current level"""
        enemy_count = 0

        for i, room in enumerate(self.rooms):
            # Skip the first room (player start)
            if i == 0:
                continue

            # Determine number of enemies based on room type and level
            if room.room_type == "normal":
                num_enemies = random.randint(1, 2 + self.current_level_number // 3)
            elif room.room_type == "challenge":
                num_enemies = random.randint(2, 3 + self.current_level_number // 2)
            elif room.room_type == "boss":
                # Boss room has one boss and some regular enemies
                # Add boss enemy marker (we'll handle this specially)
                self.enemy_positions.append(("boss", room.get_center()))
                enemy_count += 1

                # Add some regular enemies too
                num_enemies = random.randint(2, 3 + self.current_level_number // 3)
            else:  # treasure room
                num_enemies = random.randint(0, 1)  # Few or no enemies

            # Cap based on max enemies
            num_enemies = min(num_enemies, self.max_enemies - enemy_count)

            # Generate positions
            for _ in range(num_enemies):
                self.enemy_positions.append(room.get_random_position())
                enemy_count += 1

                # Stop if we've reached the maximum
                if enemy_count >= self.max_enemies:
                    return

    def _generate_items(self):
        """Generate item positions based on room types"""
        item_count = 0

        for i, room in enumerate(self.rooms):
            # Determine number of items based on room type
            if room.room_type == "normal":
                num_items = random.randint(0, 1)
            elif room.room_type == "treasure":
                num_items = random.randint(2, 3)  # More items in treasure rooms
            elif room.room_type == "challenge":
                num_items = 1  # One reward for challenge rooms
            elif room.room_type == "boss":
                num_items = random.randint(2, 3)  # Good rewards in boss rooms
            else:
                num_items = 0

            # Cap based on max items
            num_items = min(num_items, self.items_per_level - item_count)

            # Generate positions
            for _ in range(num_items):
                self.item_positions.append(room.get_random_position())
                item_count += 1

                # Stop if we've reached the maximum
                if item_count >= self.items_per_level:
                    return

    def _create_room(self, room):
        """Carve out a room in the tiles"""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if 0 <= y < self.height and 0 <= x < self.width:
                    self.tiles[y][x] = 0  # 0 = floor

    def _create_corridor(self, start, end):
        """Create a corridor between two points"""
        x1, y1 = start
        x2, y2 = end

        # Randomly decide whether to go horizontal first or vertical first
        if random.random() < 0.5:
            # Horizontal then vertical
            self._create_h_corridor(x1, x2, y1)
            self._create_v_corridor(y1, y2, x2)
        else:
            # Vertical then horizontal
            self._create_v_corridor(y1, y2, x1)
            self._create_h_corridor(x1, x2, y2)

    def _create_h_corridor(self, x1, x2, y):
        """Create a horizontal corridor with width of 2 tiles"""
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 <= y < self.height and 0 <= x < self.width:
                self.tiles[y][x] = 0  # 0 = floor
                # Make corridor 2 tiles wide by adding floor tiles above and below
                if y > 0:  # Avoid index errors at the top edge
                    self.tiles[y-1][x] = 0
                if y < self.height - 1:  # Avoid index errors at the bottom edge
                    self.tiles[y+1][x] = 0

    def _create_v_corridor(self, y1, y2, x):
        """Create a vertical corridor with width of 2 tiles"""
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 <= y < self.height and 0 <= x < self.width:
                self.tiles[y][x] = 0  # 0 = floor
                # Make corridor 2 tiles wide by adding floor tiles to the left and right
                if x > 0:  # Avoid index errors at the left edge
                    self.tiles[y][x-1] = 0
                if x < self.width - 1:  # Avoid index errors at the right edge
                    self.tiles[y][x+1] = 0
