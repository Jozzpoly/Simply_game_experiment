"""
Advanced Procedural Generation System for Phase 3

This module provides sophisticated level generation with:
- Architectural themes (cathedral, fortress, cavern, etc.)
- Narrative-driven layouts
- Dynamic difficulty zones
- Secret areas and hidden content
- Multi-layer generation approach
"""

import pygame
import random
import math
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from config import ADVANCED_GENERATION_CONFIG, BIOME_TYPES
from level.level_generator import LevelGenerator, Room
from utils.constants import *

logger = logging.getLogger(__name__)


@dataclass
class ArchitecturalTheme:
    """Represents an architectural theme for level generation"""
    name: str
    config: Dict[str, Any]

    def get_room_modifier(self, room_type: str) -> Dict[str, Any]:
        """Get room modifications for this theme"""
        return self.config.get('room_modifiers', {}).get(room_type, {})


@dataclass
class DifficultyZone:
    """Represents a zone with specific difficulty characteristics"""
    zone_type: str  # safe, challenge, elite, puzzle, ambush
    area: pygame.Rect
    difficulty_multiplier: float
    special_properties: Dict[str, Any]


@dataclass
class SecretArea:
    """Represents a hidden area in the level"""
    area_type: str  # hidden_room, secret_passage, treasure_vault
    location: Tuple[int, int]
    size: Tuple[int, int]
    discovery_method: str
    rewards: List[str]


