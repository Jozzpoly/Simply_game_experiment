import pygame
import random
import math
from typing import List, Tuple, Optional
from utils.constants import *

class Particle:
    """Individual particle for visual effects"""

    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float,
                 color: Tuple[int, int, int], size: int = 2, lifetime: int = 60,
                 gravity: float = 0.0, fade: bool = True):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.gravity = gravity
        self.fade = fade
        self.alpha = 255

    def update(self) -> bool:
        """Update particle position and properties. Returns False if particle should be removed."""
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Apply gravity
        self.velocity_y += self.gravity

        # Update lifetime
        self.lifetime -= 1

        # Update alpha for fading effect
        if self.fade:
            self.alpha = int(255 * (self.lifetime / self.max_lifetime))
            self.alpha = max(0, min(255, self.alpha))

        return self.lifetime > 0

    def draw(self, surface: pygame.Surface, camera_offset_x: int = 0, camera_offset_y: int = 0):
        """Draw the particle"""
        if self.alpha <= 0:
            return

        screen_x = int(self.x - camera_offset_x)
        screen_y = int(self.y - camera_offset_y)

        # Create a surface with alpha for the particle
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        # Draw the particle with proper alpha handling
        # Ensure color is a valid RGB tuple
        if isinstance(self.color, (list, tuple)) and len(self.color) >= 3:
            color = (int(self.color[0]), int(self.color[1]), int(self.color[2]))
        else:
            color = (255, 255, 255)  # Default to white if invalid color

        pygame.draw.circle(particle_surface, color, (self.size, self.size), self.size)
        particle_surface.set_alpha(self.alpha)

        surface.blit(particle_surface, (screen_x - self.size, screen_y - self.size))

class ParticleSystem:
    """Manages multiple particles for various visual effects"""

    def __init__(self):
        self.particles: List[Particle] = []

    def add_particle(self, particle: Particle):
        """Add a single particle to the system"""
        self.particles.append(particle)

    def add_explosion(self, x: float, y: float, color: Tuple[int, int, int] = ORANGE,
                     particle_count: int = 15, intensity: float = 5.0):
        """Create an explosion effect at the given position"""
        for _ in range(particle_count):
            # Random direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, intensity)

            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed

            # Vary particle properties with clamped values
            particle_color = (
                max(0, min(255, color[0] + random.randint(-30, 30))),
                max(0, min(255, color[1] + random.randint(-30, 30))),
                max(0, min(255, color[2] + random.randint(-30, 30)))
            )

            size = random.randint(2, 4)
            lifetime = random.randint(30, 60)

            particle = Particle(x, y, velocity_x, velocity_y, particle_color,
                              size, lifetime, gravity=0.1, fade=True)
            self.add_particle(particle)

    def add_impact_effect(self, x: float, y: float, direction_x: float, direction_y: float,
                         color: Tuple[int, int, int] = WHITE, particle_count: int = 8):
        """Create an impact effect with particles flying in a specific direction"""
        for _ in range(particle_count):
            # Create particles that fly away from the impact point
            spread = 0.5  # How much the particles spread
            velocity_x = direction_x * random.uniform(2, 6) + random.uniform(-spread, spread)
            velocity_y = direction_y * random.uniform(2, 6) + random.uniform(-spread, spread)

            particle_color = (
                max(0, min(255, color[0] + random.randint(-20, 20))),
                max(0, min(255, color[1] + random.randint(-20, 20))),
                max(0, min(255, color[2] + random.randint(-20, 20)))
            )

            size = random.randint(1, 3)
            lifetime = random.randint(20, 40)

            particle = Particle(x, y, velocity_x, velocity_y, particle_color,
                              size, lifetime, gravity=0.05, fade=True)
            self.add_particle(particle)

    def add_healing_effect(self, x: float, y: float, particle_count: int = 10):
        """Create a healing effect with green particles floating upward"""
        for _ in range(particle_count):
            offset_x = random.uniform(-10, 10)
            offset_y = random.uniform(-5, 5)

            velocity_x = random.uniform(-0.5, 0.5)
            velocity_y = random.uniform(-2, -1)  # Float upward

            # Green healing colors
            green_shades = [GREEN, (0, 255, 0), (0, 200, 0), (50, 255, 50)]
            color = random.choice(green_shades)

            size = random.randint(2, 4)
            lifetime = random.randint(40, 80)

            particle = Particle(x + offset_x, y + offset_y, velocity_x, velocity_y,
                              color, size, lifetime, gravity=-0.02, fade=True)
            self.add_particle(particle)

    def add_damage_numbers(self, x: float, y: float, damage: int, color: Tuple[int, int, int] = RED):
        """Add floating damage numbers (handled separately from particles)"""
        # This will be handled by the existing floating text system
        pass

    def update(self):
        """Update all particles and remove dead ones"""
        self.particles = [particle for particle in self.particles if particle.update()]

    def draw(self, surface: pygame.Surface, camera_offset_x: int = 0, camera_offset_y: int = 0):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface, camera_offset_x, camera_offset_y)

    def clear(self):
        """Remove all particles"""
        self.particles.clear()

