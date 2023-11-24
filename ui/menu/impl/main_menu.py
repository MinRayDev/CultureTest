import time
from pathlib import Path
from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from ui.element.impl.main_menu.background import Background
from ui.element.impl.main_menu.blink_text import BlinkText
from ui.element.impl.main_menu.shine import Shine
from ui.element.impl.main_menu.sword import Sword
from ui.element.impl.main_menu.title import Title
from ui.element.impl.main_menu.triforce import Triforce
from ui.menu.menu import Menu
from utils.files import get_menus
from utils.sprites import get_center, get_shine_pos
from utils.time_util import has_elapsed
from decimal import Decimal

if TYPE_CHECKING:
    from pygame.mixer import Channel


class MainMenu(Menu):
    background: Background
    title: Title
    sword: Sword
    shine_index: Decimal
    shine_end: float
    shines: dict[Decimal, Shine]
    triforce: Triforce
    already_played: bool
    start_text: BlinkText
    init_time: float

    def __init__(self):
        super().__init__(None, Path(get_menus(), "main"), ratio=7.5)
        background: Surface = self.sprites["background"]
        self.background = Background(background, get_center(background))
        title: Surface = self.sprites["title"]
        self.title = Title(title, self.sprites["title_over"], get_center(title))
        self.sword = Sword(self.sprites["sword"], int(background.get_width()/5.5) + self.background.x)
        self.shine_index = Decimal("0")
        self.shine_end = 0
        # time: count, pos
        shines: dict[str, Surface] = {f"shine{i}": self.sprites[f"shine{i}"] for i in range(11)}
        self.shines = {
            Decimal("0"): Shine(shines, get_shine_pos(148, 66, self.title.x, self.title.y, 7.5)),
            Decimal("1.2"): Shine(shines, get_shine_pos(105, 24, self.title.x, self.title.y, 7.5)),
            Decimal("2.4"): Shine(shines, get_shine_pos(64, 64, self.title.x, self.title.y, 7.5)),
            Decimal("3.6"): Shine(shines, get_shine_pos(5, 28, self.title.x, self.title.y, 7.5))
        }
        triangles: dict[str, Surface] = {}
        for i in range(171):
            triangles[f"t{i}"] = self.sprites[f"t{i}"]
            triangles[f"rt{i}"] = self.sprites[f"rt{i}"]
        triangles["triforce"] = self.sprites["triforce"]
        self.triforce = Triforce(triangles)
        self.already_played = False
        self.start_text = BlinkText("PRESS SPACE TO START", 0, 0, (255, 255, 255), 70)
        start_text_coord: tuple[int, int] = get_center(self.start_text.rectangle)
        self.start_text.x = start_text_coord[0] - self.triforce.width // 10
        self.start_text.y = start_text_coord[1] + self.triforce.height / 1.5
        self.init_time = time.time()

    def draw(self, surface: Surface) -> None:
        if self.sword.is_down:
            self.background.draw(surface)
            if self.background.alpha == 0:
                self.start_text.draw(surface)
        if self.title.alpha >= 140:
            self.triforce.draw(surface)
            self.title.draw(surface, between=(self.sword,))
        elif has_elapsed(self.init_time, 6.4):
            self.title.draw(surface)
            self.triforce.draw(surface)
        else:
            self.triforce.draw(surface)
        if self.title.alpha > 0:
            # draw shines
            if has_elapsed(self.init_time, 6.6) and has_elapsed(self.shine_end, self.shine_index):
                self.shines[self.shine_index].draw(surface)

    def activity(self, events: dict[int, list[Event]]) -> None:
        self.triforce.activity(events)
        if has_elapsed(self.init_time, 6.4):
            self.start_text.activity(events)
            if self.title.alpha < 255:
                self.title.alpha += 2
            if self.triforce.alpha < 255 and self.title.alpha >= 200:
                self.triforce.alpha += 2
        if self.title.alpha == 255:
            self.sword.activity(events)
        if self.sword.is_down:
            if self.background.alpha > 0:
                self.background.alpha -= 2
        if has_elapsed(self.init_time, 10):
            import references
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                references.game.run = False
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                from ui.menu.impl.selection_menu import SelectionMenu
                references.game.menu = SelectionMenu()

        if has_elapsed(self.init_time, 6.6) and has_elapsed(self.shine_end, self.shine_index):
            shine: Shine = self.shines[self.shine_index]
            shine.sprite_index += 2
            if self.shine_index == Decimal("0"):
                self.shine_end = time.time()
            if shine.is_ended():
                shine.sprite_index = 0
                self.shine_index += Decimal("1.2")
                if self.shine_index > Decimal("3.6"):
                    self.shine_index = Decimal("0")

    def play(self, channel: 'Channel', loops: int = 0):
        if not self.already_played:
            super().play(channel, loops=loops)
            self.already_played = True
