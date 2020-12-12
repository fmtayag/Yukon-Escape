# Import libraries =============================================================
try:
    import pygame, os, random, math
    from itertools import repeat
    from data.scripts.sprites import Player, Obstacle, Snowmobile, Snowball, Barrier
    from data.scripts.constants import *
    from data.scripts.draw import draw_background, draw_text, draw_hp, shake
except ImportError as e:
    print(e)
    exit()

# Initialize pygame ============================================================
pygame.init()
pygame.mouse.set_visible(False) # Hide the mouse

# Program variables ============================================================
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
# Other
offset = repeat((0, 0)) # For screen shake

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

window_icon = load_png("placeholder.png", IMG_DIR, 1)
pygame.display.set_icon(window_icon)

player_img = load_png("player.png", IMG_DIR, 4)
snowmobile_img = load_png("snowmobile.png", IMG_DIR, 4)
snowball_img = load_png("snowball.png", IMG_DIR, 4)
e_bullet_img = load_png("e_bullet.png", IMG_DIR, 6)
placeholder_img = load_png("placeholder.png", IMG_DIR, 4)
background_img = load_png("background.png", IMG_DIR, 4)
background_rect = background_img.get_rect()
parallax_img = load_png("parallax.png", IMG_DIR, 4)
parallax_rect = parallax_img.get_rect()

# Sounds =======================================================================

def load_sound(filename, sfx_dir, volume):
    path = os.path.join(sfx_dir, filename)
    snd = pygame.mixer.Sound(path)
    snd.set_volume(volume)
    return snd

# Spawner Functions ============================================================

def spawn_obstacle():
    o = Obstacle(placeholder_img)
    sprites.add(o)
    enemies.add(o)

def spawn_snowmobile():
    s = Snowmobile(snowmobile_img, e_bullet_img)
    sprites.add(s)
    enemies.add(s)

def spawn_snowball():
    sb = Snowball(snowball_img, window)
    snowballs.add(sb)
    enemies.add(sb)

def spawn_barrier():
    b = Barrier(placeholder_img)
    sprites.add(b)
    enemies.add(b)

def roll_spawn():
    enemies = ["snowball", "obstacle", "snowmobile", "barrier"]
    roll = None
    
    # Generate choices and get roll
    choices = random.choices(enemies, [0.25, 0.25, 0.25, 0.25], k=10)
    roll = random.choice(choices)

    # Run spawner functions
    if roll == "obstacle":
        spawn_obstacle()
    elif roll == "snowball":
        spawn_snowball()
    elif roll == "snowmobile":
        spawn_snowmobile()
    elif roll == "barrier":
        spawn_barrier()

# Game loop ====================================================================

running = True
in_menu = False
in_game = True
in_gameover = False

while running:

    # Reset / initialize the score, and others
    score = 0
    background_y = 0 # For the background's y coordinate
    parallax_y = 0 # For the parallax's y coordinate
    sprites.empty()
    enemies.empty()

    # Initialize the player
    player = Player(player_img)
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

    while in_game:

        # Increment the background's and parallax's y positions
        background_y += 4
        parallax_y += 6

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
                        player.spdx = -6
                    else:
                        player.spdx = -4
                elif event.key == pygame.K_d:
                    if player.spdx >= 4:
                        player.spdx = 6
                    else:
                        player.spdx = 4

        # Update processes =====================================================

        if len(enemies) < 8:
            roll_spawn()

        pygame.sprite.groupcollide(impacted_snowballs, bullets, False, True)

        hits = pygame.sprite.groupcollide(impacted_snowballs, enemies, False, False)
        for hit in hits:
            hit.movspd = 4

        for sb in snowballs:
            if sb.impacted and not sb.shaked:
                offset = shake(15, sb.image.get_height() % 10)
                sb.shaked = True
                snowballs.remove(sb)
                impacted_snowballs.add(sb)

        sprites.update()
        snowballs.update()
        impacted_snowballs.update()
        bullets.update()

        # Draw processes =======================================================

        draw_background(window, background_img, background_rect, background_y)
        sprites.draw(window)
        snowballs.draw(window)
        impacted_snowballs.draw(window)
        bullets.draw(window)
        draw_background(window, parallax_img, parallax_rect, parallax_y)
        window.blit(window, next(offset)) # Screen shake

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
