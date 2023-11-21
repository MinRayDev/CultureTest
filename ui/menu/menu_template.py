import os
from pathlib import Path
from typing import Optional, TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.choice import Choice
from ui.element.impl.fairy import Fairy
from ui.element.impl.outlined_text import OutlinedText
from ui.menu.menu import Menu
from utils.files import get_menus
from utils.sprites import load, resize, get_center

if TYPE_CHECKING:
    from pygame.mixer import Channel


class MenuTemplate(Menu):
    ratio: float
    default_x: int
    default_y: int
    choices: list[Choice]
    fairy: Fairy
    title: OutlinedText
    background: Optional[Surface]
    foreground: Optional[Surface]
    coords: tuple[int, int]

    def __init__(self, parent: Optional['Menu'], resources_path: Optional[Path], title: str, ratio: float = None):
        if ratio is None:
            from references import client
            ratio = client.surface.get_height()/224

        super().__init__(parent, resources_path, ratio)

        default_path: Path = Path(get_menus(), "default")
        sprites: dict[str, Surface] = load(default_path)
        for key, value in sprites.items():
            if key not in self.sprites:
                self.sprites[key] = resize(value, ratio)

        for key, value in Sound.load_sounds(default_path).items():
            if key not in self.sounds:
                self.sounds[key] = value
        if len(self.sounds) and not self.music:
            self.music = list(self.sounds.keys())[0]

        self.choices = []
        self.ratio = ratio
        self.title = OutlinedText(title, int(112*ratio), int(23*ratio), (255, 255, 255), (0, 0, 200), int(15*ratio))
        self.default_x = int(130*ratio)
        self.default_y = int(75*ratio)
        self.fairy = Fairy(int(self.default_x-(30*self.ratio)), 0, limit=0)
        self.background = self.sprites.get("background", None)
        self.foreground = self.sprites.get("foreground", None)
        self.coords = get_center(self.background if self.background else self.foreground)

    def activity(self, events: dict[int, list['Event']]) -> None:
        if pygame.K_DOWN in events[pygame.KEYDOWN] and self.fairy.position < self.fairy.limit:
            self.fairy.position += 1
            self.fairy.move(self.choices[self.fairy.position].rectangle.y)

        elif pygame.K_UP in events[pygame.KEYDOWN] and self.fairy.position > 0:
            self.fairy.position -= 1
            self.fairy.move(self.choices[self.fairy.position].rectangle.y)
        self.fairy.activity(events)

    def draw(self, surface: Surface) -> None:
        if self.background:
            surface.blit(self.background, self.coords)
        self.title.draw(surface)
        for choice in self.choices:
            choice.draw(surface)
        self.fairy.draw(surface)
        if self.foreground:
            surface.blit(self.foreground, self.coords)

    def reload_sprites(self) -> None:
        self.background = self.sprites.get("background", None)
        self.foreground = self.sprites.get("foreground", None)

    def setup_fairy(self):
        self.fairy.limit = len(self.choices) - 1
        self.fairy.y = self.choices[0].y

    def play(self, channel: 'Channel', loops: int = -1) -> None:
        super().play(channel, loops=loops)

    def back(self):
        if self.parent:
            Sound.back.play()
            from references import game
            game.menu = self.parent
