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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Metron-Zero")
        self.clock = pygame.time.Clock()
        
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
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies = pygame.sprite.Group()
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
        
        # Spawn initial enemies
        self.spawn_enemies()

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'playing':
                        self.state = 'paused'
                    elif self.state == 'paused':
                        self.state = 'playing'
                
                elif event.key == pygame.K_i:
                    if self.state == 'playing':
                        self.state = 'inventory'
                        self.player.inventory.visible = True
                    elif self.state == 'inventory':
                        self.state = 'playing'
                        self.player.inventory.visible = False
                
                elif event.key == pygame.K_e and self.state == 'playing':
                    self.player.interact(self.npcs)
                
                elif event.key == pygame.K_SPACE and self.state == 'playing':
                    self.handle_combat()
                
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
        # Update player
        self.player.update(self.terrain_manager, self.obstacles)
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update(self.player, self.terrain_manager, self.obstacles)
        
        # Check collisions
        self.check_collisions()
        
        # Update camera
        self.camera.update(self.player)
        
        # Update UI
        self.ui.update()
        
        # Update particles
        self.particles.update()
        
        # Check game over condition
        if self.player.health <= 0:
            self.state = 'game_over'

    def render(self):
        # Draw background
        self.screen.blit(self.backgrounds[self.current_background], (0, 0))
        
        if self.state == 'playing' or self.state == 'inventory':
            # Draw terrain
            self.terrain_manager.draw(self.screen, self.camera)
            
            # Draw game objects relative to camera
            for sprite in sorted([self.player] + list(self.enemies) + list(self.obstacles), 
                               key=lambda s: s.rect.bottom):
                self.screen.blit(sprite.image, self.camera.apply(sprite))
            
            # Draw effects
            for effect in self.effects:
                effect.draw(self.screen)
            
            # Draw particles
            self.particles.draw(self.screen, self.camera)
            
            # Draw UI elements
            self.draw_ui()
            
            # Draw inventory if open
            if self.state == 'inventory':
                self.player.inventory.draw(self.screen)
        
        elif self.state == 'paused':
            self.draw_pause_menu()
        
        elif self.state == 'menu':
            self.menu.draw(self.screen)
        
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
        # Check player-enemy collisions
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(self.player, enemy):
                if not self.player.invulnerable:
                    self.player.health -= enemy.damage
                    self.player.invulnerable = True
                    self.particles.create_hit_effect(
                        self.player.rect.centerx,
                        self.player.rect.centery
                    )
                    
                    # Check if player died
                    if self.player.health <= 0:
                        self.state = 'game_over'  # Just change the state instead of calling show_game_over

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
                
                # Draw game over screen
                self.menu.draw(self.screen)
            
            # Maintain consistent frame rate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
