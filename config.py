import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
SAVES_DIR = os.path.join(BASE_DIR, 'saves')

# Asset paths
PLAYER_SPRITE = os.path.join(IMAGES_DIR, 'knight.png')
ENEMY1_SPRITE = os.path.join(IMAGES_DIR, 'enemy-1.png')
ENEMY2_SPRITE = os.path.join(IMAGES_DIR, 'enemy-2.png')
NPC_SPRITE = os.path.join(IMAGES_DIR, 'civilian-1.png')

# Sound paths
SWORD_SWING_SOUND = os.path.join(SOUNDS_DIR, 'sword_swing.wav')
HIT_SOUND = os.path.join(SOUNDS_DIR, 'hit.wav')
PLAYER_HURT_SOUND = os.path.join(SOUNDS_DIR, 'player_hurt.wav')
ITEM_PICKUP_SOUND = os.path.join(SOUNDS_DIR, 'item_pickup.wav')
BACKGROUND_MUSIC = os.path.join(SOUNDS_DIR, 'background_music.wav')

# ... (rest of the config settings remain the same) ... 