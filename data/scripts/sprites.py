import pygame, random
from data.scripts.constants import *

class Player(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.image = images
        self.image_orig = images
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_RES["W"] / 2
        self.rect.bottom = WIN_RES["H"] * 0.9
        self.direction = "forward"
        # For speed
        self.spdx = 0
        self.movspd = 6

    def update(self):

        self.spdx = 0
        self.image = self.image_orig

        # Get pressed key
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.spdx = -self.movspd
            self.rotate_img(8)
        elif pressed[pygame.K_d]:
            self.spdx = self.movspd
            self.rotate_img(-8)

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

    def rotate_img(self, degree):
        old_x = self.rect.centerx
        old_y = self.rect.centery
        self.image = pygame.transform.rotate(self.image, degree)
        self.rect.centerx = old_x
        self.rect.centery = old_y

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(64, WIN_RES["W"]-64)
        self.rect.y = random.randrange(-256, -128)
        self.movspd = SPRITE_MOVESPEED
        self.spdy = self.movspd
    
    def update(self):
        
        self.rect.y += self.spdy

        if self.rect.top > WIN_RES["H"]:
            self.kill()

class Debris(pygame.sprite.Sprite):
    def __init__(self, images, window):
        super().__init__()
        self.images = images
        size = random.randrange(200,232)
        self.img_roll = random.randrange(0, len(images))
        self.image = pygame.transform.scale(self.images["normal"][self.img_roll], (size, size))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(64, WIN_RES["W"]-64)
        self.rect.centery = random.randrange(WIN_RES["H"]*1.2, WIN_RES["H"]*1.5)
        self.window = window
        self.impacted = False
        self.img_changed = False
        self.movspd = SPRITE_MOVESPEED
        self.spdx = self.calc_spdx()
        self.shaked = False # Bool if it has shaked the screen. See game loop.
        # The point at which the object will stop moving on the y-axis
        self.max_disty = random.randrange(96, WIN_RES["H"] * 0.2)
        # For shrinking
        self.shrink_timer = pygame.time.get_ticks()
        self.shrink_delay = 120
        self.scaler = 0

    def update(self):

        # Stop on the specified y-axis line
        if self.rect.top < self.max_disty:
            self.impacted = True

        if self.impacted:
            self.rect.y += self.movspd
            if self.img_changed == False:
                self.change_image()
                self.img_changed = True
        else: 
            self.rect.y -= random.randrange(7,9)
            self.rect.x += self.spdx
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

    def change_image(self):
        old_x = self.rect.centerx
        old_y = self.rect.centery
        x_scale = self.image.get_width() - self.scaler
        y_scale = self.image.get_height() - self.scaler
        self.image = pygame.transform.scale(self.images["impacted"][self.img_roll], (x_scale, y_scale))
        self.rect.centerx = old_x
        self.rect.centery = old_y

    def calc_spdx(self):
        if self.rect.centerx > WIN_RES["W"] / 2:
            return -2
        elif self.rect.centerx < WIN_RES["W"] / 2:
            return 2
        else:
            return random.choice([-2,2])

class Particle():
    def __init__(self, window, WIN_RES, x, y, colors, launch_type):
        self.window = window
        self.WIN_RES = WIN_RES
        self.x = x
        self.y = y
        self.color = random.choice(colors)
        self.launch_type = launch_type
        if self.launch_type == "explosion":
            self.spdx = random.choice([num for num in range(-8,8) if num not in [-2,-1,0,1,2]])
            self.spdy = random.choice([num for num in range(-8,8) if num not in [-2,-1,0,1,2]])
            self.size = random.choice([4,8])
        elif self.launch_type == "trail":
            self.spdx = 0
            self.spdy = SPRITE_MOVESPEED
            self.size = 8
            self.y = self.y -32

    def update(self):
        self.x += self.spdx
        self.y += self.spdy
        if self.launch_type == "explosion":
            pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size))
        elif self.launch_type == "trail":
            pygame.draw.circle(self.window, self.color, (self.x+2, self.y), self.size)

# Unused ================================================================================================

class Snowmobile(pygame.sprite.Sprite):
    # UNUSED
    def __init__(self, image, bullet_img):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(64, WIN_RES["W"]-64)
        self.rect.y = random.randrange(WIN_RES["H"] + 64, WIN_RES["H"] + 256)
        self.bullet_img = bullet_img
        self.movspd = SPRITE_MOVESPEED
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