# Constants
import pygame, os

# Window Data ==================================================================
WIN_RES = {"W": 600, "H": 680}
TITLE = "Yukon Escape"
AUTHOR = "zyenapz"
VERSION = "1.0"

# FPS ==========================================================================
FPS = 60

# Colors =======================================================================
LIGHT_GREEN = (155,188,15)
SNOW_WHITE = (245, 245, 255)
BLACK = (27,31,33)
GRAY = (104,111,153)

# Sprite groups ================================================================
sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
debris_group = pygame.sprite.Group()
impdebris_group = pygame.sprite.Group()
fracture_group = pygame.sprite.Group()
opfracture_group = pygame.sprite.Group() # Opened fracture
player_group = pygame.sprite.Group()
particles = list()
particles_coins = list()

# Threat system ================================================================
# [obstacle, debris, fracture]
spawn_odds = dict()
spawn_odds["tectonics"] = [0, 0, 10]
spawn_odds["forest"] = [10, 0, 0]
spawn_odds["debris"] = [0, 10, 0]
spawn_odds["normal"] = [8, 1, 1]
spawn_odds["hard"] = [6,2,2]

MAX_THREAT_ENEMIES = dict()
MAX_THREAT_ENEMIES["tectonics"] = 10
MAX_THREAT_ENEMIES["forest"] = 24
MAX_THREAT_ENEMIES["debris"] = 7

# Movement =====================================================================
SPRITE_MOVESPEED = 8
PARALLAX_MOVESPEED = 10