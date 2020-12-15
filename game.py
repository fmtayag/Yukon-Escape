# Import libraries =============================================================
try:
    import pygame, os, random, math
    from itertools import repeat
    from data.scripts.sprites import Player, Obstacle, Fracture, Debris, Particle
    from data.scripts.constants import *
    from data.scripts.draw import draw_background, draw_text, shake
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
speed_timer = pygame.time.get_ticks()

# Other
GAME_FONT = os.path.join(FONT_DIR, "prstartk.ttf")
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
                 load_png("obstacle7.png", IMG_DIR, 6),
                 load_png("obstacle8.png", IMG_DIR, 6)]

# Fracture images
fracture_imgs = [load_png("fracture1.png", IMG_DIR, 6),
                 load_png("fracture2.png", IMG_DIR, 6),
                 load_png("fracture3.png", IMG_DIR, 6),
                 load_png("fracture4.png", IMG_DIR, 6),
                 load_png("fracture5.png", IMG_DIR, 6),
                 load_png("fracture6.png", IMG_DIR, 6),
                 load_png("fracture7.png", IMG_DIR, 6),
                 load_png("fracture8.png", IMG_DIR, 6)]

# Debris images
debris_imgs = dict()
debris_normal_imgs = [load_png("debris1.png", IMG_DIR, 8),
                      load_png("debris2.png", IMG_DIR, 8)]
debris_imgs["normal"] = debris_normal_imgs

debris_impacted_imgs = [load_png("debris1_impacted.png", IMG_DIR, 8),
                        load_png("debris2_impacted.png", IMG_DIR, 8)] 
debris_imgs["impacted"] = debris_impacted_imgs                  

# Other images
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

explosions_sfx = [ load_sound("explosion1.wav", SFX_DIR, 0.5),
                   load_sound("explosion2.wav", SFX_DIR, 0.5),
                   load_sound("explosion3.wav", SFX_DIR, 0.5) ]

# Spawner Functions ============================================================

def spawn_obstacle():
    o = Obstacle(obstacle_imgs)
    # Spawn sprite only if it does not overlap with any other sprite
    hits = pygame.sprite.spritecollide(o, enemies, False)
    if len(hits) == 0:
        sprites.add(o)
        enemies.add(o)
        obstacles.add(o)

def spawn_fracture():
    f = Fracture(fracture_imgs)
    hits_fractures = pygame.sprite.spritecollide(f, fracture_group, False)
    hits_enemies = pygame.sprite.spritecollide(f, enemies, False)
    if len(hits_fractures) == 0 and len(hits_enemies) == 0:
        sprites.add(f)
        enemies.add(f)
        fracture_group.add(f)

def spawn_debris():
    d = Debris(debris_imgs, window)
    hits_debris = pygame.sprite.spritecollide(d, debris_group, False)
    hits_enemies = pygame.sprite.spritecollide(d, enemies, False)
    if len(hits_debris) == 0 and len(hits_enemies) == 0:
        sprites.add(d)
        enemies.add(d)
        debris_group.add(d)

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

def roll_spawn(score, enemies, probability):
    roll = None
    
    # Generate choices and get roll
    choices = random.choices(enemies, probability, k=10)
    roll = random.choice(choices)

    # Run spawner functions
    if roll == "obstacle":
        spawn_obstacle()
    elif roll == "debris":
        spawn_debris()
    elif roll == "fracture":
        spawn_fracture()

# Game loop ====================================================================

running = True
in_menu = True
in_game = False
in_gameover = False

