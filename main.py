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

class Dart(sprite.Sprite):
    def __init__(self, x, y, direction):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(IMAGES['dart' + str(direction)], DART_LENGTH)
        self.rect = self.image.get_rect(midtop = (x, y))
        self.direction = direction
    def update(self, keys, *args):
        self.rect.y += self.direction * DART_SPEED[int(1 / 2.0 + self.direction / 2.0)]
        if self.rect.top <= JIMOTHY_MID or self.rect.bottom >= RESOLUTION[1] - YANA_BOTTOM: self.kill()
        game.screen.blit(self.image, self.rect)
class Dog(sprite.Sprite):
    def __init__(self, row, column):
        sprite.Sprite.__init__(self)
        self.row = row
        self.column = column
        self.image = transform.scale(IMAGES['dog' + str(self.row)], DOGS_LENGTH)
        self.rect = self.image.get_rect()
    def update(self, *args):
        game.screen.blit(self.image, self.rect)

class DogsGroup(sprite.Group):
    def __init__(self,columns,rows):
        sprite.Group.__init__(self)
        self.dogs = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.leftAddMove = 0
        self.rightAddMove = 0
        self.direction = 1
        self.rightMoves = DOGS_FREE_MOVES
        self.leftMoves = DOGS_FREE_MOVES
        self.moveNumber = DOGS_FREE_MOVES / 2 + 1
        self.timer = time.get_ticks()
        self.bottom = 0
        self.aliveColumns = list(range(columns))
        self.leftAliveColumn = 0
        self.rightAliveColumn = columns - 1
    def update(self, current_time):
        if current_time - self.timer >= DOGS_UPDATE_TIME:
            if self.direction == 1: max_move = self.rightMoves + self.rightAddMove
            else: max_move = self.leftMoves + self.leftAddMove
            if self.moveNumber >= max_move:
                self.leftMoves = DOGS_FREE_MOVES + self.rightAddMove
                self.rightMoves = DOGS_FREE_MOVES + self.leftAddMove
                self.direction *= -1
                self.moveNumber = 0
                self.bottom = 0
                for dog in self:
                    dog.rect.y += DOGS_MOVE_DOWN
                    if self.bottom < dog.rect.y + DOGS_LENGTH[1]: self.bottom = dog.rect.y + DOGS_LENGTH[1]
            else:
                for dog in self: dog.rect.x += self.direction * DOGS_VELOCITY
                self.moveNumber += 1
                self.timer += DOGS_UPDATE_TIME

    def add_internal(self, *sprites):
        super(DogsGroup, self).add_internal(*sprites)
        for s in sprites: self.dogs[s.row][s.column] = s

    def remove_internal(self, *sprites):
        super(DogsGroup, self).remove_internal(*sprites)
        for s in sprites: self.kill(s)

    def is_column_dead(self, column):
        return not any(self.dogs[row][column] for row in range(self.rows))

    def random_bottom(self):
        col = choice(self.aliveColumns)
        col_dogs = (self.dogs[row - 1][col] for row in range(self.rows, 0, -1))
        return next((en for en in col_dogs if en is not None), None)

    def kill(self, dog):
        self.dogs[dog.row][dog.column] = None
        is_column_dead = self.is_column_dead(dog.column)
        if is_column_dead: self.aliveColumns.remove(dog.column)
        if dog.column == self.rightAliveColumn:
             while self.rightAliveColumn > 0 and is_column_dead:
                self.rightAliveColumn -= 1
                self.rightAddMove += COLUMN4MOVE
                is_column_dead = self.is_column_dead(self.rightAliveColumn)
        elif dog.column == self.leftAliveColumn:
            while self.leftAliveColumn < self.columns and is_column_dead:
                self.leftAliveColumn += 1
                self.leftAddMove += COLUMN4MOVE
                is_column_dead = self.is_column_dead(self.leftAliveColumn)

class Sand(sprite.Sprite):
    def __init__(self, row, column):
        sprite.Sprite.__init__(self)
        self.row = row
        self.column = column
        self.image = transform.scale(IMAGES['sand'], SAND_LENGTH)
        self.rect = self.image.get_rect()
    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
