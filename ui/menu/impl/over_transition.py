import functools
from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from ui.menu.game_menu import GameMenu
from ui.menu.impl.game_over import GameOver
from utils.threads import thread

if TYPE_CHECKING:
    from pygame.mixer import Channel


class GameOverTransition(GameMenu):
    rads: list[Surface]
    start_time: float
    frame: int
    coords: tuple[int, int]
    frame_ratio: float = 1
    rects: list[pygame.Rect]

    def __init__(self):
        from references import client, game
        super().__init__()
        width: int = client.surface.get_width()
        height: int = client.surface.get_height()
        self.rads = get_rads(width, height)
        self.start_time = 0
        self.frame = 0
        x: int = game.player.x + game.scroll[0]
        y: int = game.player.y + game.scroll[1]
        self.coords = (x, y)
        self.rects = []
        if x < 0:
            self.rects.append(pygame.Rect(x+width, 0, -x, height))
        elif x > 0:
            self.rects.append(pygame.Rect(0, 0, x, height))
        if y < 0:
            self.rects.append(pygame.Rect(0, y+height, width, -y))
        elif y > 0:
            self.rects.append(pygame.Rect(0, 0, width, y))

    def draw(self, surface: Surface) -> None:
        frame_index: int = int(self.frame/self.frame_ratio)
        if not frame_index:
            frame_index = 1
        surface.blit(self.rads[frame_index], self.coords)
        for rect in self.rects:
            pygame.draw.rect(surface, (0, 0, 0), rect)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if int(self.frame/self.frame_ratio) >= len(self.rads)-1:
            from references import game
            game.menu = GameOver()
            return
        self.frame += 1

    def play(self, channel: 'Channel', loops: int = -1) -> None:
        super().play(channel, loops=loops)


@functools.lru_cache(maxsize=1)
def get_rads(width: int, height: int) -> list[Surface]:
    rads: list[Surface] = []
    ratio: float = 1/40
    min_width = 16*4 + 6*4
    min_height = 26*4 + 6*4
    wdt: int = width
    hgt: int = height
    while True:
        surface: Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((255, 0, 0))
        rect: pygame.Rect = pygame.Rect(0, 0, wdt, hgt)
        rect.center = (width / 2, height / 2)
        pygame.draw.ellipse(surface, (255, 255, 255, 255), rect)
        pygame.transform.threshold(surface, surface, (255, 0, 0), (1, 1, 1, 255), (0, 0, 0, 0))
        pygame.transform.threshold(surface, surface, (0, 0, 0, 0), (1, 1, 1, 255), (0, 0, 0, 255))
        rads.append(surface)
        wdt -= width * ratio
        hgt -= height * ratio
        if wdt < min_width or hgt < min_height:
            break
    return rads


@thread()
def load_rads(width: int, height: int) -> None:
    get_rads(width, height)