class ScreenEffects:
    """Handles screen-wide visual effects like screen shake and flashes"""

    def __init__(self):
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

        self.flash_color = WHITE
        self.flash_intensity = 0
        self.flash_duration = 0

    def add_screen_shake(self, intensity: float = 5.0, duration: int = 10):
        """Add screen shake effect"""
        self.shake_intensity = max(self.shake_intensity, intensity)
        self.shake_duration = max(self.shake_duration, duration)

    def add_screen_flash(self, color: Tuple[int, int, int] = WHITE,
                        intensity: int = 100, duration: int = 5):
        """Add screen flash effect"""
        self.flash_color = color
        self.flash_intensity = max(self.flash_intensity, intensity)
        self.flash_duration = max(self.flash_duration, duration)

    def update(self):
        """Update screen effects"""
        # Update screen shake
        if self.shake_duration > 0:
            self.shake_offset_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_offset_y = random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= 1

            # Reduce intensity over time
            if self.shake_duration <= 0:
                self.shake_intensity = 0
                self.shake_offset_x = 0
                self.shake_offset_y = 0

        # Update screen flash
        if self.flash_duration > 0:
            self.flash_duration -= 1
            if self.flash_duration <= 0:
                self.flash_intensity = 0

    def get_camera_shake_offset(self) -> Tuple[int, int]:
        """Get the current camera shake offset"""
        return int(self.shake_offset_x), int(self.shake_offset_y)

    def draw_flash(self, surface: pygame.Surface):
        """Draw screen flash effect"""
        if self.flash_intensity > 0:
            flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash_surface.fill((*self.flash_color, self.flash_intensity))
            surface.blit(flash_surface, (0, 0))

class VisualEffectsManager:
    """Main manager for all visual effects"""

    def __init__(self):
        self.particle_system = ParticleSystem()
        self.screen_effects = ScreenEffects()

    def update(self):
        """Update all visual effects"""
        self.particle_system.update()
        self.screen_effects.update()

    def draw(self, surface: pygame.Surface, camera_offset_x: int = 0, camera_offset_y: int = 0):
        """Draw all visual effects"""
        # Apply camera shake to offsets
        shake_x, shake_y = self.screen_effects.get_camera_shake_offset()
        adjusted_offset_x = camera_offset_x + shake_x
        adjusted_offset_y = camera_offset_y + shake_y

        # Draw particles
        self.particle_system.draw(surface, adjusted_offset_x, adjusted_offset_y)

        # Draw screen flash (always on top)
        self.screen_effects.draw_flash(surface)

    def clear(self):
        """Clear all effects"""
        self.particle_system.clear()
