import pygame
from config import *
from .weapons import Weapon, WeaponManager
from .inventory import Inventory
import math
from .animation import DirectionalAnimation

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game  # Store reference to game
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
        
        # Health properties
        self.max_health = 100
        self.health = self.max_health
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1000  # milliseconds
        
        # Attack properties
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

        # Inventory system
        self.inventory = Inventory()
        self.inventory.visible = False  # Start with inventory hidden

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
        """Check for and handle NPC interactions"""
        # Check collision with NPCs
        for npc in npcs:
            if self.rect.colliderect(npc.rect):
                # Get keyboard input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:  # Press E to interact
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

class Inventory:
    def __init__(self):
        self.items = []
        self.visible = False
        self.max_items = 20  # Maximum inventory size
        
    def add_item(self, item):
        """Add an item to inventory if there's space"""
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        """Remove an item from inventory"""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def has_item(self, item_name):
        """Check if inventory contains an item by name"""
        return any(item.name == item_name for item in self.items)
    
    def toggle_visibility(self):
        """Toggle inventory visibility"""
        self.visible = not self.visible
    
    def draw(self, screen):
        """Draw inventory if visible"""
        if not self.visible:
            return
            
        # Draw inventory background
        inventory_surface = pygame.Surface((400, 300))
        inventory_surface.fill((50, 50, 50))  # Dark gray background
        
        # Draw border
        pygame.draw.rect(inventory_surface, (200, 200, 200), 
                        inventory_surface.get_rect(), 2)  # Light gray border
        
        # Draw title
        font = pygame.font.Font(None, 36)
        title = font.render("Inventory", True, (255, 255, 255))
        inventory_surface.blit(title, (10, 10))
        
        # Draw items
        item_font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            y_pos = 50 + i * 30
            if y_pos < 280:  # Prevent drawing outside inventory window
                text = item_font.render(f"{item.name} x{item.quantity}", True, (255, 255, 255))
                inventory_surface.blit(text, (20, y_pos))
        
        # Position inventory in center of screen
        screen_rect = screen.get_rect()
        inventory_rect = inventory_surface.get_rect(center=screen_rect.center)
        screen.blit(inventory_surface, inventory_rect) 