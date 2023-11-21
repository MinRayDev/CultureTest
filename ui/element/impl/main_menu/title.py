import pygame
from pygame import Surface

from ui.element.element import Element


class Title(Element):
    sprite: Surface
    over_sprite: Surface
    __alpha: int

    def __init__(self, sprite: Surface, over_sprite: Surface, coords: tuple[int, int]):
        self.sprite = sprite
        self.over_sprite = over_sprite
        self.__alpha = 0
        self.sprite.set_alpha(self.__alpha)
        self.over_sprite.set_alpha(self.__alpha)
        super().__init__(coords[0], coords[1], rectangle=self.sprite.get_rect())

    def draw(self, surface: pygame.Surface, **kwargs) -> None:
        between: tuple[Element, ...] = kwargs.get("between", ())
        surface.blit(self.sprite, self.rectangle)
        for bet in between:
            bet.draw(surface)
        surface.blit(self.over_sprite, self.rectangle)

    @property
    def alpha(self) -> int:
        return self.__alpha

    @alpha.setter
    def alpha(self, value: int):
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        self.__alpha = value
        self.over_sprite.set_alpha(value)
        self.sprite.set_alpha(value)
