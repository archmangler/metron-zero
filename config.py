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

# Terrain sprites
SEA_SPRITE = os.path.join(IMAGES_DIR, 'sea.png')
DESERT_SPRITE = os.path.join(IMAGES_DIR, 'desert.png')
HELLSCAPE_SPRITE = os.path.join(IMAGES_DIR, 'hellscape.png')

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
INVULNERABILITY_FRAMES = 60
KNOCKBACK_FORCE = 10

# Terrain settings
CHUNK_SIZE = 64
TERRAIN_MOVEMENT_PENALTIES = {
    'sea': 0.5,
    'desert': 0.7,
    'hellscape': 1.0
}

# Make sure required directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(SOUNDS_DIR, exist_ok=True)
os.makedirs(SAVES_DIR, exist_ok=True)

# Verify assets exist
def verify_assets():
    required_images = [
        PLAYER_SPRITE,
        ENEMY1_SPRITE,
        ENEMY2_SPRITE,
        NPC_SPRITE,
        SEA_SPRITE,
        DESERT_SPRITE,
        HELLSCAPE_SPRITE
    ]
    
    missing_assets = []
    for image_path in required_images:
        if not os.path.exists(image_path):
            missing_assets.append(os.path.basename(image_path))
    
    if missing_assets:
        print("Warning: Missing game assets:", missing_assets)
        print("Using placeholder images instead.")
        return False
    return True

# Run asset verification
USING_REAL_ASSETS = verify_assets()

# ... (rest of the config settings remain the same) ... 