while running:

    # Reset / initialize the score, and others
    score = 0
    background_y = 0 # For the background's y coordinate
    parallax_y = 0 # For the parallax's y coordinate
    warmup_timer = pygame.time.get_ticks()
    warmup_duration = 3000
    disable_keys_timer = pygame.time.get_ticks()
    player_group.empty()
    enemies.empty()
    obstacles.empty()
    debris_group.empty()
    impdebris_group.empty()
    fracture_group.empty()
    particles[:] = []

    # Initialize the player
    player = Player(player_img)
    sprites.add(player)
    player_group.add(player)

    while in_menu:
        
        # Increment the background's and parallax's y positions
        background_y += SPRITE_MOVESPEED
        parallax_y += (SPRITE_MOVESPEED + 1)

        # Lock the FPS
        clock.tick(FPS)

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    in_menu = False 
                    in_game = True
                elif event.key == pygame.K_d:
                    in_menu = False 
                    running = False

        # Draw processes =======================================================

        draw_background(window, background_img, background_rect, background_y)
        draw_background(window, parallax_img, parallax_rect, parallax_y)
        draw_text(window, f"Avalanche", 54, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.1, (0,0,0), "centered")
        draw_text(window, f"Escape!", 65, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.2, (0,0,0), "centered")
        draw_text(window, f"powered by pygame", 24, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.3, (125,125,125), "centered")
        draw_text(window, f"[A] Play", 32, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.4, (0,0,0), "centered")
        draw_text(window, f"[D] Exit", 32, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.45, (0,0,0), "centered")

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

        # Player entry
        if not player.spawned:
            player.rect.y -= 3
            if player.rect.bottom <= player.spawn_y:
                player.spawned = True

        # Check collision between player and enemies
        hits = pygame.sprite.groupcollide(enemies, player_group, False, False, pygame.sprite.collide_circle)
        for hit in hits:
            if type(hit) == Debris:
                if hit.impacted:
                    player.has_collided = True
            elif type(hit) == Fracture:
                if hit.fractured:
                    player.has_collided = True
            else:
                player.has_collided = True

        # Check collision between impacted debris and obstacles
        hits = pygame.sprite.groupcollide(obstacles, impdebris_group, False, False)
        for hit in hits:
            spawn_particles(hit.rect.centerx, hit.rect.top, random.randrange(30,40), hit.palette, "explosion")
            hit.kill()
                    
        # End the game if player has collided
        if player.has_collided:
            offset = shake(30,5)
            in_game = False
            in_gameover = True
            spawn_particles(player.rect.centerx, player.rect.top, random.randrange(30,40), [(125,149,162)], "explosion")
            player.spdy = SPRITE_MOVESPEED
            disable_keys_timer = pygame.time.get_ticks()
            random.choice(explosions_sfx).play()

        now = pygame.time.get_ticks()
        if now - warmup_timer > warmup_duration:
            # Add score
            score += 0.1
                
            # Calculate enemy count
            enemy_count = (score**2) / (10**4)
            if enemy_count > 11:
                enemy_count = 11

            # Spawn enemies if no. of enemies is less than enemy count
            if len(enemies) < enemy_count:
                if score < 100:
                    roll_spawn(score, ["obstacle", "debris", "fracture"], [8,1,1])
                else:
                    roll_spawn(score, ["obstacle", "debris", "fracture"], [7,1,2])

        # Produce particle explosion and sound if debris impacted
        for d in debris_group:
            if d.impacted and not d.shaked:
                offset = shake(15, 5)
                d.shaked = True
                debris_group.remove(d)
                impdebris_group.add(d)
                enemies.add(d)
                spawn_particles(d.rect.centerx, d.rect.centery, random.randrange(30,40), [(125,149,162)], "explosion")
                random.choice(explosions_sfx).play()

        # Produce shaking and sound if fracture has opened up
        for f in fracture_group:
            if f.fractured:
                offset = shake(20,5)
                fracture_group.remove(f)
                opfracture_group.add(f)
                enemies.add(f)
                random.choice(explosions_sfx).play()
                
        # Spawn trail for player
        spawn_particles(player.rect.centerx, player.rect.bottom, 5, [(163,167,194)], "trail")

        # Update sprites group
        sprites.update()

        # Draw processes =======================================================
        draw_background(window, background_img, background_rect, background_y)
        update_particles()
        fracture_group.draw(window)
        obstacles.draw(window)
        opfracture_group.draw(window)
        impdebris_group.draw(window)
        player_group.draw(window)
        debris_group.draw(window)
        now = pygame.time.get_ticks()
        if now - warmup_timer < warmup_duration * 0.8:
            draw_text(window, f"Get Ready!", 48, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.4, (0,0,0), "centered")
        draw_text(window, f"Score", 24, GAME_FONT, 10, 10, (0,0,0))
        draw_text(window, f"{math.trunc(score)}", 24, GAME_FONT, 10, 50, (0,0,0))
        draw_background(window, parallax_img, parallax_rect, parallax_y)
        window.blit(window, next(offset)) # Screen shake

        # Update the window
        pygame.display.flip()

    while in_gameover:
        
        # Increment the background's and parallax's y positions
        background_y += SPRITE_MOVESPEED
        parallax_y += (SPRITE_MOVESPEED + 1)

        # Lock the FPS
        clock.tick(FPS)

        keys_enabled = False
        now = pygame.time.get_ticks()
        if now - disable_keys_timer > 2000:
            keys_enabled = True

        # Get input ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_gameover = False
            elif event.type == pygame.KEYDOWN and keys_enabled:
                if event.key == pygame.K_a:
                    in_gameover = False
                    in_menu = True
                elif event.key == pygame.K_d:
                    in_gameover = False
                    in_game = True

        # Update processes =====================================================

        # Spawn enemies
        enemy_count = (score**2) / (8**4)
        if enemy_count > 10:
            enemy_count = 10
        if len(enemies) < enemy_count:
            roll_spawn(score, ["obstacle", "debris", "fracture"],[10,0,0])

        # Update sprites group
        sprites.update()

        # Draw processes =======================================================

        draw_background(window, background_img, background_rect, background_y)
        update_particles()
        fracture_group.draw(window)
        obstacles.draw(window)
        impdebris_group.draw(window)
        opfracture_group.draw(window)
        player_group.draw(window)
        debris_group.draw(window)
        draw_text(window, f"Score", 24, GAME_FONT, 10, 10, (0,0,0))
        draw_text(window, f"{math.trunc(score)}", 24, GAME_FONT, 10, 50, (0,0,0))
        draw_text(window, f"GAME OVER!", 48, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.3, (0,0,0), "centered")
        draw_text(window, f"Your score is", 24, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.4, (0,0,0), "centered")
        draw_text(window, f"{math.trunc(score)}", 28, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.45, (0,0,0), "centered")
        draw_background(window, parallax_img, parallax_rect, parallax_y)
        now = pygame.time.get_ticks()
        if keys_enabled:
            draw_text(window, f"[A] Menu", 28, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.55, (0,0,0), "centered")
            draw_text(window, f" [D] Retry", 28, GAME_FONT, WIN_RES["W"] / 2, WIN_RES["H"] * 0.6, (0,0,0), "centered")
        window.blit(window, next(offset))

        # Update the window
        pygame.display.flip()

# Quit pygame
pygame.quit()
