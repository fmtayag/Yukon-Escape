import pygame, random
from data.scripts.constants import *
from data.scripts.draw import draw_text

# Draw radius
#temp_rect = self.image.get_rect()
#pygame.draw.circle(self.image, (255,0,0), temp_rect.center, self.radius)

class Player(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.image = images
        self.image_orig = images
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_RES["W"] / 2
        self.rect.bottom = WIN_RES["H"] + 64
        self.spawn_y = WIN_RES["H"] * 0.9
        self.spawned = False
        self.direction = "forward"
        self.has_collided = False
        # For speed
        self.spdx = 0
        self.movspd = 6
        self.spdy = 0
        # For collision
        self.radius = 16

    def update(self):
        if self.spawned:
            if not self.has_collided:
                self.spdx = 0
                self.image = self.image_orig

                # Get pressed key
                pressed = pygame.key.get_pressed()
                
                if pressed[pygame.K_a]:
                    self.spdx = -self.movspd
                    self.rotate_img(40)
                elif pressed[pygame.K_d]:
                    self.spdx = self.movspd
                    self.rotate_img(-40)

                # Draw radius
                #temp_rect = self.image.get_rect()
                #pygame.draw.circle(self.image, (255,0,0), temp_rect.center, self.radius)

                # Move sprite on the x-axis
                self.rect.x += self.spdx
                
                self.check_oob()
            else:
                self.rect.y += self.spdy
            

    def check_oob(self):
        # Check if sprite is out of bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.spdx = 0
        elif self.rect.right > WIN_RES["W"]:
            self.rect.right = WIN_RES["W"]
            self.spdx = 0

    def rotate_img(self, angle):
        orig_rect = self.image.get_rect()
        rot_image = pygame.transform.rotate(self.image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.palette = list()
        self.image = self.roll_img(images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIN_RES["W"]-64)
        self.rect.y = random.randrange(-1028, -128)
        self.spdy = SPRITE_MOVESPEED
        # For collision
        self.radius = 28

    def update(self):
        
        # Draw radius
        #temp_rect = self.image.get_rect()
        #pygame.draw.circle(self.image, (255,0,0), temp_rect.center, self.radius)

        self.rect.y += self.spdy

        if self.rect.top > WIN_RES["H"]:
            self.kill()

    def roll_img(self, images):
        img_list = images
        choices = random.choices(img_list, [8,8,8,1,1,1,1,1], k=10)
        choice = random.choice(choices)
        
        # Get color information of the surface
        self.palette.append(choice.get_at((32,32)))
        self.palette.append(choice.get_at((42,42)))
        self.palette.append(choice.get_at((32,48)))

        # Return choice
        return choice

class Fracture(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.variant = random.choice(["a", "b"])
        self.images = images[self.variant]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-32, WIN_RES["W"]-64)
        self.rect.y = random.randrange(-512, -128)
        self.spdy = SPRITE_MOVESPEED
        self.fracture_timer = pygame.time.get_ticks()
        self.fracture_delay = random.randrange(250,500)
        self.fractured = False
        # For animation
        self.frame = 0
        self.frame_timer = pygame.time.get_ticks()
        self.frame_delay = 200
        # For collision
        self.radius = 48

    def update(self):

        # Draw radius
        #temp_rect = self.image.get_rect()
        #pygame.draw.circle(self.image, (255,0,0), temp_rect.center, self.radius)

        self.rect.y += self.spdy

        now = pygame.time.get_ticks()
        if now - self.fracture_timer > self.fracture_delay:
            self.animate()

        if self.rect.top > WIN_RES["H"]:
            self.kill()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.frame_timer > self.frame_delay and self.frame != len(self.images) - 1:
            old_rectx = self.rect.x
            old_recty = self.rect.y
            self.frame_timer = now
            self.frame += 1
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect()
            self.rect.x = old_rectx
            self.rect.y = old_recty
            if self.frame == 4:
                self.fractured = True

class Debris(pygame.sprite.Sprite):
    def __init__(self, images, window):
        super().__init__()
        self.images = images
        size = random.randrange(200,232)
        self.img_roll = random.randrange(0, len(images))
        self.image = pygame.transform.scale(self.images["normal"][self.img_roll], (size, size))
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(64, WIN_RES["W"]-64)
        self.rect.centery = WIN_RES["H"]*1.2
        self.window = window
        self.impacted = False
        self.img_changed = False
        self.spdy = SPRITE_MOVESPEED
        self.spdx = self.calc_spdx()
        self.shaked = False # Bool if it has shaked the screen. See game loop.
        self.is_above_player = False
        # The point at which the object will stop moving on the y-axis
        self.max_disty = random.randrange(96, WIN_RES["H"] * 0.2)
        # For shrinking
        self.shrink_timer = pygame.time.get_ticks()
        self.shrink_delay = 80
        self.scaler = 0
        # For collision
        self.radius = 64

    def update(self):

        # Draw radius
        #temp_rect = self.image.get_rect()
        #pygame.draw.circle(self.image, (255,0,0), temp_rect.center, self.radius)

        # Stop on the specified y-axis line
        if self.rect.top < self.max_disty:
            self.impacted = True
        
        if self.impacted:
            self.rect.y += self.spdy
            if self.img_changed == False:
                self.change_image()
                self.img_changed = True
                self.radius = self.image.get_width() // 3
        else: 
            self.rect.y -= random.randrange(SPRITE_MOVESPEED+2,SPRITE_MOVESPEED+5)
            self.rect.x += self.spdx
            self.shrink()

        # Delete sprite if it goes off screen
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
            return random.randrange(-7,-1)
        elif self.rect.centerx < WIN_RES["W"] / 2:
            return random.randrange(1,7)
        else:
            return random.choice([-2,2])

class Particle():
    def __init__(self, window, WIN_RES, x, y, colors, launch_type, font):
        self.window = window
        self.font = font
        self.WIN_RES = WIN_RES
        self.x = x
        self.y = y
        self.movspd = SPRITE_MOVESPEED
        self.color = random.choice(colors)
        self.launch_type = launch_type
        if self.launch_type == "explosion":
            self.spdx = random.choice([num for num in range(-8,8) if num not in [-2,-1,0,1,2]])
            self.spdy = random.choice([num for num in range(-6,6) if num not in [-2,-1,0,1,2]])
            self.size = random.choice([8,12])
        elif self.launch_type == "trail":
            self.spdx = 0
            self.spdy = SPRITE_MOVESPEED
            self.size = 16
            self.y = self.y - 32
        elif self.launch_type == "coins":
            self.spdx = random.choice([-1,1])
            self.spdy = -1
            self.size = 16
            self.y = self.y + random.randrange(-16,16)

    def update(self):
        self.x += self.spdx
        self.y += self.spdy
        if self.launch_type == "explosion":
            if self.spdx > 0:
                self.spdx -= 0.1
            if self.spdy < self.movspd:
                self.spdy += 0.1
            elif self.spdy > self.movspd:
                self.spdy -= 0.1
            pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size))
        elif self.launch_type == "trail":
            pygame.draw.rect(self.window, self.color, (self.x-2, self.y, self.size, self.size))
        elif self.launch_type == "coins":
            draw_text(self.window, f"+8", 32, self.font, self.x, self.y, BLACK, "centered")
            self.spdy += 0.5