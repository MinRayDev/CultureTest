import os
from pathlib import Path
from typing import Optional

import pygame
from pygame import Surface, image


def load(dir_path: str | Path) -> dict[str, Surface]:
    """Loads the sprites from the given directory path.

        :param dir_path: The directory path of the sprites.
        :type dir_path: str.

        :return: The sprites.
        :rtype: dict[str, Surface].

    """
    if isinstance(dir_path, Path):
        dir_path = str(dir_path)
    sprites = {}
    for file in os.listdir(dir_path):
        if os.path.isfile(rf"{dir_path}\{file}") and (file.endswith(".png") or file.endswith(".jpg")):
            sprites[file[:-4]] = image.load(rf"{dir_path}\{file}").convert_alpha()
    return sprites


def load_sprite(file_path: str | Path) -> Surface:
    """Loads the sprite from the given file path.

        :param file_path: The file path of the sprite.
        :type file_path: str.

        :return: The sprite.
        :rtype: Surface.

    """
    if isinstance(file_path, Path):
        file_path = str(file_path)
    return image.load(file_path).convert_alpha()


def resize(to_resize: Surface, ratio: float) -> Surface:
    """Resizes the given surface by the given ratio.

        :param to_resize: The surface to resize.
        :type to_resize: Surface.

        :param ratio: The ratio to resize the surface by.
        :type ratio: float.

    """
    return pygame.transform.scale(to_resize, (to_resize.get_width() * ratio, to_resize.get_height() * ratio))


def get_coordinates_with_scroll(surface: Surface, x: int, y: int, parallax_ratio: float = 1) -> tuple[int, int]:
    """Get the coordinates with the scroll of the current level.

        :param surface:
        :param x: The x position to draw at.
        :type x: int.
        :param y: The y position to draw at.
        :type y: int.
        :param parallax_ratio: The parallax ratio.
        :type parallax_ratio: float.

        :return: The coordinates.
        :rtype: tuple[int, int].

    """
    import references
    return (
        x + surface.get_width() // 2 + int(references.game.scroll[0] * parallax_ratio) - references.game.player.width // 2,
        y + surface.get_height() // 2 + int(references.game.scroll[1] * parallax_ratio) - references.game.player.height // 2
    )


def draw_with_scroll(surface: Surface, to_draw: Surface, x: int, y: int, parallax_raito: float = 1) -> None:
    """Draws a surface with the scroll of the current level.

        :param surface: The surface to draw on.
        :type surface: Surface.
        :param to_draw: The surface to draw.
        :type to_draw: Surface.
        :param x: The x position to draw at.
        :type x: int.
        :param y: The y position to draw at.
        :type y: int.
        :param parallax_raito: The parallax ratio.
        :type parallax_raito: float.

    """
    surface.blit(to_draw, get_coordinates_with_scroll(surface, x, y, parallax_raito))


def get_center(element: Surface | pygame.Rect) -> tuple[int, int]:
    """Get the center of the given element.

        :param element: The element to get the center of.
        :type element: Surface | pygame.Rect.

        :return: The center of the element.
        :rtype: tuple[int, int].

    """
    import references
    width: Optional[int] = None
    height: Optional[int] = None
    if isinstance(element, pygame.Rect):
        width = element.width
        height = element.height
    elif isinstance(element, Surface):
        width = element.get_width()
        height = element.get_height()
    if width is None or height is None:
        raise TypeError("Element must be pygame.Rect or pygame.Surface")
    return (
        references.client.surface.get_width() // 2 - width // 2,
        references.client.surface.get_height() // 2 - height // 2
    )


def get_shine_pos(x: int, y: int, surface_x: int, surface_y: int, ratio: float) -> tuple[int, int]:
    """Get the position of the shine.

        :param x: The x position of the shine.
        :type x: int.
        :param y: The y position of the shine.
        :type y: int.
        :param surface_x: The x position of the surface.
        :type surface_x: int.
        :param surface_y: The y position of the surface.
        :type surface_y: int.
        :param ratio: The ratio of the surface.
        :type ratio: float.

        :return: The position of the shine.
        :rtype: tuple[int, int].

    """
    return (
        int(x*ratio) + surface_x,
        int(y*ratio) + surface_y
    )
