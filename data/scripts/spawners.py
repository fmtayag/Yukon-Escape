import pygame, random
from data.scripts.sprites import Obstacle, Fracture, Debris, Bouncy, Shadow, Particle
from data.scripts.constants import particles_coins, particles, WIN_RES

def spawn_obstacle(obstacle_imgs, enemies, obstacles, sprites):
    o = Obstacle(obstacle_imgs)
    # Spawn sprite only if it does not overlap with any other sprite
    hits = pygame.sprite.spritecollide(o, enemies, False)
    if len(hits) == 0:
        sprites.add(o)
        enemies.add(o)
        obstacles.add(o)

def spawn_fracture(fracture_imgs, fracture_group, enemies, sprites):
    f = Fracture(fracture_imgs)
    hits_fractures = pygame.sprite.spritecollide(f, fracture_group, False)
    hits_enemies = pygame.sprite.spritecollide(f, enemies, False)
    if len(hits_fractures) == 0 and len(hits_enemies) == 0:
        sprites.add(f)
        enemies.add(f)
        fracture_group.add(f)

def spawn_debris(window, debris_imgs, debris_group, enemies, shadows_list, sprites):
    # Spawn debris
    d = Debris(debris_imgs, window)
    hits_debris = pygame.sprite.spritecollide(d, debris_group, False)
    hits_enemies = pygame.sprite.spritecollide(d, enemies, False)
    
    if len(hits_debris) == 0 and len(hits_enemies) == 0:
        sprites.add(d)
        enemies.add(d)
        debris_group.add(d)

        # Spawn shadow
        spawn_shadow(window, d, shadows_list)

def spawn_bouncies(window, bouncies):
    for _ in range(5):
        b = Bouncy(window)
        bouncies.append(b)

def spawn_shadow(window, debris, shadows_list):
    shadow = Shadow(window, debris, debris.rect.centerx, debris.max_disty)
    shadows_list.append(shadow)

def spawn_particles(window, x, y, amnt, colors, launch_type, GAME_FONT):
    for _ in range(amnt):
        p = Particle(window, WIN_RES, random.randrange(x-10,x), random.randrange(y-10,y), colors, launch_type, GAME_FONT)
        if launch_type == "coins":
            particles_coins.append(p)
        else:
            particles.append(p)