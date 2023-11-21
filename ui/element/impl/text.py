import pygame
from pygame import Surface

from ui.element.element import Element
from ui.fonts import Fonts


class Text(Element):
    """Class 'Text' is a text element.

        Extends: 'Element'
        :ivar __content: The text content of the text element.
        :type __content: str.
        :ivar _text: The text of the text element.
        :type _text: pygame.Surface.
        :ivar __color: The color of the text element.
        :type __color: tuple[int, int, int].

    """
    __content: str
    _text: Surface
    __color: tuple[int, int, int]

    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int], height: int = 30):
        """Constructor of the class 'Text'.

            :param text: The text content of the text element.
            :type text: str.
            :param x: The x position of the text element.
            :type x: int.
            :param y: The y position of the text element.
            :type y: int.
            :param color: The color of the text element.
            :type color: tuple[int, int, int].
            :param height: The height of the text element.
            :type height: int.

        """
        self.__content = text
        self._text = Fonts.returnofganon.get_font(height).render(text, True, color)
        super().__init__(x, y, rectangle=self._text.get_rect())
        self.__color = color

    def draw(self, surface: Surface, **kwargs) -> None:
        """Draws the text element.

            :param surface: The surface to draw the text element on.
            :type surface: Surface.

        """
        surface.blit(self._text, self.rectangle)

    def update(self):
        self._text = Fonts.returnofganon.get_font(self.height).render(self.__content, True, self.color)

    @property
    def content(self) -> str:
        """Getter for the text content of the text element."""
        return self.__content

    @content.setter
    def content(self, value: str) -> None:
        """Setter for the text content of the text element."""
        self.__content = value
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
