"""
Enhanced Terrain System with chunk-based generation, multiple biomes, and varied textures.
Supports dynamic loading/unloading of terrain chunks for improved performance.
"""

import pygame
import random
import math
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from config import *

# Try to import noise library, fallback to simple noise if not available
try:
    import noise
    NOISE_AVAILABLE = True
except ImportError:
    NOISE_AVAILABLE = False
    # Simple noise fallback
    def simple_noise(x, y, scale=1.0, octaves=1):
        """Simple pseudo-noise function as fallback"""
        import math
        return (math.sin(x * scale) * math.cos(y * scale) +
                math.sin(x * scale * 2) * math.cos(y * scale * 2) * 0.5) / 1.5

logger = logging.getLogger(__name__)

@dataclass
class TerrainChunk:
    """Represents a chunk of terrain tiles"""
    x: int  # Chunk coordinates
    y: int
    tiles: List[List[int]]  # 2D array of tile types
    decorations: List[Tuple[int, int, str]]  # (x, y, decoration_type)
    loaded: bool = False
    last_access_time: float = 0

    def get_world_bounds(self) -> Tuple[int, int, int, int]:
        """Get world coordinates of this chunk"""
        world_x = self.x * TERRAIN_CHUNK_SIZE
        world_y = self.y * TERRAIN_CHUNK_SIZE
        return (world_x, world_y,
                world_x + TERRAIN_CHUNK_SIZE,
                world_y + TERRAIN_CHUNK_SIZE)

class BiomeGenerator:
    """Generates different biome types with unique characteristics"""

    def __init__(self, seed: int = None):
        self.seed = seed or random.randint(0, 1000000)
        random.seed(self.seed)

    def get_biome_at_position(self, world_x: int, world_y: int) -> str:
        """Determine biome type at world position"""
        if not TERRAIN_BIOME_SYSTEM_ENABLED:
            return 'dungeon'

        # Use noise to determine biome
        if NOISE_AVAILABLE:
            biome_noise = noise.pnoise2(
                world_x * 0.01,
                world_y * 0.01,
                octaves=3,
                persistence=0.5,
                lacunarity=2.0,
                base=self.seed
            )
        else:
            biome_noise = simple_noise(world_x * 0.01, world_y * 0.01, scale=1.0)

        # Map noise value to biome
        if biome_noise < -0.3:
            return 'swamp'
        elif biome_noise < -0.1:
            return 'cave'
        elif biome_noise < 0.1:
            return 'dungeon'
        elif biome_noise < 0.3:
            return 'forest'
        else:
            return 'ruins'

    def generate_chunk_terrain(self, chunk_x: int, chunk_y: int,
                              existing_tiles: Dict[Tuple[int, int], int] = None) -> TerrainChunk:
        """Generate terrain for a specific chunk"""
        tiles = [[TERRAIN_TYPES['wall'] for _ in range(TERRAIN_CHUNK_SIZE)]
                for _ in range(TERRAIN_CHUNK_SIZE)]
        decorations = []

        world_x_start = chunk_x * TERRAIN_CHUNK_SIZE
        world_y_start = chunk_y * TERRAIN_CHUNK_SIZE

        # Determine dominant biome for this chunk
        center_x = world_x_start + TERRAIN_CHUNK_SIZE // 2
        center_y = world_y_start + TERRAIN_CHUNK_SIZE // 2
        biome = self.get_biome_at_position(center_x, center_y)
        biome_config = BIOME_TYPES.get(biome, BIOME_TYPES['dungeon'])

        # Generate base terrain using noise
        for local_y in range(TERRAIN_CHUNK_SIZE):
            for local_x in range(TERRAIN_CHUNK_SIZE):
                world_x = world_x_start + local_x
                world_y = world_y_start + local_y

                # Check if we have existing tile data
                if existing_tiles and (world_x, world_y) in existing_tiles:
                    tiles[local_y][local_x] = existing_tiles[(world_x, world_y)]
                    continue

                # Generate terrain using multiple noise layers
                if NOISE_AVAILABLE:
                    terrain_noise = noise.pnoise2(
                        world_x * TERRAIN_NOISE_SCALE,
                        world_y * TERRAIN_NOISE_SCALE,
                        octaves=4,
                        persistence=0.5,
                        lacunarity=2.0,
                        base=self.seed + 1000
                    )
                else:
                    terrain_noise = simple_noise(
                        world_x * TERRAIN_NOISE_SCALE,
                        world_y * TERRAIN_NOISE_SCALE,
                        scale=1.0
                    )

                # Determine tile type based on noise and biome
                if terrain_noise > 0.3:
                    tiles[local_y][local_x] = TERRAIN_TYPES['wall']
                elif terrain_noise > 0.1:
                    tiles[local_y][local_x] = TERRAIN_TYPES[biome_config['secondary']]
                else:
                    tiles[local_y][local_x] = TERRAIN_TYPES[biome_config['primary']]

                # Add decorations
                if (random.random() < TERRAIN_DECORATION_DENSITY and
                    tiles[local_y][local_x] != TERRAIN_TYPES['wall']):
                    decoration_type = biome_config['decoration']
                    decorations.append((local_x, local_y, decoration_type))

        # Apply smoothing
        for _ in range(TERRAIN_SMOOTHING_PASSES):
            tiles = self._smooth_terrain(tiles)

        # Add special features
        self._add_terrain_features(tiles, decorations, biome)

        chunk = TerrainChunk(chunk_x, chunk_y, tiles, decorations)
        chunk.loaded = True
        chunk.last_access_time = pygame.time.get_ticks()

        return chunk

    def _smooth_terrain(self, tiles: List[List[int]]) -> List[List[int]]:
        """Apply cellular automata smoothing to terrain"""
        new_tiles = [[tile for tile in row] for row in tiles]

        for y in range(1, len(tiles) - 1):
            for x in range(1, len(tiles[0]) - 1):
                wall_count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if tiles[y + dy][x + dx] == TERRAIN_TYPES['wall']:
                            wall_count += 1

                # Apply smoothing rules
                if wall_count >= 5:
                    new_tiles[y][x] = TERRAIN_TYPES['wall']
                elif wall_count <= 3:
                    # Keep original non-wall type
                    if tiles[y][x] != TERRAIN_TYPES['wall']:
                        new_tiles[y][x] = tiles[y][x]

        return new_tiles

    def _add_terrain_features(self, tiles: List[List[int]],
                            decorations: List[Tuple[int, int, str]],
                            biome: str) -> None:
        """Add special terrain features based on biome"""
        feature_count = int(TERRAIN_CHUNK_SIZE * TERRAIN_CHUNK_SIZE * TERRAIN_FEATURE_DENSITY)

        for _ in range(feature_count):
            x = random.randint(1, TERRAIN_CHUNK_SIZE - 2)
            y = random.randint(1, TERRAIN_CHUNK_SIZE - 2)

            if tiles[y][x] != TERRAIN_TYPES['wall']:
                if biome == 'forest' and random.random() < 0.3:
                    # Add tree clusters
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if (0 <= y + dy < TERRAIN_CHUNK_SIZE and
                                0 <= x + dx < TERRAIN_CHUNK_SIZE and
                                tiles[y + dy][x + dx] != TERRAIN_TYPES['wall']):
                                decorations.append((x + dx, y + dy, 'wood'))

                elif biome == 'swamp' and random.random() < 0.4:
                    # Add water patches
                    tiles[y][x] = TERRAIN_TYPES['water']

                elif biome == 'cave' and random.random() < 0.2:
                    # Add stone formations
                    tiles[y][x] = TERRAIN_TYPES['stone']


