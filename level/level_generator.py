import random
import logging
import math
from typing import List, Tuple, Optional, Dict, Any
from utils.constants import *
from config import *
from systems.environmental_system import EnvironmentalManager

# Configure logging
logger = logging.getLogger(__name__)

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
        self.stairs_positions = []  # New: Track stairs positions
        self.player_start_pos = None

        # Enhanced scaling based on current level number
        self.max_rooms = min(MAX_ROOMS + current_level * 2, 80)  # More rooms for larger levels
        # Fix: Ensure level 1 has enemies - use max() to guarantee minimum enemies
        self.max_enemies = max(MAX_ENEMIES_BASE, min(MAX_ENEMIES_BASE + (current_level * ENEMY_SCALING_FACTOR), MAX_ENEMIES_CAP * 2))
        self.items_per_level = min(ITEMS_PER_LEVEL + current_level // 2, 15)  # More items for longer levels

        # Enemy density scaling - more enemies per room at higher levels
        self.enemy_density_multiplier = 1.0 + (current_level * 0.1)  # 10% more enemies per level
        self.min_group_size = max(1, current_level // 3)  # Start with 1 enemy groups for level 1
        self.max_group_size = max(3, current_level // 2)  # Scale group size with level

        # Enhanced level features
        self.environmental_manager = EnvironmentalManager()
        self.biome_type = self._determine_level_biome()
        self.hazard_positions = []
        self.special_feature_positions = []
        self.exit_positions = []  # Multiple exits support

        # Level complexity scaling
        self.complexity_factor = 1.0 + (current_level * COMPLEXITY_SCALING_FACTOR)
        self.hazard_density = TERRAIN_HAZARD_DENSITY * (1.0 + current_level * HAZARD_SCALING_FACTOR)

    def _determine_level_biome(self) -> str:
        """Determine the biome type for this level"""
        # Choose biome based on level and weighted probabilities
        biome_choices = []
        weights = []

        for biome_name, biome_config in BIOME_TYPES.items():
            # Adjust spawn weight based on level
            level_factor = min(self.current_level_number / 10.0, 1.0)
            adjusted_weight = biome_config['spawn_weight'] * (0.5 + level_factor)

            biome_choices.append(biome_name)
            weights.append(adjusted_weight)

        return random.choices(biome_choices, weights=weights)[0]

    def _calculate_map_width(self, level: int, base_width: int) -> int:
        """Calculate map width based on level progression with enhanced scaling"""
        # Progressive scaling with level size factor
        scaling_factor = min(LEVEL_SIZE_SCALING_FACTOR ** ((level - 1) / 5), MAX_LEVEL_SIZE_MULTIPLIER)
        return int(base_width * scaling_factor)

    def _calculate_map_height(self, level: int, base_height: int) -> int:
        """Calculate map height based on level progression with enhanced scaling"""
        # Progressive scaling with level size factor
        scaling_factor = min(LEVEL_SIZE_SCALING_FACTOR ** ((level - 1) / 5), MAX_LEVEL_SIZE_MULTIPLIER)
        return int(base_height * scaling_factor)

    def generate(self):
        """Generate a new level with enhanced design and environmental features"""
        logger.info(f"Generating level {self.current_level_number} with biome: {self.biome_type}")

        # Reset all collections
        self.tiles = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.rooms = []
        self.enemy_positions = []
        self.item_positions = []
        self.stairs_positions = []
        self.hazard_positions = []
        self.special_feature_positions = []
        self.exit_positions = []
        self.environmental_manager.clear_all()

        # Generate rooms with enhanced variety and room types
        self._generate_enhanced_rooms()

        # Add a boss room if we're at level 5 or a multiple of 5
        if self.current_level_number % 5 == 0 and len(self.rooms) > 3:
            self._add_boss_room()

        # Set player start position to the center of the first room
        if self.rooms:
            self.player_start_pos = self.rooms[0].get_center()

            # Generate all level content
            self._generate_enemies()
            self._generate_items()
            self._generate_environmental_hazards()
            self._generate_special_features()
            self._generate_multiple_exits()

        logger.info(f"Level generated: {len(self.rooms)} rooms, {len(self.enemy_positions)} enemies, "
                   f"{len(self.hazard_positions)} hazards, {len(self.special_feature_positions)} features")

        return (self.tiles, self.player_start_pos, self.enemy_positions, self.item_positions,
                self.stairs_positions, self.hazard_positions, self.special_feature_positions,
                self.exit_positions, self.biome_type)

    def _generate_enhanced_rooms(self) -> None:
        """Generate rooms with enhanced variety using new room types"""
        for room_index in range(self.max_rooms):
            # Use enhanced room type selection
            room_type, w, h = self._determine_enhanced_room_properties(room_index)

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

    def _determine_enhanced_room_properties(self, room_index: int) -> Tuple[str, int, int]:
        """Enhanced room type selection using new room types and weights"""
        # Higher levels have more variety and larger rooms
        level_factor = min(self.current_level_number / 10.0, 1.0)

        # Room type selection using weights
        if room_index == 0:
            # First room is always standard (player start)
            room_type = "standard"
            size_modifier = 0
        else:
            # Choose room type based on weights
            room_type = random.choices(ROOM_TYPES, weights=ROOM_TYPE_WEIGHTS)[0]

            # Size modifier based on room type
            size_modifiers = {
                'standard': 0,
                'large': 2,
                'corridor': -2,
                'circular': 1,
                'irregular': 1,
                'treasure': 1,
                'boss': 4,
                'puzzle': 1
            }
            size_modifier = size_modifiers.get(room_type, 0)

        # Calculate room dimensions with level scaling
        base_min = ROOM_MIN_SIZE + self.current_level_number // 5
        base_max = ROOM_MAX_SIZE + self.current_level_number // 3

        w = random.randint(base_min + size_modifier, base_max + size_modifier * 2)
        h = random.randint(base_min + size_modifier, base_max + size_modifier * 2)

        # Special handling for specific room types
        if room_type == 'corridor':
            # Corridors are long and narrow
            if random.choice([True, False]):
                w = max(w, h * 3)  # Horizontal corridor
                h = max(3, h // 2)
            else:
                h = max(h, w * 3)  # Vertical corridor
                w = max(3, w // 2)
        elif room_type == 'circular':
            # Circular rooms are roughly square
            avg_size = (w + h) // 2
            w = h = avg_size

        # Ensure rooms don't exceed map boundaries
        w = min(w, self.width // 4)
        h = min(h, self.height // 4)

        return room_type, w, h

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

        logger.info(f"Generating enemies for level {self.current_level_number}: max_enemies={self.max_enemies}, rooms={len(self.rooms)}")

        for i, room in enumerate(self.rooms):
            # Skip the first room (player start)
            if i == 0:
                continue

            # Determine number of enemies based on room type, level, and density scaling
            base_enemies = self._calculate_room_enemy_count(room)
            scaled_enemies = int(base_enemies * self.enemy_density_multiplier)

            # Cap based on max enemies
            num_enemies = min(scaled_enemies, int(self.max_enemies) - enemy_count)

            logger.info(f"Room {i} ({room.room_type}): base={base_enemies}, scaled={scaled_enemies}, final={num_enemies}")

            if num_enemies <= 0:
                continue

            # Generate enemy groups for tactical placement
            groups = self._create_enemy_groups(room, num_enemies)

            for group in groups:
                self.enemy_groups.append(group)
                for enemy_data in group['enemies']:
                    # Phase 2: Add enemy type information to positions
                    if isinstance(enemy_data, tuple) and len(enemy_data) == 2:
                        # Convert (x, y) to (enemy_type, x, y) for Phase 2
                        enemy_type = self._choose_enemy_type_for_level()
                        enhanced_enemy_data = (enemy_type, enemy_data[0], enemy_data[1])
                        self.enemy_positions.append(enhanced_enemy_data)
                        logger.debug(f"Added enhanced enemy: {enemy_type} at ({enemy_data[0]}, {enemy_data[1]})")
                    else:
                        # Keep existing format for boss enemies
                        self.enemy_positions.append(enemy_data)
                        logger.debug(f"Added boss enemy: {enemy_data}")
                    enemy_count += 1

                # Stop if we've reached the maximum
                if enemy_count >= self.max_enemies:
                    logger.info(f"Reached max enemies limit: {enemy_count}")
                    return

        logger.info(f"Enemy generation complete: {enemy_count} enemies created")

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

    def _choose_enemy_type_for_level(self) -> str:
        """Choose appropriate enemy type based on current level and Phase 2 integration"""
        # Phase 2: Use enhanced enemy types for levels 3+
        if self.current_level_number >= 3:
            from config import ENHANCED_ENEMY_TYPES

            # Get available enemy types and their weights
            available_types = list(ENHANCED_ENEMY_TYPES.keys())
            weights = [ENHANCED_ENEMY_TYPES[t]['spawn_weight'] for t in available_types]

            # Adjust weights based on level (higher levels get more exotic enemies)
            level_factor = min(self.current_level_number / 10.0, 1.0)

            # Boost Phase 2 enemy weights for higher levels
            phase2_types = ['mage', 'assassin', 'necromancer', 'golem', 'archer', 'shaman', 'berserker_elite', 'shadow']
            adjusted_weights = []

            for i, enemy_type in enumerate(available_types):
                weight = weights[i]
                if enemy_type in phase2_types:
                    # Increase Phase 2 enemy spawn chance with level
                    weight *= (1.0 + level_factor * 2.0)
                adjusted_weights.append(weight)

            return random.choices(available_types, weights=adjusted_weights)[0]
        else:
            # Early levels use original enemy types
            return random.choice(["normal", "fast", "tank", "sniper", "berserker"])

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
        """Generate enemy positions based on formation type with collision detection"""
        positions = []
        center_x, center_y = center

        if formation == 'cluster':
            # Enemies clustered around center point
            for i in range(count):
                pos = self._find_safe_enemy_position_in_room(room, center_x, center_y, 30)
                if pos:
                    positions.append(pos)
                else:
                    # Fallback to random safe position
                    fallback_pos = self._find_random_safe_position_in_room(room)
                    if fallback_pos:
                        positions.append(fallback_pos)

        elif formation == 'line':
            # Enemies in a line formation
            spacing = 40
            start_x = center_x - (count - 1) * spacing // 2
            for i in range(count):
                target_x = start_x + i * spacing
                target_y = center_y
                pos = self._find_safe_enemy_position_in_room(room, target_x, target_y, 20)
                if pos:
                    positions.append(pos)
                else:
                    fallback_pos = self._find_random_safe_position_in_room(room)
                    if fallback_pos:
                        positions.append(fallback_pos)

        elif formation == 'circle':
            # Enemies in a circle around center
            import math
            radius = 50
            for i in range(count):
                angle = (2 * math.pi * i) / count
                target_x = center_x + radius * math.cos(angle)
                target_y = center_y + radius * math.sin(angle)
                pos = self._find_safe_enemy_position_in_room(room, int(target_x), int(target_y), 20)
                if pos:
                    positions.append(pos)
                else:
                    fallback_pos = self._find_random_safe_position_in_room(room)
                    if fallback_pos:
                        positions.append(fallback_pos)

        elif formation == 'wedge':
            # V-shaped formation
            for i in range(count):
                if i == 0:
                    # Leader at the front
                    pos = self._find_safe_enemy_position_in_room(room, center_x, center_y - 20, 15)
                    if pos:
                        positions.append(pos)
                    else:
                        fallback_pos = self._find_random_safe_position_in_room(room)
                        if fallback_pos:
                            positions.append(fallback_pos)
                else:
                    # Others form the wedge
                    side = 1 if i % 2 == 1 else -1
                    row = (i + 1) // 2
                    target_x = center_x + side * row * 30
                    target_y = center_y + row * 25
                    pos = self._find_safe_enemy_position_in_room(room, target_x, target_y, 15)
                    if pos:
                        positions.append(pos)
                    else:
                        fallback_pos = self._find_random_safe_position_in_room(room)
                        if fallback_pos:
                            positions.append(fallback_pos)

        elif formation == 'defensive':
            # Defensive positions around a central point (for boss support)
            import math
            radius = 80
            for i in range(count):
                angle = (2 * math.pi * i) / count
                target_x = center_x + radius * math.cos(angle)
                target_y = center_y + radius * math.sin(angle)
                pos = self._find_safe_enemy_position_in_room(room, int(target_x), int(target_y), 25)
                if pos:
                    positions.append(pos)
                else:
                    fallback_pos = self._find_random_safe_position_in_room(room)
                    if fallback_pos:
                        positions.append(fallback_pos)

        else:  # 'ambush', 'patrol', or fallback
            # Random safe positions within room
            for _ in range(count):
                pos = self._find_random_safe_position_in_room(room)
                if pos:
                    positions.append(pos)

        return positions

    def _generate_environmental_hazards(self) -> None:
        """Generate environmental hazards based on biome and level"""
        if not TERRAIN_ENVIRONMENTAL_HAZARDS_ENABLED:
            return

        biome_config = BIOME_TYPES.get(self.biome_type, BIOME_TYPES['dungeon'])
        available_hazards = biome_config.get('hazards', [])

        if not available_hazards:
            return

        # Calculate number of hazards based on level and density
        base_hazard_count = int(len(self.rooms) * self.hazard_density)
        hazard_count = max(1, base_hazard_count)

        for _ in range(hazard_count):
            # Choose random hazard type from biome
            hazard_type = random.choice(available_hazards)

            # Choose random room (skip first room - player start)
            if len(self.rooms) > 1:
                room = random.choice(self.rooms[1:])

                # Find safe position in room
                hazard_pos = self._find_random_safe_position_in_room(room)
                if hazard_pos:
                    # Convert to pixel coordinates
                    pixel_x = hazard_pos[0] * TILE_SIZE
                    pixel_y = hazard_pos[1] * TILE_SIZE

                    self.hazard_positions.append((hazard_type, pixel_x, pixel_y))
                    self.environmental_manager.add_hazard(hazard_type, pixel_x, pixel_y)

    def _generate_special_features(self) -> None:
        """Generate special environmental features based on biome and level"""
        biome_config = BIOME_TYPES.get(self.biome_type, BIOME_TYPES['dungeon'])
        available_features = biome_config.get('special_features', [])

        if not available_features:
            return

        # Calculate number of features based on level
        feature_count = max(1, int(len(self.rooms) * TERRAIN_SECRET_DENSITY * self.complexity_factor))

        for _ in range(feature_count):
            # Choose random feature type from biome
            feature_type = random.choice(available_features)

            # Choose random room
            if self.rooms:
                room = random.choice(self.rooms)

                # Find safe position in room
                feature_pos = self._find_random_safe_position_in_room(room)
                if feature_pos:
                    # Convert to pixel coordinates
                    pixel_x = feature_pos[0] * TILE_SIZE
                    pixel_y = feature_pos[1] * TILE_SIZE

                    self.special_feature_positions.append((feature_type, pixel_x, pixel_y))
                    self.environmental_manager.add_special_feature(feature_type, pixel_x, pixel_y)

    def _generate_multiple_exits(self) -> None:
        """Generate multiple exit options for enhanced level progression"""
        if not MULTIPLE_EXITS_ENABLED or not self.rooms:
            # Fallback to single stairs generation
            self._generate_stairs()
            return

        # Calculate number of exits based on level and configuration
        max_exits = min(MAX_EXITS_PER_LEVEL, max(1, len(self.rooms) // 5))
        num_exits = random.randint(1, max_exits)

        # Find suitable rooms for exits (prefer rooms far from start)
        start_room = self.rooms[0]
        candidate_rooms = []

        for room in self.rooms[1:]:  # Skip start room
            # Calculate distance from start room
            dx = room.center_x - start_room.center_x
            dy = room.center_y - start_room.center_y
            distance = (dx * dx + dy * dy) ** 0.5
            candidate_rooms.append((room, distance))

        # Sort by distance (farthest first)
        candidate_rooms.sort(key=lambda x: x[1], reverse=True)

        # Place exits in the farthest rooms
        exits_placed = 0
        for room, distance in candidate_rooms:
            if exits_placed >= num_exits:
                break

            # Choose exit type
            exit_type = random.choice(EXIT_TYPES)

            # Find safe position in room
            exit_pos = self._find_random_safe_position_in_room(room)
            if exit_pos:
                # Convert to pixel coordinates
                pixel_x = exit_pos[0] * TILE_SIZE
                pixel_y = exit_pos[1] * TILE_SIZE

                self.exit_positions.append((exit_type, pixel_x, pixel_y))

                # Also add to stairs positions for compatibility
                if exit_type == 'stairs_down':
                    self.stairs_positions.append(("down", (pixel_x, pixel_y)))

                exits_placed += 1

        # Ensure at least one exit exists
        if not self.exit_positions and not self.stairs_positions:
            self._generate_stairs()

    def _generate_stairs(self):
        """Generate stairs positions for level progression"""
        from config import STAIRS_ENABLED

        if not STAIRS_ENABLED:
            logger.info("Stairs generation disabled in config")
            return

        if not self.rooms:
            logger.warning("No rooms available for stairs generation")
            return

        logger.info(f"Generating stairs for level {self.current_level_number} with {len(self.rooms)} rooms")

        # Place down stairs in the last room (farthest from player start)
        if len(self.rooms) >= 2:
            # Find the room farthest from the first room (player start)
            start_room = self.rooms[0]
            farthest_room = None
            max_distance = 0

            for room in self.rooms[1:]:  # Skip first room
                # Calculate distance from start room center to this room center
                dx = room.center_x - start_room.center_x
                dy = room.center_y - start_room.center_y
                distance = (dx * dx + dy * dy) ** 0.5

                if distance > max_distance:
                    max_distance = distance
                    farthest_room = room

            if farthest_room:
                # Place down stairs in the center of the farthest room
                stairs_x = farthest_room.center_x * TILE_SIZE
                stairs_y = farthest_room.center_y * TILE_SIZE

                # Ensure stairs don't overlap with existing entities
                stairs_pos = self._find_safe_position_in_room(farthest_room, stairs_x, stairs_y)
                if stairs_pos:
                    self.stairs_positions.append(("down", stairs_pos))
                    logger.info(f"Stairs placed at {stairs_pos} in room at ({farthest_room.center_x}, {farthest_room.center_y})")
                else:
                    logger.warning("Could not find safe position for stairs")
            else:
                logger.warning("Could not find farthest room for stairs")
        elif len(self.rooms) == 1:
            # Single room - place stairs in a corner
            room = self.rooms[0]
            stairs_x = (room.x + room.width - 2) * TILE_SIZE
            stairs_y = (room.y + room.height - 2) * TILE_SIZE
            stairs_pos = self._find_safe_position_in_room(room, stairs_x, stairs_y)
            if stairs_pos:
                self.stairs_positions.append(("down", stairs_pos))
                logger.info(f"Single room stairs placed at {stairs_pos}")
            else:
                logger.warning("Could not place stairs in single room")

        logger.info(f"Stairs generation complete: {len(self.stairs_positions)} stairs created")

    def _find_safe_position_in_room(self, room, preferred_x: int, preferred_y: int) -> tuple:
        """Find a safe position in room that doesn't overlap with other entities"""
        # Convert pixel coordinates to tile coordinates
        preferred_tile_x = preferred_x // TILE_SIZE
        preferred_tile_y = preferred_y // TILE_SIZE

        # Check if preferred position is safe
        if self._is_position_safe(preferred_tile_x, preferred_tile_y, room):
            return (preferred_x, preferred_y)

        # Try nearby positions in a spiral pattern
        for radius in range(1, 5):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:  # Only check perimeter
                        test_x = preferred_tile_x + dx
                        test_y = preferred_tile_y + dy

                        if self._is_position_safe(test_x, test_y, room):
                            return (test_x * TILE_SIZE, test_y * TILE_SIZE)

        # Fallback to random position in room
        return (room.center_x * TILE_SIZE, room.center_y * TILE_SIZE)

    def _is_position_safe(self, tile_x: int, tile_y: int, room) -> bool:
        """Check if a tile position is safe for placing stairs"""
        # Check if position is within room bounds
        if not room.contains_point(tile_x, tile_y):
            return False

        # Check if position is a floor tile
        if (0 <= tile_x < self.width and 0 <= tile_y < self.height and
            self.tiles[tile_y][tile_x] != 0):  # 0 = floor
            return False

        # Check if position conflicts with existing entities
        pixel_x = tile_x * TILE_SIZE
        pixel_y = tile_y * TILE_SIZE

        # Check against enemy positions
        for enemy_data in self.enemy_positions:
            if isinstance(enemy_data, tuple):
                if len(enemy_data) == 3:
                    # Enhanced enemy format: (enemy_type, x, y)
                    enemy_x, enemy_y = enemy_data[1], enemy_data[2]
                elif len(enemy_data) == 2:
                    # Regular enemy format: (x, y)
                    enemy_x, enemy_y = enemy_data[0], enemy_data[1]
                else:
                    continue

                if abs(enemy_x - pixel_x) < TILE_SIZE and abs(enemy_y - pixel_y) < TILE_SIZE:
                    return False

        # Check against item positions
        for item_pos in self.item_positions:
            if isinstance(item_pos, tuple) and len(item_pos) >= 2:
                if abs(item_pos[0] - pixel_x) < TILE_SIZE and abs(item_pos[1] - pixel_y) < TILE_SIZE:
                    return False

        return True

    def _find_safe_enemy_position_in_room(self, room, center_x: int, center_y: int, max_offset: int) -> Optional[Tuple[int, int]]:
        """Find a safe position for enemy spawning near a center point (returns pixel coordinates)"""
        # Try positions in a spiral pattern around the center
        for radius in range(0, max_offset, 5):
            for angle_step in range(0, 360, 30):  # Check every 30 degrees
                import math
                angle = math.radians(angle_step)
                test_x = center_x + radius * math.cos(angle)
                test_y = center_y + radius * math.sin(angle)

                # Convert to tile coordinates for safety check
                tile_x = int(test_x // TILE_SIZE)
                tile_y = int(test_y // TILE_SIZE)

                if self._is_enemy_position_safe(tile_x, tile_y, room):
                    # Return pixel coordinates
                    return (int(test_x), int(test_y))

        return None

    def _find_random_safe_position_in_room(self, room) -> Optional[Tuple[int, int]]:
        """Find a random safe position in a room (returns pixel coordinates)"""
        max_attempts = 20
        for _ in range(max_attempts):
            # Get random position in room
            tile_x = random.randint(room.x + 1, room.x + room.width - 2)
            tile_y = random.randint(room.y + 1, room.y + room.height - 2)

            if self._is_safe_position_for_environmental(tile_x, tile_y, room):
                # Convert to pixel coordinates
                return (tile_x * TILE_SIZE, tile_y * TILE_SIZE)

        # Fallback to room center if no safe position found (in pixel coordinates)
        return (room.center_x * TILE_SIZE, room.center_y * TILE_SIZE)

    def _is_safe_position_for_environmental(self, tile_x: int, tile_y: int, room) -> bool:
        """Check if a tile position is safe for environmental elements"""
        # Check if position is within room bounds
        if not room.contains_point(tile_x, tile_y):
            return False

        # Check if position is a floor tile (not wall)
        if (0 <= tile_x < self.width and 0 <= tile_y < self.height and
            self.tiles[tile_y][tile_x] != 0):  # 0 = floor, 1 = wall
            return False

        # Check minimum distance from player start position
        if self.player_start_pos:
            # player_start_pos is in tile coordinates
            player_tile_x = self.player_start_pos[0]
            player_tile_y = self.player_start_pos[1]
            distance = ((tile_x - player_tile_x) ** 2 + (tile_y - player_tile_y) ** 2) ** 0.5
            if distance < 2:  # Minimum 2 tiles away from player start
                return False

        return True

    def _is_enemy_position_safe(self, tile_x: int, tile_y: int, room) -> bool:
        """Check if a tile position is safe for enemy spawning"""
        # Check if position is within room bounds
        if not room.contains_point(tile_x, tile_y):
            return False

        # Check if position is a floor tile (not wall)
        if (0 <= tile_x < self.width and 0 <= tile_y < self.height and
            self.tiles[tile_y][tile_x] != 0):  # 0 = floor, 1 = wall
            return False

        # Check minimum distance from player start position
        if self.player_start_pos:
            # player_start_pos is already in tile coordinates, not pixels
            player_tile_x = self.player_start_pos[0]
            player_tile_y = self.player_start_pos[1]
            distance = ((tile_x - player_tile_x) ** 2 + (tile_y - player_tile_y) ** 2) ** 0.5
            if distance < 3:  # Minimum 3 tiles away from player start
                return False

        return True

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
