import time
from typing import Optional

import pygame
from pygame.event import Event

from entities.screen import Screen
from ui.element.game_menu import GameMenu
from utils.time_util import has_elapsed

pygame.init()
pygame.display.set_caption("AWAWA")
import references
from entities.player import Player
from utils.sprites import draw_with_scroll

# background = resize(image.load(r"C:\Users\Gekota\Documents\Dev\Python\CultureTest\resources\collisions.png").convert_alpha(), 3)
references.player = Player(0, 0, references.client.surface)
references.game.scroll = [-references.player.x, -references.player.y]
references.game.entities.append(references.player)
references.player.compute_scroll(0, 0)
ghost_switch: float = 0
while references.game.run:
    background: Optional[Screen] = references.game.screen
    events: list[Event] = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            references.game.run = False
    if references.game.menu is not None and isinstance(references.game.menu, GameMenu):
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            references.game.menu = None
    if references.game.menu is None:
        references.player.velocity = 2
        if pygame.key.get_pressed()[pygame.K_y]:
            references.player.velocity = 10
        if pygame.key.get_pressed()[pygame.K_x] and has_elapsed(ghost_switch, 0.25):
            references.player.ghost = not references.player.ghost
            ghost_switch = time.time()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            references.player.move(references.player.velocity, 0)
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            references.player.move(-references.player.velocity, 0)
        if pygame.key.get_pressed()[pygame.K_UP]:
            references.player.move(0, -references.player.velocity)
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            references.player.move(0, references.player.velocity)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            references.player.interact()
    references.client.surface.fill((0, 0, 0))
    if references.game.menu is None or isinstance(references.game.menu, GameMenu):
        draw_with_scroll(references.client.surface, background.background, background.x, background.y)
        for entity in references.game.entities:
            entity.draw(references.client.surface)
        if background.foreground is not None:
            draw_with_scroll(references.client.surface, background.foreground, background.x, background.y)
        if background.index > 0:
            draw_with_scroll(references.client.surface, references.game.hud.forest_shadow, background.x - references.game.hud.forest_shadow.get_width() // 4, background.y - references.game.hud.forest_shadow.get_height() // 4, 0.7)
        references.game.hud.draw(references.client.surface)
    if references.game.menu is not None:
        references.game.menu.draw(references.client.surface)
    pygame.display.update()
    references.client.clock.tick(120)
    # print(references.client.clock.get_fps())
pygame.quit()
