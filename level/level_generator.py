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

    def contains_point(self, x: int, y: int) -> bool:
        """Check if a point is within the room boundaries"""
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

class LevelGenerator:
    """Enhanced procedural level generator with progressive scaling and tactical enemy placement"""

    def __init__(self, width=LEVEL_WIDTH, height=LEVEL_HEIGHT, current_level=1):
        self.current_level_number = current_level

        # Progressive map scaling - larger maps for higher levels
        self.width = self._calculate_map_width(current_level, width)
        self.height = self._calculate_map_height(current_level, height)

        self.tiles = [[1 for _ in range(self.width)] for _ in range(self.height)]  # 1 = wall, 0 = floor
        self.rooms = []
        self.enemy_positions = []
        self.enemy_groups = []  # New: Track enemy groups for tactical placement
        self.item_positions = []
        self.player_start_pos = None

        # Enhanced scaling based on current level number
        self.max_rooms = min(MAX_ROOMS + current_level * 2, 80)  # More rooms for larger levels
        self.max_enemies = min(MAX_ENEMIES_BASE + (current_level * ENEMY_SCALING_FACTOR * 1.5), MAX_ENEMIES_CAP * 2)
        self.items_per_level = min(ITEMS_PER_LEVEL + current_level // 2, 15)  # More items for longer levels

        # Enemy density scaling - more enemies per room at higher levels
        self.enemy_density_multiplier = 1.0 + (current_level * 0.1)  # 10% more enemies per level
        self.min_group_size = max(2, current_level // 3)  # Larger groups at higher levels
        self.max_group_size = max(4, current_level // 2)  # Scale group size with level

    def _calculate_map_width(self, level: int, base_width: int) -> int:
        """Calculate map width based on level progression"""
        # Increase width every 3 levels, cap at 2x base size
        width_increase = (level - 1) // 3 * 10
        return min(base_width + width_increase, base_width * 2)

    def _calculate_map_height(self, level: int, base_height: int) -> int:
        """Calculate map height based on level progression"""
        # Increase height every 3 levels, cap at 2x base size
        height_increase = (level - 1) // 3 * 8
        return min(base_height + height_increase, base_height * 2)

    def generate(self):
        """Generate a new level with improved design"""
        # Reset
        self.tiles = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []
        self.enemy_positions = []
        self.item_positions = []

        # Create rooms with enhanced variety and scaling
        for room_index in range(self.max_rooms):
            # Enhanced room size calculation based on level and room type
            room_type, w, h = self._determine_room_properties(room_index)

            # Random room position with better distribution
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

    def _determine_room_properties(self, room_index: int) -> tuple[str, int, int]:
        """Determine room type and size based on level progression and room index"""
        # Higher levels have more variety and larger rooms
        level_factor = min(self.current_level_number / 10.0, 1.0)  # Cap at level 10

        # Room type probabilities change with level
        if room_index == 0:
            # First room is always normal (player start)
            room_type = "normal"
            size_modifier = 0
        elif random.random() < 0.25 + level_factor * 0.15:  # 25-40% chance for special rooms
            special_roll = random.random()
            if special_roll < 0.3:
                room_type = "treasure"
                size_modifier = 1
            elif special_roll < 0.6:
                room_type = "challenge"
                size_modifier = 2  # Challenge rooms are larger
            else:
                room_type = "arena"  # New room type for large battles
                size_modifier = 3
        else:
            room_type = "normal"
            size_modifier = random.choice([0, 0, 0, 1])  # Mostly normal size, occasionally larger

        # Calculate room dimensions with level scaling
        base_min = ROOM_MIN_SIZE + self.current_level_number // 5
        base_max = ROOM_MAX_SIZE + self.current_level_number // 3

        w = random.randint(base_min + size_modifier, base_max + size_modifier * 2)
        h = random.randint(base_min + size_modifier, base_max + size_modifier * 2)

        # Ensure rooms don't exceed map boundaries
        w = min(w, self.width // 4)
        h = min(h, self.height // 4)

        return room_type, w, h

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
        """Generate enemy positions with tactical clustering and density scaling"""
        enemy_count = 0
        self.enemy_groups = []

        for i, room in enumerate(self.rooms):
            # Skip the first room (player start)
            if i == 0:
                continue

            # Determine number of enemies based on room type, level, and density scaling
            base_enemies = self._calculate_room_enemy_count(room)
            scaled_enemies = int(base_enemies * self.enemy_density_multiplier)

            # Cap based on max enemies
            num_enemies = min(scaled_enemies, int(self.max_enemies) - enemy_count)

            if num_enemies <= 0:
                continue

            # Generate enemy groups for tactical placement
            groups = self._create_enemy_groups(room, num_enemies)

            for group in groups:
                self.enemy_groups.append(group)
                for enemy_data in group['enemies']:
                    self.enemy_positions.append(enemy_data)
                    enemy_count += 1

                # Stop if we've reached the maximum
                if enemy_count >= self.max_enemies:
                    return

    def _calculate_room_enemy_count(self, room) -> int:
        """Calculate base enemy count for a room based on type and level"""
        if room.room_type == "normal":
            return random.randint(1, 3 + self.current_level_number // 3)
        elif room.room_type == "challenge":
            return random.randint(3, 5 + self.current_level_number // 2)
        elif room.room_type == "arena":
            return random.randint(5, 8 + self.current_level_number // 2)
        elif room.room_type == "boss":
            # Boss room has one boss and several regular enemies
            return random.randint(3, 5 + self.current_level_number // 3)
        else:  # treasure room
            return random.randint(0, 2)  # Few enemies guarding treasure

    def _create_enemy_groups(self, room, total_enemies: int) -> list:
        """Create tactical enemy groups within a room"""
        groups = []
        remaining_enemies = total_enemies

        # Special handling for boss rooms
        if room.room_type == "boss":
            # Add boss enemy
            boss_group = {
                'type': 'boss_group',
                'formation': 'defensive',
                'enemies': [("boss", room.get_center())]
            }

            # Add supporting enemies around the boss
            support_count = min(remaining_enemies - 1, 4)
            if support_count > 0:
                support_positions = self._generate_formation_positions(
                    room, room.get_center(), support_count, 'defensive'
                )
                for pos in support_positions:
                    boss_group['enemies'].append(pos)

            groups.append(boss_group)
            remaining_enemies -= len(boss_group['enemies'])

        # Create regular enemy groups
        while remaining_enemies > 0:
            group_size = min(
                random.randint(self.min_group_size, self.max_group_size),
                remaining_enemies
            )

            if group_size <= 0:
                break

            # Choose formation type based on room and group size
            formation = self._choose_formation(room, group_size)

            # Generate group center position
            group_center = room.get_random_position()

            # Generate positions for this group
            group_positions = self._generate_formation_positions(
                room, group_center, group_size, formation
            )

            group = {
                'type': 'tactical_group',
                'formation': formation,
                'center': group_center,
                'enemies': group_positions
            }

            groups.append(group)
            remaining_enemies -= group_size

        return groups

    def _choose_formation(self, room, group_size: int) -> str:
        """Choose appropriate formation based on room type and group size"""
        if room.room_type == "challenge" or room.room_type == "arena":
            # More tactical formations in challenge rooms
            formations = ['line', 'wedge', 'circle', 'ambush']
        else:
            # Simpler formations in normal rooms
            formations = ['cluster', 'line', 'patrol']

        # Larger groups prefer more complex formations
        if group_size >= 4:
            formations.extend(['circle', 'wedge'])

        return random.choice(formations)

    def _generate_formation_positions(self, room, center, count: int, formation: str) -> list:
        """Generate enemy positions based on formation type"""
        positions = []
        center_x, center_y = center

        if formation == 'cluster':
            # Enemies clustered around center point
            for i in range(count):
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-30, 30)
                pos = (center_x + offset_x, center_y + offset_y)
                # Ensure position is within room bounds
                if room.contains_point(pos[0], pos[1]):
                    positions.append(pos)
                else:
                    positions.append(room.get_random_position())

        elif formation == 'line':
            # Enemies in a line formation
            spacing = 40
            start_x = center_x - (count - 1) * spacing // 2
            for i in range(count):
                pos = (start_x + i * spacing, center_y)
                if room.contains_point(pos[0], pos[1]):
                    positions.append(pos)
                else:
                    positions.append(room.get_random_position())

        elif formation == 'circle':
            # Enemies in a circle around center
            import math
            radius = 50
            for i in range(count):
                angle = (2 * math.pi * i) / count
                pos_x = center_x + radius * math.cos(angle)
                pos_y = center_y + radius * math.sin(angle)
                pos = (int(pos_x), int(pos_y))
                if room.contains_point(pos[0], pos[1]):
                    positions.append(pos)
                else:
                    positions.append(room.get_random_position())

        elif formation == 'wedge':
            # V-shaped formation
            for i in range(count):
                if i == 0:
                    # Leader at the front
                    positions.append((center_x, center_y - 20))
                else:
                    # Others form the wedge
                    side = 1 if i % 2 == 1 else -1
                    row = (i + 1) // 2
                    pos = (center_x + side * row * 30, center_y + row * 25)
                    if room.contains_point(pos[0], pos[1]):
                        positions.append(pos)
                    else:
                        positions.append(room.get_random_position())

        elif formation == 'defensive':
            # Defensive positions around a central point (for boss support)
            import math
            radius = 80
            for i in range(count):
                angle = (2 * math.pi * i) / count
                pos_x = center_x + radius * math.cos(angle)
                pos_y = center_y + radius * math.sin(angle)
                pos = (int(pos_x), int(pos_y))
                if room.contains_point(pos[0], pos[1]):
                    positions.append(pos)
                else:
                    positions.append(room.get_random_position())

        else:  # 'ambush', 'patrol', or fallback
            # Random positions within room
            for _ in range(count):
                positions.append(room.get_random_position())

        return positions

    def _generate_items(self):
        """Generate item positions based on room types"""
        item_count = 0

        for room in self.rooms:
            # Determine number of items based on room type
            if room.room_type == "normal":
                num_items = random.randint(0, 1)
            elif room.room_type == "treasure":
                num_items = random.randint(2, 3)  # More items in treasure rooms
            elif room.room_type == "challenge":
                num_items = 1  # One reward for challenge rooms
            elif room.room_type == "arena":
                num_items = random.randint(1, 2)  # Rewards for arena battles
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
