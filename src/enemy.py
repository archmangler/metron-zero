import pygame
from config import *
import math
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        
        # Load appropriate sprite based on enemy type
        sprite_path = ENEMY1_SPRITE if enemy_type == 'enemy1' else ENEMY2_SPRITE
        try:
            self.image = pygame.image.load(sprite_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        except pygame.error:
            self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
            self.image.fill(RED)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = ENEMY_SPEED
        self.original_pos = (x, y)
        
        # AI attributes
        self.state = 'patrol'
        self.patrol_timer = 0
        self.patrol_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.detection_radius = ENEMY_DETECTION_RADIUS
        
        # Game attributes
        self.health = ENEMY_HEALTH
        
        # Create mask for better collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def patrol(self):
        # Change direction periodically
        self.patrol_timer += 1
        if self.patrol_timer >= 60:  # Change direction every 60 frames
            self.patrol_timer = 0
            self.patrol_direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        
        # Move in patrol direction
        self.velocity_x = self.patrol_direction[0] * self.speed
        self.velocity_y = self.patrol_direction[1] * self.speed
        
        # Stay within patrol area
        if abs(self.rect.x - self.original_pos[0]) > 100:
            self.patrol_direction = (-self.patrol_direction[0], self.patrol_direction[1])
        if abs(self.rect.y - self.original_pos[1]) > 100:
            self.patrol_direction = (self.patrol_direction[0], -self.patrol_direction[1])

    def chase(self, player):
        # Calculate direction to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance > 0:
            # Normalize direction
            dx = dx / distance
            dy = dy / distance
            
            # Set velocity
            self.velocity_x = dx * self.speed
            self.velocity_y = dy * self.speed
            
            # Enemy type 2 has different chase behavior
            if self.enemy_type == 'enemy2':
                # Moves faster but less accurately
                self.velocity_x *= 1.5
                self.velocity_y *= 1.5
                # Add some randomness to movement
                self.velocity_x += random.uniform(-0.5, 0.5)
                self.velocity_y += random.uniform(-0.5, 0.5)

    def update_ai(self, player):
        # Calculate distance to player
        distance = math.sqrt(
            (player.rect.centerx - self.rect.centerx) ** 2 +
            (player.rect.centery - self.rect.centery) ** 2
        )
        
        # Update state based on player distance
        if distance <= self.detection_radius:
            self.state = 'chase'
        else:
            self.state = 'patrol'
        
        # Execute current state behavior
        if self.state == 'chase':
            self.chase(player)
        else:
            self.patrol()

    def move(self, obstacles):
        # Move X
        self.rect.x += self.velocity_x
        self.handle_collision(obstacles, 'x')
        
        # Move Y
        self.rect.y += self.velocity_y
        self.handle_collision(obstacles, 'y')

    def handle_collision(self, obstacles, direction):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                if direction == 'x':
                    if self.velocity_x > 0:
                        self.rect.right = obstacle.rect.left
                    elif self.velocity_x < 0:
                        self.rect.left = obstacle.rect.right
                elif direction == 'y':
                    if self.velocity_y > 0:
                        self.rect.bottom = obstacle.rect.top
                    elif self.velocity_y < 0:
                        self.rect.top = obstacle.rect.bottom

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self, obstacles, player):
        self.update_ai(player)
        self.move(obstacles) 