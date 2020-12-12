import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, WIN_RES, images, sprites):
        super().__init__()
        self.WIN_RES = WIN_RES
        self.image = images
        self.rect = self.image.get_rect()
        self.rect.centerx = self.WIN_RES["W"] * 0.2
        self.rect.bottom = self.WIN_RES["H"] * 0.9
        # Sprite groups
        self.sprites = sprites
        # For speed
        self.spdx = 0 

    def update(self):

        # Limit player speed
        if self.spdx > 8:
            self.spdx = 8
        elif self.spdx < -8:
            self.spdx = -8

        # Move player on the x-axis
        self.rect.x += self.spdx

        self.check_oob()

    def check_oob(self):
        # Check if sprite is out of bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.spdx = 0
        elif self.rect.right > self.WIN_RES["W"]:
            self.rect.right = self.WIN_RES["W"]
            self.spdx = 0