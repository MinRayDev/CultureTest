import os

import pygame
from pygame import Surface, image


def load(dir_path: str) -> dict[str, Surface]:
    """Loads the sprites from the given directory path.

        :param dir_path: The directory path of the sprites.
        :type dir_path: str.

        :return: The sprites.
        :rtype: dict[str, Surface].

    """
    sprites = {}
    for file in os.listdir(dir_path):
        if os.path.isfile(rf"{dir_path}\{file}") and (file.endswith(".png") or file.endswith(".jpg")):
            sprites[file[:-4]] = image.load(rf"{dir_path}\{file}").convert_alpha()
    return sprites


def resize(to_resize: Surface, ratio: float) -> Surface:
    """Resizes the given surface by the given ratio.

        :param to_resize: The surface to resize.
        :type to_resize: Surface.

        :param ratio: The ratio to resize the surface by.
        :type ratio: float.

    """
    return pygame.transform.scale(to_resize, (to_resize.get_width() * ratio, to_resize.get_height() * ratio))


def get_coordinates_with_scroll(surface: Surface, x: int, y: int) -> tuple[int, int]:
    """Get the coordinates with the scroll of the current level.

        :param surface:
        :param x: The x position to draw at.
        :type x: int.
        :param y: The y position to draw at.
        :type y: int.

        :return: The coordinates.
        :rtype: tuple[int, int].

    """
    import references
    return (
        x + surface.get_width() // 2 + references.game.scroll[0] - references.player.width // 2,
        y + surface.get_height() // 2 + references.game.scroll[1] - references.player.height // 2
    )


def draw_with_scroll(surface: Surface, to_draw: Surface, x: int, y: int) -> None:
    """Draws a surface with the scroll of the current level.

        :param surface: The surface to draw on.
        :type surface: Surface.
        :param to_draw: The surface to draw.
        :type to_draw: Surface.
        :param x: The x position to draw at.
        :type x: int.
        :param y: The y position to draw at.
        :type y: int.

    """
    surface.blit(to_draw, get_coordinates_with_scroll(surface, x, y))
