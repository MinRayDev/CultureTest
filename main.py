from typing import Final, Optional

import pygame
from pygame.event import Event

from entities.screen import Screen

pygame.init()
pygame.display.set_caption("AWAWA")
import references
from entities.player import Player
from utils.sprites import draw_with_scroll

# background = resize(image.load(r"C:\Users\Gekota\Documents\Dev\Python\CultureTest\resources\collisions.png").convert_alpha(), 4)
run: bool = True
references.player = Player(0, 0, references.client.client_surface)
references.game.entities.append(references.player)
background: Optional[Screen] = references.game.screen
references.background_colision = background.collisions
while run:
    references.client.client_surface.fill((0, 0, 0))
    draw_with_scroll(references.client.client_surface, background.background, background.x, background.y)
    events: list[Event] = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        references.player.move(2, 0)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        references.player.move(-2, 0)
    if pygame.key.get_pressed()[pygame.K_UP]:
        references.player.move(0, -2)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        references.player.move(0, 2)
    for entity in references.game.entities:
        entity.draw(references.client.client_surface)
    draw_with_scroll(references.client.client_surface, background.foreground, background.x, background.y)
    pygame.display.update()
    references.client.clock.tick(120)
pygame.quit()
