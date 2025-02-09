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
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 200  # milliseconds
        self.attack_damage = 25
        self.attack_range = 50
        self.direction = 'right'  # Default direction
        
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
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
            self.direction = 'left'
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
            self.direction = 'right'
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
            self.direction = 'up'
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
            self.direction = 'down'
        
        # Apply movement
        self.rect.x += dx
        self.rect.y += dy
        
        # Update attack
        if self.is_attacking:
            if current_time - self.attack_timer > self.attack_duration:
                self.is_attacking = False
        
        # Update invulnerability
        if self.invulnerable:
            if current_time - self.invulnerable_timer > INVULNERABILITY_FRAMES:
                self.invulnerable = False
        
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

    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = pygame.time.get_ticks()

    def get_attack_rect(self):
        """Get the rectangle representing the attack hitbox"""
        attack_rect = self.rect.copy()
        
        # Extend the attack rect based on direction
        if self.direction == 'right':
            attack_rect.width += self.attack_range
        elif self.direction == 'left':
            attack_rect.x -= self.attack_range
            attack_rect.width += self.attack_range
        elif self.direction == 'up':
            attack_rect.y -= self.attack_range
            attack_rect.height += self.attack_range
        elif self.direction == 'down':
            attack_rect.height += self.attack_range
        
        return attack_rect

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
