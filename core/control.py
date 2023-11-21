import pygame
from pygame.event import Event

import references
from world.facing import Facing
from ui.menu.game_menu import GameMenu
from ui.menu.menu import Menu


def check_events(events: dict[int, list[Event]]) -> None:
    if len(events[pygame.QUIT]):
        references.game.run = False

    # Menu controls
    if isinstance(references.game.menu, Menu):
        references.game.menu.activity(events)
        if not isinstance(references.game.menu, GameMenu):
            return

    # In-game controls
    if references.game.menu is None:
        references.game.player.velocity = 4

        # Debug
        if pygame.key.get_pressed()[pygame.K_y]:
            references.game.player.velocity = 20

        if pygame.K_ESCAPE in events[pygame.KEYDOWN]:
            from ui.menu.impl.settings_menu import SettingsMenu
            references.game.menu = SettingsMenu(None)
            return
        elif pygame.K_x in events[pygame.KEYDOWN]:
            # references.game.menu = GameOverTransition()
            references.game.player.life = 0
        elif pygame.K_F3 in events[pygame.KEYDOWN]:
            references.game.hud.f3_pressed = not references.game.hud.f3_pressed

        # Movement
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            references.game.player.move(Facing.EAST)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            references.game.player.move(Facing.WEST)
        if pygame.key.get_pressed()[pygame.K_UP]:
            references.game.player.move(Facing.NORTH)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            references.game.player.move(Facing.SOUTH)

        # No movement keys pressed
        if not any([pygame.key.get_pressed()[x] for x in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN)]):
            references.game.player.stop()

        # Interaction
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            references.game.player.interact()
