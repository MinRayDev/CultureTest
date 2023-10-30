import pygame
from pygame.event import Event


class Element:
    """Class 'Element' is the base class for all elements.

        :ivar x: The x position of the element.
        :type x: int.
        :ivar y: The y position of the element.
        :type y: int.
        :ivar __width: The width of the element.
        :type __width: int.
        :ivar __height: The height of the element.
        :type __height: int.
        :ivar rectangle: The rectangle of the element.
        :type rectangle: pygame.Rect.
        :ivar is_hover: Whether the element is hovered or not.
        :type is_hover: bool.

    """
    x: int
    y: int
    __width: int
    __height: int
    rectangle: pygame.Rect
    is_hover: bool

    def __init__(self, x: int | str, y: int | str, width: int, height: int, rectangle: pygame.Rect = None):
        from references import client
        """Constructor of the class 'Element'.

            :param x: The x position of the element.
            :type x: int | str.
            :param y: The y position of the element.
            :type y: int | str.
            :param width: The width of the element.
            :type width: int.
            :param height: The height of the element.
            :type height: int.
            :param rectangle: The rectangle of the element.
            :type rectangle: pygame.Rect.

        """
        if isinstance(x, str):
            if x == "CENTER":
                self.x = client.surface.get_width() // 2 - width // 2
            else:
                raise ValueError(f"Invalid x position: {x}")
        else:
            self.x: int = x
        if isinstance(y, str):
            if y == "CENTER":
                self.y = client.surface.get_height() // 2 - height // 2
            else:
                raise ValueError(f"Invalid x position: {x}")
        else:
            self.y: int = y
        self.__width: int = width
        self.__height: int = height
        self.is_hover: bool = False
        if rectangle is not None:
            self.rectangle: pygame.Rect = rectangle
        else:
            self.rectangle: pygame.Rect = pygame.Rect(self.x, self.y, width, height)

    @property
    def width(self) -> int:
        """Getter for the width of the element."""
        return self.__width

    @property
    def height(self) -> int:
        """Getter for the height of the element."""
        return self.__height

    @width.setter
    def width(self, value: int):
        """Setter for the width of the element."""
        self.__width = value

    @height.setter
    def height(self, value: int):
        """Setter for the height of the element."""
        self.__height = value

    def activity(self, events: list[Event]) -> None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        """Method 'draw' is called every frame to draw the element.

            :param surface: The surface to draw the element on.
            :type surface: pygame.Surface.

        """
        pass

    def click(self) -> None:
        """Method 'click' is called when the element is clicked."""
        pass

    def hover(self) -> int | None:
        """Method 'hover' is called when the element is hovered.

            :return: The cursor to set.
            :rtype: int | None.

        """
        return pygame.SYSTEM_CURSOR_HAND if self.rectangle.collidepoint(pygame.mouse.get_pos()) else None
