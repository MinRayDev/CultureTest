import time
from typing import Final

import pygame
from pygame import Surface
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.choice import Choice
from ui.menu.impl.text_box import TextBox
from utils.time_util import has_elapsed


class ChoiceText(Choice):
    placeholder: Surface
    selected_line_color: tuple[int, int, int]
    cursor_time_switch: float
    delete_time: list[float]
    limit: Final[int] = TextBox.limit
    unselect: bool
    has_cursor: bool

    def __init__(self, placeholder: str, x: int, y: int, height: int):
        super().__init__("", x, y, height)
        self.placeholder = self.render(placeholder)
        self.selected_line_color = (0, 0, 200)
        self.cursor_time_switch = time.time()
        self.delete_time = [0, 0]
        self.has_cursor = True

    def activity(self, events: dict[int, list[Event]]) -> None:
        """Activity of the text entry.

            :param events: The events of the text entry.
            :type events: list[Event].
        """
        if len(events[pygame.TEXTINPUT]) and len(self.content) < self.limit:
            for event in events[pygame.TEXTINPUT]:
                for char in event.text:
                    if not self.content and char == " ":
                        Sound.error.play()
                        continue
                    if char in TextBox.allowed_characters:
                        self.content += char
                    else:
                        Sound.error.play()
        elif pygame.K_BACKSPACE in events[pygame.KEYDOWN] and len(self.content) > 0:
            self.delete_time[0] = time.time()
            self.content = self.content[:-1]
        if len(self.content) > 0 and pygame.key.get_pressed()[pygame.K_BACKSPACE] and has_elapsed(self.delete_time[0], 0.5) and has_elapsed(self.delete_time[1], 0.05):
            self.content = self.content[:-1]
            self.delete_time[1] = time.time()

    def draw(self, surface: pygame.Surface, **kwargs) -> None:
        """Draws the text entry.

            :param surface: The surface of the text entry.
            :type surface: pygame.Surface.

        """
        selected = kwargs.get("selected", False)
        if not self.content:
            surface.blit(self.placeholder, self.get_coords())
        else:
            super().draw(surface)
        if selected and self.has_cursor:
            if self.cursor_time_switch+1 >= time.time():
                pygame.draw.rect(surface, self.selected_line_color, pygame.Rect(self.x + self.width, self.y+2, 3, self.height - 4))
            elif self.cursor_time_switch+2 <= time.time():
                self.cursor_time_switch = time.time()
