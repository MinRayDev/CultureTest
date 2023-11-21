import pygame
from pygame import Surface

from ui.element.impl.text import Text
from ui.fonts import Fonts


class OutlinedText(Text):
    font: pygame.font.Font
    __outline_color: tuple[int, int, int]

    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int], outline_color: tuple[int, int, int], height: int = 30):
        super().__init__(text, x, y, color, height)
        self.font = Fonts.returnofganon.get_font(height)
        self.__outline_color = outline_color
        self._text = self.render()
        self.rectangle = self._text.get_rect()
        self.x, self.y = x, y

    def update(self):
        self._text = self.render()

    @property
    def outline_color(self) -> tuple[int, int, int]:
        return self.__outline_color

    @outline_color.setter
    def outline_color(self, color: tuple[int, int, int]):
        self.__outline_color = color
        self.update()
        
    def render(self, content: str = None) -> Surface:
        if content is None:
            content = self.content
        if content == "":
            return Surface((0, 0))
        notcolor: list[int] = [c ^ 0xFF for c in self.outline_color]
        base: Surface = self.font.render(content, 0, self.outline_color, notcolor)
        size: tuple[int, int] = (base.get_width() + 2, base.get_height() + 2)
        hollow: Surface = Surface(size, pygame.SRCALPHA)
        hollow.fill(notcolor)

        for offset in [(0, 0), (2, 0), (0, 2), (2, 2)]:
            hollow.blit(base, offset)
        base.set_colorkey(0)
        base.set_palette_at(1, notcolor)
        hollow.blit(base, (1, 1))
        hollow.set_colorkey(notcolor)

        base: Surface = self.font.render(content, 0, self.color)
        outline: Surface = Surface(hollow.get_size(), 16)
        outline.blit(base, (1, 1))
        outline.blit(hollow, (0, 0))
        outline.set_colorkey(0)
        return outline
