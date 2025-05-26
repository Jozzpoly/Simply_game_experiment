#!/usr/bin/env python3
"""
In-game skill verification helper.
This script can be imported into the game to add debugging information
and visual indicators for skill effects.
"""

import pygame
from typing import Dict, Any

class SkillDebugger:
    """Helper class to debug and visualize skill effects in-game"""
    
    def __init__(self):
        self.font = None
        self.debug_enabled = True
        self.last_skill_info = {}
        
    def initialize(self):
        """Initialize the debugger (call after pygame.init())"""
        try:
            self.font = pygame.font.Font(None, 24)
        except:
            self.font = None
    
    def update_skill_info(self, player):
        """Update skill information from player"""
        if not player or not hasattr(player, 'skill_tree'):
            return
            
        self.last_skill_info = {
            'critical_chance': player.get_critical_chance(),
            'extra_projectiles': int(player.skill_tree.get_total_bonus("extra_projectiles")),
            'pierce_count': int(player.skill_tree.get_total_bonus("pierce_count")),
            'explosion_radius': player.skill_tree.get_total_bonus("explosion_radius"),
            'damage_bonus': player.skill_tree.get_total_bonus("damage_bonus"),
            'effective_damage': player.get_effective_damage(),
            'skill_points': player.skill_tree.skill_points
        }
    
    def draw_skill_debug_info(self, screen, x=10, y=10):
        """Draw skill debug information on screen"""
        if not self.debug_enabled or not self.font:
            return
            
        debug_lines = [
            f"Skill Points: {self.last_skill_info.get('skill_points', 0)}",
            f"Critical Chance: {self.last_skill_info.get('critical_chance', 0):.1%}",
            f"Extra Projectiles: {self.last_skill_info.get('extra_projectiles', 0)}",
            f"Pierce Count: {self.last_skill_info.get('pierce_count', 0)}",
            f"Explosion Radius: {self.last_skill_info.get('explosion_radius', 0):.0f}",
            f"Damage Bonus: {self.last_skill_info.get('damage_bonus', 0):.1%}",
            f"Effective Damage: {self.last_skill_info.get('effective_damage', 0):.1f}"
        ]
        
        # Draw background
        bg_height = len(debug_lines) * 25 + 10
        bg_rect = pygame.Rect(x - 5, y - 5, 250, bg_height)
        pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)
        
        # Draw text
        for i, line in enumerate(debug_lines):
            color = (255, 255, 255)
            if "Critical" in line and self.last_skill_info.get('critical_chance', 0) > 0:
                color = (255, 255, 0)  # Yellow for active critical
            elif "Extra Projectiles" in line and self.last_skill_info.get('extra_projectiles', 0) > 0:
                color = (0, 255, 255)  # Cyan for active multishot
            elif "Pierce" in line and self.last_skill_info.get('pierce_count', 0) > 0:
                color = (255, 0, 255)  # Magenta for active piercing
            elif "Explosion" in line and self.last_skill_info.get('explosion_radius', 0) > 0:
                color = (255, 165, 0)  # Orange for active explosions
                
            text_surface = self.font.render(line, True, color)
            screen.blit(text_surface, (x, y + i * 25))
    
    def draw_projectile_indicators(self, screen, projectiles, camera_offset_x=0, camera_offset_y=0):
        """Draw indicators for special projectile properties"""
        if not self.debug_enabled:
            return
            
        for projectile in projectiles:
            if not hasattr(projectile, 'is_player_projectile') or not projectile.is_player_projectile:
                continue
                
            x = projectile.rect.centerx - camera_offset_x
            y = projectile.rect.centery - camera_offset_y
            
            # Draw critical hit indicator
            if hasattr(projectile, 'is_critical') and projectile.is_critical:
                pygame.draw.circle(screen, (255, 255, 0), (x, y), 15, 2)
                
            # Draw piercing indicator
            if hasattr(projectile, 'pierce_count') and projectile.pierce_count > 0:
                remaining_pierce = projectile.pierce_count - getattr(projectile, 'pierced_enemies', 0)
                for i in range(remaining_pierce):
                    pygame.draw.circle(screen, (255, 0, 255), (x + i * 8 - 8, y - 20), 3)
                    
            # Draw explosion indicator
            if hasattr(projectile, 'explosion_radius') and projectile.explosion_radius > 0:
                pygame.draw.circle(screen, (255, 165, 0), (x, y), int(projectile.explosion_radius), 1)
    
    def toggle_debug(self):
        """Toggle debug display on/off"""
        self.debug_enabled = not self.debug_enabled
        return self.debug_enabled

# Global instance for easy access
skill_debugger = SkillDebugger()

def add_skill_debugging_to_level(level):
    """Add skill debugging to a level instance"""
    if not hasattr(level, 'skill_debugger'):
        level.skill_debugger = skill_debugger
        level.skill_debugger.initialize()
    
    # Store original draw method
    if not hasattr(level, '_original_draw'):
        level._original_draw = level.draw
    
    def enhanced_draw(screen):
        """Enhanced draw method with skill debugging"""
        # Call original draw
        level._original_draw(screen)
        
        # Add skill debugging
        if hasattr(level, 'player') and level.player:
            level.skill_debugger.update_skill_info(level.player)
            level.skill_debugger.draw_skill_debug_info(screen)
            
            if hasattr(level, 'projectiles'):
                level.skill_debugger.draw_projectile_indicators(
                    screen, level.projectiles, 
                    level.camera_offset_x, level.camera_offset_y
                )
    
    # Replace draw method
    level.draw = enhanced_draw
    
    return level

def create_skill_test_commands():
    """Create a dictionary of test commands for easy skill testing"""
    return {
        'give_skill_points': lambda player, amount=10: player.skill_tree.add_skill_points(amount),
        'max_critical': lambda player: [player.skill_tree.upgrade_skill("critical_strike") for _ in range(5)],
        'max_multishot': lambda player: [player.skill_tree.upgrade_skill("multi_shot") for _ in range(3)],
        'max_piercing': lambda player: [player.skill_tree.upgrade_skill("piercing_shots") for _ in range(3)],
        'max_explosive': lambda player: [player.skill_tree.upgrade_skill("explosive_shots") for _ in range(3)],
        'max_weapon_mastery': lambda player: [player.skill_tree.upgrade_skill("weapon_mastery") for _ in range(5)],
        'max_all_combat': lambda player: [
            player.skill_tree.add_skill_points(20),
            [player.skill_tree.upgrade_skill("critical_strike") for _ in range(5)],
            [player.skill_tree.upgrade_skill("multi_shot") for _ in range(3)],
            [player.skill_tree.upgrade_skill("piercing_shots") for _ in range(3)],
            [player.skill_tree.upgrade_skill("explosive_shots") for _ in range(3)],
            [player.skill_tree.upgrade_skill("weapon_mastery") for _ in range(5)]
        ]
    }

# Instructions for use:
"""
To use this skill verification helper:

1. In your main game file, add:
   from skill_verification_helper import add_skill_debugging_to_level, create_skill_test_commands

2. After creating your level, add:
   level = add_skill_debugging_to_level(level)

3. For testing, you can use the test commands:
   test_commands = create_skill_test_commands()
   test_commands['give_skill_points'](player, 10)
   test_commands['max_critical'](player)

4. Press a key (like F1) to toggle debug display:
   if event.key == pygame.K_F1:
       level.skill_debugger.toggle_debug()

This will show:
- Real-time skill bonuses in the top-left corner
- Visual indicators around projectiles showing their special properties
- Color-coded information (yellow for crits, cyan for multishot, etc.)
"""
