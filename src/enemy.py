import pygame
import math
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type='enemy1'):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Load enemy sprite based on type
        try:
            if enemy_type == 'enemy1':
                self.image = pygame.image.load(ENEMY1_SPRITE).convert_alpha()
            else:
                self.image = pygame.image.load(ENEMY2_SPRITE).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        except pygame.error:
            self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
            self.image.fill(RED if enemy_type == 'enemy1' else (255, 128, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        
        # Movement
        self.speed = ENEMY_SPEED
        self.velocity_x = 0
        self.velocity_y = 0
        
        # AI
        self.state = 'patrol'  # 'patrol' or 'chase'
        self.patrol_point = (x, y)  # Starting position is first patrol point
        self.patrol_timer = 0
        self.patrol_direction = pygame.math.Vector2(1, 0)  # Start moving right
        
        # Combat
        self.health = ENEMY_HEALTH
        self.attack_cooldown = 0
        self.damage = 10
        
        # Behavior specific to enemy type
        if enemy_type == 'enemy1':
            self.patrol_radius = 100
            self.detection_radius = 150
            self.speed = ENEMY_SPEED * 1.2
        else:  # enemy2
            self.patrol_radius = 150
            self.detection_radius = 200
            self.speed = ENEMY_SPEED * 0.8
    
    def update(self, player, obstacles):
        if not isinstance(player, pygame.sprite.Sprite):
            return  # Skip update if player is not valid
            
        self.update_ai(player)
        self.handle_collision(obstacles)
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def update_ai(self, player):
        # Calculate distance to player
        distance = math.sqrt(
            (player.rect.centerx - self.rect.centerx) ** 2 +
            (player.rect.centery - self.rect.centery) ** 2
        )
        
        # Update state based on distance to player
        if distance <= self.detection_radius:
            self.state = 'chase'
        else:
            self.state = 'patrol'
        
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0
        
        if self.state == 'chase':
            # Move towards player
            direction = pygame.math.Vector2(
                player.rect.centerx - self.rect.centerx,
                player.rect.centery - self.rect.centery
            )
            if direction.length() > 0:
                direction = direction.normalize()
                self.velocity_x = direction.x * self.speed
                self.velocity_y = direction.y * self.speed
        else:
            # Patrol behavior
            self.patrol()
        
        # Apply movement
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
    
    def patrol(self):
        # Update patrol timer
        self.patrol_timer += 1
        if self.patrol_timer >= 120:  # Change direction every 2 seconds
            self.patrol_timer = 0
            angle = random.uniform(0, 2 * math.pi)
            self.patrol_direction = pygame.math.Vector2(
                math.cos(angle),
                math.sin(angle)
            )
        
        # Move in patrol direction
        self.velocity_x = self.patrol_direction.x * self.speed
        self.velocity_y = self.patrol_direction.y * self.speed
        
        # Stay within patrol radius
        distance_from_start = math.sqrt(
            (self.rect.centerx - self.patrol_point[0]) ** 2 +
            (self.rect.centery - self.patrol_point[1]) ** 2
        )
        if distance_from_start > self.patrol_radius:
            # Return to patrol area
            direction = pygame.math.Vector2(
                self.patrol_point[0] - self.rect.centerx,
                self.patrol_point[1] - self.rect.centery
            ).normalize()
            self.velocity_x = direction.x * self.speed
            self.velocity_y = direction.y * self.speed
    
    def handle_collision(self, obstacles):
        # Check collision with obstacles
        for obstacle in obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                # Basic collision response
                if self.velocity_x > 0:  # Moving right
                    self.rect.right = obstacle.rect.left
                elif self.velocity_x < 0:  # Moving left
                    self.rect.left = obstacle.rect.right
                if self.velocity_y > 0:  # Moving down
                    self.rect.bottom = obstacle.rect.top
                elif self.velocity_y < 0:  # Moving up
                    self.rect.top = obstacle.rect.bottom
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill() 
