from pygame import Surface
from pygame.event import Event

from ui.element.impl.text import Text


class BlinkText(Text):
    count: int

    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int], height: int = 30):
        super().__init__(text, x, y, color, height)
        self.count = 0

    def draw(self, surface: Surface, **kwargs) -> None:
        """Draws the text element.

            :param surface: The surface to draw the text element on.
            :type surface: Surface.

        """
        if self.count <= 60:
            surface.blit(self._text, self.rectangle)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if self.count == 121:
            self.count = 0
        self.count += 1
