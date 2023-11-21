import pygame
from pygame import Surface


class Client:
    surface: Surface
    clock: pygame.time.Clock

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("CultureTest")
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
