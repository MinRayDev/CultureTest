import time

import pygame

import references
from core.player import Player
from ui.menu.impl.main_menu import MainMenu

if __name__ == '__main__':
    references.game.menu = MainMenu()
    references.game.player = Player(0, 0)
    references.game.loop()
    pygame.quit()

