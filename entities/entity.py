from pathlib import Path
from typing import Optional

import pygame
from pygame import Surface, Mask

from world.collision_type import CollisionType
from world.facing import Facing
from utils.sprites import load, resize, draw_with_scroll


class Entity:
    """Entity class.

        :ivar name: The name of the entity.
        :type name: str.
        :ivar __sprite_location: The location of the entity's sprites.
        :type __sprite_location: str.
        :ivar sprites: The entity's sprites.
        :type sprites: dict[str, Surface].
        :ivar current_sprite: The current sprite of the entity.
        :type current_sprite: Surface.
        :ivar width: The width of the entity.
        :type width: int.
        :ivar height: The height of the entity.
        :type height: int.
        :ivar x: The x position of the entity.
        :type x: int.
        :ivar y: The y position of the entity.
        :type y: int.

    """
    name: str
    __sprite_location: str
    sprites: dict[str, Surface]
    current_sprite: Surface
    width: int
    height: int
    x: int
    y: int

    def __init__(self, name: str, sprite_location: str | Path, x: int, y: int):
        """Constructor method for the Entity class.

            :param name: The name of the entity.
            :type name: str.
            :param sprite_location: The location of the entity's sprites.
            :type sprite_location: str | Path.
            :param x: The x position of the entity.
            :type x: int.
            :param y: The y position of the entity.
            :type y: int.

        """
        self.name = name
        self.__sprite_location = sprite_location
        self.sprites = {}
        s__ = load(sprite_location)
        for key, value in s__.items():
            self.sprites[key] = resize(value, 4)
        self.__current_sprite = list(self.sprites.values())[0]
        self.width = self.current_sprite.get_width()
        self.height = self.current_sprite.get_height()
        self.x = x
        self.y = y

    def draw(self, screen: Surface) -> None:
        """Draws the entity to the screen.

            :param screen: The screen to draw to.
            :type screen: Surface.

        """
        draw_with_scroll(screen, self.__current_sprite, self.x, self.y)

    @property
    def current_sprite(self) -> Surface:
        """Returns the current sprite of the entity."""
        return self.__current_sprite

    @current_sprite.setter
    def current_sprite(self, value: Surface) -> None:
        """Sets the current sprite of the entity.

            :param value: The new current sprite.
            :type value: Surface.

        """
        self.__current_sprite = value
        self.width = value.get_width()
        self.height = value.get_height()

    def collide(self, x: int, y: int, facing: Facing) -> CollisionType:
        """Checks if the entity collides with the screen.

            :param x: The x offset.
            :type x: int.
            :param y: The y offset.
            :type y: int.
            :param facing: The facing of the entity.
            :type facing: Facing.

        """
        from references import game
        current_screen = game.screen
        x_offset = -current_screen.x
        y_offset = -current_screen.y
        if facing == Facing.EAST:
            s = Surface((self.width // 2, self.height // 2))
            s.blit(self.current_sprite, (-self.width // 2, -self.height // 2))
            p_mask = pygame.mask.from_surface(s)
            mask_offset: tuple[float, float] = (
                self.x + x_offset + x + self.width // 2,
                self.y + y_offset + self.height // 2
            )
            if current_screen.masks["collisions"].overlap(p_mask, mask_offset):
                return CollisionType.collision
            if current_screen.masks["forward"].overlap(p_mask, mask_offset):
                return CollisionType.forward
            if current_screen.masks["backward"].overlap(p_mask, mask_offset):
                return CollisionType.backward
            if current_screen.masks["yforward"].overlap(p_mask, mask_offset):
                return CollisionType.bad_forward
        elif facing == Facing.WEST:
            s = Surface((self.width // 2, self.height // 2))
            s.blit(self.current_sprite, (0, -self.height // 2))
            p_mask = pygame.mask.from_surface(s)
            mask_offset: tuple[float, float] = (
                self.x + x_offset + x,
                self.y + y_offset + self.height // 2
            )
            if current_screen.masks["collisions"].overlap(p_mask, mask_offset):
                return CollisionType.collision
            if current_screen.masks["forward"].overlap(p_mask, mask_offset):
                return CollisionType.forward
            if current_screen.masks["backward"].overlap(p_mask, mask_offset):
                return CollisionType.backward
            if current_screen.masks["yforward"].overlap(p_mask, mask_offset):
                return CollisionType.bad_forward
        if facing == Facing.SOUTH:
            s = Surface((self.width, self.height // 2))
            s.blit(self.current_sprite, (0, -self.height // 2))
            p_mask = pygame.mask.from_surface(s)
            mask_offset: tuple[float, float] = (
                self.x + x_offset,
                self.y + y_offset + y + self.height // 2
            )
            if current_screen.masks["collisions"].overlap(p_mask, mask_offset):
                return CollisionType.collision
            if current_screen.masks["forward"].overlap(p_mask, mask_offset):
                return CollisionType.forward
            if current_screen.masks["backward"].overlap(p_mask, mask_offset):
                return CollisionType.backward
            if current_screen.masks["yforward"].overlap(p_mask, mask_offset):
                return CollisionType.bad_forward

        elif facing == Facing.NORTH:
            s = Surface((self.width, self.height // 2))
            s.blit(self.current_sprite, (0, -self.height // 2))
            p_mask = pygame.mask.from_surface(s)
            mask_offset: tuple[float, float] = (
                self.x + x_offset,
                self.y + y_offset + y + self.height // 2
            )
            if current_screen.masks["collisions"].overlap(p_mask, mask_offset):
                return CollisionType.collision
            if current_screen.masks["forward"].overlap(p_mask, mask_offset):
                return CollisionType.forward
            if current_screen.masks["backward"].overlap(p_mask, mask_offset):
                return CollisionType.backward
            if current_screen.masks["yforward"].overlap(p_mask, mask_offset):
                return CollisionType.bad_forward

    def get_interaction_area(self, facing: Facing, offsets: tuple[int, int]) -> tuple[Mask, tuple[float, float]]:
        """Returns the interaction area of the entity.

            :param facing: The facing of the entity.
            :type facing: Facing.
            :param offsets: The offsets of the entity.
            :type offsets: tuple[int, int].

            :return: The interaction area of the entity.
            :rtype: tuple[Mask, tuple[float, float]].

        """
        surface: Optional[Surface] = None
        mask_offset: tuple[float, float] = (0, 0)
        match facing:
            case Facing.NORTH:
                surface = Surface((self.width + 1, 2))
                mask_offset = (
                    self.x + offsets[0],
                    self.y + offsets[1] - 2
                )
            case Facing.EAST:
                surface = Surface((2, self.height + 1))
                mask_offset = (
                    self.x + self.width + offsets[0],
                    self.y + offsets[1]
                )
            case Facing.SOUTH:
                surface = Surface((self.width + 1, 2))
                mask_offset = (
                    self.x + offsets[0],
                    self.y + self.height + offsets[1]
                )
            case Facing.WEST:
                surface = Surface((2, self.height + 1))
                mask_offset = (
                    self.x + offsets[0] - 2,
                    self.y + offsets[1]
                )
        surface.fill((0, 0, 0, 255))
        mask: pygame.mask.Mask = pygame.mask.from_surface(surface)
        return mask, mask_offset
