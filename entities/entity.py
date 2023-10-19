from pygame import Surface

from utils.sprites import load, resize, draw_with_scroll


class Entity:
    name: str
    __sprite_location: str
    sprites: dict[str, Surface]
    current_sprite: Surface
    x: int
    y: int

    def __init__(self, name: str, sprite_location: str, x: int, y: int):
        self.name = name
        self.__sprite_location = sprite_location
        self.sprites = load(sprite_location)
        s__ = self.sprites.copy()
        for key, value in s__.items():
            self.sprites[key] = resize(value, 4)
        self.__current_sprite = list(self.sprites.values())[0]
        self.__width = self.current_sprite.get_width()
        self.__height = self.current_sprite.get_height()
        self.x = x
        self.y = y

    def draw(self, screen: Surface):
        draw_with_scroll(screen, self.__current_sprite, self.x, self.y)

    @property
    def current_sprite(self) -> Surface:
        return self.__current_sprite

    @current_sprite.setter
    def current_sprite(self, value: Surface):
        self.__current_sprite = value
        self.__width = value.get_width()
        self.__height = value.get_height()

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height
