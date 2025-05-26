import pygame
import math
import os
from typing import List, Dict, Optional, Tuple
from utils.constants import *
import logging

logger = logging.getLogger(__name__)

class AnimationFrame:
    """Represents a single frame in an animation"""

    def __init__(self, surface: pygame.Surface, duration: int = 1):
        self.surface = surface
        self.duration = duration  # Duration in game frames

class Animation:
    """Manages a sequence of animation frames"""

    def __init__(self, frames: List[AnimationFrame], loop: bool = True):
        self.frames = frames
        self.loop = loop
        self.current_frame = 0
        self.frame_timer = 0
        self.finished = False

    def update(self):
        """Update the animation"""
        if self.finished and not self.loop:
            return

        self.frame_timer += 1

        if self.frame_timer >= self.frames[self.current_frame].duration:
            self.frame_timer = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True

    def get_current_surface(self) -> pygame.Surface:
        """Get the current frame's surface"""
        return self.frames[self.current_frame].surface

    def reset(self):
        """Reset the animation to the beginning"""
        self.current_frame = 0
        self.frame_timer = 0
        self.finished = False

class SpriteAnimator:
    """Handles animations for sprites"""

    def __init__(self, base_surface: pygame.Surface):
        self.base_surface = base_surface
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[str] = None
        self.idle_surface = base_surface.copy()

        # Animation state
        self.facing_direction = 1  # 1 for right, -1 for left
        self.is_moving = False
        self.is_attacking = False

        # Create basic animations
        self._create_basic_animations()

    def _create_basic_animations(self):
        """Create basic animations like idle breathing"""
        # Create idle breathing animation
        idle_frames = []
        for i in range(60):  # 60 frame cycle
            frame_surface = self.base_surface.copy()

            # Subtle breathing effect
            breath_offset = int(math.sin(i * 0.1) * 0.5)
            if breath_offset != 0:
                # Slightly adjust the sprite vertically for breathing
                temp_surface = pygame.Surface(frame_surface.get_size(), pygame.SRCALPHA)
                temp_surface.blit(frame_surface, (0, breath_offset))
                frame_surface = temp_surface

            idle_frames.append(AnimationFrame(frame_surface, 1))

        self.animations["idle"] = Animation(idle_frames, loop=True)

        # Create walking animation (simple left-right bob)
        walk_frames = []
        for i in range(8):  # 8 frame walk cycle
            frame_surface = self.base_surface.copy()

            # Simple bob effect
            bob_offset = int(math.sin(i * math.pi / 4) * 1)
            if bob_offset != 0:
                temp_surface = pygame.Surface(frame_surface.get_size(), pygame.SRCALPHA)
                temp_surface.blit(frame_surface, (0, bob_offset))
                frame_surface = temp_surface

            walk_frames.append(AnimationFrame(frame_surface, 4))

        self.animations["walk"] = Animation(walk_frames, loop=True)

    def add_custom_animation(self, name: str, frames: List[pygame.Surface],
                           frame_duration: int = 4, loop: bool = True):
        """Add a custom animation"""
        animation_frames = [AnimationFrame(frame, frame_duration) for frame in frames]
        self.animations[name] = Animation(animation_frames, loop)

    def play_animation(self, name: str, force_restart: bool = False):
        """Play a specific animation"""
        if name in self.animations:
            if self.current_animation != name or force_restart:
                self.current_animation = name
                self.animations[name].reset()

    def update(self, is_moving: bool = False, is_attacking: bool = False):
        """Update the animator based on entity state"""
        self.is_moving = is_moving
        self.is_attacking = is_attacking

        # Determine which animation to play
        if is_attacking and "attack" in self.animations:
            self.play_animation("attack")
        elif is_moving and "walk" in self.animations:
            self.play_animation("walk")
        else:
            self.play_animation("idle")

        # Update current animation
        if self.current_animation and self.current_animation in self.animations:
            self.animations[self.current_animation].update()

    def get_current_surface(self) -> pygame.Surface:
        """Get the current animated surface"""
        if self.current_animation and self.current_animation in self.animations:
            surface = self.animations[self.current_animation].get_current_surface()
        else:
            surface = self.idle_surface

        # Apply facing direction
        if self.facing_direction == -1:
            surface = pygame.transform.flip(surface, True, False)

        return surface

    def set_facing_direction(self, direction: int):
        """Set the facing direction (1 for right, -1 for left)"""
        self.facing_direction = direction

