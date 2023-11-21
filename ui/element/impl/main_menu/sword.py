from typing import Final

import pygame
from pygame import Surface
from pygame.event import Event

from references import client
from ui.element.element import Element


class Sword(Element):
    sprite: Surface
    is_down: bool
    limit: Final[int] = 40
    increase: Final[int] = client.surface.get_height() // 20

    def __init__(self, sprite: Surface, x: int):
        y: int = -sprite.get_height() - 5
        self.sprite = sprite
        self.is_down = False
        self.rectangle = self.sprite.get_rect()
        super().__init__(x, y, rectangle=self.rectangle)

    def draw(self, surface: pygame.Surface, **kwargs) -> None:
        surface.blit(self.sprite, self.rectangle)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if not self.is_down:
            if self.limit > self.y + self.increase:
                self.y += self.increase
            else:
                self.y = self.limit
            if self.limit == self.y:
                self.is_down = True
