import pygame
import math
import random
from config import *
from .enemy_animation import EnemyAnimation

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="enemy1"):
        super().__init__()
        self.enemy_type = enemy_type
        self.animation = EnemyAnimation(enemy_type)
        self.image = self.animation.get_current_frame()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        
        # Movement
        self.speed = ENEMY_SPEED
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_update = pygame.time.get_ticks()
        
        # Combat
        self.health = 100
        self.max_health = 100
        self.damage = 10
        self.attack_cooldown = 0
        self.attack_range = 100
        self.detection_range = 300
        
        # AI
        self.state = 'idle'
        self.target = None
        self.path = []
        self.path_update_timer = 0
        self.path_update_delay = 1000  # Update path every second
    
    def update(self, player, terrain_manager, obstacles):
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Calculate distance to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Update state based on distance
        if distance <= self.attack_range:
            self.state = 'attack'
        elif distance <= self.detection_range:
            self.state = 'walk'
        else:
            self.state = 'idle'
        
        # Update facing direction
        self.animation.facing_right = dx > 0
        
        # Handle movement based on state
        if self.state == 'walk':
            # Move towards player
            angle = math.atan2(dy, dx)
            self.velocity_x = math.cos(angle) * self.speed
            self.velocity_y = math.sin(angle) * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
        
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
        
        # Update animation
        self.animation.update(dt, self.state, self.state == 'walk')
        self.image = self.animation.get_current_frame()
    
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
    
    def take_damage(self, amount):
        """Take damage and return True if enemy dies"""
        self.health -= amount
        return self.health <= 0 
