import pygame
from config import *
from .weapons import Weapon
import random

class NPC(pygame.sprite.Sprite):  # Make sure the class is named NPC, not npc
    def __init__(self, x, y, npc_type):
        super().__init__()
        self.npc_type = npc_type
        
        # Load appropriate sprite based on NPC type
        try:
            self.image = pygame.image.load(f"assets/images/npcs/{npc_type}.png").convert_alpha()
        except:
            # Create colored rectangle as fallback
            self.image = pygame.Surface((32, 32))
            if npc_type == 'merchant':
                self.image.fill((255, 215, 0))  # Gold for merchant
            elif npc_type == 'healer':
                self.image.fill((255, 182, 193))  # Pink for healer
            else:  # quest_giver
                self.image.fill((147, 112, 219))  # Purple for quest giver
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Interaction cooldown
        self.last_interaction = 0
        self.interaction_cooldown = 1000  # 1 second cooldown
        
        # Set NPC properties based on type
        if npc_type == 'merchant':
            self.interaction_text = "Press E to trade"
        elif npc_type == 'healer':
            self.interaction_text = "Press E to heal"
        else:  # quest_giver
            self.interaction_text = "Press E for quest"
        
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
        """Handle player interaction based on NPC type"""
        current_time = pygame.time.get_ticks()
        
        # Check cooldown
        if current_time - self.last_interaction < self.interaction_cooldown:
            return
        
        self.last_interaction = current_time
        
        if self.npc_type == 'merchant':
            print("Trading with merchant...")  # Debug output
            # TODO: Open trade menu
            player.game.ui.show_message("Welcome to my shop!")
        
        elif self.npc_type == 'healer':
            if player.health < player.max_health:
                heal_amount = 50
                old_health = player.health
                player.health = min(player.health + heal_amount, player.max_health)
                actual_heal = player.health - old_health
                print(f"Healed player for {actual_heal} health")  # Debug output
                player.game.ui.show_message(f"Healed for {actual_heal} health!")
            else:
                player.game.ui.show_message("You are already at full health!")
        
        elif self.npc_type == 'quest_giver':
            print("Getting quest...")  # Debug output
            player.game.ui.show_message("Here's a quest for you!")

    def update(self):
        # NPCs don't move, but could have idle animations
        pass
