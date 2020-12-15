# Constants
import pygame

# Window Data ==================================================================
WIN_RES = {"W": 600, "H": 680}
TITLE = "Avalanche Escape"
AUTHOR = "zyenapz"
VERSION = "1.0"

# Colors =======================================================================
LIGHT_GREEN = (155,188,15)
SNOW_WHITE = (245, 245, 255)

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

# Movement =====================================================================
SPRITE_MOVESPEED = 7