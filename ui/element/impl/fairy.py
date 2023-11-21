import functools
import os.path
import time
from pathlib import Path
from typing import Final

import pygame
from pygame import Surface
from pygame.event import Event

from ui.element.element import Element
from utils.files import get_menus
from utils.sprites import load, resize
from utils.time_util import has_elapsed


class Fairy(Element):
    PATH: Final[str] = Path(get_menus(), "fairy")
    sprite: Surface
    sprites: dict[str, Surface]
    position: int
    relative_position: int
    limit: int
    wing_flap: float

    def __init__(self, x: int, y: int, limit: int = 3):
        self.sprites = self.get_sprites()
        self.sprite = self.sprites["fairy_0"]
        self.rectangle = self.sprite.get_rect()
        self.position = 0
        self.relative_position = 0
        self.limit = limit
        self.wing_flap = 0
        super().__init__(x, y, rectangle=self.rectangle)

    def draw(self, surface: pygame.Surface, **kwargs) -> None:
        surface.blit(self.sprite, self.rectangle)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if has_elapsed(self.wing_flap, 0.25):
            self.wing_flap = time.time()
            if self.sprite == self.sprites["fairy_0"]:
                self.sprite = self.sprites["fairy_1"]
            else:
                self.sprite = self.sprites["fairy_0"]

    def move(self, y: int) -> None:
        self.rectangle.y = y

    @functools.lru_cache(maxsize=1)
    def get_sprites(self) -> dict[str, Surface]:
        sprites: dict[str, Surface] = load(self.PATH)
        return {key: resize(value, 4) for key, value in sprites.items()}
