import enum
import os

import pygame

from utils.files import get_fonts


class Fonts(str, enum.Enum):
    """Class 'Fonts'.

        Extends 'str' and 'Enum'.

        :cvar returnofganon: The returnofganon font.
        :cvar hyliaserif: The hyliaserif font.

    """
    returnofganon = os.path.join(get_fonts(), "ReturnofGanon.ttf")
    hyliaserif = os.path.join(get_fonts(), "HyliaSerifBeta-Regular.otf")

    def get_font(self, height: int) -> pygame.font.Font:
        """Returns the font with the given size.

            :param height: The size of the font.
            :type height: int.

        """
        return pygame.font.Font(self.value, height)
