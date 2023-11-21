import pygame
from pygame.event import Event

from entities.player_entity import PlayerEntity
from entities.screen import Screen, ColorManager
from references import game
from ui.menu.game_menu import GameMenu
from ui.menu.menu import Menu
from world.facing import Facing
from world.sign import read


class Player(PlayerEntity):
    def __init__(self, x, y):
        super().__init__(x, y)

    def activity(self, events: dict[int, list[Event]]):
        if len(events[pygame.QUIT]):
            game.run = False

        # Menu controls
        if isinstance(game.menu, Menu):
            game.menu.activity(events)
            if not isinstance(game.menu, GameMenu):
                return

        # In-game controls
        if game.menu is None:
            game.player.velocity = 4

            # Debug
            if pygame.key.get_pressed()[pygame.K_y]:
                game.player.velocity = 20

            if pygame.K_ESCAPE in events[pygame.KEYDOWN]:
                from ui.menu.impl.settings_menu import SettingsMenu
                game.menu = SettingsMenu(None)
                return
            elif pygame.K_F3 in events[pygame.KEYDOWN]:
                game.hud.f3_pressed = not game.hud.f3_pressed

            # Movement
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.move(Facing.EAST)
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                self.move(Facing.WEST)
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.move(Facing.NORTH)
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                self.move(Facing.SOUTH)

            # No movement keys pressed
            if not any([pygame.key.get_pressed()[x] for x in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN)]):
                self.stop()

            # Interaction
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.interact()

    def interact(self) -> None:
        current_screen: Screen = game.screen
        mask, mask_offset = self.get_interaction_area(self.facing, current_screen.get_offsets())
        for i, mask_name in enumerate(ColorManager.get_signs()):
            if current_screen.masks[mask_name.get_name()].overlap(mask, mask_offset):
                read(i)
                return