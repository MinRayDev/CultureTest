import pygame
from pygame import Surface
from pygame.event import Event

from ui.element.element import Element
from utils.sprites import get_center


class Fragment(Element):
    sprites: dict[str, Surface]
    limits: tuple[int, int]
    motion: tuple[int, int]
    prefix: str

    def __init__(self, sprites: dict[str, Surface], coords: tuple[int, int], limits: tuple[int, int], motion: tuple[int, int] = (0, 0), prefix: str = "t"):
        self.sprites = sprites
        self.limits = limits
        self.motion = motion
        self.prefix = prefix
        super().__init__(coords[0], coords[1], rectangle=sprites[f"{prefix}0"].get_rect())

    def draw(self, surface: pygame.Surface, **kwargs) -> None:
        index_: int = kwargs["index"]
        surface.blit(self.sprites[f"{self.prefix}{int(index_/2)}"], self.get_coords())

    def activity(self, events: dict[int, list[Event]]) -> None:
        if self.motion[0] > 0:
            if self.x + self.motion[0] < self.limits[0]:
                self.x += self.motion[0]
            else:
                self.x = self.limits[0]
        elif self.motion[0] < 0:
            if self.x + self.motion[0] > self.limits[0]:
                self.x += self.motion[0]
            else:
                self.x = self.limits[0]

        if self.motion[1] > 0:
            if self.y + self.motion[1] < self.limits[1]:
                self.y += self.motion[1]
            else:
                self.y = self.limits[1]
        elif self.motion[1] < 0:
            if self.y + self.motion[1] > self.limits[1]:
                self.y += self.motion[1]
            else:
                self.y = self.limits[1]


class Triforce(Element):
    sprite: Surface
    __alpha: int
    fragments: list[Fragment]
    sprite_index: int

    def __init__(self, sprites: dict[str, Surface]):
        self.sprite = sprites.pop("triforce")
        self.__alpha = 200
        self.sprite.set_alpha(self.__alpha)
        self.sprite_index = 0
        reversed_sprites: dict[str, Surface] = {}
        for key in sprites.copy():
            if key.startswith("rt"):
                reversed_sprites[key] = sprites.pop(f"{key}")

        coords = get_center(self.sprite)
        x: int = coords[0] - self.sprite.get_width() // 10
        y: int = coords[1] - self.sprite.get_height() // 10
        from references import client
        frag_limits: tuple[tuple[int, int], ...] = (
            (x, int(y + 7.5 * 36)),
            (int(x+41*7.5), int(y+7.5*36)),
            (int(x + 20*7.5), y)
        )
        frag_coords: tuple[tuple[int, int], ...] = (
            (0, client.surface.get_height() - sprites["t0"].get_height()),
            (client.surface.get_width() - sprites["t0"].get_width(), client.surface.get_height() - sprites["t0"].get_height()),
            (int(x + 20*7.5), 0)
        )
        motion_ratio: float = 1/100
        self.fragments = [
            Fragment(
                sprites,
                frag_coords[0],
                frag_limits[0],
                (int((frag_limits[0][0] - frag_coords[0][0]) * motion_ratio), int((frag_limits[0][1] - frag_coords[0][1]) * motion_ratio))
            ),
            Fragment(
                reversed_sprites,
                frag_coords[1],
                frag_limits[1],
                (int((frag_limits[1][0] - frag_coords[1][0]) * motion_ratio), int((frag_limits[1][1] - frag_coords[1][1]) * motion_ratio)),
                prefix="rt"
            ),
            Fragment(
                sprites,
                frag_coords[2],
                frag_limits[2],
                (int((frag_limits[2][0] - frag_coords[2][0]) * motion_ratio), int((frag_limits[2][1] - frag_coords[2][1]) * motion_ratio))
            )
        ]
        super().__init__(x, y, rectangle=self.sprite.get_rect())

    @property
    def alpha(self) -> int:
        return self.__alpha

    @alpha.setter
    def alpha(self, value: int) -> None:
        self.__alpha = value
        self.sprite.set_alpha(value)

    def draw(self, surface: Surface, **kwargs) -> None:
        if int(self.sprite_index/2) > 170:
            surface.blit(self.sprite, self.get_coords())
        else:
            for fragment in self.fragments:
                fragment.draw(surface, index=self.sprite_index)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if int(self.sprite_index/2) < 171:
            for fragment in self.fragments:
                if fragment.x != fragment.limits[0] or fragment.y != fragment.limits[1]:
                    fragment.activity(events)
            self.sprite_index += 1
