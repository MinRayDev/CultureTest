import string
from pathlib import Path
from typing import Final

import pygame
from pygame import Surface
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.outlined_text import OutlinedText
from ui.menu.game_menu import GameMenu
from utils.files import get_menus


class TextBox(GameMenu):
    text: OutlinedText
    frame: Surface
    coords: tuple[int, int]
    last: bool
    limit: Final[int] = 75
    allowed_characters: Final[list[str]] = string.ascii_letters + string.digits + " ?!.,;:()"

    def __init__(self, content: str, surface: Surface, last: bool = False):
        super().__init__(Path(get_menus(), "textbox"))

        if len(content) > TextBox.limit:
            raise ValueError("The content of the text box cannot be longer than 75 characters.")

        color: tuple[int, int, int] = (240, 240, 240)
        if last:
            color = (40, 40, 255)

        self.text = OutlinedText(content, 0, 0, (255, 255, 255), color, 30)
        self.frame = self.sprites["frame"]

        self.coords = (
            surface.get_width() // 2 - self.frame.get_width() // 2,
            surface.get_height() // 2 - self.frame.get_height() // 2
        )

        self.last = last

        self.text.rectangle.x = surface.get_width() // 2 - self.text.rectangle.width // 2
        self.text.rectangle.y = self.coords[1] + (7*4)
        if last:
            Sound.item_get.play()
        else:
            Sound.message.play()

    def draw(self, surface: Surface) -> None:
        surface.blit(self.frame, self.coords)
        self.text.draw(surface)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if self.last:
            if len(events[pygame.KEYDOWN]):
                from references import game
                game.run = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            from references import game
            game.menu = None
            Sound.message_finish.play()
