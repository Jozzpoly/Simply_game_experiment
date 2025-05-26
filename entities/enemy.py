import pygame
import random
import math
from entities.entity import Entity
from entities.projectile import Projectile
from utils.animation_system import EnhancedSpriteAnimator
from utils.constants import *
from config import ENEMY_BASE_SPEED, ENEMY_SPEED_MULTIPLIERS

class Enemy(Entity):
    """Enemy character class with improved AI behavior and pathfinding"""

    def __init__(self, x, y, difficulty_level=1):
        # Scale enemy health and damage based on difficulty level with exponential scaling
        health = ENEMY_HEALTH + int((difficulty_level - 1) * 5 * (1.1 ** (difficulty_level - 1)))
        damage = ENEMY_DAMAGE + int((difficulty_level - 1) * (1.15 ** (difficulty_level - 1)))

        super().__init__(x, y, ENEMY_IMG, health)
        self.speed = ENEMY_BASE_SPEED
        self.fire_rate = ENEMY_FIRE_RATE
        self.damage = damage
        self.detection_radius = 300  # Pixels
        self.state = "idle"  # idle, chase, attack, patrol
        self.idle_timer = 0
        self.idle_direction = pygame.math.Vector2(0, 0)
        self.change_direction_time = 1000  # milliseconds

        # Pathfinding variables
        self.path = []
        self.path_index = 0
        self.path_update_timer = 0
        self.path_update_delay = 500  # milliseconds
        self.can_see_player = False

        # Visibility check optimization
        self.visibility_check_timer = 0
        self.visibility_check_frequency = 10  # Check visibility every 10 frames

        # Random movement variables
        self.random_move_timer = 0
        self.random_move_duration = random.randint(1000, 3000)  # milliseconds

        # Enhanced enemy type and behavior system
        self.enemy_type = random.choice(["normal", "fast", "tank", "sniper", "berserker"])

        # Initialize default AI properties (will be modified by type)
        self.aggression_level = random.uniform(0.3, 1.0)  # How aggressive the enemy is
        self.retreat_threshold = 0.2  # Health percentage to start retreating
        self.group_coordination = True  # Whether this enemy coordinates with others

        # Apply type-specific modifiers
        self._apply_enemy_type_modifiers(difficulty_level)

        # Set preferred range after type is determined
        self.preferred_range = self._get_preferred_combat_range()

        # Tactical behavior
        self.last_player_position = None
        self.prediction_accuracy = random.uniform(0.1, 0.8)  # How well it predicts player movement
        self.flanking_behavior = random.choice([True, False])  # Whether it tries to flank

        # Group coordination and AI roles
        self.group_id = None  # Will be set by level generator
        self.role = self._determine_role()  # leader, follower, support, scout
        self.formation_position = None  # Position within group formation
        self.group_members = []  # References to other enemies in the same group
        self.coordination_range = 200  # Range for group coordination

        # Advanced AI state tracking
        self.ai_difficulty = 1.0  # Will be adjusted based on player performance
        self.last_coordination_time = 0
        self.coordination_cooldown = 1000  # ms between coordination attempts

        # Create a smaller collision rectangle for better movement
        self.collision_rect = self.rect.inflate(-4, -4)

        # Performance optimization attributes
        self.ai_enabled = True  # Can be disabled for distant enemies
        self.visible = True     # Can be hidden for very distant enemies
        self.simplified_ai = False  # Use simplified AI for distant enemies
        self.last_optimization_check = 0

        # Visual differentiation based on enemy type
        self.base_color = self._get_enemy_color()
        self.current_color = self.base_color
        self.visual_state = "normal"  # normal, aggressive, retreating, coordinating
        self.color_transition_speed = 5  # Speed of color transitions
        self.state_indicator_alpha = 0  # Alpha for state indicators

        # Initialize animation system with enemy type support
        self.original_image = self.image.copy()
        self.animator = EnhancedSpriteAnimator(self.original_image, "enemy", self.enemy_type)
        self.is_moving = False
        self.is_attacking = False

    def _apply_enemy_type_modifiers(self, difficulty_level: int) -> None:
        """Apply stat modifiers based on enemy type"""
        if self.enemy_type == "fast":
            self.speed += 1.5
            self.health *= 0.6
            self.damage *= 0.8
            self.fire_rate = int(self.fire_rate * 0.8)  # Faster shooting
            self.xp_reward = int(XP_PER_ENEMY_FAST * (XP_DIFFICULTY_MULTIPLIER ** (difficulty_level - 1)))
        elif self.enemy_type == "tank":
            self.speed -= 0.8
            self.health *= 2.0
            self.damage *= 1.3
            self.fire_rate = int(self.fire_rate * 1.5)  # Slower shooting
            self.xp_reward = int(XP_PER_ENEMY_TANK * (XP_DIFFICULTY_MULTIPLIER ** (difficulty_level - 1)))
        elif self.enemy_type == "sniper":
            self.speed -= 0.3
            self.health *= 0.8
            self.damage *= 1.8
            self.fire_rate = int(self.fire_rate * 2.0)  # Much slower but powerful shots
            self.detection_radius = 400  # Longer range
            self.xp_reward = int(XP_PER_ENEMY_SNIPER * (XP_DIFFICULTY_MULTIPLIER ** (difficulty_level - 1)))
        elif self.enemy_type == "berserker":
            self.speed += 0.8
            self.health *= 1.2
            self.damage *= 1.5
            self.fire_rate = int(self.fire_rate * 0.6)  # Very fast shooting
            self.aggression_level = 1.0  # Always aggressive
            self.retreat_threshold = 0.0  # Never retreats
            self.xp_reward = int(XP_PER_ENEMY_BERSERKER * (XP_DIFFICULTY_MULTIPLIER ** (difficulty_level - 1)))
        else:  # normal
            self.xp_reward = int(XP_PER_ENEMY_BASE * (XP_DIFFICULTY_MULTIPLIER ** (difficulty_level - 1)))

    def _get_preferred_combat_range(self) -> float:
        """Get the preferred combat range based on enemy type"""
        if self.enemy_type == "sniper":
            return 250.0
        elif self.enemy_type == "tank":
            return 120.0
        elif self.enemy_type == "berserker":
            return 80.0
        elif self.enemy_type == "fast":
            return 150.0
        else:  # normal
            return 180.0

    def _determine_role(self) -> str:
        """Determine the enemy's role within a group based on type and stats"""
        if self.enemy_type == "tank":
            return random.choice(["leader", "support"])  # Tanks often lead or support
        elif self.enemy_type == "sniper":
            return random.choice(["support", "scout"])  # Snipers provide support or scout
        elif self.enemy_type == "fast":
            return random.choice(["scout", "flanker"])  # Fast enemies scout or flank
        elif self.enemy_type == "berserker":
            return random.choice(["assault", "follower"])  # Berserkers assault or follow
        else:  # normal
            return random.choice(["follower", "support", "assault"])

    def set_group_info(self, group_id: str, group_members: list, formation_position: tuple = None):
        """Set group coordination information"""
        self.group_id = group_id
        self.group_members = [member for member in group_members if member != self]
        self.formation_position = formation_position

    def _get_enemy_color(self) -> tuple:
        """Get the base color for this enemy type"""
        color_map = {
            "normal": (255, 100, 100),    # Red
            "fast": (100, 255, 100),      # Green
            "tank": (100, 100, 255),      # Blue
            "sniper": (255, 255, 100),    # Yellow
            "berserker": (255, 100, 255)  # Magenta
        }
        return color_map.get(self.enemy_type, (255, 100, 100))

    def update(self, player, walls, projectiles_group, systems_manager=None):
        """Update enemy based on improved AI behavior with performance optimization"""
        # Check if AI is disabled for performance optimization
        if not self.ai_enabled:
            return

        # Calculate distance to player
        player_pos = pygame.math.Vector2(player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        distance_to_player = player_pos.distance_to(enemy_pos)

        # Use simplified AI for distant enemies if performance optimization is enabled
        if self.simplified_ai:
            self._update_simplified_ai(player, walls, distance_to_player)
            return

        # Optimize visibility checks - only check periodically
        self.visibility_check_timer += 1
        if self.visibility_check_timer >= self.visibility_check_frequency:
            self.visibility_check_timer = 0
            # Check if we can see the player (no walls in between)
            self.can_see_player = self._can_see_player(player, walls)

        # Reset velocity
        self.velocity = pygame.math.Vector2(0, 0)

        # Store previous position to detect if we're stuck
        prev_x, prev_y = self.rect.x, self.rect.y

        # Current time for timers
        current_time = pygame.time.get_ticks()

        # Enhanced state machine for enemy behavior
        current_health_percentage = self.health / self.max_health

        # Check if enemy should retreat based on health and type
        should_retreat = (current_health_percentage < self.retreat_threshold and
                         self.enemy_type != "berserker")

        if distance_to_player <= self.detection_radius and self.can_see_player:
            # Store player position for prediction
            self.last_player_position = player_pos.copy()

            if should_retreat:
                # Retreat behavior - move away from player
                self.state = "retreat"
                self.velocity = enemy_pos - player_pos
                if self.velocity.length() > 0:
                    self.velocity.normalize_ip()
                    self.velocity *= self.speed * 1.2  # Retreat faster
            elif distance_to_player <= self.preferred_range:
                # Within preferred combat range
                self.state = "attack"
                self._execute_combat_behavior(player_pos, enemy_pos, distance_to_player)
            else:
                # Player is detected but not in range, approach
                self.state = "chase"
                self._execute_chase_behavior(player_pos, enemy_pos)
        else:
            # Player is not detected or not visible
            # Use pathfinding if player is within range but not visible
            if distance_to_player <= self.detection_radius * 1.5 and not self.can_see_player:
                self.state = "pathfinding"

                # Update path periodically
                if current_time - self.path_update_timer > self.path_update_delay:
                    self.path_update_timer = current_time
                    self._find_path_to_player(player, walls)

                # Follow the path if we have one
                if self.path and self.path_index < len(self.path):
                    target_pos = self.path[self.path_index]
                    target_vector = pygame.math.Vector2(target_pos[0] - self.rect.centerx,
                                                       target_pos[1] - self.rect.centery)

                    # If we're close to the current waypoint, move to the next one
                    if target_vector.length() < 10:
                        self.path_index += 1
                    else:
                        # Move toward the current waypoint
                        if target_vector.length() > 0:
                            target_vector.normalize_ip()
                            self.velocity = target_vector * self.speed
            else:
                # Random movement behavior
                self.state = "idle"

                # Change direction randomly or when timer expires
                if (current_time - self.random_move_timer > self.random_move_duration or
                    random.random() < RANDOM_MOVE_CHANCE):
                    self.random_move_timer = current_time
                    self.random_move_duration = random.randint(1000, 3000)
                    self._choose_random_direction()

                self.velocity = self.idle_direction * (self.speed * 0.5)

        # Move the enemy
        self.move(self.velocity.x, self.velocity.y, walls)

        # Update collision rectangle position to match the sprite
        if hasattr(self, 'collision_rect'):
            self.collision_rect.center = self.rect.center

        # Check if we're stuck (position didn't change despite having velocity)
        if (self.rect.x == prev_x and self.rect.y == prev_y and
            self.velocity.length() > 0):
            # We're stuck, try a different direction
            self._choose_random_direction()
            # Immediately try moving in the new direction
            self.velocity = self.idle_direction * self.speed
            self.move(self.velocity.x, self.velocity.y, walls)

        # Group coordination behavior
        current_time = pygame.time.get_ticks()
        if (self.group_coordination and self.group_members and
            current_time - self.last_coordination_time > self.coordination_cooldown):
            self._execute_group_coordination(player, current_time)
            self.last_coordination_time = current_time

        # Enhanced shooting behavior based on state and enemy type
        if self.state in ["attack", "retreat"] and self.can_shoot() and self.can_see_player:
            self._execute_shooting_behavior(player, projectiles_group)

        # Update visual state and color transitions
        self._update_visual_state()
        self._update_color_transitions()

        # Update animation system
        self.is_moving = self.velocity.length() > 0.1
        self.is_attacking = self.state == "attack" and self.can_see_player
        self.animator.update(self.is_moving, self.is_attacking)

        # Update sprite image from animation
        self.image = self.animator.get_current_surface()

    def _update_simplified_ai(self, player, walls, distance_to_player: float) -> None:
        """Simplified AI update for distant enemies to improve performance"""
        # Very basic behavior - just move towards player occasionally
        if distance_to_player <= self.detection_radius * 1.5:
            # Simple movement towards player
            player_pos = pygame.math.Vector2(player.rect.center)
            enemy_pos = pygame.math.Vector2(self.rect.center)

            direction = player_pos - enemy_pos
            if direction.length() > 0:
                direction.normalize_ip()
                self.velocity = direction * (self.speed * 0.5)  # Slower movement

            # Simple movement with basic collision
            self.move(self.velocity.x, self.velocity.y, walls)
        else:
            # Stay idle if too far
            self.velocity = pygame.math.Vector2(0, 0)

        # Update collision rectangle
        if hasattr(self, 'collision_rect'):
            self.collision_rect.center = self.rect.center

    def _choose_random_direction(self):
        """Choose a random direction for movement"""
        angle = random.uniform(0, 2 * math.pi)
        self.idle_direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))

    def _can_see_player(self, player, walls):
        """Check if there's a clear line of sight to the player"""
        return self._can_see_from_point(self.rect.center, player.rect.center, walls)

    def _can_see_from_point(self, start_point, end_point, walls):
        """Check if there's a clear line of sight between two points"""
        # Create a line from start to end
        start_pos = pygame.math.Vector2(start_point)
        end_pos = pygame.math.Vector2(end_point)

        # Check distance first (optimization)
        if start_pos.distance_to(end_pos) > self.detection_radius * 1.5:
            return False

        # Calculate direction and distance
        direction = end_pos - start_pos
        distance = direction.length()

        if distance == 0:
            return True

        direction.normalize_ip()

        # Check for wall collisions along the line
        step_size = 10  # pixels per step
        steps = int(distance / step_size)

        for i in range(1, steps + 1):
            # Calculate point along the line
            check_distance = i * step_size
            if check_distance >= distance:
                break

            check_point = start_pos + direction * check_distance

            # Create a small rect at this point to check for wall collision
            check_rect = pygame.Rect(0, 0, 4, 4)
            check_rect.center = (check_point.x, check_point.y)

            # Check if this point collides with any wall
            for wall in walls:
                if wall.rect.colliderect(check_rect):
                    return False

        return True

    def _find_path_to_player(self, player, walls):
        """Simple pathfinding to navigate around obstacles"""
        # Only do pathfinding if player is within range but not too close
        player_pos = pygame.math.Vector2(player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        distance = player_pos.distance_to(enemy_pos)

        if distance > PATHFINDING_MAX_DISTANCE or distance < 50:
            self.path = []
            return

        # Simple pathfinding: try to find a path around obstacles
        # This is a very basic implementation - a real game would use A* or similar

        # Start with a direct path
        self.path = [player.rect.center]
        self.path_index = 0

        # If we can see the player directly, no need for complex path
        if self._can_see_player(player, walls):
            return

        # Try to find a path by checking points around obstacles
        # This is a simplified approach - just try a few points in different directions
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Cardinal directions
            (1, 1), (-1, 1), (1, -1), (-1, -1)  # Diagonals
        ]

        # Try to find waypoints around obstacles
        waypoints = []
        for direction in directions:
            # Try a point offset from our position
            test_point = (
                self.rect.centerx + direction[0] * 100,
                self.rect.centery + direction[1] * 100
            )

            # Create a temporary rect for collision checking
            test_rect = pygame.Rect(0, 0, 4, 4)
            test_rect.center = test_point

            # Skip if the point is inside a wall
            wall_collision = False
            for wall in walls:
                if wall.rect.colliderect(test_rect):
                    wall_collision = True
                    break

            if wall_collision:
                continue

            # Check if we can see this point using the new helper method
            if not self._can_see_from_point(self.rect.center, test_point, walls):
                continue

            # If we can reach this point, check if it has a clear line to the player
            if self._can_see_from_point(test_point, player.rect.center, walls):
                waypoints.append(test_point)

        # If we found any valid waypoints, use the first one
        if waypoints:
            self.path = [waypoints[0], player.rect.center]
            self.path_index = 0

    def _execute_combat_behavior(self, player_pos: pygame.math.Vector2,
                                enemy_pos: pygame.math.Vector2, distance: float) -> None:
        """Execute combat behavior based on enemy type and situation"""
        if self.enemy_type == "sniper":
            # Snipers try to maintain maximum range and stay stationary when shooting
            if distance < self.preferred_range * 0.8:
                # Too close, back away
                self.velocity = enemy_pos - player_pos
                if self.velocity.length() > 0:
                    self.velocity.normalize_ip()
                    self.velocity *= self.speed * 0.7
            else:
                # Good range, stay still for accuracy
                self.velocity = pygame.math.Vector2(0, 0)

        elif self.enemy_type == "berserker":
            # Berserkers charge directly at the player
            self.velocity = player_pos - enemy_pos
            if self.velocity.length() > 0:
                self.velocity.normalize_ip()
                self.velocity *= self.speed * self.aggression_level

        elif self.enemy_type == "fast":
            # Fast enemies use hit-and-run tactics
            if self.flanking_behavior and random.random() < 0.3:
                # Try to circle around the player
                perpendicular = pygame.math.Vector2(-(player_pos.y - enemy_pos.y),
                                                  player_pos.x - enemy_pos.x)
                if perpendicular.length() > 0:
                    perpendicular.normalize_ip()
                    self.velocity = perpendicular * self.speed
            else:
                # Standard approach
                self.velocity = player_pos - enemy_pos
                if self.velocity.length() > 0:
                    self.velocity.normalize_ip()
                    self.velocity *= self.speed

        else:  # tank or normal
            # Try to maintain optimal distance
            if distance < self.preferred_range * 0.7:
                # Too close, back away slightly
                self.velocity = enemy_pos - player_pos
                if self.velocity.length() > 0:
                    self.velocity.normalize_ip()
                    self.velocity *= self.speed * 0.5
            elif distance > self.preferred_range * 1.2:
                # Too far, move closer
                self.velocity = player_pos - enemy_pos
                if self.velocity.length() > 0:
                    self.velocity.normalize_ip()
                    self.velocity *= self.speed * 0.8
            else:
                # Good range, minimal movement
                self.velocity *= 0.3

    def _execute_chase_behavior(self, player_pos: pygame.math.Vector2,
                               enemy_pos: pygame.math.Vector2) -> None:
        """Execute chase behavior with prediction and flanking"""
        # Basic chase direction
        chase_direction = player_pos - enemy_pos

        # Add movement prediction for smarter enemies
        if self.last_player_position and self.prediction_accuracy > 0.5:
            player_velocity = player_pos - self.last_player_position
            predicted_position = player_pos + (player_velocity * self.prediction_accuracy)
            chase_direction = predicted_position - enemy_pos

        # Apply flanking behavior for certain enemy types
        if self.flanking_behavior and self.enemy_type in ["fast", "normal"]:
            if random.random() < 0.2:  # 20% chance to flank
                # Add perpendicular component for flanking
                perpendicular = pygame.math.Vector2(-chase_direction.y, chase_direction.x)
                if perpendicular.length() > 0:
                    perpendicular.normalize_ip()
                    chase_direction += perpendicular * 0.5

        if chase_direction.length() > 0:
            chase_direction.normalize_ip()
            self.velocity = chase_direction * self.speed

    def _execute_shooting_behavior(self, player, projectiles_group) -> None:
        """Execute shooting behavior based on enemy type and state"""
        if self.enemy_type == "sniper":
            # Snipers aim more carefully and predict movement
            if self.last_player_position:
                player_velocity = pygame.math.Vector2(player.rect.center) - self.last_player_position
                predicted_pos = pygame.math.Vector2(player.rect.center) + (player_velocity * 2)
                self.shoot(predicted_pos.x, predicted_pos.y, projectiles_group)
            else:
                self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)

        elif self.enemy_type == "berserker" and self.state == "attack":
            # Berserkers shoot rapidly when in attack mode
            self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)

        else:
            # Standard shooting behavior
            self.shoot(player.rect.centerx, player.rect.centery, projectiles_group)

    def _execute_group_coordination(self, player, current_time: int) -> None:
        """Execute group coordination behaviors based on role and situation"""
        if not self.group_members:
            return

        player_pos = pygame.math.Vector2(player.rect.center)
        my_pos = pygame.math.Vector2(self.rect.center)

        # Count nearby group members
        nearby_members = []
        for member in self.group_members:
            if hasattr(member, 'rect'):  # Ensure member is still alive
                member_pos = pygame.math.Vector2(member.rect.center)
                if my_pos.distance_to(member_pos) <= self.coordination_range:
                    nearby_members.append(member)

        if not nearby_members:
            return

        # Role-based coordination behavior
        if self.role == "leader":
            self._coordinate_as_leader(player_pos, nearby_members)
        elif self.role == "scout":
            self._coordinate_as_scout(player_pos, nearby_members)
        elif self.role == "support":
            self._coordinate_as_support(player_pos, nearby_members)
        elif self.role == "flanker":
            self._coordinate_as_flanker(player_pos, nearby_members)
        else:  # follower, assault
            self._coordinate_as_follower(player_pos, nearby_members)

    def _coordinate_as_leader(self, player_pos: pygame.math.Vector2, nearby_members: list) -> None:
        """Leader coordination - direct group tactics"""
        # Leaders try to position themselves optimally and signal others
        if len(nearby_members) >= 2:
            # If we have enough members, try to coordinate a flanking maneuver
            if random.random() < 0.3:  # 30% chance to initiate flanking
                self._signal_flanking_maneuver(player_pos, nearby_members)

        # Leaders maintain formation and don't retreat easily
        if self.retreat_threshold > 0:
            self.retreat_threshold *= 0.7  # Leaders retreat less

    def _coordinate_as_scout(self, player_pos: pygame.math.Vector2, nearby_members: list) -> None:
        """Scout coordination - information gathering and positioning"""
        # Scouts try to maintain distance and provide overwatch
        my_pos = pygame.math.Vector2(self.rect.center)
        distance_to_player = my_pos.distance_to(player_pos)

        if distance_to_player < self.preferred_range * 1.5:
            # Scout is too close, try to reposition
            retreat_direction = my_pos - player_pos
            if retreat_direction.length() > 0:
                retreat_direction.normalize_ip()
                # Modify velocity to maintain scouting position
                self.velocity += retreat_direction * (self.speed * 0.3)

    def _coordinate_as_support(self, player_pos: pygame.math.Vector2, nearby_members: list) -> None:
        """Support coordination - assist other group members"""
        # Support units try to stay behind other members and provide covering fire
        my_pos = pygame.math.Vector2(self.rect.center)

        # Find the closest member to the player
        closest_member = None
        closest_distance = float('inf')

        for member in nearby_members:
            if hasattr(member, 'rect'):
                member_pos = pygame.math.Vector2(member.rect.center)
                distance = member_pos.distance_to(player_pos)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_member = member

        if closest_member:
            # Position behind the closest member
            member_pos = pygame.math.Vector2(closest_member.rect.center)
            support_direction = member_pos - player_pos
            if support_direction.length() > 0:
                support_direction.normalize_ip()
                ideal_position = member_pos + support_direction * 60
                move_direction = ideal_position - my_pos
                if move_direction.length() > 20:  # Only move if significantly out of position
                    move_direction.normalize_ip()
                    self.velocity += move_direction * (self.speed * 0.2)

    def _coordinate_as_flanker(self, player_pos: pygame.math.Vector2, nearby_members: list) -> None:
        """Flanker coordination - attempt to get behind or to the side of player"""
        my_pos = pygame.math.Vector2(self.rect.center)

        # Try to move to the player's flank
        to_player = player_pos - my_pos
        if to_player.length() > 0:
            # Calculate perpendicular direction for flanking
            perpendicular = pygame.math.Vector2(-to_player.y, to_player.x)
            perpendicular.normalize_ip()

            # Choose left or right flank based on current position
            if random.random() < 0.5:
                perpendicular *= -1

            # Combine approach and flanking movement
            flank_direction = (to_player.normalize() * 0.3 + perpendicular * 0.7)
            self.velocity += flank_direction * (self.speed * 0.4)

    def _coordinate_as_follower(self, player_pos: pygame.math.Vector2, nearby_members: list) -> None:
        """Follower coordination - follow group leader or strongest member"""
        my_pos = pygame.math.Vector2(self.rect.center)

        # Find a leader or strong member to follow
        leader = None
        for member in nearby_members:
            if hasattr(member, 'role') and member.role == "leader":
                leader = member
                break

        if not leader:
            # No leader found, follow the strongest member (tank or highest health)
            strongest_member = None
            max_health = 0
            for member in nearby_members:
                if hasattr(member, 'health') and member.health > max_health:
                    max_health = member.health
                    strongest_member = member
            leader = strongest_member

        if leader and hasattr(leader, 'rect'):
            # Follow the leader but maintain some distance
            leader_pos = pygame.math.Vector2(leader.rect.center)
            distance_to_leader = my_pos.distance_to(leader_pos)

            if distance_to_leader > 80:  # Too far from leader
                follow_direction = leader_pos - my_pos
                follow_direction.normalize_ip()
                self.velocity += follow_direction * (self.speed * 0.3)
            elif distance_to_leader < 40:  # Too close to leader
                avoid_direction = my_pos - leader_pos
                avoid_direction.normalize_ip()
                self.velocity += avoid_direction * (self.speed * 0.2)

    def _signal_flanking_maneuver(self, player_pos: pygame.math.Vector2, nearby_members: list) -> None:
        """Signal nearby members to execute a flanking maneuver"""
        # This is a simplified signaling system - in a more complex implementation,
        # this could involve setting flags on other enemies or using a message system
        flankers = [member for member in nearby_members
                   if hasattr(member, 'role') and member.role in ["flanker", "scout", "assault"]]

        if len(flankers) >= 1:
            # Encourage flankers to move to player's sides
            for flanker in flankers[:2]:  # Limit to 2 flankers
                if hasattr(flanker, 'flanking_behavior'):
                    flanker.flanking_behavior = True
                    # Temporarily increase their aggression
                    if hasattr(flanker, 'aggression_level'):
                        flanker.aggression_level = min(1.0, flanker.aggression_level + 0.2)

    def _update_visual_state(self) -> None:
        """Update visual state based on current AI state and behavior"""
        current_health_percentage = self.health / self.max_health

        # Determine visual state based on AI state and health
        if self.state == "retreat" or current_health_percentage < self.retreat_threshold:
            self.visual_state = "retreating"
        elif self.state == "attack" and self.aggression_level > 0.7:
            self.visual_state = "aggressive"
        elif self.group_coordination and self.group_members:
            # Check if we're actively coordinating
            nearby_count = sum(1 for member in self.group_members
                             if hasattr(member, 'rect') and
                             pygame.math.Vector2(self.rect.center).distance_to(
                                 pygame.math.Vector2(member.rect.center)) <= self.coordination_range)
            if nearby_count >= 2:
                self.visual_state = "coordinating"
            else:
                self.visual_state = "normal"
        else:
            self.visual_state = "normal"

    def _update_color_transitions(self) -> None:
        """Update color transitions based on visual state"""
        target_color = self.base_color

        # Modify color based on visual state
        if self.visual_state == "aggressive":
            # Brighter, more intense colors when aggressive
            target_color = tuple(min(255, int(c * 1.3)) for c in self.base_color)
        elif self.visual_state == "retreating":
            # Darker, muted colors when retreating
            target_color = tuple(max(50, int(c * 0.6)) for c in self.base_color)
        elif self.visual_state == "coordinating":
            # Slight blue tint when coordinating
            r, g, b = self.base_color
            target_color = (max(50, int(r * 0.8)), max(50, int(g * 0.8)), min(255, int(b * 1.2)))

        # Smooth color transition
        current_r, current_g, current_b = self.current_color
        target_r, target_g, target_b = target_color

        # Interpolate towards target color
        speed = self.color_transition_speed
        new_r = current_r + (target_r - current_r) / speed
        new_g = current_g + (target_g - current_g) / speed
        new_b = current_b + (target_b - current_b) / speed

        self.current_color = (int(new_r), int(new_g), int(new_b))

    def get_visual_indicators(self) -> dict:
        """Get visual indicators for rendering (state icons, effects, etc.)"""
        indicators = {
            'color': self.current_color,
            'state': self.visual_state,
            'type': self.enemy_type,
            'role': self.role,
            'health_percentage': min(1.0, max(0.0, self.health / self.max_health))
        }

        # Add special indicators based on state
        if self.visual_state == "aggressive":
            indicators['effect'] = 'aggressive_aura'
        elif self.visual_state == "retreating":
            indicators['effect'] = 'retreat_indicator'
        elif self.visual_state == "coordinating":
            indicators['effect'] = 'coordination_lines'

        return indicators

    def shoot(self, target_x, target_y, projectiles_group):
        """Shoot a projectile towards the target position"""
        # Calculate direction vector
        start_x = self.rect.centerx
        start_y = self.rect.centery

        # Create direction vector
        direction = pygame.math.Vector2(target_x - start_x, target_y - start_y)
        if direction.length() > 0:
            direction.normalize_ip()

        # Create projectile
        projectile = Projectile(
            start_x,
            start_y,
            direction,
            ENEMY_PROJECTILE_IMG,
            PROJECTILE_SPEED,
            self.damage,
            is_player_projectile=False
        )

        # Add to group
        projectiles_group.add(projectile)

        # Play enemy shooting sound
        if hasattr(self, 'audio_manager') and self.audio_manager:
            self.audio_manager.play_sound('enemy_shoot', volume_modifier=0.7)

        return True

    def take_damage(self, amount):
        """Take damage with visual effects"""
        # Apply damage using parent method
        result = super().take_damage(amount)

        # Add visual effects if the enemy dies
        if result:  # Enemy died
            # Play enemy death sound
            if hasattr(self, 'audio_manager') and self.audio_manager:
                self.audio_manager.play_sound('enemy_death')

            # Add explosion effect at enemy position
            if hasattr(self, 'visual_effects') and self.visual_effects:
                # Create a more impressive explosion based on enemy type
                if self.enemy_type == "tank":
                    # Bigger explosion for tank enemies
                    self.visual_effects.particle_system.add_explosion(
                        self.rect.centerx, self.rect.centery,
                        ORANGE, particle_count=20, intensity=8.0
                    )
                    # Stronger screen shake
                    self.visual_effects.screen_effects.add_screen_shake(intensity=6.0, duration=12)
                elif self.enemy_type == "fast":
                    # Quick, bright explosion for fast enemies
                    self.visual_effects.particle_system.add_explosion(
                        self.rect.centerx, self.rect.centery,
                        CYAN, particle_count=12, intensity=7.0
                    )
                    # Brief but intense screen shake
                    self.visual_effects.screen_effects.add_screen_shake(intensity=4.0, duration=6)
                else:
                    # Standard explosion for normal enemies
                    self.visual_effects.particle_system.add_explosion(
                        self.rect.centerx, self.rect.centery,
                        RED, particle_count=15, intensity=6.0
                    )
                    # Standard screen shake
                    self.visual_effects.screen_effects.add_screen_shake(intensity=4.0, duration=8)

        return result

    def draw(self, screen):
        """Draw the enemy with enhanced visual differentiation"""
        # Draw main enemy body with current color
        pygame.draw.rect(screen, self.current_color, self.rect)

        # Draw type indicator (small shape in corner)
        self._draw_type_indicator(screen)

        # Draw state effects
        self._draw_state_effects(screen)

        # Draw health bar if damaged
        if self.health < self.max_health:
            self._draw_health_bar(screen)

    def _draw_type_indicator(self, screen):
        """Draw a small indicator showing enemy type"""
        indicator_size = 6
        x, y = self.rect.topleft

        if self.enemy_type == "fast":
            # Triangle for fast enemies
            points = [(x + 2, y + 2), (x + 8, y + 2), (x + 5, y + 8)]
            pygame.draw.polygon(screen, (255, 255, 255), points)
        elif self.enemy_type == "tank":
            # Square for tank enemies
            pygame.draw.rect(screen, (255, 255, 255), (x + 2, y + 2, indicator_size, indicator_size))
        elif self.enemy_type == "sniper":
            # Cross for sniper enemies
            pygame.draw.line(screen, (255, 255, 255), (x + 2, y + 5), (x + 8, y + 5), 2)
            pygame.draw.line(screen, (255, 255, 255), (x + 5, y + 2), (x + 5, y + 8), 2)
        elif self.enemy_type == "berserker":
            # X for berserker enemies
            pygame.draw.line(screen, (255, 255, 255), (x + 2, y + 2), (x + 8, y + 8), 2)
            pygame.draw.line(screen, (255, 255, 255), (x + 8, y + 2), (x + 2, y + 8), 2)
        # Normal enemies have no special indicator

    def _draw_state_effects(self, screen):
        """Draw visual effects based on current state"""
        center_x, center_y = self.rect.center

        if self.visual_state == "aggressive":
            # Pulsing red aura for aggressive enemies
            import math
            pulse = int(20 + 10 * math.sin(pygame.time.get_ticks() * 0.01))
            # Draw aura as a larger rectangle behind the enemy
            aura_rect = self.rect.inflate(pulse, pulse)
            # Create a surface for alpha blending
            aura_surface = pygame.Surface((aura_rect.width, aura_rect.height))
            aura_surface.set_alpha(100)
            aura_surface.fill((255, 100, 100))
            screen.blit(aura_surface, aura_rect.topleft)

        elif self.visual_state == "retreating":
            # Yellow warning triangle above retreating enemies
            triangle_points = [
                (center_x, center_y - 25),
                (center_x - 8, center_y - 15),
                (center_x + 8, center_y - 15)
            ]
            pygame.draw.polygon(screen, (255, 255, 0), triangle_points)

        elif self.visual_state == "coordinating":
            # Blue coordination indicator
            pygame.draw.circle(screen, (100, 150, 255), (center_x, center_y - 20), 5)

    def _draw_health_bar(self, screen):
        """Draw a health bar above the enemy"""
        bar_width = self.rect.width
        bar_height = 4
        bar_x = self.rect.x
        bar_y = self.rect.y - 8

        # Background (red)
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # Health (green to red gradient based on health percentage)
        health_percentage = self.health / self.max_health
        health_width = int(bar_width * health_percentage)

        if health_percentage > 0.6:
            health_color = (0, 255, 0)  # Green
        elif health_percentage > 0.3:
            health_color = (255, 255, 0)  # Yellow
        else:
            health_color = (255, 0, 0)  # Red

        if health_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))