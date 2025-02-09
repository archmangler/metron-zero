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

# Enemy spawn positions (x, y)
ENEMY1_SPAWN_POSITIONS = [
    (100, 100),
    (700, 100),
    (100, 500)
]

ENEMY2_SPAWN_POSITIONS = [
    (700, 500),
    (400, 400)
]

# Asset paths
ASSETS_DIR = 'assets/'
PLAYER_SPRITE = ASSETS_DIR + 'knight.png'
ENEMY1_SPRITE = ASSETS_DIR + 'enemy-1.png'
ENEMY2_SPRITE = ASSETS_DIR + 'enemy-2.png'
NPC_SPRITE = ASSETS_DIR + 'civilian-1.png'

# Weapon settings
WEAPON_COOLDOWN = 30
DEFAULT_WEAPON_RANGE = 50

# Terrain settings
CHUNK_SIZE = 200
TERRAIN_MOVEMENT_PENALTIES = {
    'sea': 0.5,
    'desert': 0.7,
    'hellscape': 1.0
}

# Combat settings
INVULNERABILITY_FRAMES = 30
KNOCKBACK_FORCE = 10 