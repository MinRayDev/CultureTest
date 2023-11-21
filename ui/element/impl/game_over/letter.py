from pygame import Surface

from ui.element.element import Element
from ui.fonts import Fonts


class Letter(Element):
    limit_x: int
    final_x: int
    __char: str
    _text: Surface
    __color: tuple[int, int, int]
    reached_limit: bool
    is_finished: bool
    regrouped: bool
    regrouping: bool

    def __init__(self, char: str, x: int, y: int):
        self.limit_x = 0
        self.final_x = 0
        self.__char = char
        self._text = Fonts.hyliaserif.get_font(65).render(char, True, (255, 255, 255))
        super().__init__(x, y, rectangle=self._text.get_rect())
        self.__color = (255, 255, 255)
        self.reached_limit = False
        self.is_finished = False
        self.regrouped = False
        self.regrouping = False

    def draw(self, surface: Surface, **kwargs) -> None:
        """Draws the text element.

            :param surface: The surface to draw the text element on.
            :type surface: Surface.

        """
        surface.blit(self._text, self.rectangle)

    def update(self):
        self._text = Fonts.hyliaserif.get_font(self.height).render(self.__char, True, self.color)

    @property
    def content(self) -> str:
        """Getter for the text content of the text element."""
        return self.__char

    @content.setter
    def content(self, value: str) -> None:
        """Setter for the text content of the text element."""
        self.__char = value
        self.update()

    @property
    def color(self) -> tuple[int, int, int]:
        """Getter for the color of the text element."""
        return self.__color

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        """Setter for the color of the text element."""
        self.__color = value
        self.update()

    @property
    def x(self) -> int:
        """Getter for the x position of the text element."""
        return self.rectangle.x

    @x.setter
    def x(self, value: int) -> None:
        """Setter for the x position of the text element."""
        self.rectangle.x = value
        if self.rectangle.x == self.limit_x:
            self.reached_limit = True
        if self.regrouped:
            if self.rectangle.x == self.final_x:
                self.is_finished = True
