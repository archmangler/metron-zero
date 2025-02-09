import pygame
import sys
import os
import math
import random
import importlib
from config import *
from .player import Player
from .enemy import Enemy
from .npc import NPC
from .environment import TerrainManager
from .weapons import WeaponManager
from .effects import ParticleEffect, AnimationManager
from .sound import SoundManager
from .menu import Menu
from .save_system import SaveSystem
from .inventory import Inventory
from .quest import QuestManager
from .ui import UI
from .particles import ParticleSystem
from .camera import Camera

# Force reload the terrain module
from . import terrain
importlib.reload(terrain)

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()  # Initialize the audio system
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Metron-Zero")
        self.clock = pygame.time.Clock()
        
        # Load sound effects
        try:
            self.hit_sound = pygame.mixer.Sound("assets/sounds/hit.wav")
            self.hit_sound.set_volume(0.3)  # Adjust volume as needed
        except:
            print("Warning: Could not load hit sound")
            self.hit_sound = None
        
        # Initialize game systems
        self.animation_manager = AnimationManager()
        self.sound_manager = SoundManager()
        self.save_system = SaveSystem(self)
        self.quest_manager = QuestManager()
        self.menu = Menu(self)
        self.effects = []
        
        # Initialize sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        # Game state
        self.state = 'menu'  # 'menu', 'playing', 'inventory', 'paused'
        self.current_background = 'hellscape'
        
        # Load backgrounds
        self.backgrounds = self.load_backgrounds()
        
        # Initialize terrain
        self.terrain_manager = terrain.TerrainManager()
        self.terrain_manager.generate_terrain()
        
        # Add terrain obstacles to obstacle group
        self.obstacles.add(self.terrain_manager.obstacles)
        
        # Initialize new systems
        self.weapon_manager = WeaponManager()
        
        # Initialize camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize UI
        self.ui = UI(self)
        
        # Initialize particles
        self.particles = ParticleSystem()
        
        # Setup initial game state
        self.setup_game()
        
        # Start background music
        self.sound_manager.play_music('background_music.wav')

    def load_backgrounds(self):
        try:
            return {
                'sea': pygame.transform.scale(
                    pygame.image.load(os.path.join(IMAGES_DIR, 'sea.png')).convert_alpha(),
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
                ),
                'desert': pygame.transform.scale(
                    pygame.image.load(os.path.join(IMAGES_DIR, 'desert.png')).convert_alpha(),
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
                ),
                'hellscape': pygame.transform.scale(
                    pygame.image.load(os.path.join(IMAGES_DIR, 'hellscape.png')).convert_alpha(),
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
            }
        except pygame.error as e:
            print(f"Warning: Could not load background images: {e}")
            # Create fallback solid color backgrounds
            fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fallback.fill((100, 100, 100))  # Gray color
            return {
                'sea': fallback.copy(),
                'desert': fallback.copy(),
                'hellscape': fallback.copy()
            }

    def setup_game(self):
        # Initialize game objects
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self)
        self.enemies = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.particles = ParticleSystem()
        
        # Initialize camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize terrain with explicit import
        self.terrain_manager = terrain.TerrainManager()
        
        # Add terrain obstacles to game obstacles
        self.obstacles.add(self.terrain_manager.obstacles)
        
        # Initialize UI
        self.ui = UI(self)
        
        # Initialize score
        self.score = 0
        
        # Spawn initial enemies and NPCs
        self.spawn_enemies()
        self.spawn_npcs()

    def spawn_enemies(self):
        # Clear existing enemies
        self.enemies.empty()
        
        # Spawn new enemies
        for _ in range(5):  # Spawn 5 enemies
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            enemy_type = random.choice(['enemy1', 'enemy2'])
            enemy = Enemy(x, y, enemy_type)
            self.enemies.add(enemy)

    def spawn_npcs(self):
        """Spawn NPCs at random positions"""
        # Clear existing NPCs
        self.npcs.empty()
        
        # Spawn 3 NPCs
        npc_types = ['merchant', 'healer', 'quest_giver']
        for npc_type in npc_types:
            # Spawn NPC away from player start position
            while True:
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
                
                # Check distance from player start position
                dx = x - SCREEN_WIDTH // 2
                dy = y - SCREEN_HEIGHT // 2
                distance = (dx * dx + dy * dy) ** 0.5
                
                if distance > 200:  # Minimum distance from player
                    npc = NPC(x, y, npc_type)
                    self.npcs.add(npc)
                    break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'menu'
                elif event.key == pygame.K_t:
                    self.ui.toggle_radar()
                elif event.key == pygame.K_SPACE:
                    if self.state == 'game_over':
                        self.setup_game()
                        self.state = 'playing'
                    else:
                        self.player.attack()  # Trigger attack on space
                elif event.key == pygame.K_i:
                    if self.state == 'playing':
                        self.state = 'inventory'
                        self.player.inventory.visible = True
                    elif self.state == 'inventory':
                        self.state = 'playing'
                        self.player.inventory.visible = False
                
                elif event.key == pygame.K_e and self.state == 'playing':
                    self.player.interact(self.npcs)
                
                # Quick save/load for testing
                elif event.key == pygame.K_F5:
                    self.save_system.save_game()
                    self.create_effect("Save successful!", (SCREEN_WIDTH//2, 50), GREEN)
                elif event.key == pygame.K_F9:
                    if self.save_system.load_game():
                        self.create_effect("Load successful!", (SCREEN_WIDTH//2, 50), GREEN)
                    else:
                        self.create_effect("No save file found!", (SCREEN_WIDTH//2, 50), RED)
            
            # Handle inventory item usage
            if self.state == 'inventory' and event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_inventory_click(event.pos)
        
        return True

    def handle_combat(self):
        if self.player.current_weapon:
            self.sound_manager.play_sound('sword_swing')
            hit_enemies = pygame.sprite.spritecollide(
                self.player, self.enemies, False,
                pygame.sprite.collide_mask
            )
            
            for enemy in hit_enemies:
                enemy.take_damage(self.player.current_weapon.damage)
                self.create_hit_effect(enemy.rect.center)
                self.sound_manager.play_sound('hit')
                
                # Update quest progress if enemy dies
                if enemy.health <= 0:
                    self.quest_manager.update_quest_progress("QUEST_001", 0)

    def create_hit_effect(self, position):
        effect = ParticleEffect(position[0], position[1], RED)
        self.effects.append(effect)

    def create_effect(self, text, position, color):
        # Create floating text effect
        pass  # Implement text effect system

    def handle_inventory_click(self, pos):
        if self.player.inventory.visible:
            clicked_item = self.player.inventory.get_clicked_item(pos)
            if clicked_item:
                clicked_item.use(self.player)

    def update(self):
        if self.state == 'playing':
            # Update player
            self.player.update(self.terrain_manager, self.obstacles)
            
            # Handle NPC interactions
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:  # E key for interaction
                for npc in self.npcs:
                    if pygame.sprite.collide_rect(self.player, npc):
                        npc.interact(self.player)
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.player, self.terrain_manager, self.obstacles)
            
            # Check collisions
            self.check_collisions()
            
            # Check victory condition
            if len(self.enemies) == 0:
                self.state = 'victory'
            
            # Update camera
            self.camera.update(self.player)
            
            # Update UI
            self.ui.update()
            
            # Update particles
            self.particles.update()

    def render(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw terrain
        self.terrain_manager.draw(self.screen, self.camera)
        
        # Draw all game objects relative to camera
        for sprite in sorted(
            [self.player] + 
            list(self.enemies) + 
            list(self.npcs) +  # Add NPCs to rendering
            list(self.obstacles), 
            key=lambda s: s.rect.bottom
        ):
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        # Draw particles
        self.particles.draw(self.screen, self.camera)
        
        # Draw UI (not affected by camera)
        self.ui.draw(self.screen)
        
        # Update display
        pygame.display.flip()

    def draw_ui(self):
        # Draw player health
        health_text = f"Health: {self.player.health}"
        health_surface = pygame.font.Font(None, 36).render(health_text, True, WHITE)
        self.screen.blit(health_surface, (10, 10))
        
        # Draw current weapon
        if self.player.current_weapon:
            weapon_text = f"Weapon: {self.player.current_weapon.name}"
            weapon_surface = pygame.font.Font(None, 36).render(weapon_text, True, WHITE)
            self.screen.blit(weapon_surface, (10, 50))
        
        # Draw active quests
        self.draw_quest_tracker()

    def draw_quest_tracker(self):
        y_offset = 100
        for quest in self.quest_manager.active_quests.values():
            quest_text = f"{quest.title}: "
            for objective in quest.objectives:
                quest_text += f"{objective.current_amount}/{objective.required_amount}"
            
            quest_surface = pygame.font.Font(None, 24).render(quest_text, True, WHITE)
            self.screen.blit(quest_surface, (10, y_offset))
            y_offset += 30

    def draw_pause_menu(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause menu options
        pause_text = pygame.font.Font(None, 74).render("PAUSED", True, WHITE)
        self.screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))

    def check_collisions(self):
        # Check player-enemy collisions for damage to player
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(self.player, enemy):
                if not self.player.invulnerable:
                    self.player.health -= enemy.damage
                    self.player.invulnerable = True
                    
                    # Play hit sound
                    if self.hit_sound:
                        self.hit_sound.play()
                    
                    # Create hit effect
                    self.particles.create_hit_effect(
                        self.player.rect.centerx,
                        self.player.rect.centery
                    )
                    
                    # Check if player died
                    if self.player.health <= 0:
                        self.state = 'game_over'
        
        # Check player attack collisions with enemies
        if self.player.is_attacking:
            attack_rect = self.player.get_attack_rect()
            for enemy in self.enemies:
                if attack_rect.colliderect(enemy.rect):
                    # Play hit sound
                    if self.hit_sound:
                        self.hit_sound.play()
                    
                    # Create hit effect
                    self.particles.create_hit_effect(
                        enemy.rect.centerx,
                        enemy.rect.centery
                    )
                    
                    # Damage and possibly kill enemy
                    enemy.take_damage(self.player.attack_damage)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 100  # Add score for killing enemy

    def run(self):
        running = True
        while running:
            # Handle events based on game state
            if self.state == 'menu':
                running = self.menu.handle_events()
                self.menu.draw(self.screen)
            elif self.state == 'playing':
                running = self.handle_events()
                self.update()
                self.render()
            elif self.state == 'game_over':
                # Handle game over events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.setup_game()
                            self.state = 'playing'
                        elif event.key == pygame.K_ESCAPE:
                            self.state = 'menu'
                self.menu.draw(self.screen)
            elif self.state == 'victory':
                # Handle victory events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.setup_game()
                            self.state = 'playing'
                        elif event.key == pygame.K_ESCAPE:
                            self.state = 'menu'
                self.menu.draw(self.screen)
            
            # Maintain consistent frame rate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
