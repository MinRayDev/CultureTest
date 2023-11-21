from pygame import Surface

from ui.element.element import Element


class Background(Element):
    sprite: Surface
    over_sprite: Surface
    __alpha: int

    def __init__(self, sprite: Surface, coords: tuple[int, int]):
        self.sprite = sprite
        self.over_sprite = sprite.copy()
        self.over_sprite.fill((255, 255, 255))
        self.__alpha = 255
        super().__init__(coords[0], coords[1], rectangle=self.sprite.get_rect())

    def draw(self, surface: Surface, **kwargs) -> None:
        surface.blit(self.sprite, self.rectangle)
        if self.__alpha > 0:
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
