from typing import Final

from pygame import Surface

from ui.element.element import Element


class Shine(Element):
    sprites: dict[str, Surface]
    sprite_index: int
    index_ratio: Final[int] = 4

    def __init__(self, sprites: dict[str, Surface], coords: tuple[int, int]):
        self.sprites = sprites
        self.sprite_index = 0
        width: int = self.sprites["shine0"].get_width()
        height: int = self.sprites["shine0"].get_height()
        super().__init__(coords[0] - width // 2, coords[1] - height // 2, rectangle=self.sprites["shine0"].get_rect())

    def draw(self, surface: Surface, **kwargs) -> None:
        surface.blit(
            self.sprites[f"shine{int(self.sprite_index / self.index_ratio)}"],
            self.get_coords()
        )

    def is_ended(self) -> bool:
        return int(self.sprite_index / self.index_ratio) == 11
