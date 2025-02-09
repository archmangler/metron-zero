import pygame
from config import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.load_sounds()
    
    def load_sounds(self):
        try:
            self.sounds = {
                'sword_swing': pygame.mixer.Sound(ASSETS_DIR + 'sword_swing.wav'),
                'hit': pygame.mixer.Sound(ASSETS_DIR + 'hit.wav'),
                'player_hurt': pygame.mixer.Sound(ASSETS_DIR + 'player_hurt.wav'),
                'item_pickup': pygame.mixer.Sound(ASSETS_DIR + 'item_pickup.wav')
            }
            
            # Set default volumes
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
                
        except pygame.error:
            print("Warning: Sound files could not be loaded")
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_file):
        try:
            pygame.mixer.music.load(ASSETS_DIR + music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 for loop
        except pygame.error:
            print(f"Warning: Music file {music_file} could not be loaded")
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume) 
