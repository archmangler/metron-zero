import json
import os
from datetime import datetime

class SaveSystem:
    def __init__(self, game):
        self.game = game
        self.save_folder = "saves"
        self.ensure_save_directory()
    
    def ensure_save_directory(self):
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
    
    def save_game(self, slot=1):
        save_data = {
            'player': {
                'position': (self.game.player.rect.x, self.game.player.rect.y),
                'health': self.game.player.health,
                'weapons': [(w.name, w.damage, w.price) for w in self.game.player.weapons],
                'current_weapon_index': self.game.player.current_weapon_index
            },
            'enemies': [
                {
                    'type': enemy.enemy_type,
                    'position': (enemy.rect.x, enemy.rect.y),
                    'health': enemy.health
                }
                for enemy in self.game.enemies
            ],
            'npc_inventory': [
                {
                    'name': weapon['name'],
                    'damage': weapon['damage'],
                    'price': weapon['price']
                }
                for weapon in self.game.weapons_vendor.weapons_inventory
            ],
            'quests': self.game.quest_manager.get_save_data(),
            'inventory': self.game.player.inventory.get_save_data(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        filename = f"{self.save_folder}/save_slot_{slot}.json"
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=4)
        
        return True
    
    def load_game(self, slot=1):
        try:
            filename = f"{self.save_folder}/save_slot_{slot}.json"
            with open(filename, 'r') as f:
                save_data = json.load(f)
            
            # Restore player state
            self.game.player.rect.x, self.game.player.rect.y = save_data['player']['position']
            self.game.player.health = save_data['player']['health']
            self.game.player.weapons = []
            for weapon_data in save_data['player']['weapons']:
                self.game.player.add_weapon(Weapon(*weapon_data))
            self.game.player.current_weapon_index = save_data['player']['current_weapon_index']
            
            # Restore enemies
            self.game.enemies.empty()
            for enemy_data in save_data['enemies']:
                enemy = Enemy(
                    enemy_data['position'][0],
                    enemy_data['position'][1],
                    enemy_data['type']
                )
                enemy.health = enemy_data['health']
                self.game.enemies.add(enemy)
                self.game.all_sprites.add(enemy)
            
            # Restore NPC inventory
            self.game.weapons_vendor.weapons_inventory = save_data['npc_inventory']
            
            # Restore quests and inventory
            self.game.quest_manager.load_save_data(save_data['quests'])
            self.game.player.inventory.load_save_data(save_data['inventory'])
            
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False 