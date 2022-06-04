import pygame


class Entity:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, display, xcamera, ycamera):
        pygame.draw.rect(display, self.color, pygame.Rect(self.rect.x + xcamera, self.rect.y + ycamera, self.rect.width, self.rect.height))
