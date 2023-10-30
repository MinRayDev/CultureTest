from pygame import Surface

from ui.element.game_menu import GameMenu
from ui.element.impl.text import Text
from utils.sprites import load_sprite, resize


class TextBox(GameMenu):
    def __init__(self, content: str, surface: Surface):
        super().__init__()
        if len(content) > 65:
            raise ValueError("The content of the text box cannot be longer than 65 characters.")
        self.text: Text = Text(content, 0, 0, (50, 50, 255), 30)
        self.frame = resize(load_sprite(r"./resources/frame.png"), 4)
        self.x = surface.get_width() // 2 - self.frame.get_width() // 2
        self.y = surface.get_height() // 2 - self.frame.get_height() // 2
        self.text.rectangle.x = surface.get_width() // 2 - self.text.rectangle.width // 2
        self.text.rectangle.y = self.y + (7*4)

    def draw(self, surface: Surface) -> None:
        surface.blit(self.frame, (self.x, self.y))
        self.text.draw(surface)
