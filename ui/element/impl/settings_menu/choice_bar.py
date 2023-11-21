from typing import Callable

from pygame import Rect, Surface
from pygame.event import Event

from ui.element.impl.choice import Choice


class ChoiceBar(Choice):
    bar: Rect
    bar_background: Rect
    __value: float
    increment_action: Callable[[float], None]
    max_size: int
    default_content: str

    def __init__(self, text: str, x: int, y: int, height: int = 30, ratio: float = 1, action: Callable[[float], None] = None, value: float = 100):
        super().__init__(text, x, y, height, None)
        self.max_size = int(150*ratio)
        x += int(5*ratio)
        y += self._text.get_height() + int(5*ratio)
        self.bar = Rect(x, y, self.max_size, int(7*ratio))
        self.bar_background = Rect(x - int(1*ratio), y - int(1*ratio), self.max_size+int(2*ratio), int(9*ratio))
        self.__value = value
        self.bar.width = int(self.max_size * value / 100)
        self.increment_action = action
        self.rectangle.height += self.bar_background.height + int(5*ratio)
        self.default_content = self.content
        self.content = self.get_text()

    def draw(self, surface: Surface, **kwargs) -> None:
        super().draw(surface)
        surface.fill((0, 0, 200), self.bar_background)
        surface.fill((255, 255, 255), self.bar)

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float) -> None:
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        self.__value = value
        self.bar.width = int(self.max_size * value / 100)
        self.content = self.get_text()
        if self.increment_action is not None:
            self.increment_action(value)

    def get_text(self) -> str:
        return f"{self.default_content} ({self.value})"
