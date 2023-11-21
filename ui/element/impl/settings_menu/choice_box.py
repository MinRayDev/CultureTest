from typing import Callable

from pygame import Rect, Surface
from pygame.event import Event

from ui.element.impl.choice import Choice


class ChoiceBox(Choice):
    __value: bool
    set_action: Callable[[float], None]
    default_content: str

    def __init__(self, text: str, x: int, y: int, height: int = 30, action: Callable[[float], None] = None, value: bool = True):
        super().__init__(text, x, y, height, None)
        self.__value = value
        self.set_action = action
        self.default_content = self.content
        self.content = self.get_text()

    def draw(self, surface: Surface, **kwargs) -> None:
        super().draw(surface)

    @property
    def value(self) -> bool:
        return self.__value

    @value.setter
    def value(self, value: bool) -> None:
        self.__value = value
        self.content = self.get_text()
        if self.set_action is not None:
            self.set_action(value)

    def get_text(self) -> str:
        return f"{self.default_content} ({'ON' if self.value else 'OFF'})"

    def activity(self, events: dict[int, list[Event]]) -> None:
        self.value = not self.value
