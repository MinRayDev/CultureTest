import time

import pygame

import references
from entities.player_entity import PlayerEntity
from ui.menu.impl.main_menu import MainMenu
from ui.menu.impl.selection_menu import SelectionMenu

if __name__ == '__main__':
    references.game.menu = MainMenu()
    # references.game.menu = SelectionMenu()
    references.game.player = PlayerEntity(0, 0)
    references.game.loop()
    pygame.quit()

