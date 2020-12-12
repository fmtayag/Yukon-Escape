# Import libraries =============================================================
try:
    import pygame, os, random, math
    from itertools import repeat
    from data.scripts.sprites import Player
except ImportError as e:
    print(e)
    exit()

# Initialize pygame ============================================================
pygame.init()
pygame.mouse.set_visible(False) # Hide the mouse

# Program variables ============================================================
# Metadata
WIN_RES = {"W": 600, "H": 800}
TITLE = "Avalanche Game" # PLEASE CHANGE LATER PLEASE CHANGE LATER PLEASE CHANGE LATER PLEASE CHANGE LATER
AUTHOR = "zyenapz"
VERSION = "1.0"
# Colors
GREEN_LIGHT = (155,188,15)
# Directories
GAME_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(GAME_DIR, "data")
IMG_DIR = os.path.join(DATA_DIR, "img")
SFX_DIR = os.path.join(DATA_DIR, "sfx")
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
FONT_DIR = os.path.join(DATA_DIR, "font")
# FPS and timing
clock = pygame.time.Clock()
FPS = 60

# Initialize the window ========================================================
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = pygame.display.set_mode((WIN_RES["W"], WIN_RES["H"]))
window_rect = window.get_rect()
pygame.display.set_caption(TITLE)

# Images =======================================================================
def load_png(file, directory, scale):
    try:
        path = os.path.join(directory, file)
        img = pygame.image.load(path).convert_alpha()
        img_w = img.get_width()
        img_h = img.get_height()
        img = pygame.transform.scale(img, (img_w*scale, img_h*scale))
        return img
    except Exception as e:
        print(e)
        exit()

window_icon = load_png("player.png", IMG_DIR, 1) # PLEASE CHANGE LATER PLEASE CHANGE LATER PLEASE CHANGE LATER
pygame.display.set_icon(window_icon)

player_img = load_png("player.png", IMG_DIR, 4)

# Sounds =======================================================================

def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

# Sprite groups ================================================================

sprites = pygame.sprite.Group()

# Game loop ====================================================================

running = True
in_menu = False
in_scores = False
in_game = True
in_gameover = False

while running:

    # Initialize the player
    player = Player(WIN_RES, player_img, sprites)
    sprites.add(player)

    while in_menu:

        # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_menu = False

        # Update processes =====================================================

            # TODO

        # Draw processes =======================================================

            # TODO

        # Update the window
        pygame.display.flip()

    while in_scores:

        # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_scores = False

        # Update processes =====================================================

            # TODO

        # Draw processes =======================================================

            # TODO

        # Update the window
        pygame.display.flip()

    while in_game:

        # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if player.spdx <= -4:
                        player.spdx = -8
                    else:
                        player.spdx = -4
                elif event.key == pygame.K_d:
                    if player.spdx >= 4:
                        player.spdx = 8
                    else:
                        player.spdx = 4

        # Update processes =====================================================

        sprites.update()

        # Draw processes =======================================================

        window.fill(GREEN_LIGHT)
        sprites.draw(window)

        # Update the window
        pygame.display.flip()

    while in_gameover:

        # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_gameover = False

        # Update processes =====================================================

            # TODO

        # Draw processes =======================================================

            # TODO

        # Update the window
        pygame.display.flip()

# Quit pygame
pygame.quit()
