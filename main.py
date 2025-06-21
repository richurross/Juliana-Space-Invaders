from os.path import abspath, dirname
from random import choice, uniform
from os import environ

import pygame

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import *
import os
import sys

RESOLUTION = (1200, 700)
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("For My Girlfriend ❤️")

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#PARAMETERS:
DOGS_COLUMNS = 10
DOGS_ROWS = 4
DOGS_LENGTH = [70, 70]
DOGS_TOP = 80
DOGS_SEPARATION=[10, 10]
DOGS_UPDATE_TIME = 600
DOGS_VELOCITY = 10
DOGS_SHOOT_TIME = 800
DOGS_MOVE_DOWN = 35
DOGS_DART_MULTIPLIER = 2
YANA_LENGTH=[90, 140]
YANA_BOTTOM = 10
YANA_SPEED = 15
YANA_LIVES = 5
DART_LENGTH = [10, 30]
DART_SPEED = [20, 10]
SAND_BLOCKS = 5
SAND_COLUMNS = 10
SAND_ROWS = 3
SAND_LENGTH = [15, 15]
SAND_POSITION = 500
JIMOTHY_LENGTH = [70, 50]
JIMOTHY_MID = 50
JIMOTHY_SPEED = 15
JIMOTHY_INTERVAL = 5000
LIFE_LENGTH = [25, 25]
LATERAL_LIMIT = 10
RESOLUTION = (1200, 700)
NEW_ROUND_TIME = 3000
SCORE_2DART = 5000

#CONSTANTS:
PATH = abspath(dirname(__file__))
SCREEN = display.set_mode(RESOLUTION)
IMAGES = {name: image.load(resource_path('images/' + name + '.png')).convert_alpha()
        for name in ['yana', 'jimothy', 'dog0', 'dog1', 'dog2', 'dog3', 'dog4', 'heart', 'dart1', 'dart-1', 'sand',
                     'bgmain', 'bggame', 'bggameover', 'bgwin', 'dog_main', 'icon']}
FONT_JIMOTHY_SCORE = resource_path('../Juliana-Space-Invaders/fonts/Courier New Bold.ttf')
FONT_MAIN = resource_path('../Juliana-Space-Invaders/fonts/Phosphate.ttc')
FONT_BEGIN = resource_path('../Juliana-Space-Invaders/fonts/Copperplate.ttc')
FONT_ANNIVERSARY = resource_path('../Juliana-Space-Invaders/fonts/SnellRoundhand.ttc')
DOGS_LATERAL_FREE = (RESOLUTION[0] - DOGS_COLUMNS * DOGS_LENGTH[0] - (DOGS_COLUMNS - 1) * DOGS_SEPARATION[0]) / 2
SAND_SEPARATION = (RESOLUTION[0] - 2 * LATERAL_LIMIT - SAND_BLOCKS * SAND_COLUMNS * SAND_LENGTH[0]) / (SAND_BLOCKS + 1)
DOGS_FREE_MOVES = (DOGS_LATERAL_FREE - LATERAL_LIMIT) / DOGS_VELOCITY
COLUMN4MOVE = (DOGS_LENGTH[0] + DOGS_SEPARATION[0]) / DOGS_VELOCITY
class Yana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((90, 140))
        self.image.fill((255, 0, 0))  # Placeholder
        self.rect = self.image.get_rect(midbottom=(RESOLUTION[0] / 2, RESOLUTION[1] - 10))
        self.speed = 15

    def update(self, keys):
        if keys[K_LEFT] and self.rect.left > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < RESOLUTION[0] - 10:
            self.rect.x += self.speed

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        screen.fill((0, 0, 0))  # Black background
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()