import pygame
from ..config import *

class InventoryItem:
    def __init__(self, name, item_type, properties=None):
        self.name = name
        self.item_type = item_type  # 'weapon', 'consumable', 'quest_item'
        self.properties = properties or {}
        self.quantity = 1
    
    def use(self, player):
        if self.item_type == 'consumable':
            if 'healing' in self.properties:
                player.health = min(
                    player.health + self.properties['healing'],
                    PLAYER_HEALTH
                )
            self.quantity -= 1
            return True
        return False

class Inventory:
    def __init__(self, size=20):
        self.size = size
        self.items = []
        self.selected_index = 0
        self.visible = False
        
        # UI elements
        self.font = pygame.font.Font(None, 32)
        self.item_rects = []
        self.setup_ui()
    
    def setup_ui(self):
        self.background = pygame.Surface((400, 300))
        self.background.fill((50, 50, 50))
        self.background.set_alpha(230)
        
        # Create item slots
        for i in range(self.size):
            row = i // 5
            col = i % 5
            rect = pygame.Rect(col * 70 + 10, row * 70 + 10, 60, 60)
            self.item_rects.append(rect)
    
    def add_item(self, item):
        # Check for stackable items
        for existing_item in self.items:
            if existing_item.name == item.name and existing_item.item_type == item.item_type:
                existing_item.quantity += item.quantity
                return True
        
        if len(self.items) < self.size:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, index):
        if 0 <= index < len(self.items):
            item = self.items[index]
            item.quantity -= 1
            if item.quantity <= 0:
                self.items.pop(index)
            return True
        return False
    
    def draw(self, surface):
        if not self.visible:
            return
        
        # Draw background
        inventory_rect = self.background.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        surface.blit(self.background, inventory_rect)
        
        # Draw items
        for i, rect in enumerate(self.item_rects):
            adjusted_rect = rect.copy()
            adjusted_rect.x += inventory_rect.x
            adjusted_rect.y += inventory_rect.y
            
            # Draw slot background
            pygame.draw.rect(surface, (70, 70, 70), adjusted_rect)
            pygame.draw.rect(surface, (100, 100, 100), adjusted_rect, 2)
            
            # Draw item if it exists
            if i < len(self.items):
                item = self.items[i]
                text = self.font.render(item.name[0], True, WHITE)
                text_rect = text.get_rect(center=adjusted_rect.center)
                surface.blit(text, text_rect)
                
                # Draw quantity if more than 1
                if item.quantity > 1:
                    quantity_text = self.font.render(str(item.quantity), True, WHITE)
                    surface.blit(quantity_text, adjusted_rect.bottomright)
    
    def get_save_data(self):
        return [
            {
                'name': item.name,
                'type': item.item_type,
                'properties': item.properties,
                'quantity': item.quantity
            }
            for item in self.items
        ]
    
    def load_save_data(self, data):
        self.items = []
        for item_data in data:
            item = InventoryItem(
                item_data['name'],
                item_data['type'],
                item_data['properties']
            )
            item.quantity = item_data['quantity']
            self.items.append(item) 