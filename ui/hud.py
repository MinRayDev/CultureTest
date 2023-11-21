import os.path
from pathlib import Path

import pygame.transform
from pygame import Surface

import references
from ui.element.impl.text import Text
from utils.files import get_resources
from utils.sprites import load, resize


class HUD:
    """Class 'HUD' is the HUD of the game.

        :ivar width: The width of the HUD.
        :type width: int.
        :ivar height: The height of the HUD.
        :type height: int.
        :ivar sprites: The sprites of the HUD.
        :type sprites: dict[str, Surface].
        :ivar forest_shadow: The forest shadow of the HUD.
        :type forest_shadow: Surface.
        :ivar hearts: The hearts of the HUD.
        :type hearts: list[Surface].
        :ivar f3_pressed: Whether the F3 key is pressed or not.
        :type f3_pressed: bool.

    """
    width: int
    height: int
    sprites: dict[str, Surface]
    forest_shadow: Surface
    hearts: list[Surface]
    f3_pressed: bool

    def __init__(self):
        """Constructor of the class 'HUD'."""
        self.width, self.height = references.client.surface.get_size()
        self.sprites = {}
        sprites = load(Path(get_resources(), "hud").__str__())
        for key, value in sprites.items():
            self.sprites[key] = resize(value, 4)
        self.forest_shadow = sprites["forest_mask"]
        i: int = 30
        pygame.transform.threshold(self.forest_shadow, self.forest_shadow, (255, 255, 255, 255), (1, 1, 1, 255), (i, i, i, 120))
        pygame.transform.threshold(self.forest_shadow, self.forest_shadow, (i, i, i, 120), (1, 1, 1, 255), (0, 0, 0, 0))
        self.hearts = []
        self.set_life(3)
        self.f3_pressed = False

    def draw(self, surface: Surface) -> None:
        """Draws the HUD on the screen.

            :param surface: The surface on which the HUD is drawn.
            :type surface: Surface.

        """
        x_distance: int = self.width // 30
        default_x: int = self.width - x_distance
        default_y: int = self.height // 20
        for i, heart in enumerate(self.hearts):
            surface.blit(heart, (default_x - (i * x_distance), default_y))
        if self.f3_pressed:
            Text(f"Correct: {str(references.game.good_answers)}", 50, default_y, (0, 255, 0)).draw(surface)
            Text(f"Fps: {str(int(references.client.clock.get_fps()))}", 50, self.height // 80, (0, 255, 0)).draw(surface)

    def set_life(self, life: int) -> None:
        """Sets the life of the player.

            :param life: The life of the player.
            :type life: int.
        """
        self.hearts.clear()
        for i in range(3):
            if life > i:
                self.hearts.append(self.sprites["heart"])
            else:
                self.hearts.append(self.sprites["heart_slot"])
