from entity import Entity
import pygame
from sys import exit


class Player(Entity):
    def __init__(self, rect, color):
        super().__init__(rect, color)
        self.vely = 0
        self.velx = 0
        self.speed = 2
        self.jump_power = 4

    def update(self, gravity, static_list, keys, farpoint):
        self.vely += gravity

        self.velx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed

        for static in static_list:
            if static.rect.colliderect(pygame.Rect(self.rect.x + self.velx, self.rect.y, self.rect.width, self.rect.height)):
                self.velx = 0

            if static.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.vely, self.rect.width, self.rect.height)):
                if self.vely < 0:
                    self.rect.top = static.rect.bottom
                    self.vely = 0
                elif self.vely > 0:
                    self.rect.bottom = static.rect.top
                    self.vely = 0

            if static.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + 3, self.rect.width, self.rect.height)) and keys[pygame.K_SPACE]:
                self.vely = -self.jump_power
                self.rect.y -= 5

        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > farpoint:
            self.rect.right = farpoint
