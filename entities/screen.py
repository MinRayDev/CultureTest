import json
import os
from typing import Literal

from pygame import Surface

from entities.entity import Entity


class Screen(Entity):
    def __init__(self, background_location: str):
        config = json.load(open(os.path.join(background_location, "config.json"), "r"))
        x = config.get("x", 0)
        y = config.get("y", 0)
        self.px = config.get("px", 0)
        self.py = config.get("py", 0)
        self.custom = config.get("custom", None)
        self.addons = []
        super().__init__("Background", background_location, x, y)
        self.index = int(os.path.basename(background_location))
        self.default_background = self.background = self.sprites.get("background", None)
        # self.foreground = self.sprites["foreground"]
        self.default_foreground = self.foreground = self.sprites.get("foreground", None)
        self.foreground = None
        self.default_collisions = self.collisions = self.sprites.get("collisions", None)

        self.background = self.sprites.get("collisions", None)

    def draw(self, screen: Surface):
        pass

    def add(self, key: str, add_type: Literal["background", "foreground", "collisions"]):
        self.addons.append(key)
        if add_type == "background":
            self.background.blit(self.sprites[key], (0, 0))
        elif add_type == "foreground":
            self.foreground.blit(self.sprites[key], (0, 0))
        elif add_type == "collisions":
            self.collisions.blit(self.sprites[key], (0, 0))
            self.background.blit(self.sprites[key], (0, 0))

    def reset(self):
        self.addons.clear()
        if self.default_background is not None:
            self.background = self.default_background.copy()
        else:
            self.background = None
        if self.default_foreground is not None:
            self.foreground = self.default_foreground.copy()
        else:
            self.foreground = None
        if self.default_collisions is not None:
            self.collisions = self.default_collisions.copy()
        else:
            self.collisions = None