class EnhancedSpriteAnimator(SpriteAnimator):
    """Enhanced sprite animator that can load animation frames from files"""

    def __init__(self, base_surface: pygame.Surface, entity_type: str = "", enemy_type: str = ""):
        self.entity_type = entity_type
        self.enemy_type = enemy_type
        super().__init__(base_surface)

        # Try to load animations from files after basic initialization
        if entity_type and self._load_animations_from_files():
            logger.debug(f"Loaded animations from files for {entity_type}")

    def _load_animations_from_files(self) -> bool:
        """Load animation frames from PNG files with enemy type support"""
        try:
            # Use enemy type-specific path if available
            if self.entity_type == "enemy" and self.enemy_type:
                base_path = f"assets/images/entities/enemy_{self.enemy_type}"
            else:
                base_path = f"assets/images/entities/{self.entity_type}"

            if not os.path.exists(base_path):
                logger.debug(f"Animation path does not exist: {base_path}")
                return False

            # Define animation types and their frame counts (optimized for visibility)
            animation_configs = {
                "idle": {"frames": 4, "duration": 20, "loop": True},
                "walk": {"frames": 4, "duration": 8, "loop": True},
                "attack": {"frames": 4, "duration": 6, "loop": False}
            }

            animations_loaded = 0
            for anim_name, config in animation_configs.items():
                frames = []
                for i in range(config["frames"]):
                    frame_path = os.path.join(base_path, f"{anim_name}_{i}.png")
                    if os.path.exists(frame_path):
                        try:
                            frame_surface = pygame.image.load(frame_path).convert_alpha()
                            frames.append(AnimationFrame(frame_surface, config["duration"]))
                        except pygame.error as e:
                            logger.warning(f"Failed to load animation frame {frame_path}: {e}")
                            break
                    else:
                        logger.debug(f"Animation frame not found: {frame_path}")
                        break

                if len(frames) == config["frames"]:
                    self.animations[anim_name] = Animation(frames, loop=config["loop"])
                    animations_loaded += 1
                    logger.debug(f"Loaded {anim_name} animation with {len(frames)} frames for {base_path}")
                else:
                    logger.debug(f"Incomplete animation frames for {anim_name} in {base_path}")

            return animations_loaded > 0

        except Exception as e:
            logger.error(f"Error loading animations from files: {e}")
            return False

class FloatingText:
    """Animated floating text for damage numbers, XP gains, etc."""

    def __init__(self, text: str, x: float, y: float, color: Tuple[int, int, int],
                 font_size: int = 20, velocity_y: float = -1.0, lifetime: int = 60):
        self.text = text
        self.x = x
        self.y = y
        self.start_y = y
        self.color = color
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.max_lifetime = lifetime

        # Create text surface
        font = pygame.font.SysFont(None, font_size)
        self.text_surface = font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect()

        # Animation properties
        self.scale = 1.0
        self.alpha = 255

    def update(self) -> bool:
        """Update the floating text. Returns False if it should be removed."""
        self.y += self.velocity_y
        self.lifetime -= 1

        # Scale animation (start big, shrink to normal)
        if self.lifetime > self.max_lifetime * 0.8:
            progress = (self.max_lifetime - self.lifetime) / (self.max_lifetime * 0.2)
            self.scale = 1.5 - (0.5 * progress)

        # Fade out in the last 20% of lifetime
        if self.lifetime < self.max_lifetime * 0.2:
            fade_progress = self.lifetime / (self.max_lifetime * 0.2)
            self.alpha = int(255 * fade_progress)

        return self.lifetime > 0

    def draw(self, surface: pygame.Surface, camera_offset_x: int = 0, camera_offset_y: int = 0):
        """Draw the floating text"""
        if self.alpha <= 0:
            return

        # Apply scale
        if self.scale != 1.0:
            scaled_surface = pygame.transform.scale(
                self.text_surface,
                (int(self.text_rect.width * self.scale), int(self.text_rect.height * self.scale))
            )
        else:
            scaled_surface = self.text_surface

        # Apply alpha
        if self.alpha < 255:
            alpha_surface = scaled_surface.copy()
            alpha_surface.set_alpha(self.alpha)
            scaled_surface = alpha_surface

        # Calculate position
        screen_x = int(self.x - camera_offset_x - scaled_surface.get_width() // 2)
        screen_y = int(self.y - camera_offset_y - scaled_surface.get_height() // 2)

        surface.blit(scaled_surface, (screen_x, screen_y))

class AnimationManager:
    """Manages all animations and animated elements"""

    def __init__(self):
        self.floating_texts: List[FloatingText] = []
        self.sprite_animators: Dict[str, SpriteAnimator] = {}

    def add_floating_text(self, text: str, x: float, y: float,
                         color: Tuple[int, int, int] = WHITE, font_size: int = 20):
        """Add floating text animation"""
        floating_text = FloatingText(text, x, y, color, font_size)
        self.floating_texts.append(floating_text)

    def add_damage_text(self, damage: int, x: float, y: float):
        """Add damage number animation"""
        self.add_floating_text(f"-{damage}", x, y, RED, 24)

    def add_heal_text(self, heal: int, x: float, y: float):
        """Add healing number animation"""
        self.add_floating_text(f"+{heal}", x, y, GREEN, 20)

    def add_xp_text(self, xp: int, x: float, y: float):
        """Add XP gain animation"""
        self.add_floating_text(f"+{xp} XP", x, y, CYAN, 18)

    def register_sprite_animator(self, entity_id: str, animator: SpriteAnimator):
        """Register a sprite animator for an entity"""
        self.sprite_animators[entity_id] = animator

    def update(self):
        """Update all animations"""
        # Update floating texts
        self.floating_texts = [text for text in self.floating_texts if text.update()]

        # Update sprite animators
        for animator in self.sprite_animators.values():
            animator.update()

    def draw_floating_texts(self, surface: pygame.Surface, camera_offset_x: int = 0, camera_offset_y: int = 0):
        """Draw all floating texts"""
        for text in self.floating_texts:
            text.draw(surface, camera_offset_x, camera_offset_y)

    def clear(self):
        """Clear all animations"""
        self.floating_texts.clear()
        self.sprite_animators.clear()
