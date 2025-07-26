"""
Essential Constants - Simplified Utility Module
Reduced from complex utility systems to basic mathematical and game constants.
"""

import math

# ============================================================================
# MATHEMATICAL CONSTANTS
# ============================================================================
PI = math.pi
TWO_PI = 2 * math.pi

# ============================================================================
# DIRECTION VECTORS
# ============================================================================
DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'UP_LEFT': (-1, -1),
    'UP_RIGHT': (1, -1),
    'DOWN_LEFT': (-1, 1),
    'DOWN_RIGHT': (1, 1)
}

# ============================================================================
# COLLISION LAYERS
# ============================================================================
COLLISION_WALL = 1
COLLISION_ENEMY = 2
COLLISION_PLAYER = 3
COLLISION_PROJECTILE = 4

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def distance(pos1, pos2):
    """Calculate distance between two points"""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return math.sqrt(dx * dx + dy * dy)

def normalize_vector(vector):
    """Normalize a 2D vector"""
    x, y = vector
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)

def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))

def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t
