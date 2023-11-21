from typing import Callable

from pygame.event import Event

from ui.element.impl.outlined_text import OutlinedText


class Choice(OutlinedText):
    action: Callable[[], None]

    def __init__(self, text: str, x: int, y: int, height: int = 30, action: Callable[[], None] = None):
        super().__init__(text, x, y, (255, 255, 255), (0, 0, 200), height)
        self.action = action

    def activity(self, events: dict[int, list[Event]]) -> None:
        if self.action is not None:
            self.action()
