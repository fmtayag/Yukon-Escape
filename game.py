# Import libraries =============================================================
try:
    import pygame, os, random, math
    from itertools import repeat
    from data.scripts.sprites import Player, Obstacle, Snowmobile, Debris, Particle
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

window_icon = load_png("player.png", IMG_DIR, 1)
pygame.display.set_icon(window_icon)

# Player image
player_img = load_png("player.png", IMG_DIR, 4)

# Obstacle images
obstacle_imgs = [load_png("obstacle1.png", IMG_DIR, 6),
                 load_png("obstacle2.png", IMG_DIR, 6),
                 load_png("obstacle3.png", IMG_DIR, 6),
                 load_png("obstacle4.png", IMG_DIR, 6),
                 load_png("obstacle5.png", IMG_DIR, 6),
                 load_png("obstacle6.png", IMG_DIR, 6),
                 load_png("obstacle7.png", IMG_DIR, 6)]

# Debris images
debris_imgs = dict()
debris_normal_imgs = [load_png("debris1.png", IMG_DIR, 8),
                      load_png("debris2.png", IMG_DIR, 8)]
debris_imgs["normal"] = debris_normal_imgs

debris_impacted_imgs = [load_png("debris1_impacted.png", IMG_DIR, 8),
                        load_png("debris2_impacted.png", IMG_DIR, 8)] 
debris_imgs["impacted"] = debris_impacted_imgs                  

# OTher images
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
    o = Obstacle(obstacle_imgs)
    # Spawn sprite only if it does not overlap with any other sprite
    hits = pygame.sprite.spritecollide(o, enemies, False)
    if len(hits) == 0:
        sprites.add(o)
        enemies.add(o)

def spawn_snowmobile():
    s = Snowmobile(snowmobile_img, e_bullet_img)
    sprites.add(s)
    enemies.add(s)

def spawn_debris():
    d = Debris(debris_imgs, window)
    debris_group.add(d)
    enemies.add(d)

def spawn_particles(x, y, amnt, colors, launch_type):
    for _ in range(amnt):
        p = Particle(window, WIN_RES, random.randrange(x-10,x), random.randrange(y-10,y), colors, launch_type)
        particles.append(p)

def update_particles():
    for p in particles:
        p.update()

        if (p.x < -p.size or
            p.x > p.WIN_RES["W"] + p.size or
            p.y < -p.size or
            p.y > p.WIN_RES["H"] + p.size):
                particles.remove(p)
                del p

def roll_spawn():
    enemies = ["debris", "obstacle"]
    roll = None
    
    # Generate choices and get roll
    choices = random.choices(enemies, [0.25, 0.75], k=10)
    roll = random.choice(choices)

    # Run spawner functions
    if roll == "obstacle":
        spawn_obstacle()
    elif roll == "debris":
        spawn_debris()

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
    particles[:] = []

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
        background_y += SPRITE_MOVESPEED
        parallax_y += (SPRITE_MOVESPEED + 1)

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

        # Spawn enemies
        if len(enemies) < 3:
            roll_spawn()

        # Produce particle explosion if debris impacted
        for d in debris_group:
            if d.impacted and not d.shaked:
                offset = shake(15, 5)
                d.shaked = True
                debris_group.remove(d)
                impacted_debris.add(d)
                spawn_particles(d.rect.centerx, d.rect.centery, random.randrange(30,40), [(125,149,162)], "explosion")

        # Spawn trail for player
        spawn_particles(player.rect.centerx, player.rect.bottom, random.randrange(5,10), [(185,191,251)], "trail")

        # Update sprite groups
        sprites.update()
        debris_group.update()
        impacted_debris.update()
        bullets.update()

        # Draw processes =======================================================

        draw_background(window, background_img, background_rect, background_y)
        update_particles()
        sprites.draw(window)
        impacted_debris.draw(window)
        debris_group.draw(window)
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