class Jimothy(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(IMAGES['jimothy'], JIMOTHY_LENGTH)
        self.image_flipped = transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(midright = (0, JIMOTHY_MID))
        self.direction = 1
        self.oscilation = 1
        self.timer = time.get_ticks()
    def update(self, keys, currentTime, *args):
        resetTimer = False
        if currentTime - self.timer >= JIMOTHY_INTERVAL * self.oscilation:
            if self.rect.left < RESOLUTION[0] and self.direction == 1: self.rect.x += JIMOTHY_SPEED
            if self.rect.right > 0 and self.direction == -1: self.rect.x -= JIMOTHY_SPEED
            if self.direction == 1: game.screen.blit(self.image, self.rect)
            else: game.screen.blit(self.image_flipped, self.rect)
        if self.rect.left >= RESOLUTION[0]:
            self.direction = -1
            resetTimer = True
        if self.rect.right <= 0:
            self.direction = 1
            resetTimer = True
        if currentTime - self.timer > JIMOTHY_INTERVAL * self.oscilation and resetTimer:
            self.timer = currentTime
            self.oscilation = uniform(1, 2)

    def update(self, current_time, *args):
        if 300 <= current_time - self.timer <= 600: game.screen.blit(self.image, self.rect)
        elif 900 < current_time - self.timer: self.kill()
class Life(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(IMAGES['yana'], LIFE_LENGTH)
        self.rect = self.image.get_rect(center = (x,y))
    def update(self, *args):
        game.screen.blit(self.image, self.rect)
class Text(object):
    def __init__(self, textFont, size, message, color, position):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(center = position)
    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class Anniversary(object):
    def __init__(self):
        init()
        self.icon = transform.scale(IMAGES['icon'], (256, 256))
        self.set_icon(self.icon)
        self.clock = time.Clock()
        self.multiplier = 1
        self.caption = display.set_caption('ur gay')
        self.screen = SCREEN
        self.background = transform.scale(IMAGES['bgmain'], RESOLUTION)
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        self.roundsWon = 0
        self.displayWinningScreen = False
        self.dogPosition = DOGS_TOP
        self.TextTitle = Text(FONT_MAIN, 70, 'I Made This For U', (253, 253, 238), (RESOLUTION[0] / 2 + 100, RESOLUTION[1] / 2))
        self.TextBegin = Text(FONT_BEGIN, 25, 'Press a key to continue', (255, 255, 255), (RESOLUTION[0] / 2, RESOLUTION[1] - 50))
        self.gameOverText = Text(FONT_MAIN, 80, 'Game Over', (255, 255, 255), (RESOLUTION[0] / 2, RESOLUTION[1] / 2))
        self.nextRoundText = Text(FONT_MAIN, 50, 'Next Round', (100, 120, 100), (RESOLUTION[0] / 2, RESOLUTION[1] / 2))
        self.winText = Text(FONT_MAIN, 70, 'Can I Be Your Boyfriend?', (128, 0, 128),
                       (RESOLUTION[0] / 2, RESOLUTION[1] / 2 + 200))
        self.winText2 = Text(FONT_MAIN, 70, "let's have shrex", (196, 211, 0),
                            (RESOLUTION[0] / 2, RESOLUTION[1] - 50))
        self.AnniversaryText = Text(FONT_ANNIVERSARY, 40, 'Hey cutie', (255, 255, 255), (RESOLUTION[0] / 2  , RESOLUTION[1] / 2 - 40))
        self.scoreText = Text(FONT_MAIN, 20, 'Score', (255, 255, 255), (50, 20))
        self.livesText = Text(FONT_MAIN, 20, 'Lives', (255, 255, 255), (RESOLUTION[0] - 3 * (LIFE_LENGTH[0] + 10) - 120, 20))
        self.life = [Life(RESOLUTION[0] - i * (LIFE_LENGTH[0] + 10) - 30, 20) for i in range(YANA_LIVES)]
        self.livesGroup = sprite.Group(self.life[i] for i in range(YANA_LIVES))

    def make_sand_block(self, block_number):
        sandGroup = sprite.Group()
        for row in range(SAND_ROWS):
            for column in range(SAND_COLUMNS):
                sand = Sand(row, column)
                sand.rect.x = LATERAL_LIMIT + block_number * SAND_COLUMNS * SAND_LENGTH[0] + (block_number + 1) * SAND_SEPARATION + column * SAND_LENGTH[0]
                sand.rect.y = SAND_POSITION + (row * SAND_LENGTH[1])
                sandGroup.add(sand)
        return sandGroup
    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if e.type == QUIT: exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.darts) == 0 and self.yanaAlive:
                        if self.score < SCORE_2DART:
                            dart = Dart(self.player.rect.centerx, self.player.rect.y, -1)
                            self.darts.add(dart)
                            self.allSprites.add(self.darts)
                        else:
                            leftdart = Dart(self.player.rect.centerx -YANA_LENGTH[0] / 5, self.player.rect.y, -1)
                            rightdart = Dart(self.player.rect.centerx +YANA_LENGTH[0] / 5, self.player.rect.y, -1)
                            self.darts.add(leftdart)
                            self.darts.add(rightdart)
                            self.allSprites.add(self.darts)

    def main(self):
        while True:
            if self.mainScreen:
                self.background = transform.scale(IMAGES['bgmain'], RESOLUTION)
                self.screen.blit(self.background, (0, 0))
                dog_main = transform.scale(IMAGES['dog_main'], (200,200))
                self.screen.blit(dog_main, (RESOLUTION[0] / 2 + 150, RESOLUTION[1] / 2 - 190))
                self.TextTitle.draw(self.screen)
                self.TextBegin.draw(self.screen)
                self.AnniversaryText.draw(self.screen)
                for e in event.get():
                    if e.type == QUIT: exit()
                    if e.type == KEYUP:
                        self.allSand = sprite.Group()
                        for i in range(SAND_BLOCKS): self.allSand.add(self.make_sand_block(i))
                        self.livesGroup.add(self.life[i] for i in range(YANA_LIVES))
                        self.reset(0)
                        self.startGame = True
                        self.mainScreen = False

if __name__ == '__main__':
    game = Anniversary()
    game.main()
