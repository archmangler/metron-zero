import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
SAVES_DIR = os.path.join(BASE_DIR, 'saves')

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

# Player settings
PLAYER_SPEED = 5
PLAYER_SIZE = 64
PLAYER_HEALTH = 100
INTERACTION_RADIUS = 50

# Enemy settings
ENEMY_SPEED = 3
ENEMY_SIZE = 64
ENEMY_DETECTION_RADIUS = 200
ENEMY_HEALTH = 50

# Enemy spawn positions
ENEMY1_SPAWN_POSITIONS = [
    (100, 100),
    (700, 100),
    (100, 500)
]

ENEMY2_SPAWN_POSITIONS = [
    (700, 500),
    (400, 400)
]

# Weapon settings
WEAPON_COOLDOWN = 30
DEFAULT_WEAPON_RANGE = 50

# Combat settings
INVULNERABILITY_FRAMES = 30
KNOCKBACK_FORCE = 10

# Terrain settings
CHUNK_SIZE = 200
TERRAIN_MOVEMENT_PENALTIES = {
    'sea': 0.5,
    'desert': 0.7,
    'hellscape': 1.0
}

# ... (rest of the config settings remain the same) ... 