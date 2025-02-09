import pygame
from ..config import *
from .weapons import Weapon, WeaponManager
from .inventory import Inventory
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load and scale player image
        try:
            self.image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        except pygame.error:
            # Fallback to a colored rectangle if image loading fails
            self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
            self.image.fill(BLUE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = PLAYER_SPEED
        
        # Game attributes
        self.health = PLAYER_HEALTH
        self.weapons = []
        self.current_weapon_index = 0
        self.invulnerability_frames = 0
        self.facing_direction = pygame.math.Vector2(1, 0)  # Default facing right
        
        # Create a mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # Add starting weapon
        starter_weapon = WeaponManager.create_weapon({
            'name': 'Rusty Sword',
            'damage': 10,
            'price': 0,
            'range': 40
        })
        self.add_weapon(starter_weapon)

    def move(self, obstacles):
        keys = pygame.key.get_pressed()
        
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Handle movement input
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed
            
        # Normalize diagonal movement
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)
        
        # Move X
        self.rect.x += self.velocity_x
        self.handle_collision(obstacles, 'x')
        
        # Move Y
        self.rect.y += self.velocity_y
        self.handle_collision(obstacles, 'y')

    def handle_collision(self, obstacles, direction):
        # Check collision with obstacles
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if direction == 'x':
                    if self.velocity_x > 0:  # Moving right
                        self.rect.right = obstacle.rect.left
                    elif self.velocity_x < 0:  # Moving left
                        self.rect.left = obstacle.rect.right
                elif direction == 'y':
                    if self.velocity_y > 0:  # Moving down
                        self.rect.bottom = obstacle.rect.top
                    elif self.velocity_y < 0:  # Moving up
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

    def update(self, obstacles, *args):
        # Update invulnerability frames
        if self.invulnerability_frames > 0:
            self.invulnerability_frames -= 1
        
        # Update current weapon cooldown
        if self.current_weapon:
            self.current_weapon.update()
        
        # Get terrain effect
        terrain = args[0].get_terrain_at_position(self.rect.centerx, self.rect.centery)
        if terrain:
            self.speed = PLAYER_SPEED * terrain.movement_penalty
        
        self.move(obstacles)
        self.update_facing_direction()

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
        if self.invulnerability_frames <= 0:
            self.health -= amount
            self.invulnerability_frames = INVULNERABILITY_FRAMES
            if self.health <= 0:
                self.kill() 