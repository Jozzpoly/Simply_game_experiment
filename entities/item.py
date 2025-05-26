import pygame
import random
from utils.constants import *

class Item(pygame.sprite.Sprite):
    """Base class for all collectible items"""

    def __init__(self, x, y, image_path):
        super().__init__()

        # Load image
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Item properties
        self.name = "Item"
        self.description = "A generic item"

        # Animation properties for floating effect
        self.float_offset = 0
        self.float_speed = 0.05
        self.float_direction = 1
        self.float_max = 3

        # Visual effects
        self.original_image = self.image.copy()
        self.glow_timer = 0
        self.glow_effect = False

        # Pre-render the glow effect image for better performance
        self.glow_image = self._create_glow_image(self.original_image)

    def _create_glow_image(self, original):
        """Create a pre-rendered glow effect image for better performance"""
        glow_image = original.copy()

        # Create a surface for the brightness overlay
        brightness = pygame.Surface(glow_image.get_size(), pygame.SRCALPHA)
        brightness.fill((40, 40, 40, 0))  # RGBA with alpha=0 for additive blending

        # Apply the brightness using blending
        glow_image.blit(brightness, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        return glow_image

    def update(self):
        """Update item animation"""
        # Simple floating animation
        self.float_offset += self.float_speed * self.float_direction
        if abs(self.float_offset) >= self.float_max:
            self.float_direction *= -1

        # Apply floating effect to visual position only (not collision rect)
        self.rect.y += self.float_direction * self.float_speed

        # Glow effect - simplified to use pre-rendered images
        self.glow_timer += 1
        if self.glow_timer >= 30:  # Change glow state every 30 frames
            self.glow_timer = 0
            self.glow_effect = not self.glow_effect

            # Simply switch between pre-rendered images
            if self.glow_effect:
                self.image = self.glow_image
            else:
                self.image = self.original_image.copy()

    def collect(self, player):
        """Called when the player collects this item"""
        # Base implementation just removes the item
        # Subclasses should override this to provide specific effects
        # The player parameter is used by subclasses but not in the base implementation
        self.kill()
        return True

class HealthPotion(Item):
    """Health potion that restores player health"""

    def __init__(self, x, y, heal_amount=20):
        super().__init__(x, y, HEALTH_POTION_IMG)
        self.name = "Health Potion"
        self.description = f"Restores {heal_amount} health"
        self.heal_amount = heal_amount

    def collect(self, player):
        """Heal the player when collected"""
        player.heal(self.heal_amount)
        # Play a sound effect here if we had sound implemented
        self.kill()
        return True

class DamageBoost(Item):
    """Damage boost that increases player's damage"""

    def __init__(self, x, y, boost_amount=DAMAGE_BOOST_AMOUNT):
        super().__init__(x, y, DAMAGE_BOOST_IMG)
        self.name = "Damage Boost"
        self.description = f"Increases damage by {boost_amount}"
        self.boost_amount = boost_amount

    def collect(self, player):
        """Increase player's damage when collected"""
        player.damage += self.boost_amount
        self.kill()
        return True

class SpeedBoost(Item):
    """Speed boost that increases player's movement speed"""

    def __init__(self, x, y, boost_amount=SPEED_BOOST_AMOUNT):
        super().__init__(x, y, SPEED_BOOST_IMG)
        self.name = "Speed Boost"
        self.description = f"Increases speed by {boost_amount}"
        self.boost_amount = boost_amount

    def collect(self, player):
        """Increase player's speed when collected"""
        player.speed += self.boost_amount
        self.kill()
        return True

class FireRateBoost(Item):
    """Fire rate boost that decreases player's fire cooldown"""

    def __init__(self, x, y, boost_amount=FIRE_RATE_BOOST_AMOUNT):
        super().__init__(x, y, FIRE_RATE_BOOST_IMG)
        self.name = "Fire Rate Boost"
        self.description = f"Decreases fire cooldown by {boost_amount}ms"
        self.boost_amount = boost_amount

    def collect(self, player):
        """Decrease player's fire cooldown when collected"""
        # Ensure fire rate doesn't go below 100ms
        player.fire_rate = max(100, player.fire_rate - self.boost_amount)
        self.kill()
        return True

class ShieldBoost(Item):
    """Shield that absorbs damage for a limited time"""

    def __init__(self, x, y):
        super().__init__(x, y, SHIELD_BOOST_IMG)
        self.name = "Shield"
        self.description = f"Absorbs {SHIELD_ABSORPTION} damage"

    def collect(self, player):
        """Give player a temporary shield"""
        if not hasattr(player, 'shield_health'):
            player.shield_health = 0
            player.shield_duration = 0

        player.shield_health = SHIELD_ABSORPTION
        player.shield_duration = SHIELD_DURATION
        self.kill()
        return True

class XPBoost(Item):
    """XP boost that gives bonus experience points"""

    def __init__(self, x, y):
        super().__init__(x, y, XP_BOOST_IMG)
        self.name = "XP Boost"
        self.description = f"Grants {XP_BOOST_AMOUNT} bonus XP"

    def collect(self, player):
        """Give player bonus XP"""
        player.add_xp(XP_BOOST_AMOUNT)
        self.kill()
        return True

class MultiShotBoost(Item):
    """Multi-shot that allows player to shoot multiple projectiles"""

    def __init__(self, x, y):
        super().__init__(x, y, MULTI_SHOT_BOOST_IMG)
        self.name = "Multi-Shot"
        self.description = f"Triple shot for {MULTI_SHOT_DURATION // 60} seconds"

    def collect(self, player):
        """Give player multi-shot ability - stacks duration properly"""
        if not hasattr(player, 'multi_shot_duration'):
            player.multi_shot_duration = 0

        # Add to existing duration instead of replacing it (proper stacking)
        player.multi_shot_duration += MULTI_SHOT_DURATION

        # Cap the maximum duration to prevent excessive stacking
        max_duration = MULTI_SHOT_DURATION * 5  # Max 5 stacks
        player.multi_shot_duration = min(player.multi_shot_duration, max_duration)

        self.kill()
        return True

class InvincibilityBoost(Item):
    """Temporary invincibility"""

    def __init__(self, x, y):
        super().__init__(x, y, INVINCIBILITY_BOOST_IMG)
        self.name = "Invincibility"
        self.description = f"Invincible for {INVINCIBILITY_DURATION // 60} seconds"

    def collect(self, player):
        """Give player temporary invincibility"""
        if not hasattr(player, 'invincibility_duration'):
            player.invincibility_duration = 0

        player.invincibility_duration = INVINCIBILITY_DURATION
        self.kill()
        return True

def create_random_item(x, y):
    """Factory function to create a random item"""
    item_type = random.choices(
        ["health", "damage", "speed", "fire_rate", "shield", "xp", "multi_shot", "invincibility"],
        weights=[0.3, 0.15, 0.15, 0.15, 0.1, 0.05, 0.05, 0.05],  # Health most common, special items rare
        k=1
    )[0]

    if item_type == "health":
        return HealthPotion(x, y, HEALTH_POTION_HEAL)
    elif item_type == "damage":
        return DamageBoost(x, y)
    elif item_type == "speed":
        return SpeedBoost(x, y)
    elif item_type == "fire_rate":
        return FireRateBoost(x, y)
    elif item_type == "shield":
        return ShieldBoost(x, y)
    elif item_type == "xp":
        return XPBoost(x, y)
    elif item_type == "multi_shot":
        return MultiShotBoost(x, y)
    elif item_type == "invincibility":
        return InvincibilityBoost(x, y)
    else:
        return HealthPotion(x, y)  # Default fallback


class EquipmentItem(Item):
    """Equipment item that can be equipped by the player"""

    def __init__(self, x, y, equipment):
        # Get equipment-specific icon from mapping
        icon_path = EQUIPMENT_ICON_MAPPING.get(equipment.name, DAMAGE_BOOST_IMG)
        super().__init__(x, y, icon_path)
        self.equipment = equipment
        self.name = equipment.get_display_name()
        self.description = f"Equipment: {equipment.equipment_type}"

    def collect(self, player):
        """Add equipment to player's inventory or equip it"""
        # Try to add to inventory first
        if player.equipment_manager.add_to_inventory(self.equipment):
            player.update_progression_stats("items_collected")
            player.update_progression_stats("equipment_equipped")

            # Check if player has full equipment set
            equipped_count = sum(1 for eq in player.equipment_manager.equipped.values() if eq is not None)
            if equipped_count == len(player.equipment_manager.equipped):
                player.update_progression_stats("full_equipment_sets")

            self.kill()
            return True
        else:
            # If inventory is full, still remove the item but don't give the equipment
            # This prevents items from staying on the ground forever
            # TODO: Consider adding a message about full inventory
            self.kill()
            return True
