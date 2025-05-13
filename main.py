import pygame
from pygame import *

RESOLUTION = (1200, 700)
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("For My Girlfriend ❤️")


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