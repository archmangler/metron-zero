import pygame
from config import *
from .weapons import Weapon, WeaponManager
from .inventory import Inventory
import math
from .animation import DirectionalAnimation

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Initialize directional animation
        self.animation = DirectionalAnimation()
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        
        # Movement
        self.speed = PLAYER_SPEED
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_update = pygame.time.get_ticks()
        
        # Combat
        self.health = PLAYER_HEALTH
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.attacking = False
        
        # Weapons
        self.weapons = []
        self.current_weapon_index = 0
        self.attack_cooldown = 0
        
        # Initialize with a basic weapon
        self.add_weapon(Weapon('Basic Sword', 10, 100))

    def update(self, terrain_manager, obstacles):
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Get input
        keys = pygame.key.get_pressed()
        
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0
        is_moving = False
        direction = self.animation.current_direction
        
        # Movement and direction
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            direction = 'left'
            is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            direction = 'right'
            is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
            direction = 'up'
            is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed
            direction = 'down'
            is_moving = True
            
        # Attack input
        if keys[pygame.K_SPACE]:
            self.attacking = True
        else:
            self.attacking = False
        
        # Update animation
        self.animation.update(dt, direction, is_moving)
        self.image = self.animation.get_current_frame()
        
        # Apply terrain movement penalty
        current_terrain = terrain_manager.get_terrain_at_position(
            self.rect.centerx, 
            self.rect.centery
        )
        terrain_penalty = TERRAIN_MOVEMENT_PENALTIES.get(current_terrain, 1.0)
        self.velocity_x *= terrain_penalty
        self.velocity_y *= terrain_penalty
        
        # Move X
        self.rect.x += self.velocity_x
        self.handle_collision(obstacles, 'x')
        
        # Move Y
        self.rect.y += self.velocity_y
        self.handle_collision(obstacles, 'y')
        
        # Update invulnerability
        if self.invulnerable:
            self.invulnerable_timer += 1
            if self.invulnerable_timer >= INVULNERABILITY_FRAMES:
                self.invulnerable = False
                self.invulnerable_timer = 0
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def handle_collision(self, obstacles, direction):
        for obstacle in obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                if direction == 'x':
                    if self.velocity_x > 0:  # Moving right
                        self.rect.right = obstacle.rect.left
                    else:  # Moving left
                        self.rect.left = obstacle.rect.right
                else:  # direction == 'y'
                    if self.velocity_y > 0:  # Moving down
                        self.rect.bottom = obstacle.rect.top
                    else:  # Moving up
                        self.rect.top = obstacle.rect.bottom

    def interact(self, npcs):
        # Check for nearby NPCs to interact with
        for npc in npcs:
            distance = math.sqrt(
                (self.rect.centerx - npc.rect.centerx) ** 2 +
                (self.rect.centery - npc.rect.centery) ** 2
            )
            if distance <= INTERACTION_RADIUS:
                npc.interact(self)

    def update_facing_direction(self):
        # Update facing direction based on movement
        if self.velocity_x != 0 or self.velocity_y != 0:
            self.facing_direction = pygame.math.Vector2(
                self.velocity_x, self.velocity_y).normalize()

    def attack(self, target_group):
        if not self.current_weapon or not self.current_weapon.can_attack():
            return
        
        # Calculate attack area based on facing direction and weapon range
        attack_range = self.current_weapon.range
        attack_point = (
            self.rect.centerx + self.facing_direction.x * attack_range,
            self.rect.centery + self.facing_direction.y * attack_range
        )
        
        # Check for hits
        for target in target_group:
            distance = math.sqrt(
                (target.rect.centerx - attack_point[0]) ** 2 +
                (target.rect.centery - attack_point[1]) ** 2
            )
            
            if distance <= attack_range:
                self.apply_hit(target)
        
        # Start weapon cooldown
        self.current_weapon.current_cooldown = self.current_weapon.cooldown

    def apply_hit(self, target):
        # Apply damage and knockback
        target.take_damage(self.current_weapon.damage)
        
        # Calculate knockback direction
        knockback = self.facing_direction * KNOCKBACK_FORCE
        target.rect.x += knockback.x
        target.rect.y += knockback.y

    @property
    def current_weapon(self):
        return self.weapons[self.current_weapon_index] if self.weapons else None

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def switch_weapon(self):
        if len(self.weapons) > 1:
            self.current_weapon_index = (self.current_weapon_index + 1) % len(self.weapons)

    def take_damage(self, amount):
        if self.invulnerable:
            return
        self.health -= amount
        self.invulnerable = True
        self.invulnerable_timer = 0 
