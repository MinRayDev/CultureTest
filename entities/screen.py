import functools
import json
import os
from enum import Enum
from pathlib import Path
from typing import Literal, Optional

import pygame
from pygame import Surface

from core.sound import Sound
from entities.entity import Entity


class ColorManager(Enum):
    question = (125, 125, 125, 255)
    answer1 = (125, 0, 0, 255)
    answer2 = (0, 125, 0, 255)
    answer3 = (0, 0, 125, 255)
    final_text = (125, 0, 125, 255)

    collision = (255, 0, 0, 255)
    forward = (0, 255, 255, 255)
    backward = (0, 255, 0, 255)
    yforward = (255, 255, 0, 255)

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    @staticmethod
    @functools.lru_cache()
    def get_signs():
        return ColorManager.question, ColorManager.answer1, ColorManager.answer2, ColorManager.answer3, ColorManager.final_text

    @staticmethod
    @functools.lru_cache()
    def get_collisions():
        return ColorManager.collision, ColorManager.question, ColorManager.answer1, ColorManager.answer2, ColorManager.answer3, ColorManager.final_text


class Screen(Entity):
    border: bool
    px: int
    py: int
    custom: list[list[int]]
    addons: list[str]
    index: int
    default_background: Surface
    default_foreground: Surface
    default_collisions: Surface
    background: Optional[Surface]
    foreground: Optional[Surface]
    collisions: Optional[Surface]
    masks: dict[str, pygame.mask.Mask]
    sounds: dict[str, pygame.mixer.Sound]
    current_sound: Optional[str]

    def __init__(self, path: Path):
        config = json.load(open(Path(path, "config.json"), "r"))
        x = config.get("x", 0)
        y = config.get("y", 0)
        self.border = config.get("border", True)
        self.px = config.get("px", 0)
        self.py = config.get("py", 0)
        self.custom = config.get("custom", [])
        self.addons = []
        super().__init__("Background", path, x, y)
        self.index = int(os.path.basename(path))
        self.default_background = self.background = self.sprites.get("background", None)
        self.default_foreground = self.foreground = self.sprites.get("foreground", None)
        self.default_collisions = self.collisions = self.sprites.get("collisions", None)
        self.sounds = Sound.load_sounds(path)
        self.current_sound = None
        if len(self.sounds) > 0:
            self.current_sound = list(self.sounds.keys())[0]
        self.masks = {}
        # self.background = self.collisions
        self.get_masks()

    def draw(self, screen: Surface) -> None:
        pass

    def add(self, key: str, add_type: Literal["background", "foreground", "collisions"]) -> None:
        self.addons.append(key)
        if add_type == "background":
            self.background.blit(self.sprites[key], (0, 0))
        elif add_type == "foreground":
            self.foreground.blit(self.sprites[key], (0, 0))
        elif add_type == "collisions":
            self.collisions.blit(self.sprites[key], (0, 0))
            self.background.blit(self.sprites[key], (0, 0))
        self.get_masks()

    def reset(self) -> None:
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
        if self.collisions:
            self.masks["forward"] = pygame.mask.from_threshold(self.collisions, ColorManager.forward.get_value(), (1, 1, 1, 255))
            self.masks["backward"] = pygame.mask.from_threshold(self.collisions, ColorManager.backward.get_value(), (1, 1, 1, 255))
            self.masks["yforward"] = pygame.mask.from_threshold(self.collisions, ColorManager.yforward.get_value(), (1, 1, 1, 255))
            self.masks["question"] = pygame.mask.from_threshold(self.collisions, ColorManager.question.get_value(), (1, 1, 1, 255))
            self.masks["answer1"] = pygame.mask.from_threshold(self.collisions, ColorManager.answer1.get_value(), (1, 1, 1, 255))
            self.masks["answer2"] = pygame.mask.from_threshold(self.collisions, ColorManager.answer2.get_value(), (1, 1, 1, 255))
            self.masks["answer3"] = pygame.mask.from_threshold(self.collisions, ColorManager.answer3.get_value(), (1, 1, 1, 255))
            self.masks["final_text"] = pygame.mask.from_threshold(self.collisions, ColorManager.final_text.get_value(), (1, 1, 1, 255))

            self.masks["collisions"] = pygame.mask.from_threshold(self.collisions, ColorManager.collision.get_value(), (1, 1, 1, 255))
        for key, value in self.masks.items():
            if key not in {"collisions", "forward", "backward", "yforward"}:
                self.masks["collisions"].draw(value, (0, 0))

    def __str__(self) -> str:
        return f"Screen {self.index}"

    def __int__(self):
        return self.index

    @functools.lru_cache()
    def get_offsets(self) -> tuple[int, int]:
        return -self.x, -self.y

    @functools.lru_cache()
    def get_borders(self):
        sw, sh = self.background.get_size()
        return (
            self.y,
            sw + self.x,
            sh + self.y,
            self.x
        )