class AdvancedLevelGenerator(LevelGenerator):
    """Enhanced level generator with advanced features"""

    def __init__(self, current_level: int = 1, biome_type: str = None):
        # Call parent constructor with proper parameters
        super().__init__(current_level=current_level)

        # Override biome type if specified
        if biome_type:
            self.biome_type = biome_type

        self.config = ADVANCED_GENERATION_CONFIG
        self.architectural_theme: Optional[ArchitecturalTheme] = None
        self.difficulty_zones: List[DifficultyZone] = []
        self.secret_areas: List[SecretArea] = []
        self.narrative_flow: List[str] = []

        # Enhanced generation layers
        self.generation_layers = [
            self._generate_structure,
            self._apply_architectural_theme,
            self._create_narrative_flow,
            self._place_difficulty_zones,
            self._generate_secret_areas,
            self._add_environmental_details,
            self._apply_final_polish
        ]

    def generate(self) -> Tuple:
        """Enhanced generation with multi-layer approach"""
        logger.info(f"Starting advanced generation for level {self.current_level_number}")

        # Choose architectural theme
        self._choose_architectural_theme()

        # Run generation layers
        for layer_func in self.generation_layers:
            try:
                layer_func()
            except Exception as e:
                logger.warning(f"Generation layer {layer_func.__name__} failed: {e}")

        # Call parent generation for basic structure
        result = super().generate()

        # Enhance the result with advanced features
        enhanced_result = self._enhance_generation_result(result)

        logger.info(f"Advanced generation complete: theme={self.architectural_theme.name if self.architectural_theme else 'none'}")
        return enhanced_result

    def _choose_architectural_theme(self) -> None:
        """Choose an architectural theme based on biome and level"""
        if not self.config.get('enabled', True):
            return

        themes_config = self.config.get('architectural_themes', {})

        # Map biomes to preferred themes
        biome_theme_preferences = {
            'dungeon': ['fortress', 'ruins'],
            'forest': ['ruins', 'temple'],
            'cave': ['cavern', 'ruins'],
            'volcanic': ['fortress', 'laboratory'],
            'crystal_cavern': ['cavern', 'temple'],
            'necropolis': ['ruins', 'temple'],
            'frozen_wastes': ['fortress', 'ruins'],
            'shadow_realm': ['temple', 'laboratory']
        }

        # Get preferred themes for current biome
        preferred_themes = biome_theme_preferences.get(self.biome_type, list(themes_config.keys()))

        # Add level-based preferences
        if self.current_level_number >= 10:
            preferred_themes.extend(['laboratory', 'temple'])
        if self.current_level_number >= 20:
            preferred_themes.extend(['cathedral'])

        # Choose theme
        if preferred_themes:
            theme_name = random.choice(preferred_themes)
            if theme_name in themes_config:
                self.architectural_theme = ArchitecturalTheme(theme_name, themes_config[theme_name])
                logger.info(f"Selected architectural theme: {theme_name}")

    def _generate_structure(self) -> None:
        """Generate basic structural layout"""
        # This is handled by the parent class
        pass

    def _apply_architectural_theme(self) -> None:
        """Apply architectural theme modifications to rooms"""
        if not self.architectural_theme:
            return

        theme_config = self.architectural_theme.config

        # Apply theme-specific modifications to rooms
        for room in self.rooms:
            self._apply_theme_to_room(room, theme_config)

    def _apply_theme_to_room(self, room: Room, theme_config: Dict[str, Any]) -> None:
        """Apply theme modifications to a specific room"""
        # Room height modifications
        height_multiplier = theme_config.get('room_height_multiplier', 1.0)
        if height_multiplier != 1.0:
            room.height = int(room.height * height_multiplier)

        # Corridor width modifications
        corridor_width = theme_config.get('corridor_width', 1)
        room.corridor_width = corridor_width

        # Add theme-specific features
        if theme_config.get('pillar_frequency', 0) > 0:
            self._add_pillars_to_room(room, theme_config['pillar_frequency'])

        if theme_config.get('irregular_walls', False):
            self._make_walls_irregular(room)

        # Add special room features
        room.theme_features = []

        if random.random() < theme_config.get('vault_ceiling_chance', 0):
            room.theme_features.append('vault_ceiling')

        if random.random() < theme_config.get('stained_glass_chance', 0):
            room.theme_features.append('stained_glass')

        if random.random() < theme_config.get('battlements_chance', 0):
            room.theme_features.append('battlements')

    def _add_pillars_to_room(self, room: Room, frequency: float) -> None:
        """Add pillars to a room based on frequency"""
        pillar_count = int(room.width * room.height * frequency / 100)

        for _ in range(pillar_count):
            # Find a good position for a pillar
            pillar_x = random.randint(room.x + 2, room.x + room.width - 3)
            pillar_y = random.randint(room.y + 2, room.y + room.height - 3)

            # Add pillar to tiles (represented as a special wall type)
            if 0 <= pillar_y < len(self.tiles) and 0 <= pillar_x < len(self.tiles[0]):
                self.tiles[pillar_y][pillar_x] = 2  # Pillar tile type

    def _make_walls_irregular(self, room: Room) -> None:
        """Make room walls irregular for natural cave feel"""
        # Add random variations to wall positions
        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                if (x == room.x or x == room.x + room.width - 1 or
                    y == room.y or y == room.y + room.height - 1):
                    # This is a wall position
                    if random.random() < 0.3:  # 30% chance to modify
                        # Randomly extend or contract the wall
                        if random.random() < 0.5:
                            # Extend wall inward
                            if x == room.x and x + 1 < room.x + room.width - 1:
                                self.tiles[y][x + 1] = 1
                            elif x == room.x + room.width - 1 and x - 1 > room.x:
                                self.tiles[y][x - 1] = 1
                            elif y == room.y and y + 1 < room.y + room.height - 1:
                                self.tiles[y + 1][x] = 1
                            elif y == room.y + room.height - 1 and y - 1 > room.y:
                                self.tiles[y - 1][x] = 1

    def _create_narrative_flow(self) -> None:
        """Create narrative-driven room connections"""
        narrative_config = self.config.get('narrative_layouts', {})

        if not narrative_config.get('enabled', True):
            return

        # Define narrative beats for the level
        self.narrative_flow = ['entrance', 'exploration', 'challenge', 'revelation', 'climax']

        # Assign narrative roles to rooms
        if len(self.rooms) >= len(self.narrative_flow):
            for i, narrative_beat in enumerate(self.narrative_flow):
                if i < len(self.rooms):
                    self.rooms[i].narrative_role = narrative_beat

        # Apply narrative-specific modifications
        if narrative_config.get('dramatic_reveals', 0) > 0:
            self._create_dramatic_reveals()

        if narrative_config.get('climactic_positioning', False):
            self._position_climactic_elements()

    def _create_dramatic_reveals(self) -> None:
        """Create dramatic reveal moments in the level"""
        reveal_chance = self.config.get('narrative_layouts', {}).get('dramatic_reveals', 0.2)

        for room in self.rooms:
            if random.random() < reveal_chance:
                room.dramatic_reveal = True
                # This room will have special visual treatment

    def _position_climactic_elements(self) -> None:
        """Position important elements for maximum dramatic impact"""
        if not self.rooms:
            return

        # Find the room farthest from start for climactic placement
        start_room = self.rooms[0]
        farthest_room = None
        max_distance = 0

        for room in self.rooms[1:]:
            distance = math.sqrt((room.center_x - start_room.center_x)**2 +
                               (room.center_y - start_room.center_y)**2)
            if distance > max_distance:
                max_distance = distance
                farthest_room = room

        if farthest_room:
            farthest_room.climactic_room = True

    def _place_difficulty_zones(self) -> None:
        """Place zones with different difficulty characteristics"""
        zones_config = self.config.get('dynamic_difficulty_zones', {})

        if not zones_config.get('enabled', True):
            return

        # Calculate zone placements
        total_area = self.width * self.height

        zone_types = {
            'safe_zones': zones_config.get('safe_zones', 0.1),
            'challenge_zones': zones_config.get('challenge_zones', 0.2),
            'elite_zones': zones_config.get('elite_zones', 0.05),
            'puzzle_zones': zones_config.get('puzzle_zones', 0.1),
            'ambush_zones': zones_config.get('ambush_zones', 0.15)
        }

        for zone_type, frequency in zone_types.items():
            zone_count = int(len(self.rooms) * frequency)

            for _ in range(zone_count):
                self._create_difficulty_zone(zone_type.replace('_zones', ''))

    def _create_difficulty_zone(self, zone_type: str) -> None:
        """Create a specific type of difficulty zone"""
        if not self.rooms:
            return

        # Choose a random room for this zone
        room = random.choice(self.rooms)

        # Define zone properties
        zone_properties = {
            'safe': {'difficulty_multiplier': 0.5, 'healing_rate': 2.0},
            'challenge': {'difficulty_multiplier': 1.5, 'enemy_density': 1.5},
            'elite': {'difficulty_multiplier': 2.0, 'elite_enemies': True},
            'puzzle': {'difficulty_multiplier': 1.0, 'puzzle_required': True},
            'ambush': {'difficulty_multiplier': 1.8, 'surprise_spawns': True}
        }

        properties = zone_properties.get(zone_type, {})

        zone = DifficultyZone(
            zone_type=zone_type,
            area=pygame.Rect(room.x * TILE_SIZE, room.y * TILE_SIZE,
                           room.width * TILE_SIZE, room.height * TILE_SIZE),
            difficulty_multiplier=properties.get('difficulty_multiplier', 1.0),
            special_properties=properties
        )

        self.difficulty_zones.append(zone)
        room.difficulty_zone = zone

    def _generate_secret_areas(self) -> None:
        """Generate hidden areas and secret content"""
        secrets_config = self.config.get('secret_areas', {})

        if not secrets_config.get('enabled', True):
            return

        # Generate different types of secret areas
        secret_types = {
            'hidden_room': secrets_config.get('hidden_room_chance', 0.15),
            'secret_passage': secrets_config.get('secret_passage_chance', 0.1),
            'treasure_vault': secrets_config.get('treasure_vault_chance', 0.05)
        }

        for secret_type, chance in secret_types.items():
            if random.random() < chance:
                self._create_secret_area(secret_type)

    def _create_secret_area(self, area_type: str) -> None:
        """Create a specific type of secret area"""
        if not self.rooms:
            return

        # Choose location near an existing room
        base_room = random.choice(self.rooms)

        # Determine secret area properties
        if area_type == 'hidden_room':
            size = (random.randint(3, 6), random.randint(3, 6))
            rewards = ['rare_equipment', 'bonus_xp']
        elif area_type == 'secret_passage':
            size = (random.randint(1, 2), random.randint(5, 10))
            rewards = ['shortcut', 'hidden_lore']
        elif area_type == 'treasure_vault':
            size = (random.randint(4, 8), random.randint(4, 8))
            rewards = ['legendary_equipment', 'meta_currency']
        else:
            return

        # Choose discovery method
        discovery_methods = self.config.get('secret_areas', {}).get('discovery_methods', ['hidden_switch'])
        discovery_method = random.choice(discovery_methods)

        # Find a position adjacent to the base room
        location = self._find_secret_area_location(base_room, size)

        if location:
            secret_area = SecretArea(
                area_type=area_type,
                location=location,
                size=size,
                discovery_method=discovery_method,
                rewards=rewards
            )

            self.secret_areas.append(secret_area)
            self._carve_secret_area(secret_area)

    def _find_secret_area_location(self, base_room: Room, size: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Find a suitable location for a secret area"""
        # Try positions around the base room
        attempts = 20

        for _ in range(attempts):
            # Choose a side of the room
            side = random.choice(['north', 'south', 'east', 'west'])

            if side == 'north':
                x = random.randint(base_room.x, base_room.x + base_room.width - size[0])
                y = base_room.y - size[1] - 1
            elif side == 'south':
                x = random.randint(base_room.x, base_room.x + base_room.width - size[0])
                y = base_room.y + base_room.height + 1
            elif side == 'east':
                x = base_room.x + base_room.width + 1
                y = random.randint(base_room.y, base_room.y + base_room.height - size[1])
            else:  # west
                x = base_room.x - size[0] - 1
                y = random.randint(base_room.y, base_room.y + base_room.height - size[1])

            # Check if location is valid
            if (0 <= x < self.width - size[0] and 0 <= y < self.height - size[1]):
                return (x, y)

        return None

    def _carve_secret_area(self, secret_area: SecretArea) -> None:
        """Carve out the secret area in the level tiles"""
        x, y = secret_area.location
        width, height = secret_area.size

        # Carve out the area
        for dy in range(height):
            for dx in range(width):
                if 0 <= y + dy < len(self.tiles) and 0 <= x + dx < len(self.tiles[0]):
                    self.tiles[y + dy][x + dx] = 0  # Floor tile

        # Add walls around the area
        for dy in range(-1, height + 1):
            for dx in range(-1, width + 1):
                tile_x, tile_y = x + dx, y + dy
                if (0 <= tile_y < len(self.tiles) and 0 <= tile_x < len(self.tiles[0]) and
                    (dx == -1 or dx == width or dy == -1 or dy == height)):
                    if self.tiles[tile_y][tile_x] != 0:  # Don't overwrite floors
                        self.tiles[tile_y][tile_x] = 1  # Wall tile

    def _add_environmental_details(self) -> None:
        """Add environmental details based on theme and biome"""
        if not self.architectural_theme:
            return

        # Add theme-specific environmental elements
        theme_name = self.architectural_theme.name

        if theme_name == 'cavern':
            self._add_cave_details()
        elif theme_name == 'temple':
            self._add_temple_details()
        elif theme_name == 'laboratory':
            self._add_laboratory_details()

    def _add_cave_details(self) -> None:
        """Add cave-specific environmental details"""
        # Add stalactites, underground rivers, etc.
        pass

    def _add_temple_details(self) -> None:
        """Add temple-specific environmental details"""
        # Add altars, ritual circles, etc.
        pass

    def _add_laboratory_details(self) -> None:
        """Add laboratory-specific environmental details"""
        # Add equipment, containment units, etc.
        pass

    def _apply_final_polish(self) -> None:
        """Apply final polish and quality improvements"""
        # Smooth rough edges, ensure connectivity, etc.
        self._ensure_all_areas_connected()
        self._smooth_wall_transitions()

    def _ensure_all_areas_connected(self) -> None:
        """Ensure all areas including secrets are properly connected"""
        # Implementation would use pathfinding to verify connectivity
        pass

    def _smooth_wall_transitions(self) -> None:
        """Smooth wall transitions for better visual appearance"""
        # Implementation would smooth jagged wall edges
        pass

    def _enhance_generation_result(self, base_result: Tuple) -> Tuple:
        """Enhance the base generation result with advanced features"""
        if len(base_result) != 9:
            return base_result

        (tiles, player_pos, enemy_positions, item_positions, stairs_positions,
         hazard_positions, special_feature_positions, exit_positions, biome_type) = base_result

        # Add advanced generation data
        advanced_data = {
            'architectural_theme': self.architectural_theme.name if self.architectural_theme else None,
            'difficulty_zones': [(zone.zone_type, zone.area, zone.difficulty_multiplier)
                                for zone in self.difficulty_zones],
            'secret_areas': [(area.area_type, area.location, area.size, area.discovery_method)
                           for area in self.secret_areas],
            'narrative_flow': self.narrative_flow
        }

        # Return enhanced result with additional data
        return (tiles, player_pos, enemy_positions, item_positions, stairs_positions,
                hazard_positions, special_feature_positions, exit_positions, biome_type, advanced_data)
