import json
import os
from typing import Literal

import pygame
from pygame import Surface

from entities.entity import Entity
from ui.color_reference import ColorReference


class Screen(Entity):
    masks: dict[str, pygame.mask.Mask]

    def __init__(self, background_location: str):
        config = json.load(open(os.path.join(background_location, "config.json"), "r"))
        x = config.get("x", 0)
        y = config.get("y", 0)
        self.border = config.get("border", True)
        self.px = config.get("px", 0)
        self.py = config.get("py", 0)
        self.custom = config.get("custom", None)
        self.addons = []
        super().__init__("Background", background_location, x, y)
        self.index = int(os.path.basename(background_location))
        self.default_background = self.background = self.sprites.get("background", None)
        self.default_foreground = self.foreground = self.sprites.get("foreground", None)
        self.default_collisions = self.collisions = self.sprites.get("collisions", None)

        self.masks = {}
        # self.background = self.collisions
        self.get_masks()

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
        self.get_masks()

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
        self.get_masks()

    def get_masks(self) -> None:
        self.masks.clear()
        self.masks["forward"] = pygame.mask.from_threshold(self.collisions, ColorReference.forward.get_value(), (1, 1, 1, 255))
        self.masks["backward"] = pygame.mask.from_threshold(self.collisions, ColorReference.backward.get_value(), (1, 1, 1, 255))
        self.masks["yforward"] = pygame.mask.from_threshold(self.collisions, ColorReference.yforward.get_value(), (1, 1, 1, 255))
        self.masks["question"] = pygame.mask.from_threshold(self.collisions, ColorReference.question.get_value(), (1, 1, 1, 255))
        self.masks["answer1"] = pygame.mask.from_threshold(self.collisions, ColorReference.answer1.get_value(), (1, 1, 1, 255))
        self.masks["answer2"] = pygame.mask.from_threshold(self.collisions, ColorReference.answer2.get_value(), (1, 1, 1, 255))
        self.masks["answer3"] = pygame.mask.from_threshold(self.collisions, ColorReference.answer3.get_value(), (1, 1, 1, 255))

        self.masks["collisions"] = pygame.mask.from_threshold(self.collisions, ColorReference.collision.get_value(), (1, 1, 1, 255))
        for key, value in self.masks.items():
            if key not in {"collisions", "forward", "backward", "yforward"}:
                self.masks["collisions"].draw(value, (0, 0))

    def __str__(self) -> str:
        return f"Screen {self.index}"
