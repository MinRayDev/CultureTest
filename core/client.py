import pygame


class Client:
    def __init__(self):
        self.client_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()