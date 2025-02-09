import pygame
from config import *
from .weapons import Weapon
import random

class NPC(pygame.sprite.Sprite):  # Make sure the class is named NPC, not npc
    def __init__(self, x, y):
        super().__init__()
        # Load NPC sprite
        try:
            self.image = pygame.image.load(NPC_SPRITE).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_SIZE, ENEMY_SIZE))
        except pygame.error:
            self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
            self.image.fill(GREEN)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # NPC properties
        self.weapons_inventory = []
        self.has_weapons = False
        self.restock_timer = 0
        self.restock_delay = 300  # Frames between restocks
        
        # Initial stock
        self.restock_inventory()
    
    def restock_inventory(self):
        if random.random() < 0.5:  # 50% chance to restock
            self.weapons_inventory = [
                {
                    'name': 'Iron Sword',
                    'damage': 20,
                    'price': 150
                },
                {
                    'name': 'Steel Axe',
                    'damage': 25,
                    'price': 200
                }
            ]
            self.has_weapons = True
        else:
            self.weapons_inventory = []
            self.has_weapons = False

    def interact(self, player):
        if self.has_weapons:
            # Show available weapons
            print("Available weapons:")  # Replace with proper UI implementation
            for weapon in self.weapons_inventory:
                print(f"{weapon['name']} - Damage: {weapon['damage']} - Price: {weapon['price']}")
        else:
            print("I will go out and look for weapons parts. Please come back later.")

    def update(self, *args):
        # Attempt to restock periodically
        self.restock_timer += 1
        if self.restock_timer >= self.restock_delay:
            self.restock_timer = 0
            self.restock_inventory()
