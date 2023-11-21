import pygame


class Client:
    """Client class for the game.

        :ivar surface: The surface of the game.
        :type surface: pygame.Surface
        :ivar clock: The clock of the game.
        :type clock: pygame.time.Clock
    """
    surface: pygame.Surface
    clock: pygame.time.Clock

    def __init__(self):
        """Constructor of the Client class."""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("CultureTest")
        self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
