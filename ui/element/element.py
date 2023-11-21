from typing import Protocol

import pygame
from pygame.event import Event


class Element:
    """Class 'Element' is the  class for all elements.

        :ivar rectangle: The rectangle of the element.
        :type rectangle: pygame.Rect.
        :ivar is_hover: Whether the element is hovered or not.
        :type is_hover: bool.

    """
    rectangle: pygame.Rect
    is_hover: bool

    def __init__(self, x: int, y: int, width: int = None, height: int = None, rectangle: pygame.Rect = None):
        """Constructor of the class 'Element'.

            :param x: The x position of the element.
            :type x: int.
            :param y: The y position of the element.
            :type y: int.
            :param width: The width of the element.
            :type width: int.
            :param height: The height of the element.
            :type height: int.
            :param rectangle: The rectangle of the element.
            :type rectangle: pygame.Rect.

        """
        self.is_hover: bool = False
        if rectangle is None and (width is None or height is None):
            raise ValueError("Either rectangle or width and height must be given.")
        if rectangle is not None:
            self.rectangle: pygame.Rect = rectangle
            rectangle.x = x
            rectangle.y = y
            if width != -1 and width is not None:
                rectangle.width = width
            if height != -1 and height is not None:
                rectangle.height = height
        else:
            self.rectangle: pygame.Rect = pygame.Rect(x, y, width, height)

    @property
    def x(self) -> int:
        """Getter for the x position of the element."""
        return self.rectangle.x

    @x.setter
    def x(self, value: int):
        """Setter for the x position of the element."""
        self.rectangle.x = value

    @property
    def y(self) -> int:
        """Getter for the y position of the element."""
        return self.rectangle.y

    @y.setter
    def y(self, value: int):
        """Setter for the y position of the element."""
        self.rectangle.y = value

    @property
    def width(self) -> int:
        """Getter for the width of the element."""
        return self.rectangle.width

    @property
    def height(self) -> int:
        """Getter for the height of the element."""
        return self.rectangle.height

    @width.setter
    def width(self, value: int):
        """Setter for the width of the element."""
        self.rectangle.width = value

    @height.setter
    def height(self, value: int):
        """Setter for the height of the element."""
        self.rectangle.height = value

    def activity(self, events: dict[int, list[Event]]) -> None:
        """Method 'activity' is called every frame to update the element.

            :param events: The list of events.
            :type events: list[Event].
        """
        ...

    def draw(self, surface: pygame.Surface, **kwargs) -> None:
        """Method 'draw' is called every frame to draw the element.

            :param surface: The surface to draw the element on.
            :type surface: pygame.Surface.

        """
        ...

    def click(self) -> None:
        """Method 'click' is called when the element is clicked."""
        pass

    def hover(self) -> int | None:
        """Method 'hover' is called when the element is hovered.

            :return: The cursor to set.
            :rtype: int | None.

        """
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None

    def get_coords(self) -> tuple[int, int]:
        """Method 'get_coords' returns the coordinates of the element.

            :return: The coordinates of the element.
            :rtype: tuple[int, int].

        """
        return self.rectangle.x, self.rectangle.y
