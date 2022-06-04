import pygame
import pytmx
import tkinter as tk

from tkinter import filedialog
from enemy import Enemy
from player import Player
from static import Static
from sys import exit


class Game:
    def __init__(self):
        root = tk.Tk()
        root.withdraw()

        self.player = None
        self.map = None
        self.font = None
        self.farpoint = 0

        self.FPS = 60
        self.gravity = 0.2

        self.tile_width = 16
        self.tile_height = 16

        self.background_color = (72, 209, 204)

        self.xcamera = 0

        self.screen_size = self.width, self.height = 320, 240
        self.display = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()

        self.static_list = []
        self.enemy_list = []
        self.waypoint_list = []

        # 0 - gameover; 1 - game
        self.state = 0

        self.run()

    def run(self):
        pygame.init()

        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

        pygame.display.set_caption("platformer")

        running = True
        while running:
            self.clock.tick(self.FPS)
            self.display.fill(self.background_color)

            if self.state == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                self.update()
                self.draw()

            if self.state == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: running = False
                    if event.type == pygame.KEYDOWN:
                        self.load_map()
                        self.state = 1
                self.gameoverdraw()

            pygame.display.flip()

    def update(self):
        self.player.update(self.gravity, self.static_list, pygame.key.get_pressed(), self.farpoint)

        for enemy in self.enemy_list:
            enemy.update(self.waypoint_list)
            if self.player.rect.colliderect((enemy.rect.x, enemy.rect.y, enemy.rect.width, enemy.rect.height)):
                self.state = 0

        if self.player.rect.top > self.screen_size[1]:
            self.state = 0

        self.xcamera = -self.player.rect.centerx + self.display.get_rect().centerx

        if self.player.rect.centerx < 0 + self.display.get_rect().centerx:
            self.xcamera = 0
        if self.player.rect.centerx > self.farpoint - self.display.get_rect().centerx:
            self.xcamera = -(self.farpoint - self.display.get_rect().width)

    def draw(self):
        for static in self.static_list: static.draw(self.display, self.xcamera)

        for enemy in self.enemy_list: enemy.draw(self.display, self.xcamera)

        self.player.draw(self.display, self.xcamera)

    def gameoverdraw(self):
        self.display.blit(self.font.render('Press any key', True, (255, 255, 255)),
                          (self.screen_size[0] / 2 - 80, self.screen_size[1] / 2 - 10))

    def load_map(self):
        try:
            file_path = filedialog.askopenfilename()
            self.map = pytmx.load_pygame(file_path)
        except:
            print("Please load a tmx map with static, player, enemy, waypoint layers")
            exit()

        self.tile_height = self.map.tileheight
        self.tile_width = self.map.tilewidth

        self.farpoint = 0

        self.static_list.clear()
        self.enemy_list.clear()
        self.waypoint_list.clear()

        for layer in self.map.visible_layers:
            if layer.name == "static":
                for x, y, gid in layer.tiles():
                    if x * self.tile_width > self.farpoint: self.farpoint = x * self.tile_width
                    self.static_list.append(Static(
                        pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height),
                        (0, 255, 0)))

            if layer.name == "player":
                for x, y, gid in layer.tiles():
                    self.player = Player(
                        pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height),
                        (255, 255, 0))

            if layer.name == "enemy":
                for x, y, gid in layer.tiles():
                    self.enemy_list.append(
                        Enemy(pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height),
                              (255, 0, 0)))

            if layer.name == "waypoint":
                for x, y, gid in layer.tiles():
                    self.waypoint_list.append(
                        pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))


if __name__ == "__main__":
    Game()