class TerrainManager:
    """Manages terrain chunks, loading/unloading, and rendering"""

    def __init__(self, seed: int = None):
        self.biome_generator = BiomeGenerator(seed)
        self.loaded_chunks: Dict[Tuple[int, int], TerrainChunk] = {}
        self.chunk_cache_size = TERRAIN_CACHE_SIZE
        self.tile_textures: Dict[int, pygame.Surface] = {}
        self.decoration_textures: Dict[str, pygame.Surface] = {}

        # Load textures
        self._load_textures()

        # Performance tracking
        self.chunks_loaded_this_frame = 0
        self.chunks_unloaded_this_frame = 0

    def _load_textures(self) -> None:
        """Load all terrain textures"""
        # Create basic textures if files don't exist
        tile_size = TILE_SIZE

        # Floor texture
        floor_surface = pygame.Surface((tile_size, tile_size))
        floor_surface.fill((139, 69, 19))  # Brown
        self.tile_textures[TERRAIN_TYPES['floor']] = floor_surface

        # Wall texture
        wall_surface = pygame.Surface((tile_size, tile_size))
        wall_surface.fill((105, 105, 105))  # Gray
        self.tile_textures[TERRAIN_TYPES['wall']] = wall_surface

        # Grass texture
        grass_surface = pygame.Surface((tile_size, tile_size))
        grass_surface.fill((34, 139, 34))  # Forest green
        self.tile_textures[TERRAIN_TYPES['grass']] = grass_surface

        # Dirt texture
        dirt_surface = pygame.Surface((tile_size, tile_size))
        dirt_surface.fill((160, 82, 45))  # Saddle brown
        self.tile_textures[TERRAIN_TYPES['dirt']] = dirt_surface

        # Stone texture
        stone_surface = pygame.Surface((tile_size, tile_size))
        stone_surface.fill((112, 128, 144))  # Slate gray
        self.tile_textures[TERRAIN_TYPES['stone']] = stone_surface

        # Water texture
        water_surface = pygame.Surface((tile_size, tile_size))
        water_surface.fill((0, 191, 255))  # Deep sky blue
        self.tile_textures[TERRAIN_TYPES['water']] = water_surface

        # Wood texture
        wood_surface = pygame.Surface((tile_size, tile_size))
        wood_surface.fill((101, 67, 33))  # Dark brown
        self.tile_textures[TERRAIN_TYPES['wood']] = wood_surface

        # Sand texture
        sand_surface = pygame.Surface((tile_size, tile_size))
        sand_surface.fill((238, 203, 173))  # Peach puff
        self.tile_textures[TERRAIN_TYPES['sand']] = sand_surface

        # Gravel texture
        gravel_surface = pygame.Surface((tile_size, tile_size))
        gravel_surface.fill((169, 169, 169))  # Dark gray
        self.tile_textures[TERRAIN_TYPES['gravel']] = gravel_surface

        # Decoration textures (smaller)
        decoration_size = tile_size // 2

        # Wood decoration (tree/log)
        wood_decoration = pygame.Surface((decoration_size, decoration_size))
        wood_decoration.fill((101, 67, 33))
        self.decoration_textures['wood'] = wood_decoration

        # Stone decoration (rock)
        stone_decoration = pygame.Surface((decoration_size, decoration_size))
        stone_decoration.fill((112, 128, 144))
        self.decoration_textures['stone'] = stone_decoration

        # Grass decoration (bush)
        grass_decoration = pygame.Surface((decoration_size, decoration_size))
        grass_decoration.fill((0, 100, 0))
        self.decoration_textures['grass'] = grass_decoration

    def update(self, camera_x: float, camera_y: float, screen_width: int, screen_height: int) -> None:
        """Update terrain system based on camera position"""
        if not DYNAMIC_TERRAIN_ENABLED:
            return

        self.chunks_loaded_this_frame = 0
        self.chunks_unloaded_this_frame = 0

        # Calculate required chunks based on camera position
        required_chunks = self._get_required_chunks(camera_x, camera_y, screen_width, screen_height)

        # Load missing chunks
        for chunk_pos in required_chunks:
            if chunk_pos not in self.loaded_chunks:
                self._load_chunk(chunk_pos[0], chunk_pos[1])

        # Unload distant chunks
        self._unload_distant_chunks(required_chunks)

        # Update access times for loaded chunks
        current_time = pygame.time.get_ticks()
        for chunk_pos in required_chunks:
            if chunk_pos in self.loaded_chunks:
                self.loaded_chunks[chunk_pos].last_access_time = current_time

    def _get_required_chunks(self, camera_x: float, camera_y: float,
                           screen_width: int, screen_height: int) -> Set[Tuple[int, int]]:
        """Calculate which chunks are needed for the current view"""
        required_chunks = set()

        # Calculate visible area in world coordinates
        left = camera_x
        right = camera_x + screen_width
        top = camera_y
        bottom = camera_y + screen_height

        # Add buffer for smooth loading
        buffer = TERRAIN_GENERATION_RADIUS * TILE_SIZE
        left -= buffer
        right += buffer
        top -= buffer
        bottom += buffer

        # Convert to chunk coordinates
        chunk_left = int(left // (TERRAIN_CHUNK_SIZE * TILE_SIZE))
        chunk_right = int(right // (TERRAIN_CHUNK_SIZE * TILE_SIZE)) + 1
        chunk_top = int(top // (TERRAIN_CHUNK_SIZE * TILE_SIZE))
        chunk_bottom = int(bottom // (TERRAIN_CHUNK_SIZE * TILE_SIZE)) + 1

        for chunk_y in range(chunk_top, chunk_bottom):
            for chunk_x in range(chunk_left, chunk_right):
                required_chunks.add((chunk_x, chunk_y))

        return required_chunks

    def _load_chunk(self, chunk_x: int, chunk_y: int) -> None:
        """Load a terrain chunk"""
        chunk = self.biome_generator.generate_chunk_terrain(chunk_x, chunk_y)
        self.loaded_chunks[(chunk_x, chunk_y)] = chunk
        self.chunks_loaded_this_frame += 1

        logger.debug(f"Loaded terrain chunk ({chunk_x}, {chunk_y})")

    def _unload_distant_chunks(self, required_chunks: Set[Tuple[int, int]]) -> None:
        """Unload chunks that are no longer needed"""
        if len(self.loaded_chunks) <= self.chunk_cache_size:
            return

        # Find chunks to unload (not in required set)
        chunks_to_unload = []
        for chunk_pos, chunk in self.loaded_chunks.items():
            if chunk_pos not in required_chunks:
                chunks_to_unload.append((chunk_pos, chunk.last_access_time))

        # Sort by last access time (oldest first)
        chunks_to_unload.sort(key=lambda x: x[1])

        # Unload oldest chunks until we're under the cache limit
        excess_count = len(self.loaded_chunks) - self.chunk_cache_size
        for i in range(min(excess_count, len(chunks_to_unload))):
            chunk_pos = chunks_to_unload[i][0]
            del self.loaded_chunks[chunk_pos]
            self.chunks_unloaded_this_frame += 1
            logger.debug(f"Unloaded terrain chunk {chunk_pos}")

    def get_tile_at_position(self, world_x: int, world_y: int) -> int:
        """Get tile type at world position"""
        chunk_x = world_x // (TERRAIN_CHUNK_SIZE * TILE_SIZE)
        chunk_y = world_y // (TERRAIN_CHUNK_SIZE * TILE_SIZE)

        chunk_pos = (chunk_x, chunk_y)
        if chunk_pos not in self.loaded_chunks:
            return TERRAIN_TYPES['wall']  # Default to wall for unloaded chunks

        chunk = self.loaded_chunks[chunk_pos]
        local_x = (world_x // TILE_SIZE) % TERRAIN_CHUNK_SIZE
        local_y = (world_y // TILE_SIZE) % TERRAIN_CHUNK_SIZE

        if 0 <= local_x < TERRAIN_CHUNK_SIZE and 0 <= local_y < TERRAIN_CHUNK_SIZE:
            return chunk.tiles[local_y][local_x]

        return TERRAIN_TYPES['wall']

    def render_visible_terrain(self, surface: pygame.Surface, camera_x: float, camera_y: float) -> None:
        """Render all visible terrain chunks"""
        for chunk in self.loaded_chunks.values():
            self._render_chunk(surface, chunk, camera_x, camera_y)

    def _render_chunk(self, surface: pygame.Surface, chunk: TerrainChunk,
                     camera_x: float, camera_y: float) -> None:
        """Render a single terrain chunk"""
        world_x_start = chunk.x * TERRAIN_CHUNK_SIZE * TILE_SIZE
        world_y_start = chunk.y * TERRAIN_CHUNK_SIZE * TILE_SIZE

        for local_y in range(TERRAIN_CHUNK_SIZE):
            for local_x in range(TERRAIN_CHUNK_SIZE):
                world_x = world_x_start + local_x * TILE_SIZE
                world_y = world_y_start + local_y * TILE_SIZE

                screen_x = world_x - camera_x
                screen_y = world_y - camera_y

                # Skip if outside screen bounds
                if (screen_x < -TILE_SIZE or screen_x > surface.get_width() or
                    screen_y < -TILE_SIZE or screen_y > surface.get_height()):
                    continue

                tile_type = chunk.tiles[local_y][local_x]
                if tile_type in self.tile_textures:
                    surface.blit(self.tile_textures[tile_type], (screen_x, screen_y))

        # Render decorations
        for local_x, local_y, decoration_type in chunk.decorations:
            world_x = world_x_start + local_x * TILE_SIZE
            world_y = world_y_start + local_y * TILE_SIZE

            screen_x = world_x - camera_x
            screen_y = world_y - camera_y

            if (screen_x >= -TILE_SIZE and screen_x <= surface.get_width() and
                screen_y >= -TILE_SIZE and screen_y <= surface.get_height()):
                if decoration_type in self.decoration_textures:
                    # Center decoration in tile
                    decoration_surface = self.decoration_textures[decoration_type]
                    decoration_x = screen_x + (TILE_SIZE - decoration_surface.get_width()) // 2
                    decoration_y = screen_y + (TILE_SIZE - decoration_surface.get_height()) // 2
                    surface.blit(decoration_surface, (decoration_x, decoration_y))

    def get_performance_stats(self) -> Dict[str, int]:
        """Get terrain system performance statistics"""
        return {
            "loaded_chunks": len(self.loaded_chunks),
            "chunks_loaded_this_frame": self.chunks_loaded_this_frame,
            "chunks_unloaded_this_frame": self.chunks_unloaded_this_frame,
            "cache_size": self.chunk_cache_size
        }
