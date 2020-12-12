import pygame, random
from data.scripts.constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.image = images
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_RES["W"] / 2
        self.rect.bottom = WIN_RES["H"] * 0.9
        # For speed
        self.spdx = 0 

    def update(self):

        self.spdx = 0

        # Get pressed key
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.spdx = -6
        if pressed[pygame.K_d]:
            self.spdx = 6

        # Move sprite on the x-axis
        self.rect.x += self.spdx

        self.check_oob()

    def check_oob(self):
        # Check if sprite is out of bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.spdx = 0
        elif self.rect.right > WIN_RES["W"]:
            self.rect.right = WIN_RES["W"]
            self.spdx = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(64, WIN_RES["W"]-64)
        self.rect.y = random.randrange(-256, -32)
        self.movspd = 4
        self.spdy = self.movspd
    
    def update(self):
        
        self.rect.y += self.spdy

        if self.rect.top > WIN_RES["H"]:
            self.kill()

class Barrier(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.rotate(image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([0, WIN_RES["W"]-64])
        self.rect.y = random.randrange(-256, -32)
        self.movspd = 4
        self.spdy = self.movspd
    
    def update(self):
        
        self.rect.y += self.spdy

        if self.rect.top > WIN_RES["H"]:
            self.kill()

class Snowmobile(pygame.sprite.Sprite):
    def __init__(self, image, bullet_img):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(64, WIN_RES["W"]-64)
        self.rect.y = random.randrange(WIN_RES["H"] + 64, WIN_RES["H"] + 256)
        self.bullet_img = bullet_img
        self.spdx = 0
        self.spdy = 6
        self.spawned = False
        # The point at which the object will stop moving on the y-axis
        self.max_disty = random.randrange(96, WIN_RES["H"] * 0.4)
        # For shooting
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_delay = random.randrange(800, 1000)

    def update(self):

        if self.rect.top < WIN_RES["H"]:
            self.spawned = True

        # Stop on the specified y-axis line
        if self.rect.top < self.max_disty:
            self.shoot()
            self.set_spdx()

            self.spdy -= 0.2
            if self.spdy <= 0:
                self.spdy = 0

        # Move the sprite
        self.rect.x += self.spdx 
        self.rect.y -= self.spdy

        # Kill sprite if it moves off screen
        if ((self.rect.top > WIN_RES["H"] and self.spawned) or 
             self.rect.right < 0 or
             self.rect.left > WIN_RES["W"]):
            self.kill()

    def set_spdx(self):
        if self.spdx == 0:
            if self.rect.centerx > WIN_RES["W"] / 2:
                self.spdx = -2
            elif self.rect.centerx < WIN_RES["W"] / 2:
                self.spdx = 2
            else:
                self.spdx = random.choice([-2,2])

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = now
            b = Bullet(self.bullet_img, self.rect.centerx, self.rect.bottom)
            bullets.add(b)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, xpos, ypos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.top = ypos

    def update(self):

        # Kill the object if it is out of bounds
        if self.rect.top > WIN_RES["H"]:
            self.kill()
        
        # Move the sprite
        self.rect.y += 14

class Snowball(pygame.sprite.Sprite):
    def __init__(self, image, window):
        super().__init__()
        self.image = pygame.transform.scale(image, (192, 192))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(64, WIN_RES["W"]-64)
        self.rect.y = random.randrange(WIN_RES["H"]*1.2, WIN_RES["H"]*1.5)
        self.window = window
        self.impacted = False
        self.shaked = False # Bool if it has shaked the screen. See game loop.
        # The point at which the object will stop moving on the y-axis
        self.max_disty = random.randrange(45, WIN_RES["H"] * 0.2)
        # For shrinking
        self.shrink_timer = pygame.time.get_ticks()
        self.shrink_delay = 140
        self.scaler = 0

    def update(self):

        # Stop on the specified y-axis line
        if self.rect.top < self.max_disty:
            self.impacted = True

        if self.impacted:
            self.rect.y += 4
        else: 
            self.rect.y -= 8
            self.shrink()

        if self.impacted and self.rect.top > WIN_RES["H"]:
            self.kill()

    def shrink(self):
        now = pygame.time.get_ticks()
        if now - self.shrink_timer > self.shrink_delay:
            old_x = self.rect.centerx
            old_y = self.rect.centery
            self.shrink_timer = now
            x_scale = self.image.get_width() - self.scaler
            y_scale = self.image.get_height() - self.scaler
            self.image = pygame.transform.scale(self.image, (x_scale,y_scale))
            self.rect = self.image.get_rect()
            self.rect.centerx = old_x
            self.rect.centery = old_y
            self.scaler += 1